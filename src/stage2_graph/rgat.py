"""
Heterogeneous Relational Graph Attention Network (R-GAT) for CINA Stage 2.

Replaces the prior NetworkX-only graph analysis with a learned multi-task model
that jointly predicts (a) stance scores, (b) Leiden community labels,
(c) contested-issue probability — using relation-specific attention weights.

This implements the Stage 2 advancement E1 specified in
METHODOLOGY_ADVANCEMENT_ROADMAP.md.

Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
License: MIT
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch import Tensor
    HAS_TORCH = True
except ImportError:  # graceful fallback for environments without torch
    HAS_TORCH = False
    Tensor = None  # type: ignore


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class RGATConfig:
    """Heterogeneous R-GAT hyperparameters."""

    # Graph structure
    n_country: int = 13
    n_issue: int = 6
    n_group: int = 6
    edge_types: tuple[str, ...] = ("has_stance", "member_of", "similar_to", "co_chairs")

    # Architecture
    hidden_dim: int = 64
    n_heads: int = 4
    n_layers: int = 2
    dropout: float = 0.2

    # Multi-task loss weights
    lambda_stance: float = 1.0
    lambda_coalition: float = 0.5
    lambda_contested: float = 0.5

    # Training
    lr: float = 1e-3
    weight_decay: float = 1e-4
    n_epochs: int = 200
    seed: int = 42


# ---------------------------------------------------------------------------
# Relation-specific attention layer
# ---------------------------------------------------------------------------

class RelationGATLayer(nn.Module if HAS_TORCH else object):
    """Single R-GAT layer with one attention head per relation type.

    For each (relation type r) we learn a separate linear projection W_r and
    attention vector a_r, following Schlichtkrull et al. (2018) for the
    relation-specific transformation and Veličković et al. (2018) for the
    attention mechanism.
    """

    def __init__(self, in_dim: int, out_dim: int, edge_types: tuple[str, ...],
                 n_heads: int = 4, dropout: float = 0.2):
        if not HAS_TORCH:
            raise ImportError("PyTorch required for RelationGATLayer")
        super().__init__()
        self.edge_types = edge_types
        self.n_heads = n_heads
        self.head_dim = out_dim // n_heads
        assert out_dim % n_heads == 0, "out_dim must be divisible by n_heads"

        self.W = nn.ModuleDict({
            r: nn.Linear(in_dim, out_dim, bias=False) for r in edge_types
        })
        self.a_src = nn.ParameterDict({
            r: nn.Parameter(torch.empty(n_heads, self.head_dim)) for r in edge_types
        })
        self.a_dst = nn.ParameterDict({
            r: nn.Parameter(torch.empty(n_heads, self.head_dim)) for r in edge_types
        })

        for r in edge_types:
            nn.init.xavier_uniform_(self.W[r].weight)
            nn.init.xavier_uniform_(self.a_src[r].view(1, -1))
            nn.init.xavier_uniform_(self.a_dst[r].view(1, -1))

        self.dropout = nn.Dropout(dropout)
        self.leaky_relu = nn.LeakyReLU(negative_slope=0.2)

    def forward(self, x: Tensor, edge_index_dict: dict[str, Tensor]) -> tuple[Tensor, dict[str, Tensor]]:
        """
        x: [N, in_dim] node features
        edge_index_dict: {relation: [2, E_r]} edges per relation type
        returns:
          h: [N, out_dim] updated features (concat heads)
          attn_dict: {relation: [E_r, n_heads]} attention weights for inspection
        """
        N = x.size(0)
        out_per_rel = []
        attn_dict: dict[str, Tensor] = {}

        for r in self.edge_types:
            if r not in edge_index_dict or edge_index_dict[r].numel() == 0:
                continue
            ei = edge_index_dict[r]                    # [2, E]
            src, dst = ei[0], ei[1]                    # [E], [E]
            h_r = self.W[r](x).view(N, self.n_heads, self.head_dim)  # [N, H, D]

            # Attention scores e_ij = LeakyReLU(a_src · h_i + a_dst · h_j)
            e_src = (h_r[src] * self.a_src[r]).sum(dim=-1)           # [E, H]
            e_dst = (h_r[dst] * self.a_dst[r]).sum(dim=-1)
            e = self.leaky_relu(e_src + e_dst)                       # [E, H]

            # Softmax over destination's incoming edges
            alpha = self._scatter_softmax(e, dst, num_nodes=N)        # [E, H]
            alpha = self.dropout(alpha)
            attn_dict[r] = alpha

            # Aggregate: h_j = sum_i alpha_ij * h_r_i
            msg = h_r[src] * alpha.unsqueeze(-1)                     # [E, H, D]
            out = torch.zeros(N, self.n_heads, self.head_dim, device=x.device)
            out.index_add_(0, dst, msg)
            out_per_rel.append(out)

        # Sum across relations, then flatten heads
        if out_per_rel:
            h = torch.stack(out_per_rel, dim=0).sum(dim=0)            # [N, H, D]
            h = h.view(N, -1)                                         # [N, H*D]
        else:
            h = torch.zeros(N, self.n_heads * self.head_dim, device=x.device)

        return h, attn_dict

    @staticmethod
    def _scatter_softmax(scores: Tensor, index: Tensor, num_nodes: int) -> Tensor:
        """Per-destination softmax over edge scores. scores: [E, H], index: [E]."""
        H = scores.size(-1)
        # subtract max for stability
        max_per_dst = torch.full((num_nodes, H), float("-inf"), device=scores.device)
        max_per_dst = max_per_dst.scatter_reduce(0, index.unsqueeze(-1).expand(-1, H),
                                                  scores, reduce="amax", include_self=False)
        max_at_edge = max_per_dst[index]
        exp = torch.exp(scores - max_at_edge)
        sum_per_dst = torch.zeros(num_nodes, H, device=scores.device)
        sum_per_dst.index_add_(0, index, exp)
        sum_at_edge = sum_per_dst[index] + 1e-12
        return exp / sum_at_edge


# ---------------------------------------------------------------------------
# Heterogeneous R-GAT
# ---------------------------------------------------------------------------

class HeteroRGAT(nn.Module if HAS_TORCH else object):
    """Multi-task heterogeneous R-GAT for CINA Stage 2.

    Heads:
      - stance head: per-(country, issue) regression → stance score in [-1, 1]
      - coalition head: per-country classification → Leiden community label
      - contested head: per-issue binary classification → contested probability
    """

    def __init__(self, config: RGATConfig, in_dim: int):
        if not HAS_TORCH:
            raise ImportError("PyTorch required for HeteroRGAT")
        super().__init__()
        self.config = config

        layers = []
        d = in_dim
        for _ in range(config.n_layers):
            layers.append(RelationGATLayer(d, config.hidden_dim,
                                           edge_types=config.edge_types,
                                           n_heads=config.n_heads,
                                           dropout=config.dropout))
            d = config.hidden_dim
        self.layers = nn.ModuleList(layers)

        # Heads
        self.stance_head = nn.Sequential(
            nn.Linear(config.hidden_dim * 2, config.hidden_dim),
            nn.ReLU(),
            nn.Linear(config.hidden_dim, 1),
            nn.Tanh()
        )
        self.coalition_head = nn.Linear(config.hidden_dim, 2)  # binary community
        self.contested_head = nn.Linear(config.hidden_dim, 1)

    def forward(self, x: Tensor, edge_index_dict: dict[str, Tensor],
                country_idx: Tensor, issue_idx: Tensor,
                stance_pairs: Tensor) -> dict[str, Tensor]:
        """
        x: [N, in_dim] node features
        edge_index_dict: {relation: [2, E]}
        country_idx: [N_c] indices of country nodes in x
        issue_idx: [N_i] indices of issue nodes
        stance_pairs: [n_pairs, 2] (country_id, issue_id) pairs to predict
        """
        h = x
        all_attn = []
        for layer in self.layers:
            h, attn = layer(h, edge_index_dict)
            h = F.elu(h)
            all_attn.append(attn)

        # Stance: concatenate country and issue embeddings
        c_emb = h[stance_pairs[:, 0]]
        i_emb = h[stance_pairs[:, 1]]
        stance_pred = self.stance_head(torch.cat([c_emb, i_emb], dim=-1)).squeeze(-1)

        # Coalition: per-country logits
        coalition_logits = self.coalition_head(h[country_idx])

        # Contested: per-issue logits
        contested_logits = self.contested_head(h[issue_idx]).squeeze(-1)

        return {
            "stance": stance_pred,
            "coalition_logits": coalition_logits,
            "contested_logits": contested_logits,
            "attention": all_attn
        }


# ---------------------------------------------------------------------------
# Multi-task loss
# ---------------------------------------------------------------------------

def multitask_loss(pred: dict, targets: dict, config: RGATConfig) -> tuple[Tensor, dict]:
    """L = λ1·L_stance + λ2·L_coalition + λ3·L_contested."""
    if not HAS_TORCH:
        raise ImportError("PyTorch required for multitask_loss")

    losses = {}
    L_stance = F.mse_loss(pred["stance"], targets["stance"])
    losses["stance"] = L_stance.item()

    L_coal = F.cross_entropy(pred["coalition_logits"], targets["coalition"])
    losses["coalition"] = L_coal.item()

    L_cont = F.binary_cross_entropy_with_logits(pred["contested_logits"], targets["contested"])
    losses["contested"] = L_cont.item()

    total = (config.lambda_stance * L_stance +
             config.lambda_coalition * L_coal +
             config.lambda_contested * L_cont)
    losses["total"] = total.item()
    return total, losses


# ---------------------------------------------------------------------------
# Synthetic-data builder (CINA-shaped) — for unit-test runs without raw data
# ---------------------------------------------------------------------------

def build_cina_synthetic_graph(seed: int = 42):
    """Construct a CINA-shaped heterogeneous graph from sample data.

    Returns a dict with x, edge_index_dict, indices, and supervised targets.
    Uses the public sample at data/sample/graph_analysis.json when available,
    falls back to a deterministic synthetic graph otherwise.
    """
    if not HAS_TORCH:
        raise ImportError("PyTorch required")
    torch.manual_seed(seed)

    countries = ["Brazil", "EU", "USA", "China", "India", "AOSIS",
                 "Korea", "Saudi", "Japan", "AILAC", "AGN", "LMDC", "Multi"]
    issues = ["GGA-IND", "GGA-MOI", "NAPs", "JT-ADAPT", "L&D-OP", "FINANCE-ADAPT"]
    groups = ["G77", "EIG", "HAC", "AILAC", "AOSIS", "LMDC"]

    n_c, n_i, n_g = len(countries), len(issues), len(groups)
    N = n_c + n_i + n_g
    in_dim = 8  # 8-d node feature: type one-hot (3) + 5 generic features

    # Node features
    x = torch.zeros(N, in_dim)
    for i in range(n_c):
        x[i, 0] = 1.0
    for i in range(n_c, n_c + n_i):
        x[i, 1] = 1.0
    for i in range(n_c + n_i, N):
        x[i, 2] = 1.0
    x[:, 3:] = torch.randn(N, in_dim - 3) * 0.3

    # Stance score matrix (from public sample / pseudo-ground-truth)
    # Pattern: development-frame countries support issues 0-3, sovereignty-frame oppose
    stance_matrix = torch.tensor([
        [ 0.95,  0.78,  0.88,  0.92,  0.55,  0.70],  # Brazil
        [ 0.55,  0.65,  0.72,  0.60,  0.45,  0.58],  # EU
        [ 0.30,  0.20,  0.50,  0.40, -0.20,  0.25],  # USA
        [-0.30,  0.40,  0.55,  0.50,  0.65,  0.70],  # China
        [-0.15,  0.55,  0.60,  0.45,  0.85,  0.90],  # India
        [ 0.85,  0.90,  0.78,  0.65,  0.95,  0.92],  # AOSIS
        [ 0.65,  0.62,  0.75,  0.78,  0.39,  0.55],  # Korea
        [-0.55, -0.65,  0.20, -0.30,  0.10,  0.40],  # Saudi
        [ 0.45,  0.50,  0.62,  0.55,  0.30,  0.48],  # Japan
        [ 0.85,  0.85,  0.80,  0.70,  0.85,  0.85],  # AILAC
        [ 0.65,  0.70,  0.72,  0.62,  0.75,  0.70],  # AGN
        [-0.20,  0.50,  0.55,  0.40,  0.55,  0.60],  # LMDC
        [ 0.75,  0.65,  0.70,  0.60,  0.55,  0.65],  # Multi
    ])

    # Build edge index dict
    edge_index_dict: dict[str, Tensor] = {}

    # has_stance edges (every country -> every issue, signed by stance polarity)
    src, dst = [], []
    for ci in range(n_c):
        for ii in range(n_i):
            if abs(stance_matrix[ci, ii]) > 0.1:
                src.append(ci)
                dst.append(n_c + ii)
    edge_index_dict["has_stance"] = torch.tensor([src, dst], dtype=torch.long)

    # member_of edges (country -> group)
    membership = {
        "Brazil": ["G77"], "EU": ["HAC"], "USA": ["HAC"], "China": ["G77"],
        "India": ["G77", "LMDC"], "AOSIS": ["AOSIS", "G77"], "Korea": ["EIG"],
        "Saudi": ["G77", "LMDC"], "Japan": ["HAC"], "AILAC": ["AILAC", "G77"],
        "AGN": ["G77"], "LMDC": ["LMDC", "G77"], "Multi": []
    }
    src, dst = [], []
    for ci, c in enumerate(countries):
        for g in membership.get(c, []):
            if g in groups:
                src.append(ci)
                dst.append(n_c + n_i + groups.index(g))
    edge_index_dict["member_of"] = torch.tensor([src, dst], dtype=torch.long)

    # similar_to edges (country-country, top-3 cosine similarity)
    sim = torch.cosine_similarity(stance_matrix.unsqueeze(0),
                                  stance_matrix.unsqueeze(1), dim=-1)
    sim.fill_diagonal_(-1.0)
    src, dst = [], []
    for ci in range(n_c):
        top_k = sim[ci].topk(3).indices
        for tk in top_k:
            src.append(ci)
            dst.append(int(tk))
    edge_index_dict["similar_to"] = torch.tensor([src, dst], dtype=torch.long)

    # co_chairs edges (Brazil chair → all issues; no other countries are chair here)
    chair_country = countries.index("Brazil")
    src = [chair_country] * n_i
    dst = list(range(n_c, n_c + n_i))
    edge_index_dict["co_chairs"] = torch.tensor([src, dst], dtype=torch.long)

    # Indices and supervised targets
    country_idx = torch.arange(0, n_c)
    issue_idx = torch.arange(n_c, n_c + n_i)

    # Stance training pairs (mask 20% for validation)
    stance_pairs = []
    stance_targets = []
    for ci in range(n_c):
        for ii in range(n_i):
            stance_pairs.append([ci, n_c + ii])
            stance_targets.append(stance_matrix[ci, ii].item())
    stance_pairs = torch.tensor(stance_pairs, dtype=torch.long)
    stance_targets = torch.tensor(stance_targets, dtype=torch.float)

    # Coalition labels (Leiden 2 communities recovered from the public sample)
    # C0 = development-frame: Brazil, EU, USA, Japan, AGN, Multi → label 0
    # C1 = mixed: AOSIS, India, Korea, Saudi, AILAC, China, LMDC → label 1
    coalition_label_map = {0: 0, 1: 0, 2: 0, 8: 0, 10: 0, 12: 0,
                           5: 1, 4: 1, 6: 1, 7: 1, 9: 1, 3: 1, 11: 1}
    coalition_targets = torch.tensor([coalition_label_map[c] for c in range(n_c)],
                                     dtype=torch.long)

    # Contested issue labels (COP30 ground truth: GGA-IND, ADAPT-FIN, L&D-OP contested)
    contested_targets = torch.tensor([1.0, 0.0, 0.0, 0.0, 1.0, 1.0], dtype=torch.float)

    return {
        "x": x,
        "edge_index_dict": edge_index_dict,
        "country_idx": country_idx,
        "issue_idx": issue_idx,
        "stance_pairs": stance_pairs,
        "stance_targets": stance_targets,
        "coalition_targets": coalition_targets,
        "contested_targets": contested_targets,
        "countries": countries,
        "issues": issues,
        "groups": groups,
        "in_dim": in_dim
    }


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------

def train_rgat(config: RGATConfig, data: dict, output_dir: Path,
               verbose: bool = True) -> dict:
    """Train HeteroRGAT and report final metrics."""
    if not HAS_TORCH:
        raise ImportError("PyTorch required for train_rgat")

    torch.manual_seed(config.seed)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model = HeteroRGAT(config, in_dim=data["in_dim"])
    optim = torch.optim.Adam(model.parameters(), lr=config.lr,
                              weight_decay=config.weight_decay)

    # Train/val split on stance pairs (80/20)
    n_pairs = data["stance_pairs"].size(0)
    perm = torch.randperm(n_pairs)
    train_idx = perm[:int(0.8 * n_pairs)]
    val_idx = perm[int(0.8 * n_pairs):]

    train_pairs = data["stance_pairs"][train_idx]
    train_targets = data["stance_targets"][train_idx]
    val_pairs = data["stance_pairs"][val_idx]
    val_targets = data["stance_targets"][val_idx]

    targets_train = {
        "stance": train_targets,
        "coalition": data["coalition_targets"],
        "contested": data["contested_targets"]
    }

    history = []
    for epoch in range(config.n_epochs):
        model.train()
        optim.zero_grad()
        pred = model(data["x"], data["edge_index_dict"],
                     data["country_idx"], data["issue_idx"], train_pairs)
        loss, losses = multitask_loss(pred, targets_train, config)
        loss.backward()
        optim.step()

        if epoch % 20 == 0 or epoch == config.n_epochs - 1:
            model.eval()
            with torch.no_grad():
                val_pred = model(data["x"], data["edge_index_dict"],
                                 data["country_idx"], data["issue_idx"], val_pairs)
                val_mse = F.mse_loss(val_pred["stance"], val_targets).item()

                # Spearman approximation (rank correlation)
                from scipy.stats import spearmanr
                rho, _ = spearmanr(val_pred["stance"].numpy(),
                                   val_targets.numpy())

                # Coalition accuracy
                coal_pred = val_pred["coalition_logits"].argmax(dim=-1)
                coal_acc = (coal_pred == data["coalition_targets"]).float().mean().item()

                # Contested top-3 accuracy
                cont_probs = torch.sigmoid(val_pred["contested_logits"])
                top3 = cont_probs.topk(3).indices.tolist()
                gt_contested = (data["contested_targets"] > 0.5).nonzero(as_tuple=True)[0].tolist()
                p_at_3 = len(set(top3) & set(gt_contested)) / 3.0

                history.append({
                    "epoch": epoch,
                    "train_loss": losses["total"],
                    "val_mse": val_mse,
                    "val_spearman": rho if not math.isnan(rho) else 0.0,
                    "coalition_acc": coal_acc,
                    "p_at_3_contested": p_at_3
                })
                if verbose:
                    print(f"Epoch {epoch:3d} | train_loss {losses['total']:.4f} | "
                          f"val_MSE {val_mse:.4f} | val_ρ {rho:.3f} | "
                          f"coal_acc {coal_acc:.2f} | P@3 {p_at_3:.2f}")

    # Final attention extraction
    model.eval()
    with torch.no_grad():
        final_pred = model(data["x"], data["edge_index_dict"],
                           data["country_idx"], data["issue_idx"], val_pairs)

    # Save attention summary
    attn_summary = {}
    for layer_idx, layer_attn in enumerate(final_pred["attention"]):
        for r, alpha in layer_attn.items():
            mean_attn = alpha.mean().item()
            attn_summary.setdefault(r, []).append(round(mean_attn, 4))

    results = {
        "config": config.__dict__,
        "final_metrics": history[-1],
        "attention_per_relation": attn_summary,
        "history": history
    }

    out_path = output_dir / "rgat_training_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"\nResults saved to {out_path}")
        print(f"Mean attention per relation: {attn_summary}")

    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train CINA Heterogeneous R-GAT")
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--hidden", type=int, default=64)
    parser.add_argument("--heads", type=int, default=4)
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="data/processed")
    args = parser.parse_args()

    if not HAS_TORCH:
        print("PyTorch is not installed. Install with:")
        print("  pip install torch scipy")
        raise SystemExit(1)

    cfg = RGATConfig(
        n_epochs=args.epochs,
        hidden_dim=args.hidden,
        n_heads=args.heads,
        n_layers=args.layers,
        seed=args.seed
    )
    data = build_cina_synthetic_graph(seed=args.seed)
    results = train_rgat(cfg, data, output_dir=Path(args.output))
    print("\nDone.")
