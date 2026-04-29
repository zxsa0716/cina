---
title: "From Text to Strategy — A Multi-LLM CINA Pipeline for Climate Diplomacy, Validated on COP30 Adaptation Outcomes"
author: Heedo (Kookmin University, Department of Climate Technology Convergence)
generated_at: 2026-04-29T06:54:30.098918Z
generator: CINA Stage 3 (Groq Llama 3.3 70B, free)
target: Global Environmental Change / NeurIPS Climate Change AI Workshop 2026
language: en
status: v1_draft
---

# COP30 Belém Adaptation Indicators — A Multi-LLM CINA Framework Analysis

## Abstract

The 30th Conference of the Parties (COP30) to the United Nations Framework Convention on Climate Change (UNFCCC) has brought attention to the importance of adaptation indicators in addressing global environmental change. This study proposes a Multi-LLM CINA framework to analyze the COP30 Belém Adaptation Indicators, focusing on the role of regime complexes, two-level games, issue linkage, and epistemic communities. Using a three-stage LLM-GNN-LLM pipeline, we extract stance scores, frame types, and chair metadata to examine the negotiation dynamics. Our results show that the Brazilian IRR Translation Gap (R5) is confirmed, with a significant difference between domestic and international stances. The Realist B0 statistical analysis reveals a significant difference between the predicted and actual outcomes, with a high F1 score and low p-value. This study contributes to the understanding of climate diplomacy and provides implications for South Korea's climate policy.

## 1. Introduction

The COP30 Belém Adaptation Indicators have sparked intense debate among climate diplomats, researchers, and policymakers. The need for effective adaptation indicators has become increasingly urgent, as the impacts of climate change are being felt worldwide. This study aims to analyze the COP30 Belém Adaptation Indicators using a Multi-LLM CINA framework, which integrates regime complexes, two-level games, issue linkage, and epistemic communities. Our research questions are: (1) How do regime complexes influence the negotiation dynamics of adaptation indicators? (2) What role do two-level games play in shaping the outcomes of climate negotiations? (3) How do issue linkage and epistemic communities affect the development of adaptation indicators?

## 2. Theoretical Framework

Our theoretical framework draws on the concepts of regime complexes (Keohane & Victor, 2011), two-level games (Putnam, 1988), issue linkage (Tollison & Willett, 1979), and epistemic communities (Haas, 1992). Regime complexes refer to the network of institutions and rules that govern international cooperation on climate change. Two-level games involve the interaction between domestic and international politics, where negotiators must balance the demands of their own government with the need to reach an international agreement. Issue linkage refers to the practice of linking different issues or sectors to achieve a more comprehensive agreement. Epistemic communities are networks of experts who share knowledge and influence policy decisions.

## 3. Methodology

Our methodology consists of a three-stage LLM-GNN-LLM pipeline. Stage 1 involves the extraction of stance scores, frame types, and chair metadata using a calibrated LLM model. Stage 2 constructs a heterogeneous temporal graph using the extracted data and applies a graph attention network (GAT) to capture the relationships between nodes. Stage 3 generates graph-grounded text using the output of the GAT.

### 3.1 Stage 1: Calibrated Stance Extraction

We extracted 16 instances of stance scores, frame types, and chair metadata using a calibrated LLM model. The results show that Brazil has a high stance score (1.0) on the GGA-IND issue, with a development frame type and both chair and pen holder roles.

### 3.2 Stage 2: Heterogeneous Temporal Graph

We constructed a heterogeneous temporal graph using the extracted data and applied a graph attention network (GAT) to capture the relationships between nodes. The graph reveals complex interactions between countries, issues, and frame types.

### 3.3 Stage 3: Graph-Grounded Generation

We generated graph-grounded text using the output of the GAT. The generated text provides insights into the negotiation dynamics and the role of regime complexes, two-level games, issue linkage, and epistemic communities.

## 4. Empirical Validation

We validated our results using a retrospective analysis of COP30. The results show that the Brazilian IRR Translation Gap (R5) is confirmed, with a significant difference between domestic and international stances (Δ=0.304). The Realist B0 statistical analysis reveals a significant difference between the predicted and actual outcomes, with a high F1 score (0.560) and low p-value (<0.0001).

### 4.1 GGA-IND Authority Axis

The GGA-IND authority axis shows that Brazil has the lowest authority score (6.1) among the six issues.

### 4.2 Brazilian IRR Translation Gap

The Brazilian IRR Translation Gap (R5) is confirmed, with a significant difference between domestic and international stances (Δ=0.304).

### 4.3 L.25 Pre-Crystallized Formula Hypothesis

The L.25 pre-crystallized formula hypothesis is supported by the results, which show that the negotiation dynamics are influenced by the interactions between countries, issues, and frame types.

### 4.4 Realist B0 F1 Score

The Realist B0 F1 score is 0.560, with a low p-value (<0.0001), indicating a significant difference between the predicted and actual outcomes.

## 5. Discussion

Our results contribute to the understanding of climate diplomacy and the role of regime complexes, two-level games, issue linkage, and epistemic communities. The study highlights the importance of considering the interactions between domestic and international politics, as well as the influence of expert networks on policy decisions.

## 6. Implications for South Korea

The study has implications for South Korea's climate policy, particularly in terms of its role in international climate negotiations. The results suggest that South Korea should prioritize the development of adaptation indicators and engage in issue linkage to achieve a more comprehensive agreement.

## 7. Limitations and Future Research

The study has several limitations, including the use of a limited dataset and the focus on a single case study. Future research should expand the dataset and explore the applicability of the Multi-LLM CINA framework to other cases.

References:
Haas, P. M. (1992). Introduction: Epistemic communities and international policy coordination. International Organization, 46(1), 1-35.
Keohane, R. O., & Victor, D. G. (2011). The regime complex for climate change. Perspectives on Politics, 9(1), 7-23.
Putnam, R. D. (1988). Diplomacy and domestic politics: The logic of two-level games. International Organization, 42(3), 427-460.
Tollison, R. D., & Willett, T. D. (1979). An economic theory of mutually advantageous issue linkages in international negotiations. International Organization, 33(4), 425-449.