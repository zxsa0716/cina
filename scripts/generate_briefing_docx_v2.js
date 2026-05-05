// COP31 적응 협상 전략 브리핑 v2 — 압축 + 한국어 보고서 톤 정제판
// 저자: 최희도 (Heedo Choi), 국민대학교 대학원 기후기술융합학과
// 출력: FOR_SUBMISSION/01_AgentAI를 활용한 장관급브리핑.docx
//
// v1 대비 변경 사항
// - 16,142자 → 약 11,500자로 압축 (~30% 감소)
// - "Ⅳ. 연합 Matrix" → "연합 구도" 번역 오류 수정
// - 영-한 혼용 정제 (institutional support pledge → 자발적 기관 지원 약정 등)
// - 자기 참조 / throat-clearing 표현 제거
// - 외교부 공식 보고서 톤으로 voice 정렬
// - 부록 A/B/C 본문에서 핵심만 인라인으로 통합

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType,
  HeadingLevel, LevelFormat, PageBreak, PageNumber, BorderStyle,
  ShadingType, WidthType
} = require('docx');

const KO_FONT = "Malgun Gothic";

function P(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: opts.before || 0, after: opts.after || 160 },
    indent: opts.indent ? { firstLine: 360 } : undefined,
    children: text.map(seg => {
      if (typeof seg === 'string') {
        return new TextRun({ text: seg, font: KO_FONT, size: 22 });
      }
      return new TextRun({ font: KO_FONT, size: 22, ...seg });
    })
  });
}

function H1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 480, after: 240 },
    children: [new TextRun({ text, font: KO_FONT, bold: true, size: 32, color: "1c2536" })]
  });
}

function H2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 360, after: 180 },
    children: [new TextRun({ text, font: KO_FONT, bold: true, size: 26, color: "2a5298" })]
  });
}

function H3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, font: KO_FONT, bold: true, size: 23, color: "1c2536" })]
  });
}

function NumberedRec(text, num) {
  return new Paragraph({
    numbering: { reference: "rec-numbers", level: 0 },
    spacing: { line: 340, before: 120, after: 160 },
    alignment: AlignmentType.JUSTIFIED,
    children: text.map(seg => {
      if (typeof seg === 'string') return new TextRun({ text: seg, font: KO_FONT, size: 22 });
      return new TextRun({ font: KO_FONT, size: 22, ...seg });
    })
  });
}

const doc = new Document({
  creator: "Heedo Choi (최희도)",
  title: "COP31 적응 협상 전략 브리핑",
  description: "외교부 기후환경과학외교국 — 한국 기후대사 / 기후에너지환경부 장관 보고",
  styles: {
    default: { document: { run: { font: KO_FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: KO_FONT, size: 32, bold: true, color: "1c2536" },
        paragraph: { spacing: { before: 480, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: KO_FONT, size: 26, bold: true, color: "2a5298" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: KO_FONT, size: 23, bold: true, color: "1c2536" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 } }
    ]
  },
  numbering: {
    config: [
      { reference: "rec-numbers", levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 480, hanging: 360 } } } }
      ]}
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "COP31 적응 협상 전략 브리핑 · 외교부 기후환경과학외교국",
            font: KO_FONT, size: 18, color: "888888" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "최희도 · 국민대학교 대학원 기후기술융합학과 · ",
              font: KO_FONT, size: 18, color: "888888" }),
            new TextRun({ text: "p. ", font: KO_FONT, size: 18, color: "888888" }),
            new TextRun({ children: [PageNumber.CURRENT], font: KO_FONT, size: 18, color: "888888" })
          ]
        })]
      })
    },
    children: [
      // ========== 표지 ==========
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 1200, after: 240 },
        children: [new TextRun({ text: "외교부 기후환경과학외교국 보고",
          font: KO_FONT, size: 28, color: "445566" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [new TextRun({ text: "COP31 적응(Adaptation) 협상 전략 브리핑",
          font: KO_FONT, size: 44, bold: true, color: "1c2536" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 480 },
        children: [new TextRun({
          text: "— 의장국 브라질에서 튀르키예로의 전환기, 한국의 협상 좌표 —",
          font: KO_FONT, size: 24, italics: true, color: "445566" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120, before: 800 },
        children: [new TextRun({ text: "보고 대상: 한국 기후대사 · 기후에너지환경부 장관",
          font: KO_FONT, size: 22, color: "222222" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: "작성: 최희도 (Heedo Choi)", font: KO_FONT, size: 22 })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: "국민대학교 대학원 기후기술융합학과",
          font: KO_FONT, size: 22 })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: "zxsa0716@kookmin.ac.kr", font: KO_FONT, size: 20, color: "666666" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120, before: 480 },
        children: [new TextRun({ text: "분류: 수업 제출용 / 공개 자료 기반",
          font: KO_FONT, size: 20, italics: true, color: "888888" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [new TextRun({ text: "작성일: 2026년 5월",
          font: KO_FONT, size: 20, color: "888888" })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== I. 요약 ==========
      H1("Ⅰ. 요약"),

      P([
        "COP30(2025년 11월, 브라질 벨렘)에서 채택된 글로벌 적응 목표 결정문(FCCC/PA/CMA/2025/L.25E)과 적응 재원 결정문(L.24)은 형식적 합의를 이루었으나, 그 운영적 함의는 의장국 브라질의 정교한 텍스트 설계에 의해 결정되었다. 결정문 7항의 자발적·비처방적·비징벌적·촉진적이라는 어휘 네 단어가 단일 문장 안에 연속 배치된 점, 9항이 ",
        { text: "“추가적 재정 의무를 발생시키지 않는다(shall not create new financial obligations)”", italics: true },
        "라는 부정적 권한(negative authority)을 명시한 점은 합의가 운영 단계에서 의무를 발생시키지 않도록 설계되었음을 보여준다."
      ], { indent: true }),

      P([
        "이러한 출발점 위에서 본 보고는 한국이 2026년 11월 튀르키예 COP31에서 직면할 협상 좌표를 다음 세 가지 결론으로 정리한다. 첫째, 한국 적응정책의 글로벌 정합도는 ",
        { text: "이행률(IRR) 0.653 (신뢰구간 0.55–0.71)", bold: true },
        "로 양호한 수준이다. 둘째, 손실·피해 운영(L&D-OP) 영역의 IRR이 ",
        { text: "0.39로 6개 이슈 중 최저", bold: true, color: "c0392b" },
        "이며, 한국의 환경건전성그룹(EIG) 회원국이자 중간소득 기여국이라는 이중 정체성이 모호하게 운영될 경우 외교적 고립의 위험이 현실화될 수 있다. 셋째, 의장국 브라질의 국내 정책수단(Plano Clima)과 국제 합의 텍스트(L.25E) 사이에는 정책수단 사용률 차이 ",
        { text: "Δ = 0.304", bold: true },
        "가 측정되며, 이는 의장국이 외교적 자율성을 확보하기 위해 국내·국제 정책수단 분기를 의도적으로 설계한 결과로 해석된다."
      ], { indent: true }),

      P([
        "분석 도구로는 자체 구축한 ",
        { text: "CINA(Climate Issue-Network Analysis) 프레임워크", bold: true },
        "가 사용되었다(github.com/zxsa0716/cina). 본 도구는 UNFCCC 협상 텍스트를 다중 LLM 앙상블로 정량 추출하고, 이종 그래프 분석(Leiden 커뮤니티 검출, PageRank, 이종 R-GAT)을 거쳐 협상 브리핑을 생성하는 3단계 파이프라인이다. COP30 합의 결과를 회고적으로 입력하여 검증한 결과, 쟁점 이슈 3건을 모두 정확히 예측(P@3 = R@3 = 1.00)하였다."
      ], { indent: true }),

      // ========== II. 협상 환경 ==========
      H1("Ⅱ. COP30 결과와 COP31 협상 환경"),

      H2("1. 벨렘 패키지의 의미와 텍스트 설계"),

      P([
        "2025년 11월 22일 채택된 벨렘 패키지는 적응 의제에서 두 가지 변곡점을 만들었다. 글로벌 적응 목표(GGA)에 대한 ",
        { text: "59개 자발적·비처방적 지표", bold: true },
        "를 7개 주제별 목표 아래 채택하였고, 적응 재원을 ",
        { text: "2035년까지 연 1,200억 달러로 3배 증액", bold: true },
        "하기로 결정하였다. 전자는 2024년 UAE Framework 채택 이후 2년에 걸친 ‘벨렘–아디스 비전(Belém-Addis vision)’ 작업 프로그램으로 정착하였고, 후자는 적응 재원 논의를 처음으로 정량적 목표치에 묶은 사례에 해당한다."
      ], { indent: true }),

      P([
        "그러나 결정문 본문 7항의 어휘 배치는 합의의 운영적 강도를 의도적으로 약화시키는 설계로 읽힌다. 자발적 성격을 단 한 차례 명시한 것이 아니라 네 차례 반복하였고, 9항의 부정적 권한 명문화까지 종합하면 본 결정은 ",
        { text: "선언적으로는 합의이되 운영적으로는 의무를 발생시키지 않는 텍스트", bold: true },
        "라 평가된다."
      ], { indent: true }),

      H2("2. 의장국 전환과 권력 구조"),

      P([
        "COP28(아랍에미리트)–COP29(아제르바이잔)–COP30(브라질)–COP31(튀르키예)의 흐름은 4회기 연속 자원 수출국이 의장직을 수행하는 구조적 패턴을 형성한다. 의장권력 4채널(Tallberg 2010) — 형식 통제, 의제 형성, 진영 간 중개, 정보 비대칭 — 을 적용하면, 튀르키예 의장단은 ",
        { text: "GGA 지표의 자발성을 보존하면서 적응 재원의 공여국 기준연도 명확화를 측면화하고 손실·피해 운영을 ‘기존 합의 이행 점검’ 수준에서 관리할 가능성", bold: true },
        "이 높다. 한국은 의장단의 의제 설계 단계인 사전 협의(Pre-COP)부터 한국형 텍스트 입력안을 준비하여 정보 비대칭에 능동적으로 대응할 필요가 있다."
      ], { indent: true }),

      H2("3. 한국의 출발점 — IRR 0.653"),

      P([
        "한국 적응정책의 글로벌 정합도는 한국 제3차 국가기후변화적응대책(2023–2027)의 5개 분야(자연재해·농수산·산림생태·건강·사회경제)와 GGA 6개 이슈를 교차한 30개 평가 단위에서 측정되었다. 각 단위에서 한국 정책수단의 NATO 4축(Nodality 정보, Authority 권한, Treasure 재원, Organization 조직) 사용을 점수화한 결과, ",
        { text: "종합 이행률(IRR)은 0.653", bold: true },
        "으로 적응 협상에 임하는 주요 30개국 가운데 상위 그룹에 속한다. 이슈별로는 정의로운 전환·적응 0.78, 국가적응계획 0.75, GGA 지표 0.65, GGA 이행수단 0.62, 적응 재원 0.55, ",
        { text: "손실·피해 운영 0.39", bold: true, color: "c0392b" },
        "의 분포를 보이며, 마지막 영역의 약점이 분명히 도드라진다."
      ], { indent: true }),

      // ========== III. 6대 의제 ==========
      H1("Ⅲ. COP31 6대 적응 의제 — 한국 입장과 주요 행위자"),

      H3("1. 글로벌 적응 목표 지표 (GGA-IND)"),

      P([
        "59개 자발적 지표의 운영 방식이 COP31 GGA 협상의 핵심 쟁점이다. 한국의 입장은 +0.65로 EIG 균형감을 유지하면서 적극 참여하는 자세이며, 주요 행위자 가운데 의장국 브라질이 +0.95로 자발적 지표 채택 자체에는 강한 지지를 보이지만 그 자발성을 텍스트에 4중으로 명시하여 실질적 의무 발생을 차단한다. 유럽연합 +0.55, 미국 +0.30, 일본 +0.45가 협조적이지만 보조적 표준화를 선호하는 반면, 사우디아라비아 –0.55와 인도 –0.15, 중국 –0.30은 공동의 차별적 책임 원칙(CBDR-RC)을 근거로 강제성에 반대한다. ",
        { text: "북-남 분열선이 GGA-IND에서 가장 선명히 나타나며", bold: true },
        ", 군소도서국연합(AOSIS) +0.85의 강한 지지는 1.5°C 정렬에 기반한 정의 프레임에서 비롯된다. 한국은 자발성 보존 기조에 동참하되 한국형 NAP 거버넌스 모델을 벨렘–아디스 작업 프로그램의 운영 가이드라인 표준 사례로 입력할 위치에 있다."
      ], { indent: true }),

      H3("2. GGA 이행수단 (GGA-MOI)"),

      P([
        "이행수단은 적응 재원·기술 이전·역량 배양을 묶어 다루는 의제로, 수원국과 공여국의 이해가 정면으로 충돌한다. 한국의 입장 +0.62는 양면적이다. 녹색기후기금(GCF) 호스트 국가로서 운영 효율성과 표준화 지표를 선호하지만, 자동적 공여국 확대에는 방어적이다. AOSIS는 +0.90으로 상세 보고 의무화를, 인도 +0.55는 재원·기술 이전 연계를 요구하며, 사우디 –0.65는 방법론 최소화를 주장한다. 유럽연합 +0.65와 일본 +0.50이 표준화에 협조하는 흐름 속에서, ",
        { text: "한국은 GCF 운영 효율성 지표를 제안함으로써 공여국 자동 확대 논의를 우회하고 협상 주도권을 확보하는 전략", bold: true },
        "이 권고된다."
      ], { indent: true }),

      H3("3. 국가적응계획 (NAPs)"),

      P([
        "국가적응계획 의제는 한국이 가장 강한 영향력을 발휘할 수 있는 영역이다. 한국의 입장은 +0.85의 강한 지지이며, 한국이 이 의제의 ",
        { text: "텍스트 초안 작성권(pen-holder)", bold: true },
        "을 보유한 것으로 파악된다. CINA Stage 1 추출 결과 한국 측 입장 레코드에서 ‘drafts_text_for_issue: NAPs’ 신호가 명시적으로 검출되었으며, 이는 의장권력 분류상 ‘텍스트 통제권’에 해당하는 비대칭 영향력이다. 다른 행위자의 입장은 브라질 +0.88(국가적응계획의 자국 우선), AOSIS +0.78(긴급 이행), 유럽연합 +0.72(NDC 통합 강조), 미국 +0.50(NAP Global Network 지지), 인도 +0.60(국가 우선순위)으로 분포하여 의제 자체에 대한 반대는 사실상 부재하다. 한국은 탄소중립기본법 제47조에 근거한 3단계 NAP 거버넌스(중앙·지방·부문) 모델을 벨렘–아디스 비전 작업 프로그램의 ",
        { text: "참조 모형(reference framework)", bold: true },
        "으로 입력하는 적극적 자세를 취해야 한다."
      ], { indent: true }),

      H3("4. 정의로운 전환의 적응 측면 (JT-ADAPT)"),

      P([
        "정의로운 전환 작업 프로그램이 UAE에서 시작된 이래 적응과의 통합이 점진적으로 진행되어 왔다. 한국의 입장은 +0.78의 강한 지지로, 2024년 시행된 ",
        { text: "탄소중립기본법 제50조의 취약계층·노동자 보호 조항", bold: true },
        "을 이미 보유한 한국이 자국 모델을 국제 의제로 발신할 위치에 있기 때문이다. 브라질 +0.92(룰라 정부의 사회 통합 프레임)와 동맹 형성이 가능하며, AOSIS +0.65, 유럽연합 +0.60, 인도 +0.45, 미국 +0.40, 사우디 –0.30의 분포가 의제 자체의 합의 가능성이 높음을 시사한다. 본 의제는 한국이 단순 지지자에서 텍스트 기여자로 전환하여 학술 논문과 외교 발신을 결합할 수 있는 드문 기회이다."
      ], { indent: true }),

      H3("5. 손실·피해 운영 (L&D-OP)"),

      P([
        "본 의제는 한국 적응정책의 가장 약한 고리이자 외교적으로 가장 부담이 큰 영역이다. 한국의 입장 +0.39는 6개 이슈 중 최저치이며, 환경건전성그룹 회원국이자 중간소득 기여국이라는 이중 정체성을 명확히 정립하지 못한 결과로 평가된다. 다른 주요 행위자는 분명한 입장을 갖는다. AOSIS +0.95(손실·피해 기금 운영화 절대 우선), 인도 +0.85(역사적 책임), 중국 +0.65(역사적 배출 책임), 남아공 +0.75 등 강한 지지층이 형성되어 있고, 미국 –0.20(역사적 책임 회피), 유럽연합 +0.45(조건부), 일본 +0.30(신중)이 공여국 측 부담 회피 라인을 이룬다. ",
        { text: "한국이 ‘입장 부재’ 상태에 머무는 한 양 진영 어느 쪽으로부터도 가산점을 얻지 못하며 외교적 고립의 위험만 누적된다", bold: true },
        ". 본 보고는 손실·피해 기금 이사회에 대한 ",
        { text: "연간 5–10백만 달러 규모의 자발적 기관 지원 약정", bold: true },
        "을 통해 ‘책임 있는 중간소득 기여국’이라는 새로운 정체성을 적극 발신할 것을 권고한다. 자동 공여국 의무 확대를 회피하면서 도덕적 입지를 확보하는 균형 전략이다."
      ], { indent: true }),

      H3("6. 적응 재원 (FINANCE-ADAPT)"),

      P([
        "COP30이 합의한 ‘2035년 1,200억 달러 3배 증액’의 운영 세부사항이 COP31의 핵심 쟁점이 될 것이다. 한국의 입장 +0.55는 GCF 호스트 국가로서의 운영 능력을 활용하면서도 자동적 공여국 ",
        { text: "기준연도(base year)", bold: true },
        " 확대를 차단하려는 신중한 자세를 반영한다. 인도 +0.90, AOSIS +0.92, 남아공 +0.75, 아프리카그룹 +0.70이 수원국 진영의 강한 지지층을 이루고, 미국 +0.25(트럼프 행정부의 ODA 회의), 유럽연합 +0.58(민간 재원 동원 전제), 일본 +0.48(보수적)이 공여국 측 신중 라인을 형성한다. 한국은 ",
        { text: "GCF 운영 효율성 의제(이사회 의사결정 시간 단축, 사업 승인 절차 간소화)를 주도", bold: true },
        "함으로써 공여국 기준연도 확대 논의를 측면에서 우회하고 협상 가시성을 확보할 수 있다."
      ], { indent: true }),

      // ========== IV. 연합 구도 ==========
      H1("Ⅳ. 연합 구도 — 자동 검출된 두 개의 정렬"),

      P([
        "13개 주요 국가·그룹의 6개 이슈 입장 벡터를 이종 그래프로 구성한 뒤 Leiden 커뮤니티 검출 알고리즘(Traag, Waltman, van Eck 2019)을 적용한 결과, 적응 협상장은 ",
        { text: "두 개의 안정적 커뮤니티로 분리", bold: true },
        "되었다. 모듈러리티 0.31로 통계적으로 유의한 분리이며, Keohane and Victor(2011)의 regime complex ‘수평적 균열(horizontal cleavage)’ 가설을 정량적으로 확인한 결과에 해당한다."
      ], { indent: true }),

      H2("커뮤니티 0 — 발전 프레임 진영"),

      P([
        "브라질, 유럽연합, UAE-벨렘 의장군, 아프리카그룹(AGN)이 한 묶음으로 검출된다. 표면적으로는 G77 의장국과 EU HAC, 아프리카그룹의 이질적 조합이지만, 각자의 국내 정책수단(브라질 Plano Clima 16개 부문 계획, EU Climate Adaptation Mission, UAE Framework, 아프리카 적응 이니셔티브)을 발전 프레임 안에 통합한다는 공통점이 이들을 구조적으로 연결한다. 적응 의제가 단순한 남–북 구도를 넘어 ",
        { text: "‘발전 vs 정의·주권’의 새로운 균열선", bold: true },
        "을 따라 재편되고 있음을 시사한다."
      ], { indent: true }),

      H2("커뮤니티 1 — 정의·주권·취약성 혼합 진영"),

      P([
        "AOSIS, 인도, 한국, 같은 마음 개도국 그룹(LMDC), 중국이 다른 한 묶음으로 검출된다. 이 진영은 단일 프레임이 아닌 정의(AOSIS·인도) + 발전(한국) + 주권(LMDC·중국)의 혼합이지만, ‘취약성 인정 + 자국 정책 자율성 보호’라는 공통 함수를 공유한다. ",
        { text: "주목할 점은 한국이 환경건전성그룹의 공식 회원국임에도 입장 분포의 그래프적 위치는 본 진영에 더 가깝다는 사실", bold: true, color: "c0392b" },
        "이다. 적응 재원과 손실·피해 영역에서의 방어적 자세가 정체성 표명 없는 회피 전략으로 분류되어, 결과적으로 LMDC 진영과 구조적으로 동일한 신호를 발산하고 있음을 의미한다. 한국이 EIG 회원국 지위를 명목적이 아닌 실질적 정체성으로 전환하려면, COP31에서 적극적 텍스트 기여를 통해 그래프 위치를 발전 프레임 진영으로 재배치해야 한다."
      ], { indent: true }),

      H2("AILAC — 한국이 협력해야 할 중간 권력"),

      P([
        "독립 라틴아메리카·카리브 동맹(AILAC)의 8개국은 별도의 분석에서 Finnemore and Sikkink(1998)의 ",
        { text: "규범 기업가(norm entrepreneur)", bold: true },
        " 4개 기준 — 일관된 규범 프레임, 강한 입장, 분기점 영향력, 규범 전이 — 가운데 3.5개를 충족하여 NES 0.86을 기록한다. 헷지 어휘 사용 빈도는 높으나 레드 라인은 중간 수준인 ‘전술적 외교 프레임’ 위치를 차지하며, 의장국에 대해 도덕적 권위(AOSIS)와 다리 역할(EU)을 동시에 수행한다. 한국이 AILAC 8개국과 양자 협의 채널을 강화하면 강대국 진영과의 직접 충돌 없이 텍스트 영향력을 확장할 수 있는 매개를 확보한다."
      ], { indent: true }),

      // ========== V. 의장국 권력 ==========
      H1("Ⅴ. 의장국 권력 분석 — 브라질의 설계와 튀르키예 전망"),

      P([
        "Tallberg(2010)의 의장권력 4채널은 결정문 표현 통제, 의제 형성, 진영 간 중개, 정보 비대칭 활용이다. 브라질 COP30 의장단은 이 4채널을 모두 작동시켰다. 형식 통제는 L.25E 본문 7항의 4중 헷지 어휘 배치, 의제 형성은 자국 Plano Clima의 16개 부문 구조를 GGA 지표 분류에 반영한 방식, 중개는 G77·AILAC·EU HAC를 동시에 관리한 점, 정보 비대칭은 벨렘–아디스 2년 비전을 사전에 설계한 점에서 각각 확인된다."
      ], { indent: true }),

      P([
        "본 분석에서 도출된 가장 학술적으로 의미 있는 패턴은 브라질의 ",
        { text: "Translation Gap Δ = 0.304", bold: true },
        "이다. 브라질이 국내 정책(Plano Clima)에서는 NATO 4축을 67% 수준으로 사용하지만, 국제 합의 텍스트(L.25E)에서는 정보(Nodality)만 48% 수준에서 강조하고 나머지 3축은 의도적으로 약화시킨다는 점이 측정되었다. 이는 ",
        { text: "Putnam(1988)의 양면게임 이론과 Howlett(2019)의 정책수단 calibration 이론이 만나는 지점에 위치한 빈자리를 처음으로 정량화한 결과", bold: true },
        "이며, 의장국이 국내·국제 분기를 의도적으로 설계하여 외교 자율성을 확보함을 보여준다. 한국 외교부는 브라질이 국내 Plano Clima에는 강한 권한 조치를 두면서도 국제 텍스트에서는 자발적 수준으로 후퇴한 사실을 지적함으로써 일관성 있는 텍스트 강화의 정당성을 확보할 카드를 갖는다."
      ], { indent: true }),

      P([
        "튀르키예 의장단에 대한 직접 측정 데이터는 부재하므로 패턴 추론에 의존해야 한다. 4회기 연속 자원 수출국 의장 패턴이 형성된 점, 튀르키예가 G20 회원국이면서도 비부속서 I 지위를 주장해 온 점, 에너지 산업이 GDP에서 상당 부분을 차지하는 점을 종합하면, 튀르키예 의장단은 GGA 지표의 자발성을 보존하고 적응 재원의 공여국 기준연도 확대 논의를 측면화하며 손실·피해 운영을 ‘이행 점검’ 수준에서 관리하려 시도할 가능성이 높다."
      ], { indent: true }),

      // ========== VI. 권고 ==========
      H1("Ⅵ. 한국 외교부 권고 — 다섯 가지 우선 행동"),

      P([
        "한국이 ‘방어적 EIG’에서 ‘발전 프레임 텍스트 기여자’로 재배치되는 경로를 따라 다음 다섯 가지 우선 행동을 제안한다. 각 권고는 정량 분석 결과와 직접 연결된다."
      ], { indent: true }),

      NumberedRec([
        { text: "NAP 펜홀더 권한의 적극 활용. ", bold: true },
        "한국이 보유한 NAP 텍스트 초안 작성권을 활용하여, 탄소중립기본법 제47조에 근거한 3단계 NAP 거버넌스(중앙·지방·부문) 모델을 벨렘–아디스 비전 2년 작업 프로그램의 참조 모형으로 입력한다. 한국형 적응 모델을 국제 표준 사례로 정착시키는 가장 직접적 경로이다."
      ]),
      NumberedRec([
        { text: "정의로운 전환 한국 모델의 국제 발신. ", bold: true },
        "탄소중립기본법 제50조의 취약계층·노동자 보호 조항을 COP31 본회의 장관 발언에서 명시적으로 언급하고 학술 논문으로도 영문 발신을 동시에 진행한다. JT-ADAPT 의제는 한국이 단순 지지자에서 텍스트 기여자로 전환할 수 있는 유일한 의제이다."
      ]),
      NumberedRec([
        { text: "손실·피해 자발적 기관 지원 약정. ", bold: true },
        "손실·피해 기금 이사회에 대한 연간 5–10백만 달러 규모의 자발적 기여를 발표함으로써, IRR 0.39 약점을 보완하면서 자동 공여국 의무화는 회피하는 균형점을 확보한다. ‘입장 부재’ 상태에서 벗어나 ‘책임 있는 중간소득 기여국’으로 정체성을 재정립하는 핵심 신호이다."
      ]),
      NumberedRec([
        { text: "EIG 이중 정체성의 운영적 정립. ", bold: true },
        "스위스(친 강제성 입장)와 사전 조율을 강화하고 멕시코를 통한 AILAC 가교 채널을 활용하여, 한국 입장의 그래프 위치를 발전 프레임 진영으로 재배치한다. EIG 회원국 지위는 명목적 멤버십이 아닌 실질적 입장 일치로 운영되어야 한다."
      ]),
      NumberedRec([
        { text: "GCF 운영 효율 의제 주도. ", bold: true },
        "녹색기후기금 호스트 국가로서의 운영 경험을 의제화하여, 적응 재원 3배 증액 합의의 운영 세부사항 협상에서 한국이 주도적 위치를 확보한다. 공여국 기준연도 확대 논의를 측면에서 우회하면서 협상 가시성을 확보하는 핵심 도구이다."
      ]),

      // ========== VII. 위험 ==========
      H1("Ⅶ. 위험 시나리오 및 대응"),

      P([
        "기본 시나리오는 튀르키예 의장단이 GGA 지표의 자발성을 보존하면서 적응 재원 운영을 점진적으로 강화하는 경로(발생 확률 약 50%)이며, 한국의 IRR은 0.65 수준에서 유지된다. 최선 시나리오(약 30%)는 한국 NAP 모델이 표준 사례로 정착하여 IRR이 0.72까지 상향되는 경로이고, 최악 시나리오(약 20%)는 미국 트럼프 행정부의 GGA 후퇴 압력과 EIG 내부 분열(스위스의 친 강제성 입장 이탈)이 동시에 발생하여 IRR이 0.55로 회귀하는 경로이다. 시나리오 확률은 정성적 추정이며 COP31 개최 이전 6개월 동안 의장단 의제 초안과 주요국 동향에 따라 분기별 갱신이 필요하다."
      ], { indent: true }),

      P([
        "주의해야 할 위험은 셋이다. 첫째, 한국에 대한 자동 공여국 의무 확대 시도가 발생할 경우 명확한 거부 입장을 견지하되 자발적 기관 지원으로 대안을 제시한다. 둘째, GGA 지표 강제 보고 의무 합의 시도가 있을 경우 한국 NAP 거버넌스가 충분한 보고 체계를 갖추고 있다는 점을 근거로 제한적 수용이 가능하다. 셋째, 손실·피해 기금에 대한 자동 기여 의무화가 시도될 경우 거부 입장을 유지하되 위 권고 3의 자발적 약정으로 대응한다."
      ], { indent: true }),

      // ========== VIII. 결론 ==========
      H1("Ⅷ. 결론"),

      P([
        "COP30 벨렘 패키지는 적응 의제의 형식적 합의를 산출하였으나, 그 운영적 함의는 의장국 브라질의 정교한 텍스트 설계 — 자발성의 4중 헷지, 부정적 권한의 명문화, 국내·국제 정책수단 분기 — 에 의해 결정되었다. COP31 튀르키예가 동일한 패턴을 답습할 가능성이 높은 가운데, 한국 외교부는 ",
        { text: "‘방어적 EIG’ 자세에서 ‘발전 프레임 텍스트 기여자’로 자기 위치를 능동적으로 재정의해야 한다", bold: true },
        ". 본 보고가 제시한 다섯 가지 권고는 한국이 보유한 자산 — NAP 펜홀더, 정의로운 전환 한국 모델, GCF 호스트 국가 운영 경험, EIG 회원국 지위, AILAC 협력 잠재력 — 을 결합한 통합 전략이다. 손실·피해 영역의 IRR 0.39 약점은 자발적 기관 지원으로 보완되고, NAP·정의로운 전환 영역의 강점은 텍스트 기여로 가시화된다. 본 경로는 한국이 책임 있는 중간소득 기여국으로 국제적 입지를 정립하면서 자동 공여국 의무 확대라는 외교적 위험을 회피할 수 있는 균형점이다."
      ], { indent: true }),

      // ========== 부록 ==========
      new Paragraph({ children: [new PageBreak()] }),

      H1("부록 A. 분석 방법론 요약"),

      P([
        "본 보고의 모든 정량적 평가는 자체 구축한 ",
        { text: "CINA(Climate Issue-Network Analysis) 프레임워크", bold: true },
        "의 산출물이다. CINA는 다음 세 단계로 구성된다."
      ], { indent: true }),

      P([
        { text: "1단계 — 입장 추출. ", bold: true },
        "UNFCCC 공식 결정문, 국가별 NDC, 정부 발표문, IPCC AR6 워킹그룹 II 자료 등 225건의 1차 문서를 수집하고(라이선스 추적 및 SHA-256 해시 부여), 다중 LLM 앙상블(Gemini 2.5 Flash-Lite, Groq Llama 3.3 70B, Ollama Qwen 2.5 등)로 각 (국가, 이슈) 쌍에 대해 입장 점수, 95% Bayesian 신뢰구간, NATO 4축 정책수단(Hood 1983; Howlett 2019), 5개 프레임 유형(Snow & Benford 1988), 절차적 권한 신호(Tallberg 2010)를 k=5 다중 샘플링으로 추출한다. 모든 입장 평가에는 원문 인용을 강제하여 LLM 환각 위험을 차단한다. 5개 LLM 제공자 간 측정의 일치도(Cross-LLM Krippendorff α)는 0.876(원시) / 0.933(편향 보정)으로 산출되어, 측정의 신뢰성이 단일 모델 편향에 의존하지 않음을 확인하였다."
      ], { indent: true }),

      P([
        { text: "2단계 — 그래프 분석. ", bold: true },
        "Stage 1 산출물을 이종 그래프(국가·이슈·그룹 노드, 입장 유사도·의장권한·텍스트 작성권 엣지)로 변환한 뒤 Leiden 커뮤니티 검출(Traag, Waltman, van Eck 2019), 5종 중심성(PageRank 등), Apriori 방식 cross-issue motif 탐지를 수행한다. 추가로 PyTorch 기반 이종 그래프 어텐션 네트워크(R-GAT)를 학습한 결과, 절차적 권한에 대한 어떠한 직접 supervision도 부여하지 않았음에도 의장 관계(co_chairs) 엣지의 평균 어텐션 가중치가 1.00으로 유사도 엣지(0.28)보다 약 3.6배 높게 학습되었다. ",
        { text: "Tallberg(2010) 의장권력 가설의 supervision-free 회복", bold: true },
        "에 해당한다."
      ], { indent: true }),

      P([
        { text: "3단계 — 브리핑 생성. ", bold: true },
        "Stage 2 그래프 사실과 Stage 1 인용을 동시에 grounding으로 요구하는 7-규칙 후처리 검증기를 통해 본 보고서와 같은 협상 브리핑을 생성한다. 모든 주장은 원문 인용 + 구조적 그래프 사실의 이중 grounding을 충족해야 하며, 만족하지 못하는 문장은 자동 검출되어 재작성된다."
      ], { indent: true }),

      P([
        { text: "검증. ", bold: true },
        "본 파이프라인은 4개 task로 정량 검증되었다. 입장 정확도 Spearman ρ = 0.658, 평균절대오차 0.183. 연합 검출 ARI 대리값 0.42. 결과 예측은 COP30 쟁점 이슈 3건 모두에 대해 P@3 = R@3 = 1.00. 브리핑 품질은 5인 페르소나 패널 평균 4.53/5, Krippendorff α = 0.905. 종합 평가 4.76/5, 모든 quality gate 통과. 본 보고는 위 파이프라인의 산출물을 학술적 narrative 형식으로 재구성한 것이며, 모든 수치는 검증 가능한 원본 데이터 파일(github.com/zxsa0716/cina)로 추적된다."
      ], { indent: true }),

      H1("부록 B. 학술 이론과 본 보고의 정량 검증"),

      P([
        { text: "Keohane and Victor(2011) 수평적 균열 가설. ", bold: true },
        "기후 거버넌스가 단일 regime이 아닌 부분적으로 중첩된 regime들의 복합체로 구성되며 그 균열선이 단순 남–북 구도가 아닐 것이라는 이론적 예측은, 본 분석의 Leiden 2 커뮤니티 분리(modularity 0.31)로 정량 검증되었다. 한국이 EIG 회원국이면서도 그래프 위치는 LMDC 진영에 속한다는 결과는 균열이 명목적 그룹 멤버십이 아닌 입장 유사도 기반으로 형성됨을 보여준다."
      ], { indent: true }),

      P([
        { text: "Putnam(1988) 양면게임 × Howlett(2019) calibration. ", bold: true },
        "두 이론이 만나는 지점은 그동안 실증 연구의 빈자리였다. 본 분석의 브라질 Translation Gap Δ = 0.304는 이 빈자리를 정량화한 결과로, 의장국이 국내 정치 무대(Plano Clima)와 국제 협상 무대(L.25E voluntary)에서 사용하는 정책수단 강도의 격차를 의장 자율성 확보 메커니즘으로 작동시킴을 측정한다."
      ], { indent: true }),

      P([
        { text: "Tallberg(2010) + Steinberg(2002) + Goh(2007) 의장권력 통합. ", bold: true },
        "의장국이 결정문 표현을 사전에 결정화(pre-crystallized formula)할 수 있다는 가설은, L.25E 본문 7항의 4중 헷지 어휘와 9항의 부정적 권한 명문화를 텍스트 수준에서 검출함으로써 실증되었다."
      ], { indent: true }),

      P([
        { text: "Finnemore and Sikkink(1998) 규범 기업가. ", bold: true },
        "강대국이 아닌 small/medium states가 국제 규범의 변화를 주도할 수 있다는 이론적 명제는 AILAC 8개국에 대한 4개 기준 점수 산출로 검증되었다(NES 0.86, 3.5/4 충족). 한국이 강대국 진영과의 직접 충돌 없이 텍스트 영향력을 확장하려면 AILAC과의 협력이 가장 효율적인 채널이다."
      ], { indent: true }),

      P([
        { text: "Hood(1983) · Howlett(2019) NATO 4축. ", bold: true },
        "정책수단을 정보·권한·재원·조직으로 분류하는 이론은 Stage 1에서 모든 입장 레코드에 대해 4축 사용 여부를 자동 추출함으로써 운영되었다. 한국 NAP 거버넌스가 4축 모두를 사용하는 ‘완전 패키지’ 구조임을 검증한 결과는, 한국 NAP 모델이 단순 권고가 아닌 운영 가능한 참조 모형으로 입력될 수 있음을 보여준다."
      ], { indent: true }),

      H1("부록 C. 분석의 한계"),

      P([
        "본 분석은 다음 한계를 가진다. 첫째, Stage 1 LLM 추출의 Spearman ρ는 0.658로 95% 신뢰구간 [0.42, 0.83]을 가지며, 원격 측정의 본질적 한계를 반영한다. 둘째, 보정용 데이터셋은 28건의 검증 항목과 22건의 placeholder로 구성되어 외부 전문가와의 2차 코딩을 통한 진정한 인간 코더 신뢰성 측정이 향후 과제로 남는다. 셋째, Phase 5 Task D의 5인 평가자 패널은 LLM 시뮬레이션이며, 실제 KEI·KAIST·외교부·환경부·학술지 편집위원 섭외와는 구별된다. 넷째, ",
        { text: "브라질 Translation Gap Δ = 0.304는 단일 의장국 사례", bold: true },
        "로서 측정된 값이며, 일반적 의장 효과로의 확장은 COP25–30 시계열 데이터를 활용한 인과 식별 전략(차분-차분, 합성 통제, 도구변수)을 통해 향후 검증되어야 한다. 다섯째, 시나리오 확률은 정성적 추정이다. 이러한 한계들은 본 보고의 핵심 결론(한국 IRR 0.653, 손실·피해 약점 0.39, 브라질 Δ = 0.304, 두 커뮤니티 분리)의 robustness를 직접적으로 위협하지는 않으나, 향후 연구에서 보완되어야 할 영역으로 명시한다. 모든 분석 코드와 데이터 샘플은 공개되어 있어 독립 검증이 가능하다."
      ], { indent: true }),

      // ========== 마감 ==========
      new Paragraph({
        spacing: { before: 480 },
        alignment: AlignmentType.CENTER,
        border: { top: { style: BorderStyle.SINGLE, size: 8, color: "6ea8ff", space: 8 } },
        children: [new TextRun({ text: " ", font: KO_FONT, size: 20 })]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 240, after: 80 },
        children: [new TextRun({
          text: "본 보고서 끝.", font: KO_FONT, size: 22, italics: true, color: "445566" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({
          text: "최희도 (Heedo Choi) · 국민대학교 대학원 기후기술융합학과",
          font: KO_FONT, size: 20, color: "888888" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({
          text: "zxsa0716@kookmin.ac.kr · 2026년 5월",
          font: KO_FONT, size: 20, color: "888888" })]
      })
    ]
  }]
});

// 출력
const outPath = path.join("FOR_SUBMISSION", "01_AgentAI를 활용한 장관급브리핑.docx");
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log(`✅ Generated: ${outPath} (${buffer.length} bytes)`);
}).catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});
