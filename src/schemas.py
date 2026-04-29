"""CINA 공통 Pydantic 스키마."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class EvidenceQuote(BaseModel):
    quote: str = Field(..., min_length=20)
    source_doc_id: str
    paragraph: int | None = None
    confidence: float = Field(0.5, ge=0.0, le=1.0)


class ExtractionMetadata(BaseModel):
    model: str
    temperature: float
    samples: int
    prompt_version: str
    prompt_hash: str | None = None
    extracted_at: datetime
    extraction_latency_sec: float | None = None


class EpistemicAlignment(BaseModel):
    cites_ipcc: bool = False
    cites_leg_technical: bool = False
    aligns_with_expert_proposal: Literal["full", "partial", "divergent", "unknown"] = "unknown"


StanceCategory = Literal[
    "strong_support", "support", "conditional_support",
    "neutral_or_silent", "oppose", "strong_oppose",
]


class Stance(BaseModel):
    """Stage 1 스탠스 레코드. docs/03_data_architecture.md §4 준수."""
    stance_id: str
    country: str
    iso3: str | None = None
    issue: str  # e.g., "GGA-IND"
    issue_description: str | None = None
    cop_session: str
    date_context: str

    stance_score_raw_samples: list[float] = Field(default_factory=list)
    stance_score_mean: float = Field(..., ge=-1.0, le=1.0)
    stance_score_std: float = 0.0
    stance_score_calibrated: float = Field(..., ge=-1.0, le=1.0)
    ci_lower_95: float = Field(..., ge=-1.0, le=1.0)
    ci_upper_95: float = Field(..., ge=-1.0, le=1.0)

    stance_category: StanceCategory
    key_demands: list[str] = Field(default_factory=list, max_length=5)
    red_lines: list[str] = Field(default_factory=list, max_length=3)
    flexibility_signals: list[str] = Field(default_factory=list, max_length=5)

    evidence_quotes: list[EvidenceQuote] = Field(..., min_length=1)
    epistemic_alignment: EpistemicAlignment = Field(default_factory=EpistemicAlignment)
    extraction_metadata: ExtractionMetadata


class Document(BaseModel):
    """수집된 문서 정규화 스키마. docs/03 §3."""
    doc_id: str
    source: str
    cop_session: str
    subsidiary_body: str | None = None
    document_type: str
    date: str
    authors: list[str]
    topics: list[str] = Field(default_factory=list)
    language: str = "en"
    full_text: str
    paragraphs: list[dict] = Field(default_factory=list)
    url: str | None = None
    retrieved_at: datetime
    sha256: str


class CommunityCluster(BaseModel):
    cluster_id: int
    label: str | None = None
    countries: list[str]
    centroid_stance: float
    within_cluster_agreement: float | None = None


class BridgeCountry(BaseModel):
    country: str
    betweenness: float
    rationale: str | None = None


class CrossIssueHyperedge(BaseModel):
    issues: list[str]
    countries: list[str]
    support: float
    pattern: Literal["linked_concession", "package_demand", "divergent"]
    interpretation: str | None = None


class EpistemicDivergence(BaseModel):
    predicted_divergence_risk: float
    high_political_weight_dissenters: list[str]
    interpretation: str | None = None


class IssueAnalysis(BaseModel):
    issue_code: str
    communities: list[CommunityCluster]
    bridge_countries: list[BridgeCountry]
    top_attention_nodes: list[dict]


class GraphAnalysis(BaseModel):
    """Stage 2 출력. docs/05 §5 준수."""
    timestamp: datetime
    model_version: str
    focal_country: str
    issue_analyses: dict[str, IssueAnalysis]
    cross_issue_hyperedges: list[CrossIssueHyperedge]
    epistemic_divergence: dict[str, EpistemicDivergence]


class VerifiedClaim(BaseModel):
    claim_id: str
    sentence: str
    evidence_quote: str | None = None
    source_doc_id: str | None = None
    structural_fact: str | None = None
    confidence: float


class VerificationReport(BaseModel):
    draft_section: str
    verified_claims: list[VerifiedClaim]
    unverified_claims: list[dict]
    warnings: list[dict]
    total_sentences: int
    verified_count: int
    unverified_count: int
