---
theme: default
title: "CUBRID Python Ecosystem — From Contributors to Maintainers"
info: "2026 OSS Developer Contest Finals"
author: "CUBRID Lab — Yeongseon Choe & Gyeongjun Paik"
drawings:
  persist: false
transition: fade
# Finals run offline: no Google Fonts / CDN favicon (Pretendard is bundled in public/fonts)
fonts:
  provider: none
favicon: /favicon.svg
# Hash routes (/#/5) survive a refresh on any static server, no SPA fallback needed
routerMode: hash
# 840 instead of 980: same 16:9 slide, everything ~17% larger on screen
canvasWidth: 840
layout: default
class: navy
---

<div class="eyebrow">2026 OSS 개발자대회 본선 <span class="crit">CUBRID Lab</span></div>

<div class="cover">
  <h1>2020년,<br>두 사람이 만났다</h1>
  <p class="lede">멘토 최영선 × 멘티 백경준 — 오픈소스 컨트리뷰톤 CNBT-41</p>

  <div class="facts">
    <div><span class="muted">배운 것</span><b>SQLAlchemy</b></div>
    <div><span class="muted">만난 사람</span><b>Mike Bayer <small>창시자 · Gitter</small></b></div>
    <div><span class="muted">만든 커뮤니티</span><b>SQLAlchemy Korea</b></div>
  </div>

  <p class="then"><span class="accent">6년 후,</span> 하나의 생태계를 들고 돌아왔다</p>
</div>

<style>
.cover { display: grid; gap: 18px; margin-top: 26px; }
.cover h1 { font-size: 3.1rem; line-height: 1.12; }
.facts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: #22385a; border: 1px solid #22385a; border-radius: 10px; overflow: hidden; margin-top: 8px; }
.facts > div { background: var(--navy); padding: 12px 16px; display: grid; gap: 4px; }
.facts span { font-size: 0.7rem; font-weight: 600; }
.facts b { font-size: 1.05rem; font-weight: 700; }
.facts small { font-size: 0.72rem; font-weight: 500; color: var(--on-navy-muted); }
.then { font-size: 1.45rem; font-weight: 700; margin-top: 10px; letter-spacing: -0.02em; }
</style>

<!--
2020년, NIPA가 운영하는 오픈소스 컨트리뷰톤에서 두 사람이 만났습니다.
멘토와 멘티로요. 저희입니다.
그때 SQLAlchemy를 배웠고, Gitter에서 창시자 Mike Bayer님과 대화하면서
한국 커뮤니티도 만들었습니다. 6년 후, 하나의 생태계를 들고 왔습니다.
-->

---

<div class="eyebrow">The Gap <span class="crit">활용성</span></div>

<div class="gap">
  <div class="share">
    <span class="num">13.24<small>%</small></span>
    <p class="big">한국 공공부문 DBMS 점유율 <b>2위</b></p>
    <p class="muted">2,367개 설치 · Oracle 다음 · 2025년 말</p>
    <p class="src">행정안전부·NIA 「2026년도 범정부EA기반 공공부문 정보자원 현황 통계보고서」</p>
  </div>

  <div class="dead">
    <h2>그런데 Python은<br><span class="seal">죽어 있었다</span></h2>
    <div class="row"><span class="d seal">2012</span><div><b>zzzeek/sqlalchemy_cubrid</b><p class="muted">Mike Bayer가 만든 방언 — 이후 방치</p></div></div>
    <div class="row"><span class="d seal">2014-05-15</span><div><b>공식 Python 드라이버</b><p class="muted">마지막 릴리스 — asyncio · SQLAlchemy 2.x 미지원</p></div></div>
    <p class="quote">"방언을 살리려니 — 드라이버부터 새로 만들어야 했다."</p>
  </div>
</div>

<EvidenceFooter claim="cubrid-public-sector, official-driver-2014" />

<style>
.gap { display: grid; grid-template-columns: 1fr 1.15fr; gap: 44px; margin-top: 18px; align-items: start; }
.share { display: grid; gap: 8px; padding-top: 6px; }
.share .num { font-size: 6.2rem; color: var(--blue); }
.share .num small { font-size: 0.45em; margin-left: 4px; letter-spacing: 0; }
.share .big { font-size: 1.25rem; font-weight: 650; }
.share .src { margin-top: 10px; max-width: 30ch; }
.dead { display: grid; gap: 14px; }
.dead h2 { font-size: 2rem; line-height: 1.2; margin-bottom: 4px; }
.row { display: grid; grid-template-columns: 104px 1fr; gap: 14px; align-items: baseline; border-top: 1px solid var(--line); padding-top: 12px; }
.row .d { font-weight: 800; font-size: 0.95rem; font-variant-numeric: tabular-nums; }
.row b { font-size: 0.95rem; }
.row p { font-size: 0.8rem; margin-top: 2px; }
.quote { font-size: 1rem; font-weight: 650; border-left: 3px solid var(--seal); padding-left: 12px; margin-top: 6px; }
</style>

---

<div class="eyebrow">What We Built <span class="crit">PT</span></div>

## 각 단계가 다음 단계를 낳았다

<p class="lede">방언을 살리려다 드라이버를, 드라이버를 알리려다 예제를, 그리고 AI가 쓰는 길까지.</p>

<div class="timeline mid">
  <div class="tl"><span class="dot">1</span><span class="yr">2021–22</span><span class="name">sqlalchemy-cubrid</span><span class="what">SQLAlchemy 2.0 ORM 방언<br>공식 테스트 스위트 통합</span></div>
  <div class="tl"><span class="dot">2</span><span class="yr">2025</span><span class="name">pycubrid</span><span class="what">순수 Python 드라이버<br>CAS 프로토콜 구현 · 의존성 0</span></div>
  <div class="tl"><span class="dot">3</span><span class="yr">2026</span><span class="name">cubrid-cookbook</span><span class="what">68 예제 + 7 템플릿<br>매일 밤 실서버 검증</span></div>
  <div class="tl now"><span class="dot">4</span><span class="yr">2026</span><span class="name">cubrid-mcp-server</span><span class="what">세계 최초 CUBRID MCP<br>AI/LLM이 CUBRID에 접근</span></div>
</div>

<EvidenceFooter claim="mcp-world-first" />

---

<div class="eyebrow">Developer Experience <span class="crit">활용성 15점</span></div>

## `pip install` 한 줄, 5분이면 시작

<div class="dx mid">
<div>

```bash
pip install pycubrid      # C 컴파일러 불필요
```

```python
import pycubrid

conn = pycubrid.connect(host="localhost", port=33000,
                        database="demodb", user="dba")
cur = conn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())     # (1,)
```

</div>
<div class="side">
  <p class="h">7개 프로덕션 템플릿 <span class="muted">— 복사해서 바로 수정</span></p>
  <div class="chips">
    <span class="chip on">FastAPI · REST + Docker</span>
    <span class="chip on">Django · ORM + Admin</span>
    <span class="chip on">Streamlit 대시보드</span>
    <span class="chip on">AI 에이전트 · MCP</span>
    <span class="chip">Celery 워커</span>
    <span class="chip">Pandas ETL</span>
    <span class="chip">Flask 웹앱</span>
  </div>
  <div class="docs">
    <div><span class="num">4</span><span class="muted">문서 사이트</span></div>
    <div><span class="num">34</span><span class="muted">한국어 페이지</span></div>
  </div>
  <p class="muted small">모든 README에 데모 GIF · GETTING_STARTED.md</p>
</div>
</div>

<style>
.dx { display: grid; grid-template-columns: 1.25fr 1fr; gap: 28px; margin-top: 18px; align-items: start; }
.dx .side { display: grid; gap: 12px; }
.dx .h { font-size: 0.95rem; font-weight: 700; }
.docs { display: flex; gap: 28px; margin-top: 6px; }
.docs div { display: grid; gap: 2px; }
.docs .num { font-size: 2.2rem; color: var(--blue); }
.docs .muted { font-size: 0.75rem; }
.small { font-size: 0.72rem; }
</style>

<!--
개발자가 이 생태계를 시작하는 데 5분이면 됩니다.
pip install 한 줄, C 컴파일러도 필요 없습니다.
7개 프로덕션 템플릿이 있어서 복사해서 바로 수정하면 됩니다.
FastAPI, Django, Streamlit 대시보드, 심지어 AI 에이전트 템플릿까지.
문서는 4개 사이트에 한국어 34페이지, 데모 GIF도 모든 README에 있습니다.
-->

---

<div class="eyebrow">Code Quality <span class="crit">기능테스트 10점</span></div>

<div class="qa">
  <div class="lead">
    <span class="num">2,200</span>
    <p class="big">개의 테스트</p>
    <p class="muted">AI가 작성한 코드도<br>이 게이트를 모두 통과해야 머지됩니다.</p>
    <p class="quote">품질은 목표가 아니라<br>전제 조건입니다.</p>
  </div>
  <div class="gates">
    <div class="stat"><span class="k">mypy --strict</span><span class="v">타입 오류 0 · CI 강제</span></div>
    <div class="stat"><span class="k">Coverage ≥ 95%</span><span class="v">미달 시 머지 불가</span></div>
    <div class="stat"><span class="k">hypothesis</span><span class="v">랜덤 입력으로 엣지 케이스 탐색</span></div>
    <div class="stat"><span class="k">api-baseline.json</span><span class="v">공개 API 변경 감지</span></div>
    <div class="stat"><span class="k">Golden tests · 45</span><span class="v">매일 밤 CUBRID 11.2 + 11.4 실서버</span></div>
    <div class="stat"><span class="k">SQLAlchemy 공식 스위트 · 720</span><span class="v">방언 호환성 검증</span></div>
    <div class="stat"><span class="k">CodeQL</span><span class="v">모든 PR 보안 스캔</span></div>
    <div class="stat"><span class="k">ruff check + format</span><span class="v">린트 · 포맷 게이트</span></div>
  </div>
</div>

<style>
.qa { display: grid; grid-template-columns: 0.8fr 1.4fr; gap: 36px; margin-top: 14px; align-items: start; }
.qa .lead { display: grid; gap: 8px; }
.qa .lead .num { font-size: 5.4rem; color: var(--blue); }
.qa .big { font-size: 1.3rem; font-weight: 700; margin-top: -4px; }
.qa .muted { font-size: 0.88rem; line-height: 1.5; }
.qa .quote { font-size: 1.05rem; font-weight: 700; border-left: 3px solid var(--blue); padding-left: 12px; margin-top: 10px; line-height: 1.4; }
.gates { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.gates .stat { padding: 11px 14px; gap: 3px; }
</style>

<!--
2,200개 테스트는 우연이 아닙니다. 품질 게이트 시스템이 있습니다.
mypy strict 모드로 타입 오류 0개를 CI에서 강제합니다.
커버리지 95% 이상이 아니면 머지가 안 됩니다.
hypothesis로 랜덤 입력 테스트를 돌리고,
api-baseline.json으로 공개 API가 의도치 않게 바뀌는 것을 감지합니다.
45개 골든 테스트는 매일 밤 실서버 CUBRID에서 실행됩니다.
AI가 작성한 코드가 이 모든 게이트를 통과해야 머지됩니다.
-->

---

<div class="eyebrow">Performance <span class="crit">기능테스트</span></div>

## 사용자가 알려주지 않으니, 직접 측정한다

<p class="lede">니치 시장에는 성능 리포트를 보내줄 사용자가 없습니다. 벤치마크 저장소를 따로 만들고, 프로파일링으로 병목을 찾았습니다.</p>

<div class="perf mid"><SnapshotMetrics category="performance" /></div>

<p class="repro">재현: <b>github.com/cubrid-lab/cubrid-benchmark</b></p>

<style>
.perf { margin-top: 30px; }
.perf .stat .num { font-size: 2.6rem; }
.repro { font-size: 0.8rem; margin-top: 18px; color: var(--muted); }
.repro b { color: var(--ink); font-family: var(--mono); font-weight: 600; }
</style>

---

<div class="eyebrow">Standards & Open Source <span class="crit">OSS 적절성 15점</span></div>

## 폐쇄형 데모가 아니라, 개방형 표준 위의 인프라

<div class="std mid">
  <div class="stat"><span class="k accent">PEP 249 · DB-API 2.0</span><span class="t">pycubrid 완전 준수</span><span class="v">1,147 테스트</span></div>
  <div class="stat"><span class="k accent">PEP 561 · 타입</span><span class="t">py.typed · mypy strict 0</span><span class="v">CI 강제</span></div>
  <div class="stat"><span class="k accent">SQLAlchemy Dialect API</span><span class="t">공식 테스트 스위트 통합</span><span class="v">53 feature flags</span></div>
  <div class="stat"><span class="k accent">Model Context Protocol</span><span class="t">Tools · Resources · Prompts</span><span class="v">세계 최초 CUBRID MCP</span></div>
</div>

<p class="stackh">기반 오픈소스</p>
<div class="chips">
  <span class="chip">SQLAlchemy · MIT</span>
  <span class="chip">zzzeek/sqlalchemy_cubrid · MIT</span>
  <span class="chip">node-cubrid · BSD (프로토콜 참고)</span>
  <span class="chip">MCP · MIT</span>
  <span class="chip">pytest · hypothesis</span>
  <span class="chip">CodeQL · Dependabot</span>
</div>

<p class="quote">오픈소스 기여로 배우고, 멈춘 프로젝트에서 영감을 받아, 새 생태계를 만들었다.</p>

<EvidenceFooter claim="pep249-compliance" />

<style>
.std { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 22px; }
.std .t { font-size: 0.95rem; font-weight: 700; line-height: 1.35; }
.std .k { font-size: 0.7rem; letter-spacing: 0.02em; }
.stackh { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin: 26px 0 8px; }
.quote { font-size: 1rem; font-weight: 650; border-left: 3px solid var(--blue); padding-left: 12px; margin-top: 24px; }
</style>

---
class: navy
---

<div class="eyebrow">Live Demo <span class="crit">데모 10점 · 2분</span></div>

## 온나라 데이터를 Python과 AI로

<p class="lede">행안부 전자결재(온나라) 시나리오 — CUBRID 위의 공공 업무 데이터, 지금까지는 Java 중심.</p>

<div class="timing"><span>대시보드 15s</span><span class="core">Claude + MCP 90s</span><span>터미널 15s</span></div>

<div class="asks">
  <div class="ask"><span class="n">1</span><span class="q">"이 DB에 어떤 테이블이 있어?"</span><span class="beat">탐색</span></div>
  <div class="ask star"><span class="n">2</span><span class="q">"결재가 지연된 문서 TOP 5는? 평균 처리일과 대기 수로"</span><span class="beat">AI 운영 분석</span></div>
  <div class="ask"><span class="n">3</span><span class="q">"기밀 문서는 부처별로 몇 개야? 내용은 보지 말고 집계만"</span><span class="beat">집계만 질의</span></div>
  <div class="ask reject"><span class="n">4</span><span class="q">"결재 대기 문서를 전부 승인 처리해줘"</span><span class="stamp">반려</span></div>
</div>

<p class="note">MCP 서버는 기본이 읽기 전용 — 쓰기 도구는 노출되지 않고, 쓰기 SQL은 화이트리스트에서 거부됩니다.</p>

<style>
.asks .ask:last-child { padding-block: 4px; }
.note { font-size: 0.78rem; color: var(--on-navy-muted); margin-top: 14px; }
</style>

<!--
온나라 시나리오로 데모하겠습니다. 행안부 온나라는 47개 부처가 쓰는
CUBRID 기반 전자결재 시스템입니다 — 전부 Java로 구축됐습니다.
저희가 이 데이터를 Python과 AI에서 다룰 수 있게 만들었습니다.
문서 처리 현황 대시보드부터 시작합니다.

(#4 차단 후) 결재 대기 문서를 전부 승인하려는 AI 명령이 서버에서 차단됐습니다.
MCP 서버는 기본이 읽기 전용입니다 — 쓰기 도구는 노출조차 되지 않고,
쓰기 SQL은 화이트리스트에서 거부됩니다. 쓰기는 운영자가 연결별로 명시적으로 켤 때만 가능합니다.
-->

---

<div class="eyebrow">How We Work <span class="crit">커뮤니티 5점</span></div>

## AI가 쓰고, 사람이 책임진다

<div class="flow">
  <div class="step human"><span class="who">사람</span><span class="t">AGENTS.md</span><span class="d">규칙 정의</span></div>
  <div class="arrow">→</div>
  <div class="step"><span class="who">AI</span><span class="t">구현</span><span class="d">코드 · 테스트 · 문서</span></div>
  <div class="arrow">→</div>
  <div class="step human"><span class="who">사람</span><span class="t">리뷰</span><span class="d">모든 PR</span></div>
  <div class="arrow">→</div>
  <div class="step"><span class="who">CI</span><span class="t">게이트</span><span class="d">타입 · 커버리지 · 라이브 DB</span></div>
  <div class="arrow">→</div>
  <div class="step human"><span class="who">사람</span><span class="t">릴리스</span><span class="d">태그는 사람만</span></div>
</div>

<div class="work mid">
  <div class="stat hl"><span class="num">450</span><span class="k">Merged PRs</span><span class="v">CI 게이트 통과 후 병합 · 드라이버·방언은 20조합 라이브 DB</span></div>
  <div class="stat"><span class="k">번역 동기화 CI</span><span class="v">한국어 문서가 영어와 어긋나면 실패</span></div>
  <div class="stat"><span class="k">라벨 체계 + 주간 점검</span><span class="v">이슈 분류가 흐트러지지 않게</span></div>
  <div class="stat"><span class="k">SBOM + SPDX</span><span class="v">모든 릴리스에 첨부</span></div>
</div>

<style>
.work { display: grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 12px; margin-top: 22px; }
.work .num { font-size: 2.6rem; }
</style>

---

<div class="eyebrow">Licensing <span class="crit">라이선스 5점</span></div>

<div class="lic mid">
  <div>
    <span class="num">MIT × 4</span>
    <p class="big">GPL 없음</p>
    <p class="muted">4개 패키지 모두 MIT · 의존성 트리에도 GPL 없음</p>
  </div>
  <div class="cards">
    <div class="stat"><span class="k">우리 패키지</span><span class="v">독립 wire-protocol 클라이언트 — CUBRID 서버 코드를 포함하지 않음</span></div>
    <div class="stat"><span class="k">CUBRID 서버</span><span class="v">Apache-2.0 엔진 · BSD 커넥터 — 업스트림 COPYING 직접 확인</span></div>
    <div class="stat"><span class="k">배포물</span><span class="v">THIRD_PARTY_LICENSES · NOTICE · SPDX SBOM</span></div>
  </div>
</div>

<style>
.lic { display: grid; grid-template-columns: 1fr 1.2fr; gap: 44px; margin-top: 40px; align-items: center; }
.lic .num { font-size: 4.6rem; color: var(--blue); }
.lic .big { font-size: 1.6rem; font-weight: 750; margin-top: 10px; }
.lic .muted { font-size: 0.85rem; margin-top: 6px; }
.lic .cards { display: grid; gap: 10px; }
</style>

---

<div class="eyebrow">Ecosystem Vision <span class="crit">커뮤니티 + 발전가능성</span></div>

## Python이 레퍼런스 — 같은 순서로 4개 언어

<p class="lede">드라이버 → ORM → 예제 → AI. 한 번 검증한 순서를 다른 언어에 그대로 적용합니다.</p>

<div class="langs mid">
  <div class="stat hl"><span class="k">Python · 완성</span><span class="t">pycubrid v1.7.1</span><span class="t">sqlalchemy-cubrid v1.7.1</span></div>
  <div class="stat"><span class="k">TypeScript · 진행</span><span class="t">cubrid-client v1.1.0</span><span class="t">drizzle-cubrid v0.2.1</span></div>
  <div class="stat"><span class="k">Go · 진행</span><span class="t">cubrid-go v0.2.1</span><span class="t">gorm-cubrid v0.1.0</span></div>
  <div class="stat"><span class="k">Rust · 진행</span><span class="t">cubrid-rs v0.1.0</span><span class="t">sea-orm-cubrid v0.1.0</span></div>
</div>

<div class="sus">
  <p><b>커뮤니티</b> <span class="muted">SQLAlchemy Korea 운영 경험 (2020~)</span></p>
  <p><b>지속가능성</b> <span class="muted">MIT · 문서화된 거버넌스 · AI/MCP로 다음 세대 개발자와 연결</span></p>
</div>

<style>
.langs { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 26px; }
.langs .t { font-family: var(--mono); font-size: 0.78rem; font-weight: 600; }
.langs .stat.hl .t { color: #fff; }
.sus { display: grid; gap: 8px; margin-top: 26px; font-size: 0.9rem; }
.sus b { display: inline-block; min-width: 88px; }
</style>

---

<div class="eyebrow">Judge Verification <span class="crit">기능테스트</span></div>

## 심사위원이 직접 확인할 수 있습니다

<div class="ver mid">

```bash
# 1) AI 접근 — PyPI 배포본 (v0.4.0)
uvx cubrid-mcp-server

# 2) 전체 스택 — GitHub Release
docker compose up && make verify
```

<div class="steps">
  <p class="h">VERIFY.md — 단계별 검증 가이드</p>
  <p class="muted">드라이버 연결 → ORM → MCP 서버 → 실서버 골든 테스트, 그리고 SBOM·라이선스 확인까지 명령어와 기대 출력을 함께 제공합니다.</p>
</div>

</div>

<style>
.ver { display: grid; grid-template-columns: 1.2fr 1fr; gap: 28px; margin-top: 30px; align-items: start; }
.ver pre.slidev-code { font-size: 0.9rem !important; }
.steps { display: grid; gap: 8px; }
.steps .h { font-size: 1rem; font-weight: 700; }
.steps .muted { font-size: 0.85rem; line-height: 1.55; }
</style>

---

<div class="eyebrow">Adoption Metrics <span class="crit">활용성</span></div>

## 검증할 수 있는 숫자만

<div class="adopt mid"><SnapshotMetrics category="adoption" /></div>

<p class="honest">GitHub 클론 수는 CI 러너의 checkout이 대부분이라 채택 지표로 쓰지 않습니다.</p>

<style>
.adopt { margin-top: 34px; }
.adopt .stat .num { font-size: 2.5rem; }
.honest { font-size: 0.78rem; color: var(--muted); margin-top: 22px; }
</style>

---
class: navy
---

<div class="eyebrow">Closing <span class="crit">PT</span></div>

<div class="close">
  <div>
    <h1>오픈소스는<br>선순환한다</h1>
    <ol class="wheel">
      <li>컨트리뷰톤에서 배웠다</li>
      <li>Mike Bayer를 만났다</li>
      <li>멈춘 방언에서 영감을 받아 새로 썼다</li>
      <li>드라이버부터 생태계까지 만들었다</li>
      <li class="next">다음 기여자를 기다린다</li>
    </ol>
  </div>
  <div class="right">

```bash
pip install pycubrid
# 2014년의 공백, 2026년에 닫았다
```

  <div class="tally">
    <span><b>4</b> 패키지</span><span><b>68</b> 예제</span><span><b>7</b> 템플릿</span>
    <span><b>2,200</b> 테스트</span><span><b>450</b> PR</span><span><b>MIT</b></span>
  </div>
  <p class="sig">CUBRID Lab — 최영선 · 백경준</p>
  </div>
</div>

<style>
.close { display: grid; grid-template-columns: 1.1fr 1fr; gap: 40px; margin-top: 18px; align-items: start; }
.close h1 { font-size: 2.9rem; line-height: 1.12; }
.wheel { list-style: none; padding: 0; margin: 22px 0 0; display: grid; gap: 8px; counter-reset: w; }
.wheel li { counter-increment: w; font-size: 1rem; font-weight: 600; display: grid; grid-template-columns: 26px 1fr; align-items: baseline; color: var(--on-navy); }
.wheel li::before { content: counter(w); font-size: 0.75rem; font-weight: 800; color: #7fb0ec; }
.wheel li.next { color: #7fb0ec; }
.close .right { display: grid; gap: 18px; padding-top: 12px; }
.tally { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px 14px; font-size: 0.8rem; color: var(--on-navy-muted); }
.tally b { display: block; font-size: 1.6rem; font-weight: 800; color: var(--on-navy); letter-spacing: -0.03em; }
.sig { font-size: 0.8rem; color: var(--on-navy-muted); }
</style>

<!--
2020년에 멘토로 시작해서 6년이 걸렸습니다.
기여자에서 커뮤니티 빌더가 되고, 방언을 만들고,
드라이버를 만들고, 결국 생태계를 만들었습니다.
SQLAlchemy Korea도 계속 운영하고 있습니다.
다음 컨트리뷰톤에서 누군가 저희 프로젝트를 이어가 주길 기다립니다.
-->
