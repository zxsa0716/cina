"""
P0-4: Hedging Density x Group Red Line 2D Plot
CINA Round 5 - Data Refinement Agent

matplotlib scatter: x=hedging_density, y=group_redline_salience
color by negotiating group
"""
import json
import re
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'C:/Users/admin/Desktop/대학원수업/1학기/리더쉽'

# === Load documents.jsonl ===
docs = []
with open(f'{BASE}/data/processed/documents.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            docs.append(json.loads(line))
print(f"Loaded {len(docs)} documents")

# === Hedging modal verb keywords ===
HEDGING_KEYWORDS = [
    r'\bmay\b', r'\bmight\b', r'\bcould\b', r'\bshould\b',
    r'\bwould\b', r'\bencourage[sd]?\b', r'\bvoluntar\w*\b',
    r'\bnon-prescriptive\b', r'\bnon-punitive\b', r'\bfacilitative\b',
    r'\bwhere\s+applicable\b', r'\bas\s+appropriate\b',
    r'\bif\s+appropriate\b', r'\bwhere\s+relevant\b',
    r'\bas\s+relevant\b', r'\bat\s+their\s+discretion\b',
    r'\bsubject\s+to\s+availability\b',
]

# === Group red line keywords ===
# Each group's core demands that define their "red lines"
GROUP_REDLINE_PATTERNS = {
    'AOSIS': [
        r'\b1\.5\s*[°]?C\b', r'\b1\.5\s*degrees?\b',
        r'\bsmall\s+island\b', r'\bSIDS\b', r'\bsea\s*[- ]level\s+rise\b',
        r'\bexistential\s+threat\b', r'\bclimate\s+emergency\b',
        r'\bsurvival\b', r'\bsmall\s+island\s+developing\b',
    ],
    'LDC': [
        r'\bloss\s+and\s+damage\b', r'\bL&D\b',
        r'\bleast\s+developed\b', r'\bLDC\b',
        r'\bnon-economic\s+loss\b', r'\badaptation\s+finance\b',
        r'\bmeans\s+of\s+implementation\b', r'\bvulnerable\s+communities?\b',
    ],
    'AILAC': [
        r'\bglobal\s+stocktake\b', r'\bGST\b', r'\bAILAC\b',
        r'\bCaribbean\b', r'\bCentral\s+America\b', r'\bLatin\s+America\b',
        r'\bjust\s+transition\b', r'\bendogenous\b',
        r'\bhigh\s+ambition\b', r'\bphase.*out.*fossil\b',
    ],
    'G77': [
        r'\bG-?77\b', r'\bcommon\s+but\s+differentiated\b', r'\bCBDR\b',
        r'\bdeveloping\s+countr\w+\b', r'\bequity\b',
        r'\bnational\s+sovereignty\b', r'\bnational\s+circumstances\b',
        r'\btechnology\s+transfer\b', r'\bcapacity.building\b',
    ],
    'EU': [
        r'\bEuropean\s+Union\b', r'\bEU\b',
        r'\btransparency\s+framework\b', r'\bglobal\s+ratchet\b',
        r'\bnet\s*[- ]zero\b', r'\bclimate\s+neutrality\b',
        r'\bmonitoring.*evaluation\b', r'\bMRV\b',
        r'\baccountability\b', r'\bbenchmark\b',
    ],
    'LMDC': [
        r'\bLMDC\b', r'\blike-minded\b', r'\bdeveloping\s+countr\w+\b',
        r'\bChina\b', r'\bIndia\b', r'\bhistorical\s+responsibilit\w+\b',
        r'\bper\s+capita\b', r'\bfossil\s+fuel\s+subsid\w+\b',
        r'\bvoluntar\w+\b', r'\bnon-prescriptive\b',
    ],
}

# === Group assignment for each document ===
# Based on authors and groups_referenced fields
def assign_group(doc):
    authors = [a.lower() for a in doc.get('authors', [])]
    groups = [g.lower() for g in doc.get('groups_referenced', [])]
    source = doc.get('source', '').lower()
    doc_kind = doc.get('doc_kind', '').lower()

    # Direct group indicators
    all_text = ' '.join(authors + groups + [source, doc_kind])

    if 'aosis' in all_text or 'small island' in all_text:
        return 'AOSIS'
    if 'ailac' in all_text:
        return 'AILAC'
    if 'ldc' in all_text or 'least developed' in all_text:
        return 'LDC'
    if 'eu' in groups or 'european union' in all_text:
        return 'EU'
    if 'lmdc' in all_text or 'like-minded' in all_text:
        return 'LMDC'
    if 'brazil' in all_text or 'bra' in authors:
        return 'G77_BRA'
    if 'korea' in all_text or 'kor' in authors or 'korean' in all_text:
        return 'EIG_KOR'
    if 'g77' in all_text or 'developing countr' in all_text:
        return 'G77'
    if 'ipcc' in all_text or 'wg2' in all_text:
        return 'SCIENCE'
    return 'OTHER'


def compute_hedging_density(text):
    if not text or len(text.strip()) == 0:
        return 0.0
    words = text.split()
    n_words = len(words)
    if n_words == 0:
        return 0.0
    hedge_count = 0
    for pat in HEDGING_KEYWORDS:
        hedge_count += len(re.findall(pat, text, re.IGNORECASE))
    return hedge_count / n_words


def compute_redline_salience(text, group):
    if not text or not group or group not in GROUP_REDLINE_PATTERNS:
        return 0.0
    patterns = GROUP_REDLINE_PATTERNS.get(group, GROUP_REDLINE_PATTERNS['G77'])
    total_hits = 0
    for pat in patterns:
        total_hits += len(re.findall(pat, text, re.IGNORECASE))
    # Normalize by document length (per 1000 words)
    words = len(text.split())
    if words == 0:
        return 0.0
    salience = total_hits / (words / 1000)
    # Cap at 1.0 for scatter plot
    return min(salience / 10.0, 1.0)


# Compute metrics for each document
doc_metrics = []
for doc in docs:
    # Concatenate paragraphs
    paras = doc.get('paragraphs', [])
    if paras:
        if isinstance(paras[0], dict):
            text = ' '.join(p.get('text', '') for p in paras)
        else:
            text = ' '.join(str(p) for p in paras)
    else:
        text = ''

    group = assign_group(doc)
    hedging = compute_hedging_density(text)
    redline = compute_redline_salience(text, group)

    doc_metrics.append({
        'doc_id': doc['doc_id'],
        'source': doc.get('source', ''),
        'group': group,
        'cop_session': doc.get('cop_session', ''),
        'hedging_density': round(hedging, 4),
        'redline_salience': round(redline, 4),
        'word_count': len(text.split()),
        'topics': doc.get('topics', []),
    })

# Group-level aggregation
from collections import defaultdict
group_data = defaultdict(list)
for m in doc_metrics:
    group_data[m['group']].append(m)

group_summary = {}
for grp, items in group_data.items():
    hd_vals = [x['hedging_density'] for x in items]
    rl_vals = [x['redline_salience'] for x in items]
    group_summary[grp] = {
        'n': len(items),
        'hedging_mean': round(sum(hd_vals)/len(hd_vals), 4),
        'hedging_std': round((sum((x - sum(hd_vals)/len(hd_vals))**2 for x in hd_vals) / len(hd_vals))**0.5, 4),
        'redline_mean': round(sum(rl_vals)/len(rl_vals), 4),
        'redline_std': round((sum((x - sum(rl_vals)/len(rl_vals))**2 for x in rl_vals) / len(rl_vals))**0.5, 4),
    }

print(f"\n--- Group metrics summary ---")
for grp, s in sorted(group_summary.items()):
    print(f"  {grp}: n={s['n']}, hedging={s['hedging_mean']:.4f}+/-{s['hedging_std']:.4f}, redline={s['redline_mean']:.4f}+/-{s['redline_std']:.4f}")

# Save JSON data
out_json = {
    'analysis_label': 'Hedging_Density_x_Group_Redline_2D',
    'processing_version': 'round5-v1.4',
    'processed_at': '2026-04-26T00:00:00Z',
    'n_documents': len(doc_metrics),
    'hedging_keywords_used': len(HEDGING_KEYWORDS),
    'group_redline_patterns': {g: len(p) for g, p in GROUP_REDLINE_PATTERNS.items()},
    'group_summary': group_summary,
    'document_level_metrics': doc_metrics,
}

json_out_path = f'{BASE}/deliverables/hedging_density_2d_data.json'
with open(json_out_path, 'w', encoding='utf-8') as f:
    json.dump(out_json, f, ensure_ascii=False, indent=2)
print(f"\nJSON data saved to {json_out_path}")

# === Matplotlib scatter plot ===
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import Ellipse
    import numpy as np

    GROUP_COLORS = {
        'AOSIS': '#2196F3',     # blue
        'LDC': '#4CAF50',       # green
        'AILAC': '#F44336',     # red
        'EU': '#9C27B0',        # purple
        'LMDC': '#FF9800',      # orange
        'G77': '#795548',       # brown
        'G77_BRA': '#E91E63',   # pink/magenta (Brazil as G77 chair)
        'EIG_KOR': '#00BCD4',   # cyan (Korea EIG)
        'SCIENCE': '#607D8B',   # blue-grey (IPCC)
        'OTHER': '#9E9E9E',     # grey
    }

    GROUP_LABELS = {
        'AOSIS': 'AOSIS',
        'LDC': 'LDC',
        'AILAC': 'AILAC',
        'EU': 'EU',
        'LMDC': 'LMDC',
        'G77': 'G77',
        'G77_BRA': 'G77/BRA',
        'EIG_KOR': 'EIG/KOR',
        'SCIENCE': 'Science',
        'OTHER': 'Other',
    }

    fig, ax = plt.subplots(figsize=(12, 9))

    plotted_groups = set()
    for m in doc_metrics:
        grp = m['group']
        color = GROUP_COLORS.get(grp, '#9E9E9E')
        label = GROUP_LABELS.get(grp, grp) if grp not in plotted_groups else '_nolegend_'
        ax.scatter(m['hedging_density'], m['redline_salience'],
                   c=color, alpha=0.6, s=50, label=label, edgecolors='white', linewidth=0.5)
        plotted_groups.add(grp)

    # Add group centroid ellipses (1 std)
    for grp, s in group_summary.items():
        if s['n'] < 2:
            continue
        color = GROUP_COLORS.get(grp, '#9E9E9E')
        cx = s['hedging_mean']
        cy = s['redline_mean']
        ex = s['hedging_std'] * 2 + 0.003
        ey = s['redline_std'] * 2 + 0.01

        ellipse = Ellipse((cx, cy), width=ex, height=ey,
                          edgecolor=color, facecolor='none',
                          linewidth=1.5, linestyle='--', alpha=0.7)
        ax.add_patch(ellipse)

        # Label centroid
        lbl = GROUP_LABELS.get(grp, grp)
        ax.annotate(lbl, (cx, cy),
                    fontsize=9, fontweight='bold', color=color,
                    ha='center', va='bottom',
                    xytext=(0, 8), textcoords='offset points')

    ax.set_xlabel('Hedging Density (modal verbs + voluntary language / word count)', fontsize=12)
    ax.set_ylabel('Group Red Line Salience (group-specific keywords per 1000 words, normalized)', fontsize=12)
    ax.set_title('Hedging Density x Group Red Line Salience\nCINA CINA 114 Documents — COP Adaptation Negotiations',
                 fontsize=13, fontweight='bold')

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(),
              loc='upper right', fontsize=9, framealpha=0.8,
              title='Negotiating Group')

    ax.grid(True, alpha=0.3, linestyle=':')
    ax.set_xlim(-0.005, max(m['hedging_density'] for m in doc_metrics) * 1.15 + 0.01)
    ax.set_ylim(-0.02, 1.05)

    # Quadrant annotations
    x_mid = 0.05
    y_mid = 0.3
    ax.axvline(x=x_mid, color='grey', linestyle=':', alpha=0.5)
    ax.axhline(y=y_mid, color='grey', linestyle=':', alpha=0.5)
    ax.text(x_mid*0.4, y_mid*0.5, 'Low hedge\nLow red line', fontsize=7, color='grey', ha='center')
    ax.text(x_mid*1.6, y_mid*1.5, 'High hedge\nHigh red line\n(Norm entrepreneurship)', fontsize=7, color='darkred', ha='center')

    plt.tight_layout()

    os.makedirs(f'{BASE}/data/processed/figures', exist_ok=True)
    png_path = f'{BASE}/data/processed/figures/hedging_vs_redline_2d.png'
    svg_path = f'{BASE}/data/processed/figures/hedging_vs_redline_2d.svg'

    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(svg_path, format='svg', bbox_inches='tight')
    plt.close(fig)
    print(f"Plot saved: {png_path}")
    print(f"SVG saved: {svg_path}")

    # Also save deliverables copy
    import shutil
    shutil.copy(png_path, f'{BASE}/deliverables/hedging_density_2d_plot.png')
    print(f"Deliverables copy saved")

except Exception as e:
    print(f"Plot error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone.")
