"""
P0-1: Extract chair_metadata from 24 historical chair PDFs
CINA Round 5 - Data Refinement Agent
"""
import fitz
import json
import re
import hashlib
import os
from datetime import datetime

BASE = 'C:/Users/admin/Desktop/대학원수업/1학기/리더쉽'

CHAIR_BASE = f'{BASE}/data/raw/historical_chair'
pdfs = []
for root, dirs, files in os.walk(CHAIR_BASE):
    for f in files:
        if f.endswith('.pdf'):
            pdfs.append(os.path.join(root, f))
pdfs.sort()
print(f"Found {len(pdfs)} historical chair PDFs")

PRESIDENCY_MAP = {
    'COP21': {'country': 'France', 'iso3': 'FRA', 'chair': 'Laurent Fabius', 'energy_exporter': False},
    'COP22': {'country': 'Morocco', 'iso3': 'MAR', 'chair': 'Salaheddine Mezouar', 'energy_exporter': False},
    'COP23': {'country': 'Fiji', 'iso3': 'FJI', 'chair': 'Frank Bainimarama', 'energy_exporter': False},
    'COP24': {'country': 'Poland', 'iso3': 'POL', 'chair': 'Michal Kurtyka', 'energy_exporter': True},
    'COP25': {'country': 'Chile', 'iso3': 'CHL', 'chair': 'Caroline Schmidt', 'energy_exporter': False},
    'COP26': {'country': 'UK', 'iso3': 'GBR', 'chair': 'Alok Sharma', 'energy_exporter': False},
    'COP27': {'country': 'Egypt', 'iso3': 'EGY', 'chair': 'Sameh Shoukry', 'energy_exporter': False},
    'COP28': {'country': 'UAE', 'iso3': 'ARE', 'chair': 'Sultan Al Jaber', 'energy_exporter': True},
    'COP29': {'country': 'Azerbaijan', 'iso3': 'AZE', 'chair': 'Mukhtar Babayev', 'energy_exporter': True},
    'COP30': {'country': 'Brazil', 'iso3': 'BRA', 'chair': 'Andre Aranha Correa do Lago', 'energy_exporter': False},
}

FORMULA_CONTROL_PATTERNS = [
    r'\b(take note|taking note|proposal by the president|president.s proposal|chair.s text|non-paper by the president|elements of outcome)\b',
    r'\b(brackets removed|proposed decision|draft decision.*president|draft text)\b',
]
AGENDA_SHAPING_PATTERNS = [
    r'\b(agenda|work programme|session.*focus|focus.*session|priority.*issue|strategic.*direction|incoming presidency)\b',
    r'\b(intersessional|roadmap|workplan|new agenda item|additional.*item)\b',
]
BROKERAGE_PATTERNS = [
    r'\b(bridge|bridging|middle ground|compromise|balance|convergence|landing zone|consensus)\b',
    r'\b(consult|informal|facilitat|bring.*together|close.*gap|common ground)\b',
]
INFORMATION_PATTERNS = [
    r'\b(inform|update|note|report|technical paper|synthesis|summary|progress|status|outcome)\b',
    r'\b(transparency|data|science|evidence|knowledge|learning)\b',
]

TOPIC_PATTERNS = {
    "GGA-IND": r"(GGA|Global Goal on Adaptation|adaptation indicators|UAE Framework|Belem Adaptation)",
    "ADAPT-FIN": r"(adaptation finance|NCQG|billion|adaptation fund)",
    "L&D-OP": r"(loss and damage|L&D fund|non-economic|Warsaw International)",
    "NAPs": r"(National Adaptation Plan|NAP process|LEG|LDC Expert Group)",
    "MIT-ADAPT": r"(co-benefits|mitigation.adaptation|synergies|trade-offs)",
    "JT-ADAPT": r"(just transition|JTWP|indigenous|gender.responsive)",
}


def compute_signals(text):
    text_lower = text.lower()
    result = {}
    for name, patterns in [
        ('formula_control_signal', FORMULA_CONTROL_PATTERNS),
        ('agenda_shaping_signal', AGENDA_SHAPING_PATTERNS),
        ('brokerage_signal', BROKERAGE_PATTERNS),
        ('information_signal', INFORMATION_PATTERNS),
    ]:
        found = any(re.search(p, text_lower) for p in patterns)
        result[name] = found
    return result


def compute_topics(text):
    topics = []
    for topic, pat in TOPIC_PATTERNS.items():
        if re.search(pat, text, re.IGNORECASE):
            topics.append(topic)
    return topics


def infer_doc_kind(filename, text_lower):
    fn = filename.lower()
    if 'notification' in fn or 'notification' in text_lower[:500]:
        return 'notification_to_parties'
    elif 'letter' in fn:
        if 'vision' in fn:
            return 'vision_letter'
        elif 'president' in fn and '17nov' in fn:
            return 'president_letter'
        elif 'incoming' in fn:
            return 'incoming_president_letter'
        elif 'ministerial' in fn:
            return 'ministerial_letter'
        elif 'pre_cop' in fn or 'pre-cop' in fn:
            return 'pre_cop_letter'
        elif 'designate' in fn:
            return 'president_designate_letter'
        elif 'cpd' in fn:
            return 'cop30_cpd_letter'
        else:
            return 'chair_letter'
    elif 'statement' in fn:
        return 'president_statement'
    elif 'report' in fn:
        return 'session_report'
    elif 'summary' in fn:
        if 'pre_cop' in fn or 'joint' in fn:
            return 'pre_cop_summary'
        return 'summary_note'
    elif 'elements' in fn or 'possible' in fn:
        return 'elements_of_outcome'
    elif 'reflections' in fn:
        return 'reflections_note'
    elif 'update' in fn:
        return 'president_update'
    elif 'information' in fn:
        return 'information_note'
    return 'chair_communication'


def infer_date(filename, cop_session):
    fn = filename.lower()
    session_dates = {
        'COP21': '2015-11-30', 'COP22': '2016-11-07',
        'COP23': '2017-11-06', 'COP24': '2018-12-03',
        'COP25': '2019-12-02', 'COP26': '2021-11-01',
        'COP27': '2022-11-07', 'COP28': '2023-11-30',
        'COP29': '2024-11-11', 'COP30': '2025-11-10',
    }
    if 'mar2025' in fn or 'vision_letter' in fn:
        return '2025-03-01'
    if 'may2025' in fn or '2nd_letter' in fn:
        return '2025-05-01'
    if 'jun2025' in fn or '4th_letter' in fn:
        return '2025-06-01'
    if 'aug2025' in fn and '5th' in fn:
        return '2025-08-01'
    if 'aug2025' in fn and '7th' in fn:
        return '2025-08-15'
    if '10th' in fn or ('final_letter' in fn and 'nov2025' in fn):
        return '2025-11-15'
    if '12th' in fn or 'jan2026' in fn:
        return '2026-01-15'
    if '17nov2025' in fn:
        return '2025-11-17'
    if '05dec2015' in fn:
        return '2015-12-05'
    if '15nov2016' in fn:
        return '2016-11-15'
    if '16nov2017' in fn:
        return '2017-11-16'
    if 'oct2018' in fn and 'notification' in fn:
        return '2018-10-11'
    if 'oct2018' in fn and 'krakow' in fn:
        return '2018-10-24'
    if 'sep2021' in fn:
        return '2021-09-01'
    if 'jul2021' in fn:
        return '2021-07-01'
    if 'oct2021' in fn:
        return '2021-10-28'
    if 'reflections' in fn:
        return '2021-10-28'
    if '01nov2022' in fn or 'incoming' in fn:
        return '2022-11-01'
    if '16nov2022' in fn or 'president_update' in fn:
        return '2022-11-16'
    if 'gcf' in fn or 'report_to_cop26' in fn:
        return '2021-10-15'
    if 'jun2019' in fn or 'cop25_cmp15' in fn:
        return '2019-06-28'
    return session_dates.get(cop_session, '2025-01-01')


def extract_cop_session(filename):
    fn = os.path.basename(filename)
    match = re.match(r'(COP\d+)', fn)
    if match:
        return match.group(1)
    return 'COP30'


new_records = []
extraction_log = []

for pdf_path in pdfs:
    fn = os.path.basename(pdf_path)
    cop_session = extract_cop_session(fn)
    presidency_info = PRESIDENCY_MAP.get(cop_session, {})

    try:
        doc = fitz.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        extraction_log.append({'file': fn, 'status': 'error', 'msg': str(e)})
        continue

    is_scanned = len(text.strip()) < 50
    if is_scanned:
        chair_name = presidency_info.get('chair', 'Unknown')
        text = f"[SCANNED PDF - {fn}] Chair communication from {chair_name} ({cop_session})"

    sha256 = hashlib.sha256(text.encode('utf-8', errors='replace')).hexdigest()[:12]
    doc_id = f"round4_t01_chair-{sha256}"

    signals = compute_signals(text)
    topics = compute_topics(text)
    doc_kind = infer_doc_kind(fn, text.lower()[:500])
    date = infer_date(fn, cop_session)
    presidency_country = presidency_info.get('country', None)

    tallberg_primary = 'information'
    if signals['formula_control_signal']:
        tallberg_primary = 'formula_control'
    elif signals['brokerage_signal']:
        tallberg_primary = 'brokerage'
    elif signals['agenda_shaping_signal']:
        tallberg_primary = 'agenda_shaping'

    record = {
        'doc_id': doc_id,
        'source': 'round4_t01_chair',
        'source_type': 'historical_chair_letter',
        'cop_session': cop_session,
        'subsidiary_body': None,
        'document_type': 'chair_communication',
        'doc_kind': doc_kind,
        'date': date,
        'presidency_country': presidency_country,
        'presidency_iso3': presidency_info.get('iso3', None),
        'chair_name': presidency_info.get('chair', None),
        'energy_exporter_presidency': presidency_info.get('energy_exporter', False),
        'is_chair_role': True,
        'is_pen_holder': False,
        'is_co_facilitator': False,
        'chair_role': 'presidency',
        'formula_control_signal': signals['formula_control_signal'],
        'agenda_shaping_signal': signals['agenda_shaping_signal'],
        'brokerage_signal': signals['brokerage_signal'],
        'information_signal': signals['information_signal'],
        'tallberg_primary_channel': tallberg_primary,
        'is_scanned_pdf': is_scanned,
        'topics': topics,
        'procedural_phrases': [],
        'sha256': sha256,
        'char_count': len(text),
        'processing_version': 'round5-v1.4',
        'processed_at': '2026-04-26T00:00:00Z',
        'source_file': fn,
    }
    new_records.append(record)
    extraction_log.append({
        'file': fn, 'status': 'ok', 'cop': cop_session,
        'chars': len(text), 'scanned': is_scanned, 'tallberg': tallberg_primary,
        'topics_n': len(topics)
    })

print(f"\nExtracted {len(new_records)} new records")
for log in extraction_log:
    print(f"  {log['file']}: {log['status']}, chars={log['chars']}, scanned={log['scanned']}, tallberg={log['tallberg']}, topics={log['topics_n']}")

with open(f'{BASE}/data/processed/_temp_new_chair_records.json', 'w', encoding='utf-8') as f:
    json.dump(new_records, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(new_records)} temp records")
