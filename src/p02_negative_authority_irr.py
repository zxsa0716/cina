"""
P0-2: Brazilian L.25E Negative Authority Separation + IRR_intl Recalculation
CINA Round 5 - Data Refinement Agent

Rule-based extraction of negative binding patterns vs positive binding patterns.
Recalculate IRR_intl_revised and delta_revised.
"""
import re
import json
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'C:/Users/admin/Desktop/대학원수업/1학기/리더쉽'

# Load pre-extracted L.25E text
l25e_text_path = f'{BASE}/data/processed/temp_l25e_text.txt'
with open(l25e_text_path, 'r', encoding='utf-8') as f:
    l25e_text = f.read()

print(f"L.25E text loaded: {len(l25e_text)} chars")

# --- NATO 4-axis keyword patterns (same as Round 4) ---
NATO_PATTERNS_EN = {
    "Nodality": r"\b(voluntary|non-prescriptive|facilitative|non-punitive|indicator|reporting|information|transparency|encourage|invite|invites|encourages)\b",
    "Authority_positive": r"\b(shall\s+(?!not|NOT)|must\s+(?!not)|decides to|calls upon|requests|reaffirms)\b",
    "Authority_negative": r"\b(shall not|shall NOT|should not|not create|not become|not be used|not establish|without prejudice|no single)\b",
    "Treasure": r"\b(finance|fund|resource|investment|GCF|GEF|billion|budget|financial)\b",
    "Organization": r"\b(committee|secretariat|bodies|body|programme|plan|mechanism|taskforce|technical|expert|group|network)\b",
}

# Run pattern matching on full document
counts = {}
matches_dict = {}
for axis, pattern in NATO_PATTERNS_EN.items():
    matches = re.findall(pattern, l25e_text, re.IGNORECASE)
    counts[axis] = len(matches)
    matches_dict[axis] = list(set(m.lower().strip() if isinstance(m, str) else m[0].lower().strip() for m in matches))

print("\n--- NATO 4-axis counts (with Authority split) ---")
for k, v in counts.items():
    print(f"  {k}: {v}")

# --- Para-by-para analysis for evidence quotes ---
# Split into numbered paragraphs
para_pattern = r'\n(\d+)\.\s+'
paras = re.split(para_pattern, l25e_text)

para_list = []
i = 1
while i < len(paras) - 1:
    para_num_str = paras[i]
    para_text = paras[i+1].strip() if i+1 < len(paras) else ''
    try:
        para_num = int(para_num_str)
        para_list.append({'para_num': para_num, 'text': para_text[:400]})
    except ValueError:
        pass
    i += 2

# Specific negative authority paras
NEG_AUTH_PATTERNS = [
    r'shall not',
    r'shall NOT',
    r'should not',
    r'not create new obligations',
    r'not become a barrier',
    r'not be used',
    r'not establish',
    r'nor.*liability',
    r'nor establish',
    r'no single.*approach',
    r'without prejudice',
]

neg_auth_evidence = []
for para in para_list:
    text = para['text']
    hits = []
    for pat in NEG_AUTH_PATTERNS:
        found = re.findall(pat, text, re.IGNORECASE)
        hits.extend(found)
    if hits:
        neg_auth_evidence.append({
            'para_num': para['para_num'],
            'patterns_found': list(set(hits)),
            'excerpt': text[:300]
        })

print(f"\n--- Negative Authority paragraphs: {len(neg_auth_evidence)} ---")
for ev in neg_auth_evidence:
    print(f"  Para {ev['para_num']}: {ev['patterns_found']}")
    print(f"    Excerpt: {ev['excerpt'][:150]}...")

# --- IRR Recalculation ---
# Round 4 baseline (Scenario A)
authority_r4 = 21  # total Authority (positive + negative combined)
nodality_r4 = 84
treasure_r4 = 12
organization_r4 = 56
total_r4 = 173

# Scenario A (Round 4, no split)
irr_domestic = 0.714  # from Plano Clima analysis
irr_intl_A = (authority_r4 + organization_r4) / total_r4
delta_A = irr_domestic - irr_intl_A

print(f"\n--- Scenario A (Round 4, no Authority split) ---")
print(f"  Authority_total: {authority_r4}")
print(f"  IRR_intl_A = ({authority_r4} + {organization_r4}) / {total_r4} = {irr_intl_A:.3f}")
print(f"  Delta_A = {irr_domestic} - {irr_intl_A:.3f} = {delta_A:.3f}")

# Scenario B (Round 5: split negative Authority)
# Re-count from text
authority_positive_n = counts['Authority_positive']
authority_negative_n = counts['Authority_negative']
nodality_n = counts['Nodality']
treasure_n = counts['Treasure']
organization_n = counts['Organization']

# Total recalculated (use positive Authority only in IRR numerator)
# Negative Authority REDUCES effective binding power
# IRR_intl_revised = (Authority_positive + Organization) / (Authority_positive + Authority_negative + Nodality + Treasure + Organization)
total_B = authority_positive_n + authority_negative_n + nodality_n + treasure_n + organization_n
irr_intl_B = (authority_positive_n + organization_n) / total_B if total_B > 0 else 0
delta_B = irr_domestic - irr_intl_B

print(f"\n--- Scenario B (Round 5: negative Authority separated) ---")
print(f"  Authority_positive: {authority_positive_n}")
print(f"  Authority_negative: {authority_negative_n}")
print(f"  Nodality: {nodality_n}")
print(f"  Treasure: {treasure_n}")
print(f"  Organization: {organization_n}")
print(f"  Total_B: {total_B}")
print(f"  IRR_intl_B = ({authority_positive_n} + {organization_n}) / {total_B} = {irr_intl_B:.3f}")
print(f"  Delta_B = {irr_domestic} - {irr_intl_B:.3f} = {delta_B:.3f}")
print(f"  Hypothesis Delta >= 0.30: {'CONFIRMED' if delta_B >= 0.30 else 'PARTIAL (delta=' + str(round(delta_B,3)) + ')'}")

# --- Save JSON output ---
result = {
    'analysis_label': 'IRR_Brazilian_Translation_Gap_v2_NegAuth',
    'processing_version': 'round5-v1.4',
    'processed_at': '2026-04-26T00:00:00Z',
    'source_doc': 'FCCC/PA/CMA/2025/L.25E',
    'irr_domestic': irr_domestic,
    'scenario_A': {
        'description': 'Round 4 baseline - no Authority split',
        'authority_total': authority_r4,
        'nodality': nodality_r4,
        'treasure': treasure_r4,
        'organization': organization_r4,
        'total': total_r4,
        'irr_intl': round(irr_intl_A, 4),
        'delta': round(delta_A, 4),
        'hypothesis_030': 'PARTIAL',
    },
    'scenario_B': {
        'description': 'Round 5 revised - negative Authority separated',
        'authority_positive': authority_positive_n,
        'authority_negative': authority_negative_n,
        'nodality': nodality_n,
        'treasure': treasure_n,
        'organization': organization_n,
        'total': total_B,
        'irr_intl': round(irr_intl_B, 4),
        'delta': round(delta_B, 4),
        'hypothesis_030': 'CONFIRMED' if delta_B >= 0.30 else f'PARTIAL (delta={delta_B:.3f})',
    },
    'delta_shift': round(delta_B - delta_A, 4),
    'negative_authority_evidence': neg_auth_evidence,
    'key_evidence_quotes': [
        {
            'para': 7,
            'quote': 'Emphasizes that the Belem Adaptation Indicators are voluntary, non-prescriptive, non-punitive, facilitative, global in nature, respectful of national sovereignty and national circumstances and country-driven, and that the indicators should not create additional reporting burdens... shall not become a barrier and shall not be used under any circumstances as a condition for developing country Parties to access funding.',
            'pattern_type': 'authority_negative + nodality'
        },
        {
            'para': 9,
            'quote': 'Affirms that the Belem Adaptation Indicators... shall not create new obligations for developing country Parties, benchmarks or evaluation criteria, nor establish global standardized methodologies or data-collection processes, nor establish any compliance frameworks.',
            'pattern_type': 'authority_negative (multiple)'
        },
        {
            'para': 31,
            'quote': 'Emphasizes that no single adaptation approach shall be presented as the default, superior or universally applicable pathway.',
            'pattern_type': 'authority_negative (sovereignty protection)'
        }
    ]
}

out_path = f'{BASE}/data/processed/irr_brazilian_translation_gap_v2.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\nSaved to {out_path}")
