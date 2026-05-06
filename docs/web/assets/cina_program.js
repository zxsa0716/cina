// CINA Program — Browser-side Q&A engine with BYO LLM key support
//
// Modes:
//   rule  — pure JavaScript rule-based matching (zero network, instant)
//   llm   — bring-your-own LLM API key (Gemini, Anthropic, Groq) — REAL implementation
//
// Architecture: User question → intent parse → CINA data lookup →
//   (a) rule-based response template, OR
//   (b) LLM call with grounding context (lookup results + evidence quotes)
//   → answer + citations + visualization payload
//
// API keys are stored in browser localStorage only (never sent to a CINA server).
// All LLM calls go directly from the browser to the chosen provider.
//
// Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
// License: MIT

(function() {
  "use strict";

  // ----------------------------------------------------------------
  // Aliases (Korean + English)
  // ----------------------------------------------------------------

  const COUNTRY_ALIASES = {
    "브라질": "Brazil", "brazil": "Brazil",
    "한국": "Korea", "대한민국": "Korea", "korea": "Korea",
    "미국": "USA", "usa": "USA", "us": "USA",
    "중국": "China", "china": "China",
    "인도": "India", "india": "India",
    "유럽연합": "EU", "유럽": "EU", "eu": "EU",
    "사우디": "Saudi", "사우디아라비아": "Saudi", "saudi": "Saudi",
    "일본": "Japan", "japan": "Japan",
    "튀르키예": "Türkiye", "터키": "Türkiye", "turkey": "Türkiye",
    "AOSIS": "AOSIS", "aosis": "AOSIS", "군소도서국": "AOSIS",
    "AILAC": "AILAC", "ailac": "AILAC",
    "AGN": "AGN", "agn": "AGN", "아프리카그룹": "AGN", "아프리카": "AGN",
    "LMDC": "LMDC", "lmdc": "LMDC",
    "캐나다": "Canada", "canada": "Canada",
    "호주": "Australia",
    "노르웨이": "Norway",
    "영국": "UK", "uk": "UK",
    "독일": "Germany",
    "프랑스": "France",
    "멕시코": "Mexico",
    "인도네시아": "Indonesia",
    "남아공": "South Africa",
    "이집트": "Egypt",
    "몰디브": "Maldives",
    "투발루": "Tuvalu", "tuvalu": "Tuvalu",
    "방글라데시": "Bangladesh",
    "에티오피아": "Ethiopia",
    "네팔": "Nepal",
  };

  const ISSUE_ALIASES = {
    "GGA-IND": "GGA-IND", "GGA 지표": "GGA-IND", "지표": "GGA-IND",
    "GGA-MOI": "GGA-MOI", "이행수단": "GGA-MOI",
    "NAPs": "NAPs", "NAP": "NAPs", "국가적응계획": "NAPs",
    "JT-ADAPT": "JT-ADAPT", "정의로운 전환": "JT-ADAPT",
    "L&D-OP": "L&D-OP", "손실 피해": "L&D-OP", "손실·피해": "L&D-OP", "L&D": "L&D-OP",
    "FINANCE-ADAPT": "FINANCE-ADAPT", "적응 재원": "FINANCE-ADAPT", "재원": "FINANCE-ADAPT",
  };

  const COP_ALIASES = {
    "COP26": "COP26", "글래스고": "COP26",
    "COP27": "COP27", "샤름": "COP27",
    "COP28": "COP28", "두바이": "COP28",
    "COP29": "COP29", "바쿠": "COP29",
    "COP30": "COP30", "벨렘": "COP30",
  };

  let DATA_CACHE = null;
  let MODE = "rule";
  let LLM_PROVIDER = "gemini";

  // ----------------------------------------------------------------
  // API key storage
  // ----------------------------------------------------------------

  const KEY_STORAGE = {
    gemini: "cina_byo_key_gemini",
    anthropic: "cina_byo_key_anthropic",
    groq: "cina_byo_key_groq",
  };

  function getKey(provider) {
    try { return localStorage.getItem(KEY_STORAGE[provider]) || ""; }
    catch (e) { return ""; }
  }

  function setKey(provider, key) {
    try { localStorage.setItem(KEY_STORAGE[provider], key); return true; }
    catch (e) { return false; }
  }

  function clearKey(provider) {
    try { localStorage.removeItem(KEY_STORAGE[provider]); return true; }
    catch (e) { return false; }
  }

  function hasAnyKey() {
    return ["gemini", "anthropic", "groq"].some(p => getKey(p));
  }

  // ----------------------------------------------------------------
  // Data loading
  // ----------------------------------------------------------------

  async function loadData() {
    if (DATA_CACHE) return DATA_CACHE;
    const candidates = [
      "../../data/processed/stances_v4.jsonl",
      "data/processed/stances_v4.jsonl",
      "/cina/data/processed/stances_v4.jsonl",
    ];
    for (const url of candidates) {
      try {
        const res = await fetch(url);
        if (!res.ok) continue;
        const text = await res.text();
        DATA_CACHE = text.trim().split("\n")
          .filter(l => l.trim())
          .map(l => JSON.parse(l));
        console.log(`[CINA] Loaded ${DATA_CACHE.length} records from ${url}`);
        return DATA_CACHE;
      } catch (e) { /* try next */ }
    }
    console.warn("[CINA] All data fetch attempts failed; using built-in fallback");
    DATA_CACHE = BUILTIN_FALLBACK;
    return DATA_CACHE;
  }

  // ----------------------------------------------------------------
  // Intent parsing
  // ----------------------------------------------------------------

  function parseIntent(question) {
    const q = question.trim();
    const qLower = q.toLowerCase();

    const countries = [];
    for (const [alias, canon] of Object.entries(COUNTRY_ALIASES)) {
      if (qLower.includes(alias.toLowerCase()) && !countries.includes(canon)) {
        if (alias === "브라질" && /COP30|cop30|벨렘/i.test(q)) continue;
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
    if (/비교|차이|다른|vs|versus/i.test(q) && countries.length >= 2) type = "compare";
    else if (/권고|전략|어떻게|추천|recommend/i.test(q)) type = "recommendation";
    else if (/입장|위치|스탠스|stance|position/i.test(q)) type = "lookup";
    else if (/몇|얼마|how much|what is the value|값은/i.test(q)) type = "factoid";
    else if (countries.length && issues.length) type = "lookup";
    else if (issues.length && !countries.length) type = "lookup";

    return { type, countries, issues, cop: cop || "COP30", raw: q };
  }

  function lookup(records, countries, issues, cop) {
    return records.filter(r => {
      const m = r._meta || r;
      if (countries.length && !countries.includes(m.country)) return false;
      if (issues.length && !issues.includes(m.issue)) return false;
      if (cop && m.cop !== cop) return false;
      return true;
    });
  }

  // ----------------------------------------------------------------
  // Rule-based responses (same as before)
  // ----------------------------------------------------------------

  function fmt(s) { return (s >= 0 ? "+" : "") + s.toFixed(2); }
  function lbl(s) {
    if (s >= 0.7) return "강한 지지";
    if (s >= 0.3) return "지지";
    if (s >= -0.3) return "중립";
    if (s >= -0.7) return "반대";
    return "강한 반대";
  }

  function buildCompareRule(intent, records) {
    const grouped = {};
    for (const r of records) {
      const m = r._meta;
      if (!grouped[m.country]) grouped[m.country] = {};
      grouped[m.country][m.issue] = r;
    }
    const targetIssues = intent.issues.length ? intent.issues
      : ["GGA-IND", "GGA-MOI", "NAPs", "JT-ADAPT", "L&D-OP", "FINANCE-ADAPT"];

    let html = `<p><strong>${intent.countries.join(" vs ")} 입장 비교 (${intent.cop})</strong></p>`;
    const series = [];
    const citations = [];
    for (const c of intent.countries) {
      const cRecs = grouped[c] || {};
      const scores = [];
      let countryHtml = `<p><strong>${c}</strong>:</p><ul>`;
      for (const iss of targetIssues) {
        const r = cRecs[iss];
        if (r) {
          const s = r.stance_score; scores.push(s);
          countryHtml += `<li>${iss}: <strong>${fmt(s)}</strong> (${lbl(s)})</li>`;
          if (r.evidence_quote && citations.length < 6) {
            citations.push({ country: c, issue: iss, cop: r._meta.cop, quote: r.evidence_quote, score: s });
          }
        } else { scores.push(null); }
      }
      countryHtml += "</ul>";
      html += countryHtml;
      series.push({ name: c, data: scores });
    }
    if (intent.countries.length === 2 && targetIssues.length >= 1) {
      const [c1, c2] = intent.countries;
      const r1 = (grouped[c1] || {})[targetIssues[0]];
      const r2 = (grouped[c2] || {})[targetIssues[0]];
      if (r1 && r2) {
        const diff = r1.stance_score - r2.stance_score;
        html += `<p><strong>핵심 차이 (${targetIssues[0]})</strong>: ${c1} ${fmt(r1.stance_score)} 와 `
              + `${c2} ${fmt(r2.stance_score)} 사이의 차이는 <strong>${fmt(diff)}</strong>로, `
              + `${Math.abs(diff) < 0.2 ? "유사한 입장" : "뚜렷한 입장 차이"}을 보인다.</p>`;
      }
    }
    return { html, citations, viz: { type: "comparison_bar", labels: targetIssues, series },
             confidence: 0.85, matched: Object.values(grouped).reduce((s, c) => s + Object.keys(c).length, 0) };
  }

  function buildLookupRule(intent, records) {
    if (!records.length) {
      return { html: "<p>해당 조건에 부합하는 입장 데이터를 찾지 못했습니다. 국가명·이슈명을 다시 확인해 주세요.</p>",
               citations: [], viz: null, confidence: 0.0, matched: 0 };
    }
    const byCountry = {};
    for (const r of records) {
      const c = r._meta.country;
      if (!byCountry[c]) byCountry[c] = [];
      byCountry[c].push(r);
    }
    let html = "";
    const citations = [];
    const rows = [];
    for (const [country, recs] of Object.entries(byCountry)) {
      html += `<p><strong>${country}</strong> (${intent.cop})</p><ul>`;
      for (const r of recs) {
        const iss = r._meta.issue;
        const s = r.stance_score;
        const frame = r.frame_type || "";
        const chair = r.procedural_signals && r.procedural_signals.is_chair_role ? " 👑 의장" : "";
        const pen = r.procedural_signals && r.procedural_signals.is_pen_holder ? " · 펜홀더" : "";
        html += `<li>${iss}: <strong>${fmt(s)}</strong> (${lbl(s)}) · frame=${frame}${chair}${pen}</li>`;
        rows.push({ country, issue: iss, score: s, frame });
        if (r.evidence_quote && citations.length < 6) {
          citations.push({ country, issue: iss, cop: r._meta.cop, quote: r.evidence_quote, score: s });
        }
      }
      html += "</ul>";
    }
    return { html, citations, viz: { type: "stance_table", rows },
             confidence: 0.85, matched: records.length };
  }

  const RECOMMENDATIONS = {
    "GGA-IND": "한국형 NAP 거버넌스 모델을 벨렘–아디스 작업 프로그램의 참조 모형으로 입력. 탄소중립기본법 §47에 근거한 3단계 구조(중앙·지방·부문)를 활용하여 운영 가이드라인 표준 사례 위치 확보.",
    "GGA-MOI": "GCF 운영 효율성 지표 제안을 통해 자동 공여국 확대 논의를 측면에서 우회. GCF 호스트 국가의 운영 경험을 의제화.",
    "NAPs": "NAP 펜홀더 권한을 활용하여 한국형 적응 모델을 국제 표준 사례로 정착. 다른 행위자(브라질 +0.88, AOSIS +0.78, EU +0.72)와 협력 가능한 영역.",
    "JT-ADAPT": "탄소중립기본법 §50의 취약계층·노동자 보호 조항을 COP31 본회의 장관 발언에서 명시적으로 언급하고 학술 논문으로 영문 발신을 동시 진행.",
    "L&D-OP": "한국 IRR 0.39로 6 이슈 중 최저 약점 영역. 손실·피해 기금 이사회에 대한 <strong>자발적 기관 지원 약정 (연 5–10백만 달러 규모) 검토 시작</strong>을 권고. 단, 예산 편성 절차(환경부/외교부 → 기획재정부 → 국무회의 → 국회 의결)상 사전 검토 필수.",
    "FINANCE-ADAPT": "GCF 운영 효율 의제 주도로 협상 가시성 확보. 자동 공여국 base year 확대 논의를 측면에서 우회."
  };

  function buildRecommendationRule(intent, records) {
    const target = intent.countries.includes("Korea") ? "Korea" : (intent.countries[0] || "Korea");
    const targetIssues = intent.issues.length ? intent.issues : ["GGA-IND", "L&D-OP"];
    const ownByIssue = {};
    for (const r of records) { if (r._meta.country === target) ownByIssue[r._meta.issue] = r; }

    let html = `<p><strong>${target} 외교부 권고 (${intent.cop || "COP31 prospective"})</strong></p>`;
    const citations = [];
    for (const iss of targetIssues) {
      const recText = RECOMMENDATIONS[iss];
      if (!recText) continue;
      const ownRec = ownByIssue[iss];
      const ownScore = ownRec ? fmt(ownRec.stance_score) : "?";
      html += `<p><strong>${iss}</strong> (현 입장: ${ownScore})<br>${recText}</p>`;
      if (ownRec && ownRec.evidence_quote && citations.length < 4) {
        citations.push({ country: target, issue: iss, cop: ownRec._meta.cop,
                          quote: ownRec.evidence_quote, score: ownRec.stance_score });
      }
    }
    return { html, citations, viz: null, confidence: 0.8, matched: Object.keys(ownByIssue).length };
  }

  const FACTS = {
    delta: "브라질 Translation Gap <strong>Δ = 0.304</strong> — Plano Clima 국내 정책 NATO 4축 사용률 67% 와 L.25E 국제 voluntary 텍스트 사용률 23%의 차이. Putnam(1988) × Howlett(2019) 정책수단 분기 정량화.",
    irr: "한국 적응정책 종합 이행률 <strong>IRR = 0.653</strong> (95% 신뢰구간 [0.55, 0.71]). L&D-OP 영역의 0.39가 6 이슈 중 최저로 약점.",
    nes: "AILAC 8개국 규범 기업가 점수 <strong>NES = 0.86</strong> (4 criteria 중 3.5개 충족). Finnemore-Sikkink (1998) 4 criteria 적용.",
    spearman: "CINA Stage 1 입장 추출 정확도 <strong>Spearman ρ = 0.658</strong> (전문가 reference 대비). MAE = 0.183. Phase 5 Task A 결과.",
    crossllm: "5개 LLM 제공자 간 일치도 <strong>Krippendorff α = 0.876 (원시) / 0.933 (편향 보정)</strong>. 단, 5종 모두 transformer + RLHF 기반이므로 same-paradigm agreement이지 shared-model bias 완전 분리는 아님."
  };

  function buildFactoidRule(intent) {
    const q = intent.raw.toLowerCase();
    const matched = [];
    if (/delta|δ|translation gap|번역 격차|0\.304/.test(q)) matched.push(FACTS.delta);
    if (/irr|이행률|0\.653/.test(q)) matched.push(FACTS.irr);
    if (/nes|norm entrepreneur|규범 기업가|ailac/.test(q)) matched.push(FACTS.nes);
    if (/spearman|정확도|task a/.test(q)) matched.push(FACTS.spearman);
    if (/cross-llm|krippendorff|alpha|α/.test(q)) matched.push(FACTS.crossllm);
    if (!matched.length) return { html: "<p>관련 사실을 명확히 식별하지 못했습니다.</p>", citations: [], viz: null, confidence: 0.0, matched: 0 };
    return { html: matched.map(m => `<p>${m}</p>`).join(""), citations: [], viz: null, confidence: 0.95, matched: matched.length };
  }

  function buildUnknownRule() {
    return {
      html: `<p>질문 의도를 명확히 파악하지 못했습니다. 다음 형식으로 다시 질문해 주세요:</p>
        <ul>
          <li><strong>국가 비교</strong>: '브라질과 한국의 GGA 지표 입장 차이는?'</li>
          <li><strong>입장 조회</strong>: 'AOSIS의 손실·피해 입장은?'</li>
          <li><strong>권고 요청</strong>: '한국이 COP31 L&D 이슈에서 어떻게 해야 하나?'</li>
          <li><strong>사실 확인</strong>: 'Translation Gap Δ 값은 얼마인가?'</li>
        </ul>`,
      citations: [], viz: null, confidence: 0.0, matched: 0
    };
  }

  // ----------------------------------------------------------------
  // LLM call (REAL implementation — Gemini, Anthropic, Groq)
  // ----------------------------------------------------------------

  function buildLLMContext(records, intent) {
    /** Build a compact context string for the LLM grounded in actual lookup data. */
    if (!records.length) {
      return "(No matching records found in CINA database for the parsed intent.)";
    }
    const lines = [];
    lines.push(`# CINA database extract (${records.length} matching records, intent.cop = ${intent.cop})`);
    for (const r of records.slice(0, 24)) {  // cap to 24 records to stay within context
      const m = r._meta;
      const proc = r.procedural_signals || {};
      const signals = [];
      if (proc.is_chair_role) signals.push("CHAIR");
      if (proc.is_pen_holder) signals.push("PEN_HOLDER");
      lines.push(
        `- ${m.country} | ${m.issue} | ${m.cop} | stance=${r.stance_score?.toFixed(2)} ` +
        `(${r.stance_category || "?"}) | frame=${r.frame_type || "?"}` +
        (signals.length ? ` | ${signals.join(",")}` : "") +
        (r.evidence_quote ? `\n  evidence: "${r.evidence_quote.slice(0, 200)}"` : "")
      );
    }
    return lines.join("\n");
  }

  function buildLLMPrompt(question, context, intent) {
    return `당신은 CINA(Climate Issue-Network Analysis) 협상 분석 어시스턴트입니다. UNFCCC 기후 협상의 30개국 × 6개 적응 의제 × 5 COP cycles 데이터에 정통합니다.

다음 데이터베이스 조회 결과를 *유일한 사실 근거*로 삼아 사용자 질문에 한국어로 답변하세요. 데이터에 없는 사실은 추측하지 말고 명시적으로 "데이터에 없음"이라고 표시하세요.

=== CINA 데이터 조회 결과 ===
${context}
=== 데이터 끝 ===

사용자 질문: ${question}

답변 가이드라인:
1. 한국어로 답변. 외교부 보고서 voice (정중하고 간결).
2. stance score는 항상 부호 + 소수점 2자리 (예: +0.65, -0.30).
3. 데이터에서 직접 인용한 evidence quote가 있다면 인용 부호 안에 그대로 옮길 것.
4. 답변은 4-7 문장, markdown으로 구조화 (소제목 사용 가능).
5. 추측·일반론 회피. CINA 데이터에 명시된 사항만 보고.
6. "데이터에 명시되지 않음" 정직 명시 권장.

답변:`;
  }

  async function callGemini(prompt, apiKey) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=${encodeURIComponent(apiKey)}`;
    const body = {
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.3, maxOutputTokens: 1500 }
    };
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Gemini API HTTP ${res.status}: ${err.slice(0, 200)}`);
    }
    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!text) throw new Error("Gemini returned empty response: " + JSON.stringify(data).slice(0, 200));
    return text;
  }

  async function callAnthropic(prompt, apiKey) {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true"
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-5-20250929",
        max_tokens: 1500,
        temperature: 0.3,
        messages: [{ role: "user", content: prompt }]
      })
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Anthropic API HTTP ${res.status}: ${err.slice(0, 200)}`);
    }
    const data = await res.json();
    const text = data?.content?.[0]?.text;
    if (!text) throw new Error("Anthropic returned empty response: " + JSON.stringify(data).slice(0, 200));
    return text;
  }

  async function callGroq(prompt, apiKey) {
    const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: "llama-3.3-70b-versatile",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.3,
        max_tokens: 1500
      })
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Groq API HTTP ${res.status}: ${err.slice(0, 200)}`);
    }
    const data = await res.json();
    const text = data?.choices?.[0]?.message?.content;
    if (!text) throw new Error("Groq returned empty response: " + JSON.stringify(data).slice(0, 200));
    return text;
  }

  async function callLLM(prompt) {
    const key = getKey(LLM_PROVIDER);
    if (!key) throw new Error(`${LLM_PROVIDER.toUpperCase()} API key not set. Click "🔑 API Key" to enter your key.`);
    if (LLM_PROVIDER === "gemini") return await callGemini(prompt, key);
    if (LLM_PROVIDER === "anthropic") return await callAnthropic(prompt, key);
    if (LLM_PROVIDER === "groq") return await callGroq(prompt, key);
    throw new Error("Unknown provider: " + LLM_PROVIDER);
  }

  function markdownToHtml(md) {
    // Minimal Markdown → HTML for our needs. Not a full parser.
    let html = md
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.+?)\*/g, "<em>$1</em>")
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/^### (.+)$/gm, "<h4>$1</h4>")
      .replace(/^## (.+)$/gm, "<h3>$1</h3>")
      .replace(/^# (.+)$/gm, "<h2>$1</h2>")
      .replace(/^- (.+)$/gm, "<li>$1</li>")
      .replace(/(<li>.+<\/li>)\n?/g, m => `<ul>${m}</ul>`)
      .replace(/<\/ul>\n?<ul>/g, "")
      .split(/\n\n+/).map(p => p.trim().match(/^<(h\d|ul|ol|p|li)/) ? p : `<p>${p.replace(/\n/g, "<br>")}</p>`)
      .join("\n");
    return html;
  }

  // ----------------------------------------------------------------
  // Top-level: route question to rule or LLM
  // ----------------------------------------------------------------

  async function answerQuestion(question) {
    const records = await loadData();
    const intent = parseIntent(question);
    const filtered = lookup(records, intent.countries, intent.issues, intent.cop);

    if (MODE === "llm") {
      const context = buildLLMContext(filtered, intent);
      const prompt = buildLLMPrompt(question, context, intent);
      try {
        const llmText = await callLLM(prompt);
        // Build citations from the lookup data we provided to the LLM
        const citations = filtered.slice(0, 6).map(r => ({
          country: r._meta.country, issue: r._meta.issue, cop: r._meta.cop,
          quote: r.evidence_quote || "", score: r.stance_score
        })).filter(c => c.quote);
        return {
          html: markdownToHtml(llmText),
          citations, viz: null,
          confidence: filtered.length > 0 ? 0.92 : 0.5,
          matched: filtered.length, intent,
          source: `${LLM_PROVIDER.toUpperCase()} (BYO key)`
        };
      } catch (e) {
        console.error("[CINA LLM]", e);
        return {
          html: `<p style="color:#dc2626">⚠️ <strong>LLM 호출 실패</strong>: ${e.message}</p>
                 <p style="font-size:0.88em;color:var(--c-fg-mute)">Rule-based 모드로 자동 fallback합니다.</p>` +
                 (await runRuleBased(intent, filtered)).html,
          citations: [], viz: null, confidence: 0.0, matched: 0, intent,
          source: "fallback"
        };
      }
    } else {
      const r = await runRuleBased(intent, filtered);
      return { ...r, intent, source: "rule-based" };
    }
  }

  async function runRuleBased(intent, filtered) {
    if (intent.type === "compare") return buildCompareRule(intent, filtered);
    if (intent.type === "lookup") return buildLookupRule(intent, filtered);
    if (intent.type === "recommendation") return buildRecommendationRule(intent, filtered);
    if (intent.type === "factoid") return buildFactoidRule(intent);
    return buildUnknownRule();
  }

  // ----------------------------------------------------------------
  // Visualization renderer
  // ----------------------------------------------------------------

  function renderViz(viz, container) {
    if (!viz) return;
    if (viz.type === "comparison_bar") {
      let html = `<h4 style="font-size:0.85em;color:var(--c-fg-mute);margin:0 0 0.6rem;letter-spacing:0.04em;text-transform:uppercase;">시각화 — 국가 × 이슈 비교</h4><div>`;
      for (const series of viz.series) {
        html += `<p style="margin:0.6rem 0 0.3rem;color:var(--c-accent);font-weight:600;font-size:0.9em;">${series.name}</p>`;
        for (let i = 0; i < viz.labels.length; i++) {
          const v = series.data[i];
          if (v == null) continue;
          const widthPct = Math.min(50, Math.abs(v) * 50);
          const cls = v < 0 ? "neg" : "";
          const offset = v < 0 ? `right: 50%; left: auto;` : `left: 50%;`;
          html += `<div class="viz-bar-row">
            <div class="lbl">${viz.labels[i]}</div>
            <div class="bar-bg"><div class="bar ${cls}" style="width:${widthPct}%;${offset}"></div></div>
            <div class="val">${(v >= 0 ? "+" : "") + v.toFixed(2)}</div>
          </div>`;
        }
      }
      html += "</div>";
      container.innerHTML = html;
    }
  }

  // ----------------------------------------------------------------
  // API Key Modal UI
  // ----------------------------------------------------------------

  function ensureKeyModal() {
    if (document.getElementById("key-modal")) return;
    const modal = document.createElement("div");
    modal.id = "key-modal";
    modal.style.cssText = "display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:1000;align-items:center;justify-content:center;";
    modal.innerHTML = `
      <div style="background:#11141d;border:1px solid #2a3344;border-radius:14px;padding:1.8rem 2rem;max-width:560px;width:92%;box-shadow:0 20px 60px rgba(0,0,0,0.5);">
        <h3 style="margin-top:0;color:#f8fafc;display:flex;align-items:center;gap:0.5rem;">🔑 BYO LLM API Key</h3>
        <p style="color:#94a3b8;font-size:0.92em;line-height:1.5;">
          API 키는 <strong>본인 브라우저 localStorage에만 저장</strong>되며 CINA 서버로 전송되지 않습니다.
          모든 LLM 호출은 브라우저에서 직접 provider API로 직접 갑니다.
        </p>
        <div style="display:flex;flex-direction:column;gap:1rem;margin-top:1.2rem;">
          ${["gemini", "anthropic", "groq"].map(p => `
          <div>
            <label style="display:block;font-size:0.85em;color:#cbd5e1;margin-bottom:0.3rem;font-weight:600;">
              ${p === "gemini" ? "Gemini 2.5 Flash-Lite" : p === "anthropic" ? "Anthropic Claude" : "Groq Llama 3.3 70B"}
              <span style="color:#94a3b8;font-weight:400;">
                ${p === "gemini" ? "(무료 1000 RPD · " : p === "anthropic" ? "(유료 · " : "(무료 · "}
                <a href="${p === "gemini" ? "https://aistudio.google.com/apikey" : p === "anthropic" ? "https://console.anthropic.com/settings/keys" : "https://console.groq.com/keys"}" target="_blank" rel="noopener" style="color:#6ea8ff;">키 받기 →</a>)
              </span>
            </label>
            <div style="display:flex;gap:0.5rem;align-items:center;">
              <input type="password" id="key-input-${p}" placeholder="sk-... 또는 AIzaSy..." style="flex:1;background:#0f1420;color:#f8fafc;border:1px solid #2a3344;border-radius:8px;padding:0.5rem 0.8rem;font-family:monospace;font-size:0.88em;">
              <button data-action="save" data-provider="${p}" style="background:#6ea8ff;color:#0b0d12;border:none;padding:0.5rem 0.9rem;border-radius:8px;font-weight:700;cursor:pointer;font-size:0.85em;">저장</button>
              <button data-action="clear" data-provider="${p}" style="background:transparent;color:#94a3b8;border:1px solid #2a3344;padding:0.5rem 0.9rem;border-radius:8px;cursor:pointer;font-size:0.85em;">제거</button>
            </div>
            <div id="key-status-${p}" style="margin-top:0.3rem;font-size:0.78em;color:#94a3b8;"></div>
          </div>
          `).join("")}
        </div>
        <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid #2a3344;display:flex;justify-content:space-between;align-items:center;">
          <p style="margin:0;font-size:0.78em;color:#94a3b8;">⚠️ 키 노출 위험 시 즉시 provider 콘솔에서 회전(rotate)할 것.</p>
          <button data-action="close" style="background:#2a5298;color:white;border:none;padding:0.5rem 1.4rem;border-radius:8px;font-weight:700;cursor:pointer;">닫기</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    modal.addEventListener("click", e => {
      if (e.target === modal) modal.style.display = "none";
      const action = e.target.dataset.action;
      if (action === "close") modal.style.display = "none";
      if (action === "save") {
        const p = e.target.dataset.provider;
        const v = document.getElementById(`key-input-${p}`).value.trim();
        if (v) {
          setKey(p, v);
          updateKeyStatus(p);
          document.getElementById(`key-input-${p}`).value = "";
        }
      }
      if (action === "clear") {
        const p = e.target.dataset.provider;
        clearKey(p);
        updateKeyStatus(p);
      }
    });
  }

  function updateKeyStatus(provider) {
    const el = document.getElementById(`key-status-${provider}`);
    if (!el) return;
    const k = getKey(provider);
    if (k) {
      el.innerHTML = `<span style="color:#10b981">✅ 저장됨 (${k.slice(0, 8)}...${k.slice(-4)})</span>`;
    } else {
      el.innerHTML = `<span style="color:#94a3b8">키 없음</span>`;
    }
    refreshLlmStatusBadge();
  }

  function openKeyModal() {
    ensureKeyModal();
    ["gemini", "anthropic", "groq"].forEach(updateKeyStatus);
    document.getElementById("key-modal").style.display = "flex";
  }

  // ----------------------------------------------------------------
  // Status badge in input bar
  // ----------------------------------------------------------------

  function refreshLlmStatusBadge() {
    const badge = document.getElementById("llm-status-badge");
    if (!badge) return;
    const providers = ["gemini", "anthropic", "groq"].filter(p => getKey(p));
    if (providers.length) {
      badge.innerHTML = `🟢 LLM 사용 가능: ${providers.join(", ")}`;
      badge.style.color = "#10b981";
    } else {
      badge.innerHTML = `🟡 LLM 키 없음 (rule-based만 가능)`;
      badge.style.color = "#94a3b8";
    }
  }

  // ----------------------------------------------------------------
  // UI binding
  // ----------------------------------------------------------------

  document.addEventListener("DOMContentLoaded", () => {
    const inputEl = document.getElementById("qa-input");
    const sendEl = document.getElementById("qa-send");
    const historyEl = document.getElementById("qa-history");
    const suggestEl = document.getElementById("qa-suggest");
    const modeBtns = document.querySelectorAll(".qa-mode button");

    // Inject API key button + status badge into the input bar
    const qaBar = document.querySelector(".qa-bar");
    if (qaBar && !document.getElementById("key-btn")) {
      const keyBtn = document.createElement("button");
      keyBtn.id = "key-btn";
      keyBtn.textContent = "🔑 API Key";
      keyBtn.style.cssText = "background:rgba(245,158,11,0.12);border:1px solid #f59e0b;color:#f59e0b;padding:0.45rem 0.9rem;border-radius:8px;cursor:pointer;font-size:0.85em;margin-right:0.4rem;font-weight:600;";
      keyBtn.addEventListener("click", openKeyModal);

      const llmBadge = document.createElement("span");
      llmBadge.id = "llm-status-badge";
      llmBadge.style.cssText = "font-size:0.78em;color:#94a3b8;margin-left:0.4rem;";

      const sendBtn = document.querySelector(".qa-send");
      sendBtn.parentNode.insertBefore(keyBtn, sendBtn);
      sendBtn.parentNode.insertBefore(llmBadge, sendBtn);
    }
    refreshLlmStatusBadge();

    // Mode switching
    modeBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const requested = btn.dataset.mode;
        if (requested === "llm") {
          if (!hasAnyKey()) {
            openKeyModal();
            return;
          }
          // Show provider chooser inline
          const chosen = window.prompt(
            "LLM provider 선택 (gemini / anthropic / groq):", LLM_PROVIDER
          );
          if (!chosen) return;
          if (!["gemini", "anthropic", "groq"].includes(chosen.trim().toLowerCase())) {
            alert("지원되지 않는 provider입니다."); return;
          }
          LLM_PROVIDER = chosen.trim().toLowerCase();
          if (!getKey(LLM_PROVIDER)) {
            alert(`${LLM_PROVIDER} 키가 저장되지 않음. 키 모달을 엽니다.`);
            openKeyModal(); return;
          }
        }
        modeBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        MODE = requested;
        console.log(`[CINA] Mode switched to ${MODE} (provider=${LLM_PROVIDER})`);
      });
    });

    suggestEl.querySelectorAll(".pill").forEach(p => {
      p.addEventListener("click", () => {
        inputEl.value = p.dataset.q;
        sendEl.click();
      });
    });

    sendEl.addEventListener("click", async () => {
      const q = inputEl.value.trim();
      if (!q) return;

      const empty = historyEl.querySelector(".empty-state");
      if (empty) empty.remove();

      const userTurn = document.createElement("div");
      userTurn.className = "qa-turn user";
      userTurn.innerHTML = `<div class="role"><span class="ico">Q</span>사용자</div><div class="body">${escapeHtml(q)}</div>`;
      historyEl.appendChild(userTurn);

      const asstTurn = document.createElement("div");
      asstTurn.className = "qa-turn";
      asstTurn.innerHTML = `<div class="role"><span class="ico">A</span>CINA <span style="margin-left:0.5rem;font-size:0.78em;font-weight:400;">[${MODE}${MODE === "llm" ? " · " + LLM_PROVIDER : ""}]</span></div><div class="body"><span class="loading">생각 중</span></div>`;
      historyEl.appendChild(asstTurn);

      inputEl.value = "";
      sendEl.disabled = true;

      try {
        const r = await answerQuestion(q);
        let body = r.html;
        if (r.citations && r.citations.length) {
          body += `<div class="citations"><h4>📎 인용 ${r.citations.length}건</h4>`;
          for (const c of r.citations) {
            body += `<div class="citation">
              <div class="meta">${c.country} · ${c.issue} · ${c.cop} · 점수 ${(c.score >= 0 ? "+" : "") + c.score.toFixed(2)}</div>
              <div class="quote">${escapeHtml(c.quote)}</div>
            </div>`;
          }
          body += "</div>";
        }
        if (r.viz) body += `<div class="viz-area" id="viz-${Date.now()}"></div>`;
        body += `<p style="font-size:0.78em;color:var(--c-fg-mute);margin-top:0.8rem;">
          신뢰도: ${(r.confidence * 100).toFixed(0)}% · 매칭 records: ${r.matched} · ` +
          `intent: ${r.intent.type} · source: ${r.source || "—"}</p>`;
        asstTurn.querySelector(".body").innerHTML = body;
        if (r.viz) {
          const vizContainer = asstTurn.querySelector(".viz-area");
          if (vizContainer) renderViz(r.viz, vizContainer);
        }
      } catch (e) {
        asstTurn.querySelector(".body").innerHTML =
          `<p style="color:#dc2626;">오류 발생: ${escapeHtml(e.message)}</p>`;
      } finally {
        sendEl.disabled = false;
        asstTurn.scrollIntoView({ behavior: "smooth", block: "end" });
        inputEl.focus();
      }
    });

    inputEl.addEventListener("keydown", e => {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        sendEl.click();
      }
    });

    function escapeHtml(s) {
      return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
    }

    console.log("CINA Program ready. 30 countries × 6 issues × 5 COPs = 900 records.");
  });

  // ----------------------------------------------------------------
  // Built-in fallback dataset
  // ----------------------------------------------------------------

  const BUILTIN_FALLBACK = [
    { _meta: { country: "Brazil", issue: "GGA-IND", cop: "COP30" },
      stance_score: 0.95, frame_type: "development",
      procedural_signals: { is_chair_role: true, is_pen_holder: true },
      evidence_quote: "[COP30, Brazil] 59 voluntary, non-prescriptive, non-punitive, facilitative indicators across seven thematic targets" },
    { _meta: { country: "Korea", issue: "GGA-IND", cop: "COP30" },
      stance_score: 0.65, frame_type: "mixed",
      procedural_signals: { is_chair_role: false, is_pen_holder: false },
      evidence_quote: "[COP30, Korea] balanced approach to GGA implementation guidance through NAP framework" },
    { _meta: { country: "AOSIS", issue: "L&D-OP", cop: "COP30" },
      stance_score: 0.95, frame_type: "justice",
      procedural_signals: { is_chair_role: false, is_pen_holder: false },
      evidence_quote: "[COP30, AOSIS] operationalisation of the Loss and Damage Fund must commence without delay" },
    { _meta: { country: "Korea", issue: "L&D-OP", cop: "COP30" },
      stance_score: 0.39, frame_type: "mixed",
      procedural_signals: { is_chair_role: false, is_pen_holder: false },
      evidence_quote: "[COP30, Korea] Korea is examining options to support the FRLD board through institutional cooperation" },
  ];

})();
