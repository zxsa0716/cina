// CINA Program — Browser-side Q&A engine
// Loads stances_v4.json (compact) and answers natural-language questions
// using the same intent → lookup → response logic as src/program/query_engine.py.
//
// Modes:
//   rule  — pure JavaScript rule-based matching (zero network, instant)
//   llm   — bring-your-own LLM API key (Gemini or Anthropic) for natural responses
//
// Author: Heedo Choi (Kookmin University, Department of Climate Technology Convergence)
// License: MIT

(function() {
  "use strict";

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
    "투발루": "Tuvalu",
    "tuvalu": "Tuvalu",
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

  // ----------------------------------------------------------------
  // Data loading (with graceful fallback)
  // ----------------------------------------------------------------

  async function loadData() {
    if (DATA_CACHE) return DATA_CACHE;
    try {
      const res = await fetch("../../data/processed/stances_v4.jsonl");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const text = await res.text();
      DATA_CACHE = text.trim().split("\n")
        .filter(l => l.trim())
        .map(l => JSON.parse(l));
      console.log(`[CINA Program] Loaded ${DATA_CACHE.length} records from stances_v4.jsonl`);
      return DATA_CACHE;
    } catch (e) {
      // Fallback: built-in compact dataset (a small subset for offline demo)
      console.warn("[CINA Program] stances_v4.jsonl fetch failed; using built-in fallback. Reason:", e.message);
      DATA_CACHE = BUILTIN_FALLBACK;
      return DATA_CACHE;
    }
  }

  // ----------------------------------------------------------------
  // Intent parsing (mirrors src/program/query_engine.py)
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
    if (/비교|차이|다른|vs|versus/i.test(q) && countries.length >= 2) {
      type = "compare";
    } else if (/권고|전략|어떻게|추천|recommend/i.test(q)) {
      type = "recommendation";
    } else if (/입장|위치|스탠스|stance|position/i.test(q)) {
      type = "lookup";
    } else if (/몇|얼마|how much|what is the value|값은/i.test(q)) {
      type = "factoid";
    } else if (countries.length && issues.length) {
      type = "lookup";
    } else if (issues.length && !countries.length) {
      type = "lookup";
    }

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
  // Response formatters
  // ----------------------------------------------------------------

  function formatScore(s) { return (s >= 0 ? "+" : "") + s.toFixed(2); }

  function stanceLabel(s) {
    if (s >= 0.7) return "강한 지지";
    if (s >= 0.3) return "지지";
    if (s >= -0.3) return "중립";
    if (s >= -0.7) return "반대";
    return "강한 반대";
  }

  function buildCompare(intent, records) {
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
          const s = r.stance_score;
          scores.push(s);
          countryHtml += `<li>${iss}: <strong>${formatScore(s)}</strong> (${stanceLabel(s)})</li>`;
          if (r.evidence_quote && citations.length < 6) {
            citations.push({
              country: c, issue: iss, cop: r._meta.cop,
              quote: r.evidence_quote, score: s
            });
          }
        } else {
          scores.push(null);
        }
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
        html += `<p><strong>핵심 차이 (${targetIssues[0]})</strong>: ${c1} ${formatScore(r1.stance_score)} 와 `
              + `${c2} ${formatScore(r2.stance_score)} 사이의 차이는 <strong>${formatScore(diff)}</strong>로, `
              + `${Math.abs(diff) < 0.2 ? "유사한 입장" : "뚜렷한 입장 차이"}을 보인다.</p>`;
      }
    }

    return {
      html,
      citations,
      viz: { type: "comparison_bar", labels: targetIssues, series },
      confidence: 0.85,
      matched: Object.values(grouped).reduce((s, c) => s + Object.keys(c).length, 0)
    };
  }

  function buildLookup(intent, records) {
    if (!records.length) {
      return {
        html: "<p>해당 조건에 부합하는 입장 데이터를 찾지 못했습니다. 국가명·이슈명을 다시 확인해 주세요.</p>",
        citations: [], viz: null, confidence: 0.0, matched: 0
      };
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
        html += `<li>${iss}: <strong>${formatScore(s)}</strong> (${stanceLabel(s)}) · frame=${frame}${chair}${pen}</li>`;
        rows.push({ country, issue: iss, score: s, frame });
        if (r.evidence_quote && citations.length < 6) {
          citations.push({
            country, issue: iss, cop: r._meta.cop,
            quote: r.evidence_quote, score: s
          });
        }
      }
      html += "</ul>";
    }
    return { html, citations, viz: { type: "stance_table", rows },
             confidence: 0.85, matched: records.length };
  }

  function buildRecommendation(intent, records) {
    const target = intent.countries.includes("Korea") ? "Korea"
                 : (intent.countries[0] || "Korea");
    const targetIssues = intent.issues.length ? intent.issues : ["GGA-IND", "L&D-OP"];
    const ownByIssue = {};
    for (const r of records) {
      if (r._meta.country === target) ownByIssue[r._meta.issue] = r;
    }

    const recs = {
      "GGA-IND": "한국형 NAP 거버넌스 모델을 벨렘–아디스 작업 프로그램의 참조 모형으로 입력. 탄소중립기본법 §47에 근거한 3단계 구조(중앙·지방·부문)를 활용하여 운영 가이드라인 표준 사례 위치 확보.",
      "GGA-MOI": "GCF 운영 효율성 지표 제안을 통해 자동 공여국 확대 논의를 측면에서 우회. GCF 호스트 국가의 운영 경험을 의제화.",
      "NAPs": "NAP 펜홀더 권한을 활용하여 한국형 적응 모델을 국제 표준 사례로 정착. 다른 행위자(브라질 +0.88, AOSIS +0.78, EU +0.72)와 협력 가능한 영역.",
      "JT-ADAPT": "탄소중립기본법 §50의 취약계층·노동자 보호 조항을 COP31 본회의 장관 발언에서 명시적으로 언급하고 학술 논문으로 영문 발신을 동시 진행.",
      "L&D-OP": "한국 IRR 0.39로 6 이슈 중 최저 약점 영역. 손실·피해 기금 이사회에 대한 <strong>자발적 기관 지원 약정 (연 5–10백만 달러 규모) 검토 시작</strong>을 권고. 단, 예산 편성 절차(환경부/외교부 → 기획재정부 → 국무회의 → 국회 의결)상 사전 검토 필수.",
      "FINANCE-ADAPT": "GCF 운영 효율 의제 주도로 협상 가시성 확보. 자동 공여국 base year 확대 논의를 측면에서 우회."
    };

    let html = `<p><strong>${target} 외교부 권고 (${intent.cop || "COP31 prospective"})</strong></p>`;
    const citations = [];
    for (const iss of targetIssues) {
      const recText = recs[iss];
      if (!recText) continue;
      const ownRec = ownByIssue[iss];
      const ownScore = ownRec ? formatScore(ownRec.stance_score) : "?";
      html += `<p><strong>${iss}</strong> (현 입장: ${ownScore})<br>${recText}</p>`;
      if (ownRec && ownRec.evidence_quote && citations.length < 4) {
        citations.push({
          country: target, issue: iss, cop: ownRec._meta.cop,
          quote: ownRec.evidence_quote, score: ownRec.stance_score
        });
      }
    }
    return { html, citations, viz: null, confidence: 0.8,
             matched: Object.keys(ownByIssue).length };
  }

  function buildFactoid(intent) {
    const facts = {
      delta: "브라질 Translation Gap <strong>Δ = 0.304</strong> — Plano Clima 국내 정책 NATO 4축 사용률 67% 와 L.25E 국제 voluntary 텍스트 사용률 23%의 차이. Putnam(1988) × Howlett(2019) 정책수단 분기 정량화.",
      irr: "한국 적응정책 종합 이행률 <strong>IRR = 0.653</strong> (95% 신뢰구간 [0.55, 0.71]). L&D-OP 영역의 0.39가 6 이슈 중 최저로 약점.",
      nes: "AILAC 8개국 규범 기업가 점수 <strong>NES = 0.86</strong> (4 criteria 중 3.5개 충족). Finnemore-Sikkink (1998) 4 criteria 적용.",
      spearman: "CINA Stage 1 입장 추출 정확도 <strong>Spearman ρ = 0.658</strong> (전문가 reference 대비). MAE = 0.183. Phase 5 Task A 결과.",
      crossllm: "5개 LLM 제공자 간 일치도 <strong>Krippendorff α = 0.876 (원시) / 0.933 (편향 보정)</strong>. 단, 5종 모두 transformer + RLHF 기반이므로 same-paradigm agreement이지 shared-model bias 완전 분리는 아님."
    };
    const q = intent.raw.toLowerCase();
    const matched = [];
    if (/delta|δ|translation gap|번역 격차|0\.304/.test(q)) matched.push(facts.delta);
    if (/irr|이행률|0\.653/.test(q)) matched.push(facts.irr);
    if (/nes|norm entrepreneur|규범 기업가|ailac/.test(q)) matched.push(facts.nes);
    if (/spearman|정확도|task a/.test(q)) matched.push(facts.spearman);
    if (/cross-llm|krippendorff|alpha|α/.test(q)) matched.push(facts.crossllm);
    if (!matched.length) {
      return { html: "<p>관련 사실을 명확히 식별하지 못했습니다. 다른 표현으로 다시 질문해 주세요.</p>",
               citations: [], viz: null, confidence: 0.0, matched: 0 };
    }
    return { html: matched.map(m => `<p>${m}</p>`).join(""),
             citations: [], viz: null, confidence: 0.95, matched: matched.length };
  }

  function buildUnknown() {
    return {
      html: `<p>질문 의도를 명확히 파악하지 못했습니다. 다음과 같은 형식으로 다시 질문해 주세요:</p>
        <ul>
          <li><strong>국가 비교</strong>: '브라질과 한국의 GGA 지표 입장 차이는?'</li>
          <li><strong>입장 조회</strong>: 'AOSIS의 손실·피해 입장은?'</li>
          <li><strong>권고 요청</strong>: '한국이 COP31 L&D 이슈에서 어떻게 해야 하나?'</li>
          <li><strong>사실 확인</strong>: 'Translation Gap Δ 값은 얼마인가?'</li>
        </ul>
        <p style="font-size:0.88em;color:var(--c-fg-mute)">지원 국가 (30): Brazil, EU, USA, China, India, AOSIS, Korea, Saudi, Japan, AILAC, AGN, LMDC, Multi, Canada, Australia, Norway, UK, Germany, France, Mexico, Indonesia, South Africa, Egypt, Türkiye, Maldives, Marshall Is, Tuvalu, Bangladesh, Ethiopia, Nepal</p>`,
      citations: [], viz: null, confidence: 0.0, matched: 0
    };
  }

  // ----------------------------------------------------------------
  // Top-level answer
  // ----------------------------------------------------------------

  async function answerQuestion(question) {
    const records = await loadData();
    const intent = parseIntent(question);
    const filtered = lookup(records, intent.countries, intent.issues, intent.cop);

    let response;
    if (intent.type === "compare") response = buildCompare(intent, filtered);
    else if (intent.type === "lookup") response = buildLookup(intent, filtered);
    else if (intent.type === "recommendation") response = buildRecommendation(intent, filtered);
    else if (intent.type === "factoid") response = buildFactoid(intent);
    else response = buildUnknown();

    return { ...response, intent };
  }

  // ----------------------------------------------------------------
  // Visualization renderers
  // ----------------------------------------------------------------

  function renderViz(viz, container) {
    if (!viz) return;
    if (viz.type === "comparison_bar") {
      let html = `<h4 style="font-size:0.85em;color:var(--c-fg-mute);margin:0 0 0.6rem;letter-spacing:0.04em;text-transform:uppercase;">시각화 — 국가 × 이슈 비교</h4>`;
      html += "<div>";
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
  // UI binding
  // ----------------------------------------------------------------

  document.addEventListener("DOMContentLoaded", () => {
    const inputEl = document.getElementById("qa-input");
    const sendEl = document.getElementById("qa-send");
    const historyEl = document.getElementById("qa-history");
    const suggestEl = document.getElementById("qa-suggest");
    const modeBtns = document.querySelectorAll(".qa-mode button");

    // Mode switching
    modeBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        modeBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        MODE = btn.dataset.mode;
        if (MODE === "llm") {
          alert("LLM 모드: 본 기능은 사용자 본인의 API key가 필요합니다. " +
                "현재 데모는 rule-based 모드만 지원하며, LLM 모드는 향후 별도 setup 가이드로 활성화됩니다. " +
                "(rule-based 모드로 자동 전환됩니다)");
          modeBtns.forEach(b => b.classList.remove("active"));
          modeBtns[0].classList.add("active");
          MODE = "rule";
        }
      });
    });

    // Suggestion pills
    suggestEl.querySelectorAll(".pill").forEach(p => {
      p.addEventListener("click", () => {
        inputEl.value = p.dataset.q;
        sendEl.click();
      });
    });

    // Send button
    sendEl.addEventListener("click", async () => {
      const q = inputEl.value.trim();
      if (!q) return;

      // Clear empty state
      const empty = historyEl.querySelector(".empty-state");
      if (empty) empty.remove();

      // User turn
      const userTurn = document.createElement("div");
      userTurn.className = "qa-turn user";
      userTurn.innerHTML = `<div class="role"><span class="ico">Q</span>사용자</div><div class="body">${escapeHtml(q)}</div>`;
      historyEl.appendChild(userTurn);

      // Assistant placeholder
      const asstTurn = document.createElement("div");
      asstTurn.className = "qa-turn";
      asstTurn.innerHTML = `<div class="role"><span class="ico">A</span>CINA</div><div class="body"><span class="loading">생각 중</span></div>`;
      historyEl.appendChild(asstTurn);

      inputEl.value = "";
      sendEl.disabled = true;

      // Process
      try {
        const r = await answerQuestion(q);
        let body = r.html;
        if (r.citations && r.citations.length) {
          body += `<div class="citations"><h4>📎 인용 ${r.citations.length}건</h4>`;
          for (const c of r.citations) {
            body += `<div class="citation">
              <div class="meta">${c.country} · ${c.issue} · ${c.cop} · 점수 ${formatScore(c.score)}</div>
              <div class="quote">${escapeHtml(c.quote)}</div>
            </div>`;
          }
          body += "</div>";
        }
        if (r.viz) {
          body += `<div class="viz-area" id="viz-${Date.now()}"></div>`;
        }
        body += `<p style="font-size:0.78em;color:var(--c-fg-mute);margin-top:0.8rem;">
          신뢰도: ${(r.confidence * 100).toFixed(0)}% · 매칭 records: ${r.matched} · intent: ${r.intent.type}</p>`;
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
        // Scroll to bottom
        asstTurn.scrollIntoView({ behavior: "smooth", block: "end" });
        inputEl.focus();
      }
    });

    // Enter to send
    inputEl.addEventListener("keydown", e => {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        sendEl.click();
      }
    });

    function formatScore(s) { return (s >= 0 ? "+" : "") + s.toFixed(2); }
    function escapeHtml(s) {
      return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
    }

    console.log("CINA Program ready. 30 countries × 6 issues × 5 COPs = 900 records.");
  });

  // ----------------------------------------------------------------
  // Built-in fallback dataset (small subset for offline / file:// access)
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
