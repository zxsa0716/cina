"""
P0-1 Step 2: Merge existing chair_metadata.jsonl with 24 new records
"""
import json
import os
from collections import Counter

BASE = 'C:/Users/admin/Desktop/대학원수업/1학기/리더쉽'

# Load existing records
existing = []
existing_path = f'{BASE}/data/processed/chair_metadata.jsonl'
with open(existing_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            existing.append(json.loads(line))
print(f"Existing records: {len(existing)}")

# Load new records
with open(f'{BASE}/data/processed/_temp_new_chair_records.json', 'r', encoding='utf-8') as f:
    new_records = json.load(f)
print(f"New records from historical_chair PDFs: {len(new_records)}")

# Deduplicate: check if any new record doc_id already exists
existing_ids = {r['doc_id'] for r in existing}
added = 0
skipped = 0
new_to_add = []
for rec in new_records:
    if rec['doc_id'] not in existing_ids:
        new_to_add.append(rec)
        added += 1
    else:
        skipped += 1
        print(f"  Skipping duplicate: {rec['doc_id']}")

print(f"Adding {added} new records, skipping {skipped} duplicates")

# Merge
merged = existing + new_to_add
print(f"Total merged: {len(merged)}")

# Write merged JSONL
with open(existing_path, 'w', encoding='utf-8') as f:
    for rec in merged:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
print(f"Written to {existing_path}")

# Build statistics
by_source = Counter(r.get('source', 'unknown') for r in merged)
by_cop = Counter(r.get('cop_session', 'unknown') for r in merged)
by_presidency = Counter(r.get('presidency_country') for r in merged if r.get('presidency_country'))
energy_exporter_count = sum(1 for r in merged if r.get('energy_exporter_presidency', False))
scanned_count = sum(1 for r in merged if r.get('is_scanned_pdf', False))
tallberg_dist = Counter(r.get('tallberg_primary_channel', 'unknown') for r in merged if r.get('tallberg_primary_channel'))

# COP21-30 chair coverage
chair_coverage = {}
for r in merged:
    cop = r.get('cop_session')
    if cop and cop not in chair_coverage:
        chair_coverage[cop] = {'country': r.get('presidency_country'), 'count': 0}
    if cop:
        chair_coverage[cop]['count'] = chair_coverage.get(cop, {}).get('count', 0) + 1

# Energy exporter presidencies COP21-COP30
energy_presidencies = [(cop, info['country']) for cop, info in sorted(chair_coverage.items())
                       if any(r.get('cop_session') == cop and r.get('energy_exporter_presidency', False) for r in merged)]

stats = {
    'total_records': len(merged),
    'by_source': dict(by_source),
    'by_cop_session': dict(by_cop),
    'by_presidency_country': dict(by_presidency),
    'energy_exporter_presidencies_count': energy_exporter_count,
    'energy_exporter_presidencies': energy_presidencies,
    'scanned_pdf_count': scanned_count,
    'tallberg_channel_distribution': dict(tallberg_dist),
    'cop_coverage': sorted(chair_coverage.keys()),
    'bayer_urpelainen_threshold_80_status': f"{len(merged)}/80 = {len(merged)/80*100:.1f}%",
    'processing_version': 'round5-v1.4',
    'processed_at': '2026-04-26T00:00:00Z'
}

stats_path = f'{BASE}/data/processed/chair_metadata_stats_v2.json'
with open(stats_path, 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)
print(f"\nStatistics written to {stats_path}")
print(f"\n=== SUMMARY ===")
print(f"Total records: {stats['total_records']}")
print(f"By source: {stats['by_source']}")
print(f"By COP session: {stats['by_cop_session']}")
print(f"Energy exporter presidencies: {stats['energy_exporter_presidencies_count']}")
print(f"Tallberg channels: {stats['tallberg_channel_distribution']}")
print(f"Bayer-Urpelainen threshold: {stats['bayer_urpelainen_threshold_80_status']}")

# Cleanup temp file
os.remove(f'{BASE}/data/processed/_temp_new_chair_records.json')
print(f"\nCleaned up temp file")
