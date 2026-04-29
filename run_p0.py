import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import fitz, re, json, math, os, csv

BASE = os.path.join(os.path.expanduser('~'), 'Desktop', '대학원수업', '1학기', '리더쉽')

def extract_pdf(relpath):
    path = os.path.join(BASE, *relpath.split('/'))
    doc = fitz.open(path)
    return '\n'.join(doc[i].get_text() for i in range(len(doc)))

###############################################################################
# P0-2: Brazilian IRR cross-walk
###############################################################################

apresentacao = extract_pdf('data/raw/round3/Brazilian_Plano_Clima/Brazil_Plano_Clima_Apresentacao_May2024.pdf')
sumario = extract_pdf('data/raw/round3/Brazilian_Plano_Clima/Brazil_Plano_Clima_Sumario_Executivo_2024_2035.pdf')
vol1 = extract_pdf('data/raw/round3/Brazilian_Plano_Clima/Brazil_Plano_Nacional_Adaptacao_Vol1.pdf')
l25_final = extract_pdf('data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L25E_final.pdf')
l25_advance = extract_pdf('data/raw/unfccc_submissions/cop30_curated/FCCC_PA_CMA_2025_L25_advance.pdf')

plano = apresentacao + '\n' + sumario + '\n' + vol1
print(f"Plano chars: {len(plano)}, L25E chars: {len(l25_final)}, L25 adv chars: {len(l25_advance)}")

NATO_PT = {
    'nodality': [r'indicador', r'monitoramento', r'transpar\w+', r'relat[oó]rio', r'informa[cç][aã]o',
                 r'\bdados\b', r'diagn[oó]stico', r'conhecimento', r'sistema de informa',
                 r'avalia[cç][aã]o', r'comunica[cç][aã]o'],
    'authority': [r'marcos? regulat[oó]rio', r'\blei\b', r'decreto', r'obrigat[oó]ri\w+', r'mandat[oó]rio',
                  r'regula[cç][aã]o', r'\bnorma\b', r'portaria', r'resolu[cç][aã]o', r'PNMC',
                  r'pol[ií]tica nacional', r'artigo \d+', r'instrução normativa'],
    'treasure':  [r'financiamento', r'\bfundo\b', r'investimento', r'or[cç]amento', r'cr[eé]dito',
                  r'subs[ií]dio', r'tribut\w+', r'R\$', r'financeiro', r'fundo clim[aá]tico',
                  r'recursos? financ'],
    'organization': [r'comit[eê]', r'secretaria', r'minist[eé]rio', r'\bprograma\b', r'\bplano\b',
                     r'estrat[eé]gia', r'grupo t[eé]cnico', r'comiss[aã]o', r'coordena',
                     r'implementa[cç][aã]o', r'governan[cç]a', r'\bCIM\b', r'planos setoriais',
                     r'mecanismo de acompanhamento'],
}

NATO_EN = {
    'nodality': [r'voluntary', r'non-prescriptive', r'facilitative', r'non-punitive',
                 r'indicator', r'reporting', r'information', r'transparency', r'encourage\w*',
                 r'knowledge', r'invites?'],
    'authority': [r'\bshall\b', r'\bmust\b', r'obligat\w+', r'\brequire\w*', r'decides? to',
                  r'calls upon', r'\brequests?\b'],
    'treasure':  [r'financ\w+', r'\bfund\w*\b', r'resource\w*', r'investm\w+', r'\bGCF\b',
                  r'\bGEF\b', r'billion', r'budget'],
    'organization': [r'committee', r'secretariat', r'\bbod(y|ies)\b', r'programme', r'\bplan\b',
                     r'mechanism', r'taskforce', r'work programme', r'technical\w*', r'expert\w*'],
}

def count_pats(text, pats):
    return sum(len(re.findall(p, text, re.IGNORECASE)) for p in pats)

dom = {ax: count_pats(plano, pats) for ax, pats in NATO_PT.items()}
intl = {ax: count_pats(l25_final, pats) for ax, pats in NATO_EN.items()}

dom_total = sum(dom.values())
intl_total = sum(intl.values())

print(f"\nDOMESTIC Plano Clima: N={dom['nodality']} A={dom['authority']} T={dom['treasure']} O={dom['organization']} TOTAL={dom_total}")
print(f"INTERNATIONAL L.25E : N={intl['nodality']} A={intl['authority']} T={intl['treasure']} O={intl['organization']} TOTAL={intl_total}")

# IRR: proportion of Authority+Organization (binding/implementation axis)
irr_dom  = round((dom['authority']  + dom['organization'])  / dom_total,  3) if dom_total  else 0
irr_intl = round((intl['authority'] + intl['organization']) / intl_total, 3) if intl_total else 0
gap = round(irr_dom - irr_intl, 3)

print(f"\nIRR_domestic  = {irr_dom}")
print(f"IRR_intl      = {irr_intl}")
print(f"Delta (Gap)   = {gap}  ({'CONFIRMED >=0.30' if gap >= 0.30 else 'PARTIAL >=0.20' if gap >= 0.20 else 'NOT_CONFIRMED'})")

# Also compute per-axis share (distribution)
dom_dist  = {ax: round(v/dom_total, 3)  if dom_total  else 0 for ax, v in dom.items()}
intl_dist = {ax: round(v/intl_total, 3) if intl_total else 0 for ax, v in intl.items()}
print(f"\nDomestic distribution: {dom_dist}")
print(f"International distribution: {intl_dist}")

brazil_data = {
    "domestic_plano_clima": {"counts": dom, "total": dom_total, "distribution": dom_dist, "IRR": irr_dom},
    "international_l25e": {"counts": intl, "total": intl_total, "distribution": intl_dist, "IRR": irr_intl},
    "translation_gap": gap,
    "hypothesis_confirmed": gap >= 0.30,
    "method": "NATO 4-axis keyword count (A+O proportion = IRR proxy)",
    "sources": ["Brazil_Plano_Clima_3_PDFs", "FCCC_PA_CMA_2025_L25E_final.pdf"]
}

out_path = os.path.join(BASE, 'data', 'processed', 'brazil_instrument_translation.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(brazil_data, f, ensure_ascii=False, indent=2)
print(f"\nSaved: {out_path}")

###############################################################################
# P0-3: Realist B0 baseline F1
###############################################################################
print("\n\n=== P0-3: Realist B0 Similarity Matrix ===")

import numpy as np

b0_path = os.path.join(BASE, 'data', 'processed', 'realist_baseline_b0.csv')
countries = []
features = []

with open(b0_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            co2_pc = float(row['co2_per_capita_t']) if row['co2_per_capita_t'] else None
            share  = float(row['share_global_co2_pct']) if row['share_global_co2_pct'] else None
            gdp    = float(row['gdp']) if row['gdp'] else None
            if co2_pc is not None and share is not None:
                countries.append(row['iso3'])
                features.append([co2_pc, share, math.log(gdp+1) if gdp else 0])
        except:
            pass

print(f"Countries loaded: {len(countries)}: {countries}")

# Normalize features
F = []
for i in range(3):
    col = [features[j][i] for j in range(len(features))]
    mean_v = sum(col)/len(col)
    std_v  = math.sqrt(sum((x-mean_v)**2 for x in col)/len(col)) or 1.0
    F.append([(x - mean_v)/std_v for x in col])

feat_norm = [[F[i][j] for i in range(3)] for j in range(len(countries))]

def cosine_sim(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na  = math.sqrt(sum(x*x for x in a))
    nb  = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0: return 0
    return dot / (na * nb)

N = len(countries)
sim_matrix = [[0.0]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        sim_matrix[i][j] = round(cosine_sim(feat_norm[i], feat_norm[j]), 4)

# Print matrix
print("Cosine similarity matrix (first 5x5):")
header = [''] + countries[:5]
print('\t'.join(header))
for i in range(min(5, N)):
    row = [countries[i]] + [str(sim_matrix[i][j]) for j in range(min(5, N))]
    print('\t'.join(row))

# Save full matrix as CSV
sim_out = os.path.join(BASE, 'data', 'processed', 'realist_b0_similarity_matrix.csv')
with open(sim_out, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['iso3'] + countries)
    for i in range(N):
        writer.writerow([countries[i]] + [f"{sim_matrix[i][j]:.4f}" for j in range(N)])
print(f"Saved: {sim_out}")

# Pseudo-truth: group membership based cooperation
GROUP_MEMBERSHIPS = {
    'BRA': ['G77', 'BASIC', 'LMDC'],
    'CHN': ['G77', 'BASIC', 'LMDC'],
    'IND': ['G77', 'BASIC', 'LMDC'],
    'ZAF': ['G77', 'BASIC'],
    'USA': ['UMBRELLA'],
    'CAN': ['UMBRELLA'],
    'AUS': ['UMBRELLA'],
    'JPN': ['UMBRELLA'],
    'KOR': ['EIG'],
    'CHE': ['EIG'],
    'NOR': ['EIG'],
    'MEX': ['G77'],
    'COL': ['G77', 'AILAC'],
    'CHL': ['G77', 'AILAC'],
    'CRI': ['G77', 'AILAC'],
    'SAU': ['G77', 'ARAB'],
    'ARE': ['G77', 'ARAB'],
    'EGY': ['G77', 'ARAB'],
    'KEN': ['G77', 'AGN'],
}

def same_group(iso1, iso2):
    g1 = set(GROUP_MEMBERSHIPS.get(iso1, []))
    g2 = set(GROUP_MEMBERSHIPS.get(iso2, []))
    return len(g1 & g2) > 0

# Build pseudo-truth cooperation pairs (same group = 1)
truth_pairs = set()
for i in range(N):
    for j in range(i+1, N):
        if same_group(countries[i], countries[j]):
            truth_pairs.add((countries[i], countries[j]))

print(f"\nPseudo-truth cooperative pairs: {len(truth_pairs)}")

# Top-K realist predictions
K = len(truth_pairs)
all_pairs = []
for i in range(N):
    for j in range(i+1, N):
        all_pairs.append((sim_matrix[i][j], countries[i], countries[j]))

all_pairs.sort(reverse=True)
top_k = set((b, c) for _, b, c in all_pairs[:K])

# F1 calculation
tp = len(top_k & truth_pairs)
fp = len(top_k - truth_pairs)
fn = len(truth_pairs - top_k)

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
f1        = 2*precision*recall / (precision + recall) if (precision + recall) > 0 else 0

print(f"Top-{K} pairs: TP={tp}, FP={fp}, FN={fn}")
print(f"Precision={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f}")
print(f"Hypothesis F1 < 0.7: {'CONFIRMED (realism insufficient)' if f1 < 0.70 else 'REJECTED (realism sufficient)'}")

b0_result = {
    "countries": countries,
    "K": K,
    "truth_pairs_count": len(truth_pairs),
    "top_k_predicted": K,
    "TP": tp, "FP": fp, "FN": fn,
    "precision": round(precision, 3),
    "recall": round(recall, 3),
    "f1": round(f1, 3),
    "hypothesis_f1_lt_0.7": f1 < 0.70,
    "interpretation": "Realism alone insufficient -> CINA constructivist+frame vars needed" if f1 < 0.70 else "Realism provides good baseline"
}

###############################################################################
# P0-4: L.25 advance vs final paragraph-level cosine diff
###############################################################################
print("\n\n=== P0-4: L.25 advance vs final paragraph diff ===")

def split_paragraphs(text):
    # Split on numbered paragraphs like "1.\n" or "1. " or lettered "(a)"
    # Also split on double newlines
    parts = re.split(r'\n\s*(?=\d+\.\s|\([a-z]+\)\s)', text)
    paras = []
    for p in parts:
        p = p.strip()
        if len(p) > 50:
            paras.append(p)
    return paras

adv_paras = split_paragraphs(l25_advance)
fin_paras = split_paragraphs(l25_final)
print(f"Advance paragraphs: {len(adv_paras)}, Final paragraphs: {len(fin_paras)}")

# TF-IDF cosine similarity
from collections import Counter

def tokenize(text):
    return re.findall(r'\b[a-z]{3,}\b', text.lower())

def tfidf_cosine(a_tokens, b_tokens, vocab_counter=None):
    ca = Counter(a_tokens)
    cb = Counter(b_tokens)
    vocab = set(ca.keys()) | set(cb.keys())
    dot = sum(ca.get(w, 0) * cb.get(w, 0) for w in vocab)
    na  = math.sqrt(sum(v*v for v in ca.values()))
    nb  = math.sqrt(sum(v*v for v in cb.values()))
    if na == 0 or nb == 0: return 0.0
    return dot / (na * nb)

# Match advance paragraphs to closest final paragraph
GGA_KEYWORDS = re.compile(
    r'(GGA|global goal on adaptation|adaptation indicator|UAE|Bel[eé]m|'
    r'target 9|target 10|thematic target|dimensional target|Baku adaptation|'
    r'loss and damage|finance|vulnerable|just transition)', re.IGNORECASE)

diff_results = []
matched = 0

for i, ap in enumerate(adv_paras):
    best_sim = -1
    best_j = -1
    a_tok = tokenize(ap)
    for j, fp in enumerate(fin_paras):
        sim = tfidf_cosine(a_tok, tokenize(fp))
        if sim > best_sim:
            best_sim = sim
            best_j = j

    if best_sim >= 0:
        matched += 1
        fp_text = fin_paras[best_j] if best_j >= 0 else ""
        hot_spot = best_sim < 0.85
        gga_specific = bool(GGA_KEYWORDS.search(ap)) or bool(GGA_KEYWORDS.search(fp_text))
        diff_results.append({
            "advance_para_id": i+1,
            "advance_excerpt": ap[:200],
            "final_para_id": best_j+1,
            "final_excerpt": fp_text[:200],
            "cosine_similarity": round(best_sim, 4),
            "hot_spot": hot_spot,
            "gga_specific": gga_specific
        })

hot_spots = [r for r in diff_results if r['hot_spot']]
gga_hot   = [r for r in hot_spots if r['gga_specific']]

print(f"Total matched pairs: {matched}")
print(f"Hot spots (cosine < 0.85): {len(hot_spots)}")
print(f"GGA-specific hot spots: {len(gga_hot)}")
if hot_spots:
    pct_gga = len(gga_hot)/len(hot_spots)*100 if hot_spots else 0
    print(f"% hot spots that are GGA-IND specific: {pct_gga:.1f}%")
    print(f"Tallberg formula control hypothesis: {'SUPPORTED' if pct_gga >= 70 else 'PARTIALLY' if pct_gga >= 40 else 'NOT_SUPPORTED'}")

# Save P0-4 diff JSON
diff_out = os.path.join(BASE, 'data', 'processed', 'l25_advance_vs_final_diff.json')
with open(diff_out, 'w', encoding='utf-8') as f:
    json.dump({
        "method": "TF-IDF cosine similarity, paragraph-level matching",
        "advance_paras": len(adv_paras),
        "final_paras": len(fin_paras),
        "matched_pairs": matched,
        "hot_spots_count": len(hot_spots),
        "gga_specific_hot_spots": len(gga_hot),
        "pct_gga_of_hotspots": round(len(gga_hot)/len(hot_spots)*100, 1) if hot_spots else 0,
        "tallberg_hypothesis_supported": len(gga_hot)/len(hot_spots) >= 0.70 if hot_spots else False,
        "diffs": diff_results
    }, f, ensure_ascii=False, indent=2)
print(f"Saved: {diff_out}")

# Store b0 result for combined use below
import json as _json
b0_out = os.path.join(BASE, 'data', 'processed', 'realist_b0_f1_result.json')
with open(b0_out, 'w', encoding='utf-8') as f:
    _json.dump(b0_result, f, ensure_ascii=False, indent=2)
print(f"\nSaved: {b0_out}")

print("\n=== ALL P0 COMPUTATIONS COMPLETE ===")
