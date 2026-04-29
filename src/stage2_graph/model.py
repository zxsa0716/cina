"""Heterogeneous Graph Attention Network for CINA.

docs/05_stage2_graph_analysis.md §2 참조.
"""
from __future__ import annotations

import torch
import torch.nn as nn
from torch_geometric.nn import GATv2Conv, HeteroConv, Linear


class CINAHeteroGAT(nn.Module):
    """Heterogeneous GAT for country × issue × group climate negotiation graph."""

    def __init__(
        self,
        metadata: tuple[list[str], list[tuple[str, str, str]]],
        hidden_dim: int = 64,
        num_layers: int = 3,
        heads: int = 4,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        node_types, edge_types = metadata

        self.node_embed = nn.ModuleDict(
            {nt: Linear(-1, hidden_dim) for nt in node_types}
        )

        self.convs = nn.ModuleList()
        for _ in range(num_layers):
            conv = HeteroConv(
                {
                    et: GATv2Conv(
                        (-1, -1),
                        hidden_dim,
                        heads=heads,
                        concat=False,
                        add_self_loops=False,
                        dropout=dropout,
                    )
                    for et in edge_types
                },
                aggr="sum",
            )
            self.convs.append(conv)

        self.readout = nn.ModuleDict(
            {nt: Linear(hidden_dim, hidden_dim) for nt in node_types}
        )
        self.dropout = dropout

    def forward(self, x_dict, edge_index_dict, return_attention: bool = False):
        x_dict = {k: self.node_embed[k](v).relu() for k, v in x_dict.items()}
        attn = [] if return_attention else None
        for conv in self.convs:
            if return_attention:
                x_dict, a = conv(
                    x_dict, edge_index_dict, return_attention_weights=True
                )
                attn.append(a)
            else:
                x_dict = conv(x_dict, edge_index_dict)
            x_dict = {k: torch.relu(v) for k, v in x_dict.items()}
        out = {k: self.readout[k](v) for k, v in x_dict.items()}
        if return_attention:
            return out, attn
        return out


def stance_link_loss(
    embeddings: dict, edge_index: torch.Tensor, edge_attr: torch.Tensor
) -> torch.Tensor:
    """Stance edge weight reconstruction loss (MSE)."""
    src = embeddings["country"][edge_index[0]]
    dst = embeddings["issue"][edge_index[1]]
    pred = (src * dst).sum(dim=-1)
    return torch.nn.functional.mse_loss(pred, edge_attr.float())


def coalition_triplet_loss(
    country_emb: torch.Tensor,
    positive_pairs: torch.Tensor,
    negative_pairs: torch.Tensor,
    margin: float = 1.0,
) -> torch.Tensor:
    """Triplet loss for coalition consistency.

    positive_pairs: (M, 2) indices of same-group countries
    negative_pairs: (M, 2) indices of different-group countries
    """
    anchor = country_emb[positive_pairs[:, 0]]
    pos = country_emb[positive_pairs[:, 1]]
    neg = country_emb[negative_pairs[:, 1]]
    d_pos = (anchor - pos).pow(2).sum(dim=-1)
    d_neg = (anchor - neg).pow(2).sum(dim=-1)
    return torch.clamp(d_pos - d_neg + margin, min=0).mean()
