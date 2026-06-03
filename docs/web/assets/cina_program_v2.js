// CINA Program v2 — Academic-grade browser Q&A engine
//
// v1 -> v2 upgrades:
//   * Backed by v5 dataset (2,400 records, 50 countries x 8 issues x 6 COPs)
//   * 7 intents: lookup, compare, recommendation, factoid, trend, coalition, gap
//   * 95% credible interval visual bracket per stance
//   * NATO 4-axis inline SVG bar per answer
//   * Frame distribution display
//   * Methodology footer per response (model, T, k, retrieved n, hash)
//   * Multi-turn LLM memory (last 5 turns)
//   * Export buttons: Markdown / JSON / BibTeX
//   * Top-k retrieval with relevance scoring
//
// All LLM keys remain in browser localStorage; LLM calls go directly to provider.
// Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
// License: MIT

(function () {
  "use strict";

  // ================================================================
  // Aliases (50 countries, 8 issues, 6 COPs)
  // ================================================================

  const COUNTRY_ALIASES = {
    "브라질": "Brazil", "brazil": "Brazil",
    "한국": "Korea", "대한민국": "Korea", "korea": "Korea", "south korea": "Korea",
    "미국": "USA", "usa": "USA", "us ": "USA", "united states": "USA",
    "중국": "China", "china": "China",
    "인도": "India", "india": "India",
    "유럽연합": "EU", "유럽": "EU", " eu ": "EU",
    "사우디": "Saudi", "사우디아라비아": "Saudi", "saudi": "Saudi",
    "일본": "Japan", "japan": "Japan",
    "AOSIS": "AOSIS", "aosis": "AOSIS", "군소도서국": "AOSIS",
    "AILAC": "AILAC", "ailac": "AILAC",
    "AGN": "AGN", "agn": "AGN", "아프리카그룹": "AGN",
    "LMDC": "LMDC", "lmdc": "LMDC",
    "캐나다": "Canada", "canada": "Canada",
    "호주": "Australia", "오스트레일리아": "Australia", "australia": "Australia",
    "노르웨이": "Norway", "norway": "Norway",
    "영국": "UK", "uk": "UK", "united kingdom": "UK",
    "독일": "Germany", "germany": "Germany",
    "프랑스": "France", "france": "France",
    "멕시코": "Mexico", "mexico": "Mexico",
    "인도네시아": "Indonesia", "indonesia": "Indonesia",
    "남아공": "South Africa", "남아프리카": "South Africa", "south africa": "South Africa",
    "이집트": "Egypt", "egypt": "Egypt",
    "튀르키예": "Türkiye", "터키": "Türkiye", "turkey": "Türkiye", "turkiye": "Türkiye",
    "몰디브": "Maldives", "maldives": "Maldives",
    "마샬": "Marshall Is", "마샬군도": "Marshall Is", "marshall": "Marshall Is",
    "투발루": "Tuvalu", "tuvalu": "Tuvalu",
    "방글라데시": "Bangladesh", "bangladesh": "Bangladesh",
    "에티오피아": "Ethiopia", "ethiopia": "Ethiopia",
    "네팔": "Nepal", "nepal": "Nepal",
    "스위스": "Switzerland", "switzerland": "Switzerland",
    "스페인": "Spain", "spain": "Spain",
    "이탈리아": "Italy", "italy": "Italy",
    "뉴질랜드": "New Zealand", "new zealand": "New Zealand", "nz": "New Zealand",
    "아르헨티나": "Argentina", "argentina": "Argentina",
    "콜롬비아": "Colombia", "colombia": "Colombia",
    "칠레": "Chile", "chile": "Chile",
    "페루": "Peru", "peru": "Peru",
    "코스타리카": "Costa Rica", "costa rica": "Costa Rica",
    "베트남": "Vietnam", "vietnam": "Vietnam",
    "태국": "Thailand", "thailand": "Thailand",
    "필리핀": "Philippines", "philippines": "Philippines",
    "파키스탄": "Pakistan", "pakistan": "Pakistan",
    "이란": "Iran", "iran": "Iran",
    "아랍에미리트": "UAE", "uae": "UAE", "emirates": "UAE",
    "카타르": "Qatar", "qatar": "Qatar",
    "케냐": "Kenya", "kenya": "Kenya",
    "가나": "Ghana", "ghana": "Ghana",
    "세네갈": "Senegal", "senegal": "Senegal",
    "모로코": "Morocco", "morocco": "Morocco",
  };

  const ISSUE_ALIASES = {
    "GGA-IND": "GGA-IND", "GGA 지표": "GGA-IND", "적응 지표": "GGA-IND", "지표": "GGA-IND",
    "GGA-MOI": "GGA-MOI", "이행수단": "GGA-MOI", "MoI": "GGA-MOI",
    "NAPs": "NAPs", "NAP": "NAPs", "국가적응계획": "NAPs", "적응계획": "NAPs",
    "JT-ADAPT": "JT-ADAPT", "정의로운 전환": "JT-ADAPT", "JT": "JT-ADAPT",
    "L&D-OP": "L&D-OP", "손실 피해": "L&D-OP", "손실·피해": "L&D-OP", "FRLD": "L&D-OP",
    "FINANCE-ADAPT": "FINANCE-ADAPT", "적응 재원": "FINANCE-ADAPT", "재원": "FINANCE-ADAPT",
    "TRANS-FIN": "TRANS-FIN", "재원 투명성": "TRANS-FIN", "투명성": "TRANS-FIN",
    "TECH-TRANS": "TECH-TRANS", "기술이전": "TECH-TRANS", "기술 이전": "TECH-TRANS",
  };

  const COP_ALIASES = {
    "COP25": "COP25", "cop25": "COP25", "마드리드": "COP25", "madrid": "COP25",
    "COP26": "COP26", "cop26": "COP26", "글래스고": "COP26", "glasgow": "COP26",
    "COP27": "COP27", "cop27": "COP27", "샤름": "COP27", "sharm": "COP27",
    "COP28": "COP28", "cop28": "COP28", "두바이": "COP28", "dubai": "COP28",
    "COP29": "COP29", "cop29": "COP29", "바쿠": "COP29", "baku": "COP29",
    "COP30": "COP30", "cop30": "COP30", "벨렘": "COP30", "belem": "COP30",
  };

  const ENGINE_VERSION = "v2.1.0";
  const DATASET_VERSION_TARGET = "5.0.0";
  const CORPUS_VERSION_TARGET = "6.0.0";

  // ================================================================
  // localStorage keys (BYO LLM)
  // ================================================================

  const KEY_NS = "cina_byo_key_";
  const HIST_KEY = "cina_v2_history";
  const MODE_KEY = "cina_v2_mode";

  function getKey(provider) { return localStorage.getItem(KEY_NS + provider) || ""; }
  function setKey(provider, value) { localStorage.setItem(KEY_NS + provider, value); }
  function clearKey(provider) { localStorage.removeItem(KEY_NS + provider); }
  function hasAnyKey() { return ["gemini", "anthropic", "groq"].some(p => getKey(p)); }

  function getHistory() {
    try { return JSON.parse(localStorage.getItem(HIST_KEY) || "[]"); } catch { return []; }
  }
  function pushHistory(turn) {
    const h = getHistory(); h.push(turn);
    while (h.length > 50) h.shift();   // keep last 50
    localStorage.setItem(HIST_KEY, JSON.stringify(h));
  }
  function clearHistory() { localStorage.removeItem(HIST_KEY); }

  // ================================================================
  // Data loading (v5 jsonl)
  // ================================================================

  let DATA_CACHE = null;
  let META_CACHE = null;

  async function loadData() {
    if (DATA_CACHE) return DATA_CACHE;
    const candidates = [
      "data/stances_v5.jsonl",                    // GH Pages: /web/data/stances_v5.jsonl
      "./data/stances_v5.jsonl",
      "../../data/processed/stances_v5.jsonl",    // local dev
      "data/processed/stances_v5.jsonl",
      "/cina/web/data/stances_v5.jsonl",
      "../../data/processed/stances_v4.jsonl",    // fallback to v4
    ];
    for (const url of candidates) {
      try {
        const res = await fetch(url);
        if (!res.ok) continue;
        const text = await res.text();
        DATA_CACHE = text.trim().split("\n").filter(l => l.trim()).map(l => JSON.parse(l));
        console.log(`[CINA v2] Loaded ${DATA_CACHE.length} records from ${url}`);
        return DATA_CACHE;
      } catch (e) { /* try next */ }
    }
    console.warn("[CINA v2] All data fetch attempts failed; using minimal fallback");
    DATA_CACHE = MINIMAL_FALLBACK;
    return DATA_CACHE;
  }

  // Minimal in-browser fallback if all fetches fail
  const MINIMAL_FALLBACK = [
    {_meta:{country:"Brazil",issue:"GGA-IND",cop:"COP30",source_type:"verified_canonical"},
     stance_score:1.0,ci_lower_95:0.92,ci_upper_95:1.0,frame_type:"sovereignty",
     nato_4axis:{nodality:0.55,authority:0.24,treasure:0.16,organization:0.30},
     procedural_signals:{is_chair_role:true,is_pen_holder:true},
     evidence_quote:"[COP30, Brazil] 59 voluntary, non-prescriptive, non-punitive, facilitative indicators"},
    {_meta:{country:"Korea",issue:"NAPs",cop:"COP30",source_type:"verified_canonical"},
     stance_score:0.75,ci_lower_95:0.65,ci_upper_95:0.85,frame_type:"development",
     nato_4axis:{nodality:0.48,authority:0.66,treasure:0.44,organization:0.78},
     procedural_signals:{is_pen_holder:true},
     evidence_quote:"[COP30, Korea] 3-tier national-province-municipal NAP model"},
  ];

  // ================================================================
  // Corpus loader (v6 — TF-IDF inverted index)
  // ================================================================

  let CORPUS_MANIFEST = null;
  let CORPUS_INDEX = null;

  async function loadCorpus() {
    if (CORPUS_MANIFEST && CORPUS_INDEX) return { CORPUS_MANIFEST, CORPUS_INDEX };
    const manifestCandidates = [
      "data/corpus/manifest.jsonl", "./data/corpus/manifest.jsonl",
      "../../data/corpus/manifest.jsonl",
    ];
    const indexCandidates = [
      "data/corpus/search_index.json", "./data/corpus/search_index.json",
      "../../data/corpus/search_index.json",
    ];
    for (const url of manifestCandidates) {
      try {
        const res = await fetch(url);
        if (!res.ok) continue;
        const text = await res.text();
        CORPUS_MANIFEST = text.trim().split("\n").filter(l => l.trim()).map(l => JSON.parse(l));
        console.log(`[CINA v2.1] Loaded ${CORPUS_MANIFEST.length} corpus docs from ${url}`);
        break;
      } catch (e) { /* try next */ }
    }
    for (const url of indexCandidates) {
      try {
        const res = await fetch(url);
        if (!res.ok) continue;
        CORPUS_INDEX = await res.json();
        console.log(`[CINA v2.1] Loaded corpus index (${CORPUS_INDEX.n_terms} terms) from ${url}`);
        break;
      } catch (e) { /* try next */ }
    }
    if (!CORPUS_MANIFEST) { CORPUS_MANIFEST = []; console.warn("[CINA v2.1] corpus manifest unavailable"); }
    if (!CORPUS_INDEX) { CORPUS_INDEX = { idf: {}, inverted: {} }; }
    return { CORPUS_MANIFEST, CORPUS_INDEX };
  }

  const STOP_TOKENS = new Set([
    "the","a","an","and","or","but","is","are","of","in","on","at","to","for","with","by",
    "as","that","this","it","its","not","no","from","into",
    "본","해","이","그","저","것","및","또","수","의","에","에서","으로","로","를","을","는","가",
    "있다","없다","한다","된다","것이다","위해","대한","대해","해서","하는","된","된다고","이는",
  ]);

  function corpusTokenize(text) {
    if (!text) return [];
    const raw = text.toLowerCase().match(/[가-힣]+|[A-Za-z0-9_\-\.&]+/g) || [];
    return raw.filter(t => t.length > 1 && !STOP_TOKENS.has(t));
  }

  function corpusSearch(query, topK = 8) {
    if (!CORPUS_INDEX || !CORPUS_MANIFEST) return [];
    const byId = {}; CORPUS_MANIFEST.forEach(r => byId[r.doc_id] = r);
    const toks = corpusTokenize(query);
    const scores = {};
    toks.forEach(t => {
      const idf = (CORPUS_INDEX.idf || {})[t] || 0;
      const entries = (CORPUS_INDEX.inverted || {})[t] || [];
      entries.forEach(([docId, w]) => { scores[docId] = (scores[docId] || 0) + w * idf; });
    });
    return Object.entries(scores).sort((a,b) => b[1]-a[1]).slice(0, topK)
      .map(([d, s]) => ({ doc_id: d, score: +s.toFixed(4),
                          manifest: byId[d] || { doc_id: d, title: d, path: "?", type: "?" } }));
  }

  function corpusFilterByContext(intent) {
    if (!CORPUS_MANIFEST) return [];
    const out = [], seen = new Set();
    CORPUS_MANIFEST.forEach(r => {
      let matched = false;
      if (intent.countries.length && intent.countries.includes(r.country)) matched = true;
      if (intent.issues.length && (r.issues_addressed || []).some(i => intent.issues.includes(i))) matched = true;
      if (intent.cop && r.cop === intent.cop) matched = true;
      if (matched && !seen.has(r.doc_id)) { seen.add(r.doc_id); out.push(r); }
    });
    return out;
  }

  // ================================================================
  // Intent parsing (8 types — added 'search')
  // ================================================================

  const INTENT_TRIGGERS = {
    "search":         [/원문|본문|결정문|L-document|L문서|조문|조항|where does it say|document says|텍스트|decision text|policy document|source/i],
    "trend":          [/추이|시계열|흐름|trajectory|trend|evolution|over time|변화 추이/i],
    "coalition":      [/연합|동맹|비슷한 국가|유사한 국가|비슷|coalition|similar countries|동조/i],
    "gap":            [/translation gap|국내국제|국내 국제|domestic international|delta|이중정체성|이중 정체성|괴리|이행격차|이행 격차|Δ/i],
    "compare":        [/비교| vs | versus |차이|사이|different from|compared to/i],
    "recommendation": [/권고|전략|어떻게 해야|추천|권장|recommend|수립|방안|strategy/i],
    "factoid":        [/정확히 몇|정확한 값|정확히 얼마|exact value|정확히/i],
  };

  function parseIntent(question) {
    const q = question.trim();
    const qLower = " " + q.toLowerCase() + " ";

    const countries = [];
    for (const [alias, canon] of Object.entries(COUNTRY_ALIASES)) {
      if (qLower.includes(alias.toLowerCase()) && !countries.includes(canon)) {
        countries.push(canon);
      }
    }
    const issues = [];
    for (const [alias, canon] of Object.entries(ISSUE_ALIASES)) {
      if (qLower.includes(alias.toLowerCase()) && !issues.includes(canon)) {
        issues.push(canon);
      }
    }
    let cop = null;
    for (const [alias, canon] of Object.entries(COP_ALIASES)) {
      if (qLower.includes(alias.toLowerCase())) { cop = canon; break; }
    }

    let type = "unknown";
    for (const [name, patterns] of Object.entries(INTENT_TRIGGERS)) {
      if (patterns.some(p => p.test(q))) { type = name; break; }
    }
    if (type === "compare" && countries.length < 2) type = "lookup";
    if (type === "unknown") {
      if (countries.length || issues.length) type = "lookup";
    }
    return { type, countries, issues, cop: cop || "COP30", raw: q };
  }

  // ================================================================
  // Retrieval (top-k relevance scoring)
  // ================================================================

  function recordRelevance(r, intent) {
    let s = 0;
    const m = r._meta;
    if (intent.countries.length && intent.countries.includes(m.country)) s += 1.5;
    if (intent.issues.length && intent.issues.includes(m.issue)) s += 1.5;
    if (intent.cop && m.cop === intent.cop) s += 1.0;
    s += 0.3 * (r.confidence || 0.85);
    s += 0.2 * (r.salience_score || 0.65);
    if (m.source_type === "verified_canonical") s += 0.5;
    return s;
  }

  function retrieve(records, intent, k = 24) {
    let pool = records;
    if (intent.countries.length) pool = pool.filter(r => intent.countries.includes(r._meta.country));
    if (intent.issues.length) pool = pool.filter(r => intent.issues.includes(r._meta.issue));
    if (intent.cop && intent.type !== "trend" && intent.type !== "coalition") {
      pool = pool.filter(r => r._meta.cop === intent.cop);
    }
    return pool.map(r => [r, recordRelevance(r, intent)])
               .sort((a, b) => b[1] - a[1])
               .slice(0, k)
               .map(([r, _]) => r);
  }

  // ================================================================
  // Formatting helpers
  // ================================================================

  function fmt(s) { return (s >= 0 ? "+" : "") + s.toFixed(2); }
  function stanceLabel(s) {
    if (s >= 0.7) return "강한 지지";
    if (s >= 0.3) return "지지";
    if (s >= -0.3) return "중립";
    if (s >= -0.7) return "반대";
    return "강한 반대";
  }
  function ciStr(r) {
    if (r.ci_lower_95 == null || r.ci_upper_95 == null) return "";
    return ` (95% CI [${fmt(r.ci_lower_95)}, ${fmt(r.ci_upper_95)}])`;
  }
  function natoSummary(r) {
    const n = r.nato_4axis; if (!n) return "";
    return `NATO: N=${n.nodality.toFixed(2)} A=${n.authority.toFixed(2)} T=${n.treasure.toFixed(2)} O=${n.organization.toFixed(2)}`;
  }
  function hashIntent(intent, seed) {
    const s = JSON.stringify({...intent, seed});
    let h = 0;
    for (let i = 0; i < s.length; i++) {
      h = ((h << 5) - h) + s.charCodeAt(i); h |= 0;
    }
    return Math.abs(h).toString(16).slice(0, 12);
  }

  function recordToCitation(r) {
    const m = r._meta;
    return {
      country: m.country, issue: m.issue, cop: m.cop,
      quote: r.evidence_quote || "", score: r.stance_score,
      ci_lower: r.ci_lower_95, ci_upper: r.ci_upper_95,
      frame: r.frame_type, location: r.evidence_location,
      source_type: m.source_type,
    };
  }

  // ================================================================
  // SVG mini chart helpers
  // ================================================================

  function svgSparkline(values, width = 220, height = 50) {
    const valid = values.filter(v => v != null);
    if (valid.length < 2) return "";
    const min = Math.min(...valid), max = Math.max(...valid);
    const range = max - min || 1;
    const pad = 4;
    const stepX = (width - 2 * pad) / (values.length - 1);
    const pts = values.map((v, i) => {
      if (v == null) return null;
      const x = pad + i * stepX;
      const y = height - pad - ((v - min) / range) * (height - 2 * pad);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).filter(Boolean).join(" ");
    return `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" style="background:#f8fafc;border-radius:4px">
      <polyline fill="none" stroke="#0ea5e9" stroke-width="2" points="${pts}"/>
      <line x1="${pad}" y1="${height/2}" x2="${width-pad}" y2="${height/2}" stroke="#cbd5e1" stroke-width="0.5" stroke-dasharray="2 3"/>
    </svg>`;
  }

  function svgNatoBar(nato, width = 220, height = 60) {
    const axes = [
      {k: "nodality", c: "#38bdf8", l: "N"},
      {k: "authority", c: "#a78bfa", l: "A"},
      {k: "treasure", c: "#f59e0b", l: "T"},
      {k: "organization", c: "#10b981", l: "O"},
    ];
    const barW = (width - 16) / 4;
    let svg = `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" style="background:#f8fafc;border-radius:4px">`;
    axes.forEach((a, i) => {
      const v = nato[a.k] || 0;
      const h = Math.max(2, (height - 24) * v);
      const x = 8 + i * barW;
      svg += `<rect x="${x}" y="${height - 16 - h}" width="${barW - 4}" height="${h}" fill="${a.c}"/>`;
      svg += `<text x="${x + (barW - 4) / 2}" y="${height - 4}" text-anchor="middle" font-size="9" fill="#475569">${a.l}=${v.toFixed(2)}</text>`;
    });
    svg += `</svg>`;
    return svg;
  }

  function svgHBars(labels, values, width = 280, rowH = 18) {
    const height = labels.length * rowH + 10;
    const maxAbs = Math.max(0.01, ...values.map(v => Math.abs(v)));
    let svg = `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" style="background:#f8fafc;border-radius:4px">`;
    const centreX = 100;
    const maxW = width - centreX - 8;
    labels.forEach((lab, i) => {
      const y = 6 + i * rowH;
      const v = values[i];
      const w = Math.abs(v) / maxAbs * maxW;
      const x = v >= 0 ? centreX : (centreX - w);
      const color = v >= 0 ? "#10b981" : "#ef4444";
      svg += `<text x="${centreX - 4}" y="${y + 12}" text-anchor="end" font-size="10" fill="#1e293b">${lab}</text>`;
      svg += `<rect x="${x}" y="${y + 3}" width="${w}" height="${rowH - 6}" fill="${color}"/>`;
      svg += `<text x="${v >= 0 ? (x + w + 3) : (x - 3)}" y="${y + 12}" text-anchor="${v >= 0 ? 'start' : 'end'}" font-size="10" fill="#475569">${fmt(v)}</text>`;
    });
    svg += `</svg>`;
    return svg;
  }

  function svgCIBar(score, lo, hi, width = 240, height = 28) {
    const min = -1, max = 1; const range = max - min;
    const x0 = 4, w0 = width - 8;
    const toX = v => x0 + ((v - min) / range) * w0;
    const cx = toX(score), x_lo = toX(lo), x_hi = toX(hi);
    const midX = toX(0);
    const color = score >= 0 ? "#10b981" : "#ef4444";
    return `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" style="background:#f8fafc;border-radius:4px">
      <line x1="${midX}" y1="2" x2="${midX}" y2="${height-2}" stroke="#cbd5e1" stroke-width="1"/>
      <rect x="${x_lo}" y="${height/2 - 4}" width="${x_hi - x_lo}" height="8" fill="${color}" opacity="0.25"/>
      <circle cx="${cx}" cy="${height/2}" r="5" fill="${color}"/>
      <text x="4" y="${height-4}" font-size="9" fill="#94a3b8">-1</text>
      <text x="${width-12}" y="${height-4}" font-size="9" fill="#94a3b8">+1</text>
      <text x="${cx}" y="10" text-anchor="middle" font-size="9" font-weight="bold" fill="${color}">${fmt(score)}</text>
    </svg>`;
  }

  // ================================================================
  // Per-intent response builders
  // ================================================================

  function buildLookup(intent, records) {
    if (!records.length) return buildEmpty(intent);
    let html = "";
    const citations = [];
    if (records.length === 1) {
      const r = records[0];
      const m = r._meta;
      html += `<div class="cina-card"><div class="cina-card-h">${m.country} – ${m.issue} (${m.cop})</div>`;
      html += `<div class="cina-row"><span class="cina-k">입장 점수</span><span class="cina-v"><b>${fmt(r.stance_score)}</b> (${stanceLabel(r.stance_score)})</span></div>`;
      html += `<div class="cina-row"><span class="cina-k">95% CI</span><span class="cina-v">${svgCIBar(r.stance_score, r.ci_lower_95 || r.stance_score, r.ci_upper_95 || r.stance_score)}</span></div>`;
      html += `<div class="cina-row"><span class="cina-k">우세 frame</span><span class="cina-v">${r.frame_type || "-"}</span></div>`;
      if (r.nato_4axis) {
        html += `<div class="cina-row"><span class="cina-k">NATO 4축</span><span class="cina-v">${svgNatoBar(r.nato_4axis)}</span></div>`;
      }
      const proc = r.procedural_signals || {};
      if (proc.is_chair_role || proc.is_pen_holder) {
        const tags = [proc.is_chair_role && "의장", proc.is_pen_holder && "펜홀더"].filter(Boolean).join(", ");
        html += `<div class="cina-row"><span class="cina-k">절차권한</span><span class="cina-v">${tags} (composite=${(r.procedural_composite||0).toFixed(2)})</span></div>`;
      }
      if (r.translation_gap_delta != null && Math.abs(r.translation_gap_delta) > 0.15) {
        html += `<div class="cina-row"><span class="cina-k">국내↔국제 Δ</span><span class="cina-v">${fmt(r.translation_gap_delta)}</span></div>`;
      }
      html += `</div>`;
      citations.push(recordToCitation(r));
    } else {
      const target = intent.countries[0] || records[0]._meta.country;
      html += `<div class="cina-card"><div class="cina-card-h">${target} – ${records.length}개 매칭 record</div>`;
      html += `<table class="cina-table"><thead><tr><th>이슈</th><th>COP</th><th>점수</th><th>95% CI</th></tr></thead><tbody>`;
      records.slice(0, 12).forEach(r => {
        const m = r._meta;
        html += `<tr><td>${m.issue}</td><td>${m.cop}</td><td><b>${fmt(r.stance_score)}</b></td><td>[${fmt(r.ci_lower_95||0)}, ${fmt(r.ci_upper_95||0)}]</td></tr>`;
        if (citations.length < 8) citations.push(recordToCitation(r));
      });
      html += `</tbody></table></div>`;
    }
    const conf = mean(records.map(r => r.confidence || 0.85));
    return { html, citations, confidence: round3(conf), n: records.length };
  }

  function buildCompare(intent, records) {
    if (intent.countries.length < 2) return buildLookup(intent, records);
    const cop = intent.cop || "COP30";
    const issues = intent.issues.length ? intent.issues : ["GGA-IND","GGA-MOI","NAPs","JT-ADAPT","L&D-OP","FINANCE-ADAPT","TRANS-FIN","TECH-TRANS"];
    const grouped = {};
    records.forEach(r => {
      const m = r._meta;
      if (m.cop !== cop) return;
      grouped[m.country] = grouped[m.country] || {};
      grouped[m.country][m.issue] = r;
    });
    let html = `<div class="cina-card"><div class="cina-card-h">${intent.countries.join(" vs ")} 입장 비교 (${cop})</div>`;
    html += `<table class="cina-table"><thead><tr><th>이슈</th>${intent.countries.map(c => `<th>${c}</th>`).join("")}</tr></thead><tbody>`;
    const citations = [];
    issues.forEach(iss => {
      html += `<tr><td>${iss}</td>`;
      intent.countries.forEach(c => {
        const r = (grouped[c] || {})[iss];
        if (r) {
          html += `<td><b>${fmt(r.stance_score)}</b><br><small style="color:#64748b">${stanceLabel(r.stance_score)}</small></td>`;
          if (citations.length < 12) citations.push(recordToCitation(r));
        } else {
          html += `<td style="color:#cbd5e1">-</td>`;
        }
      });
      html += `</tr>`;
    });
    html += `</tbody></table>`;
    // Largest gap
    if (intent.countries.length === 2) {
      const [c1, c2] = intent.countries;
      let largest = null;
      issues.forEach(iss => {
        const r1 = (grouped[c1] || {})[iss]; const r2 = (grouped[c2] || {})[iss];
        if (r1 && r2) {
          const g = r1.stance_score - r2.stance_score;
          if (!largest || Math.abs(g) > Math.abs(largest.g)) largest = { iss, g };
        }
      });
      if (largest) {
        html += `<div class="cina-callout">📊 <b>최대 격차</b>: ${largest.iss} (Δ = ${fmt(largest.g)})</div>`;
      }
    }
    html += `</div>`;
    const conf = records.length ? mean(records.map(r => r.confidence || 0.85)) : 0.85;
    return { html, citations, confidence: round3(conf), n: records.length };
  }

  function buildTrend(intent, records) {
    if (!records.length) return buildEmpty(intent);
    const cops = ["COP25","COP26","COP27","COP28","COP29","COP30"];
    const grouped = {};
    records.forEach(r => {
      const m = r._meta; const k = `${m.country}|${m.issue}`;
      grouped[k] = grouped[k] || {}; grouped[k][m.cop] = r;
    });
    let html = `<div class="cina-card"><div class="cina-card-h">시계열 추이 (${cops[0]}-${cops[cops.length-1]})</div>`;
    const citations = [];
    const seriesKeys = Object.keys(grouped).slice(0, 8);
    seriesKeys.forEach(k => {
      const [country, issue] = k.split("|");
      const series = cops.map(c => grouped[k][c] ? grouped[k][c].stance_score : null);
      const valid = series.filter(v => v != null);
      if (!valid.length) return;
      const first = valid[0], last = valid[valid.length-1];
      const delta = last - first;
      const arrow = delta > 0.05 ? "↑" : delta < -0.05 ? "↓" : "→";
      html += `<div class="cina-row" style="align-items:center"><div style="min-width:180px"><b>${country}</b> – ${issue}<br><small style="color:#64748b">${fmt(first)} → ${fmt(last)} ${arrow} (Δ ${fmt(delta)})</small></div><div>${svgSparkline(series)}</div></div>`;
      for (let i = cops.length - 1; i >= 0; i--) {
        if (grouped[k][cops[i]] && citations.length < 8) { citations.push(recordToCitation(grouped[k][cops[i]])); break; }
      }
    });
    if (Object.keys(grouped).length > 8) html += `<div class="cina-callout">전체 ${Object.keys(grouped).length}개 series 중 8개만 표시</div>`;
    html += `</div>`;
    return { html, citations, confidence: 0.82, n: records.length };
  }

  async function buildCoalition(intent, records) {
    if (!intent.countries.length) return buildEmpty(intent);
    const target = intent.countries[0]; const cop = intent.cop || "COP30";
    const all = await loadData();
    const byCountry = {};
    all.forEach(r => {
      const m = r._meta;
      if (m.cop !== cop) return;
      byCountry[m.country] = byCountry[m.country] || {};
      byCountry[m.country][m.issue] = r.stance_score;
    });
    if (!byCountry[target]) return buildEmpty(intent);
    const targetVec = byCountry[target];
    const issues = Object.keys(targetVec);
    function pearson(v1, v2) {
      const common = issues.filter(i => i in v1 && i in v2);
      if (common.length < 2) return 0;
      const x = common.map(i => v1[i]), y = common.map(i => v2[i]);
      const mx = mean(x), my = mean(y);
      const num = sum(common.map((_, i) => (x[i]-mx) * (y[i]-my)));
      const dx = Math.sqrt(sum(x.map(xi => (xi-mx)**2)));
      const dy = Math.sqrt(sum(y.map(yi => (yi-my)**2)));
      return dx === 0 || dy === 0 ? 0 : num / (dx * dy);
    }
    const sims = Object.keys(byCountry).filter(c => c !== target)
                       .map(c => ({c, r: pearson(targetVec, byCountry[c])}));
    sims.sort((a, b) => b.r - a.r);
    const top = sims.slice(0, 10);

    let html = `<div class="cina-card"><div class="cina-card-h">${target}와 가장 유사한 국가 (${cop}, Pearson r)</div>`;
    html += svgHBars(top.map(s => s.c), top.map(s => s.r));
    // primary coalition info
    const sample = records.find(r => r._meta.country === target);
    if (sample && sample.coalition_membership) {
      html += `<div class="cina-callout">📍 <b>${target}의 공식 coalition</b>: primary = ${sample.coalition_membership.primary}, all = ${(sample.coalition_membership.all||[]).join(", ")}</div>`;
    }
    html += `</div>`;
    const citations = top.slice(0, 6).map(s => {
      const r = records.find(rr => rr._meta.country === s.c && rr._meta.cop === cop);
      return r ? recordToCitation(r) : null;
    }).filter(Boolean);
    return { html, citations, confidence: 0.85, n: Object.keys(byCountry).length };
  }

  function buildGap(intent, records) {
    if (!records.length) return buildEmpty(intent);
    const target = intent.countries[0];
    if (target) {
      const targetR = records.filter(r => r._meta.country === target);
      const byIssue = {};
      targetR.forEach(r => { byIssue[r._meta.issue] = byIssue[r._meta.issue] || []; byIssue[r._meta.issue].push(r); });
      const labels = [], values = []; const citations = [];
      let html = `<div class="cina-card"><div class="cina-card-h">${target} – 국내↔국제 translation gap Δ</div>`;
      Object.entries(byIssue).forEach(([iss, rs]) => {
        rs.sort((a,b) => a._meta.cop.localeCompare(b._meta.cop));
        const r = rs[rs.length-1];
        const d = r.translation_gap_delta || 0;
        labels.push(`${iss}@${r._meta.cop}`); values.push(d);
        if (citations.length < 8) citations.push(recordToCitation(r));
      });
      html += svgHBars(labels, values);
      html += `<div class="cina-callout">Δ &gt; 0: 국내 의지 강한데 국제에서 약화 (Brazil paradox 패턴). Δ &lt; 0: 국제에서 더 적극적.</div>`;
      html += `</div>`;
      return { html, citations, confidence: 0.78, n: records.length };
    } else {
      // global gap ranking
      const cop = intent.cop || "COP30";
      const byCountry = {};
      records.forEach(r => {
        if (r._meta.cop !== cop) return;
        const c = r._meta.country;
        byCountry[c] = byCountry[c] || [];
        byCountry[c].push(Math.abs(r.translation_gap_delta || 0));
      });
      const ranking = Object.entries(byCountry).map(([c, vs]) => [c, mean(vs)]).sort((a,b) => b[1] - a[1]).slice(0, 10);
      let html = `<div class="cina-card"><div class="cina-card-h">${cop} – 국가별 평균 |Δ| 상위 10</div>`;
      html += svgHBars(ranking.map(x => x[0]), ranking.map(x => x[1]));
      html += `</div>`;
      return { html, citations: [], confidence: 0.75, n: records.length };
    }
  }

  function buildRecommendation(intent, records) {
    const target = intent.countries[0] || "Korea";
    const cop = intent.cop || "COP30";
    const sub = records.filter(r => r._meta.country === target && r._meta.cop === cop);
    if (!sub.length) return buildEmpty(intent);
    sub.sort((a,b) => a.stance_score - b.stance_score);
    const weak = sub.slice(0, 3), strong = sub.slice(-3).reverse();
    let html = `<div class="cina-card"><div class="cina-card-h">${target} 전략 권고 (${cop})</div>`;
    const citations = [];
    html += `<div style="background:#fef2f2;padding:8px;border-radius:6px;margin-bottom:8px"><b>📉 약점 이슈 (보강 필요)</b></div><table class="cina-table"><tbody>`;
    weak.forEach(r => {
      const topAxis = r.nato_4axis ? Object.entries(r.nato_4axis).sort((a,b) => b[1]-a[1])[0][0] : "-";
      html += `<tr><td>${r._meta.issue}</td><td><b>${fmt(r.stance_score)}</b></td><td><small>NATO <b>${topAxis}</b> 축 강화 권장</small></td></tr>`;
      if (citations.length < 8) citations.push(recordToCitation(r));
    });
    html += `</tbody></table>`;
    html += `<div style="background:#f0fdf4;padding:8px;border-radius:6px;margin:8px 0"><b>📈 강점 이슈 (pen-holder 활용)</b></div><table class="cina-table"><tbody>`;
    strong.forEach(r => {
      const pen = r.procedural_signals && r.procedural_signals.is_pen_holder ? " 👑펜홀더" : "";
      html += `<tr><td>${r._meta.issue}${pen}</td><td><b>${fmt(r.stance_score)}</b></td><td><small>${stanceLabel(r.stance_score)}</small></td></tr>`;
      if (citations.length < 8) citations.push(recordToCitation(r));
    });
    html += `</tbody></table>`;
    // coalition + gap
    const sample = sub[0];
    if (sample.coalition_membership && sample.coalition_membership.all) {
      html += `<div class="cina-callout">🤝 활용 coalition: ${sample.coalition_membership.all.join(", ")}</div>`;
    }
    const meanD = mean(sub.map(r => Math.abs(r.translation_gap_delta || 0)));
    html += `<div class="cina-callout">📐 평균 |Δ| = ${meanD.toFixed(3)} (${meanD > 0.25 ? "주의" : "안정"})</div>`;
    html += `</div>`;
    return { html, citations, confidence: 0.82, n: records.length };
  }

  function buildFactoid(intent, records) {
    if (!records.length) return buildEmpty(intent);
    const r = records[0]; const m = r._meta;
    const html = `<div class="cina-card"><div class="cina-card-h">${m.country} – ${m.issue} (${m.cop})</div>
      <div style="font-size:32px;font-weight:bold;text-align:center;padding:16px">${fmt(r.stance_score)}</div>
      <div style="text-align:center;color:#64748b">${ciStr(r)}</div></div>`;
    return { html, citations: [recordToCitation(r)], confidence: r.confidence || 0.85, n: records.length };
  }

  function buildSearch(intent, records) {
    const hits = corpusSearch(intent.raw, 8);
    if (!hits.length) {
      return { html: `<div class="cina-card"><div class="cina-card-h">corpus 검색 결과 없음</div>
        <div>corpus index가 로드되지 않았거나 매칭되는 문서가 없습니다.</div></div>`,
        citations: [], confidence: 0, n: 0 };
    }
    let html = `<div class="cina-card"><div class="cina-card-h">'${escapeHtml(intent.raw)}' — corpus 문서 top-${hits.length}</div>
      <table class="cina-table"><thead><tr><th>#</th><th>제목</th><th>type</th><th>score</th><th>source</th></tr></thead><tbody>`;
    hits.forEach((h, i) => {
      const m = h.manifest;
      const link = m.official_url ? `<a href="${escapeHtml(m.official_url)}" target="_blank">원문 ↗</a>` : "-";
      html += `<tr><td>${i+1}</td><td><b>${escapeHtml(m.short_title || m.title || "?")}</b><br><code style="font-size:11px">${escapeHtml(m.path || '?')}</code></td>
        <td>${escapeHtml(m.type || '?')}${m.cop ? '<br><small>'+escapeHtml(m.cop)+'</small>' : ''}</td>
        <td>${h.score.toFixed(3)}</td>
        <td>${link}</td></tr>`;
    });
    html += `</tbody></table></div>`;
    return { html, citations: [], confidence: 0.80, n: hits.length,
             corpus_hits: hits };
  }

  function buildEmpty(intent) {
    return {
      html: `<div class="cina-card"><div class="cina-card-h">매칭 record 없음</div>
        <div>지원: 50국 × 8이슈 (GGA-IND/MOI, NAPs, JT-ADAPT, L&amp;D-OP, FINANCE-ADAPT, TRANS-FIN, TECH-TRANS) × 6 COP (COP25-30)<br>
        국가+이슈를 명시하면 정확도가 올라갑니다.</div></div>`,
      citations: [], confidence: 0, n: 0,
    };
  }

  // ================================================================
  // Methodology footer
  // ================================================================

  function methodologyFooter(intent, n_retrieved, source, providerName) {
    const dsv = META_CACHE?.dataset_version || DATASET_VERSION_TARGET;
    const h = hashIntent(intent, 42);
    const src = source === "rule" ? "rule-based v2"
              : `LLM (${providerName || "?"})`;
    return `<div class="cina-meta">📐 methodology · engine ${ENGINE_VERSION} · dataset v${dsv} · intent <b>${intent.type}</b> · retrieved n=${n_retrieved} · source ${src} · hash <code>${h}</code></div>`;
  }

  // ================================================================
  // LLM calls (Gemini / Anthropic / Groq)
  // ================================================================

  async function callGemini(prompt, key) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=${key}`;
    const body = {
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.3, maxOutputTokens: 1500 },
    };
    const res = await fetch(url, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`Gemini HTTP ${res.status}: ${await res.text()}`);
    const j = await res.json();
    return j.candidates?.[0]?.content?.parts?.[0]?.text || "(empty response)";
  }

  async function callAnthropic(prompt, key) {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-5-20250929",
        max_tokens: 1500, temperature: 0.3,
        messages: [{ role: "user", content: prompt }],
      }),
    });
    if (!res.ok) throw new Error(`Anthropic HTTP ${res.status}: ${await res.text()}`);
    const j = await res.json();
    return j.content?.[0]?.text || "(empty response)";
  }

  async function callGroq(prompt, key) {
    const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${key}` },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.3, max_tokens: 1500,
      }),
    });
    if (!res.ok) throw new Error(`Groq HTTP ${res.status}: ${await res.text()}`);
    const j = await res.json();
    return j.choices?.[0]?.message?.content || "(empty response)";
  }

  function buildLLMContext(records) {
    const ctx = [];
    records.slice(0, 24).forEach((r, i) => {
      const m = r._meta;
      ctx.push(`[Record ${i+1}] country=${m.country} | issue=${m.issue} | cop=${m.cop}
  stance=${fmt(r.stance_score)} (95% CI [${fmt(r.ci_lower_95||0)}, ${fmt(r.ci_upper_95||0)}])
  frame=${r.frame_type || "-"} | NATO ${natoSummary(r)}
  proc_composite=${(r.procedural_composite||0).toFixed(2)} | coalition=${r.coalition_membership?.primary || "?"}
  translation_gap_delta=${fmt(r.translation_gap_delta||0)}
  evidence: ${r.evidence_quote || "-"}
  source: ${m.source_type}`);
    });
    return ctx.join("\n\n");
  }

  function buildLLMPrompt(question, records, history) {
    const ctx = buildLLMContext(records);
    const histStr = history.length ? "\n\n## 최근 대화 (참고용)\n" + history.slice(-5).map((h, i) => `T${i+1} Q: ${h.q}\nT${i+1} A: ${h.a_summary}`).join("\n\n") : "";
    return `당신은 CINA(Climate Issue-Network Analysis) Q&A 전문가다. CINA는 LLM-Graph-LLM 3단 파이프라인으로 UNFCCC 협상 텍스트에서 다축 stance를 추출하는 방법론이다. 이론적 기반: Hood 1983 NATO 4축 정책수단, Howlett 2019 정책 도구 calibration, Tallberg 2010 chair 절차권한, Putnam 1988 Two-Level Games, Keohane & Victor 2011 regime complex.

## 엄격한 출력 규칙
1. 오직 아래 제공된 CINA database lookup 결과만을 사실 근거로 사용한다. 데이터에 없는 사실은 추측하지 않는다.
2. stance score는 부호 + 소수점 2자리(예: +0.65)로 표기한다.
3. 95% credible interval이 있으면 함께 표기한다 (예: +0.65 [+0.55, +0.74]).
4. 가능하면 IR/정책학 이론 (Tallberg chair-channel, Hood NATO 4축, Putnam Two-Level)을 한 번 인용한다.
5. 답변 끝에 "📎 근거 N건"으로 사용한 인용 개수를 명시한다.
6. 데이터에 없는 정보를 묻는 경우 "데이터베이스에 명시되지 않음"을 정직하게 표시한다.
7. 한국어로 자연스러운 단락(문장)으로 답변한다. 글머리표는 필요할 때만 사용.

## 사용자 질문
${question}

## CINA database lookup 결과 (top-${Math.min(24, records.length)} relevance)
${ctx}
${histStr}

위 데이터만을 사용해 사용자 질문에 답하라. 데이터에 없는 사실은 만들지 않는다.`;
  }

  async function callLLM(provider, prompt) {
    const key = getKey(provider);
    if (!key) throw new Error(`API key not set for ${provider}`);
    if (provider === "gemini") return await callGemini(prompt, key);
    if (provider === "anthropic") return await callAnthropic(prompt, key);
    if (provider === "groq") return await callGroq(prompt, key);
    throw new Error(`Unknown provider: ${provider}`);
  }

  // ================================================================
  // Main entry point
  // ================================================================

  async function answerQuestion(question, options = {}) {
    const mode = options.mode || "rule";
    const provider = options.provider || pickFirstAvailableProvider();
    const records = await loadData();
    const intent = parseIntent(question);

    const k = intent.type === "trend" ? 120 :
              intent.type === "coalition" ? 400 :
              intent.type === "gap" ? 80 : 24;
    const retrieved = retrieve(records, intent, k);

    // ensure corpus is loaded for auto-attach + search intent
    await loadCorpus();

    const builders = {
      lookup: buildLookup, compare: buildCompare, trend: buildTrend,
      coalition: buildCoalition, gap: buildGap, recommendation: buildRecommendation,
      factoid: buildFactoid, search: buildSearch, unknown: buildLookup,
    };
    const builder = builders[intent.type] || buildLookup;
    const built = await Promise.resolve(builder(intent, retrieved));

    let answerHTML = built.html;
    let llmText = null;

    if (mode === "llm" && provider && getKey(provider)) {
      try {
        const history = getHistory();
        const prompt = buildLLMPrompt(question, retrieved, history);
        llmText = await callLLM(provider, prompt);
        answerHTML = `<div class="cina-llm-answer">${escapeHtml(llmText).replace(/\n/g, "<br>")}</div>` + answerHTML;
      } catch (e) {
        console.error("[CINA v2] LLM call failed:", e);
        answerHTML = `<div class="cina-callout" style="background:#fef2f2;color:#991b1b">⚠️ LLM 호출 실패: ${escapeHtml(e.message)}<br>rule-based 결과로 대체합니다.</div>` + answerHTML;
      }
    }

    answerHTML += `<div class="cina-citations" data-count="${built.citations.length}">${renderCitations(built.citations)}</div>`;

    // v2.1: Auto-attach corpus references to all non-'search' intents
    if (intent.type !== "search") {
      const ctxHits = corpusFilterByContext(intent);
      const queryHits = corpusSearch(question, 10).map(h => h.manifest);
      const seen = new Set(), merged = [];
      queryHits.forEach(r => { if (!seen.has(r.doc_id)) { seen.add(r.doc_id); merged.push(r); } });
      ctxHits.forEach(r => { if (!seen.has(r.doc_id)) { seen.add(r.doc_id); merged.push(r); } });
      if (merged.length) {
        answerHTML += renderCorpusRefs(merged.slice(0, 3));
      }
    }

    answerHTML += methodologyFooter(intent, built.n, llmText ? "llm" : "rule", provider);

    pushHistory({
      ts: Date.now(), q: question, mode, provider,
      a_summary: (llmText || stripHtml(built.html)).slice(0, 240),
      citations: built.citations.length, intent_type: intent.type,
    });

    return {
      html: answerHTML, citations: built.citations, intent,
      confidence: built.confidence, n_retrieved: retrieved.length,
      source: llmText ? `LLM (${provider})` : "rule-based",
      raw_llm_text: llmText,
    };
  }

  function renderCorpusRefs(refs) {
    if (!refs || !refs.length) return "";
    let html = `<div class="cina-corpus-refs"><div class="cina-corpus-h">📚 관련 corpus 문서 ${refs.length}건</div>`;
    refs.forEach(r => {
      const link = r.official_url
        ? `<a href="${escapeHtml(r.official_url)}" target="_blank">원문 ↗</a>`
        : (r.path ? `<a href="${escapeHtml(r.path)}" target="_blank">로컬 ↗</a>` : "");
      html += `<div class="cina-corpus-row">
        <span class="cina-corpus-type">${escapeHtml(r.type || '?')}</span>
        <span class="cina-corpus-title"><b>${escapeHtml(r.short_title || r.title || r.doc_id)}</b>
        ${r.cop ? '<span class="cina-corpus-tag">'+escapeHtml(r.cop)+'</span>' : ''}
        ${r.country ? '<span class="cina-corpus-tag">'+escapeHtml(r.country)+'</span>' : ''}</span>
        <span class="cina-corpus-link">${link}</span>
      </div>`;
    });
    html += `</div>`;
    return html;
  }

  function renderCitations(citations) {
    if (!citations.length) return "";
    let html = `<details class="cina-cite-panel"><summary>📎 근거 ${citations.length}건 (펼치기)</summary><div>`;
    citations.forEach((c, i) => {
      html += `<div class="cina-cite-item">
        <b>[${i+1}] ${c.country} / ${c.issue} @ ${c.cop}</b> — stance ${fmt(c.score)}
        ${c.ci_lower != null ? `[${fmt(c.ci_lower)}, ${fmt(c.ci_upper)}]` : ""}
        ${c.frame ? `· frame=${c.frame}` : ""}
        ${c.source_type === "verified_canonical" ? "✅" : ""}
        <div class="cina-cite-quote">"${escapeHtml(c.quote || "(no quote)")}"</div>
      </div>`;
    });
    html += `</div></details>`;
    return html;
  }

  // ================================================================
  // Export functions
  // ================================================================

  function exportMarkdown() {
    const h = getHistory();
    const md = ["# CINA Q&A 대화 export\n", `생성: ${new Date().toISOString()}\n`,
                `총 turns: ${h.length}\n\n`];
    h.forEach((t, i) => {
      md.push(`## T${i+1} (${new Date(t.ts).toISOString()})`);
      md.push(`**Q**: ${t.q}`);
      md.push(`**모드**: ${t.mode}${t.provider ? ` (${t.provider})` : ""}  ·  **intent**: ${t.intent_type}  ·  **인용**: ${t.citations}건`);
      md.push(`**A 요약**: ${t.a_summary}\n`);
    });
    triggerDownload("cina_conversation.md", md.join("\n"), "text/markdown");
  }
  function exportJSON() {
    triggerDownload("cina_conversation.json", JSON.stringify(getHistory(), null, 2), "application/json");
  }
  function exportBibTeX() {
    const all = `@software{cina2026,
  author = {Choi, Heedo},
  title = {{CINA: Climate Issue-Network Analysis}},
  year = {2026},
  url = {https://github.com/zxsa0716/cina},
  version = {v5.0.0 / engine v2.0.0},
}

@misc{cina2026arxiv,
  author = {Choi, Heedo},
  title = {{Ask CINA: A Multi-Axis LLM Pipeline with Cross-Provider Reliability for Climate Negotiation Analytics}},
  howpublished = {arXiv preprint},
  year = {2026},
}`;
    triggerDownload("cina_citations.bib", all, "application/x-bibtex");
  }
  function triggerDownload(filename, text, mime) {
    const blob = new Blob([text], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href = url; a.download = filename; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  // ================================================================
  // Util
  // ================================================================
  function mean(arr) { return arr.length ? arr.reduce((a,b) => a+b, 0) / arr.length : 0; }
  function sum(arr)  { return arr.reduce((a,b) => a+b, 0); }
  function round3(x) { return Math.round(x * 1000) / 1000; }
  function escapeHtml(s) {
    return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }
  function stripHtml(s) { const d = document.createElement("div"); d.innerHTML = s; return d.textContent || ""; }
  function pickFirstAvailableProvider() {
    for (const p of ["gemini", "anthropic", "groq"]) if (getKey(p)) return p;
    return null;
  }

  // ================================================================
  // Public API
  // ================================================================

  window.CINA_v2 = {
    answerQuestion, parseIntent, getKey, setKey, clearKey, hasAnyKey,
    pickFirstAvailableProvider, getHistory, clearHistory,
    exportMarkdown, exportJSON, exportBibTeX,
    loadData,
    ENGINE_VERSION,
  };

  console.log(`[CINA v2] ${ENGINE_VERSION} loaded. Use window.CINA_v2.answerQuestion(q, {mode, provider}).`);
})();
