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

<Act :n="1" />

<div class="eyebrow">2026 OSS 개발자대회 본선 <span class="crit">CUBRID Lab</span></div>

<div class="cover mid">
  <h1>2020년,<br>두 사람이 만났다</h1>
  <p class="lede">멘토 최영선 × 멘티 백경준 — 오픈소스 컨트리뷰톤 CNBT-41</p>

  <div class="facts">
    <div><span class="muted">함께 배운 것</span><b>SQLAlchemy</b></div>
    <div><span class="muted">대화한 사람</span><b>Mike Bayer <small>창시자 · Gitter</small></b></div>
    <div><span class="muted">함께 만든 것</span><b>SQLAlchemy Korea</b></div>
  </div>

  <p class="then"><span class="accent">6년 후,</span> 그때 받은 것을 돌려주러 왔습니다</p>
</div>

<style>
.cover { display: grid; gap: 18px; }
.cover h1 { font-size: 3.1rem; line-height: 1.12; }
.facts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: #22385a; border: 1px solid #22385a; border-radius: 10px; overflow: hidden; margin-top: 8px; }
.facts > div { background: var(--navy); padding: 12px 16px; display: grid; gap: 4px; }
.facts span { font-size: 0.7rem; font-weight: 600; }
.facts b { font-size: 1.05rem; font-weight: 700; }
.facts small { font-size: 0.72rem; font-weight: 500; color: var(--on-navy-muted); }
.then { font-size: 1.45rem; font-weight: 700; margin-top: 10px; letter-spacing: -0.02em; }
</style>

<!--
[0:00–0:45 · 45초]
안녕하세요, CUBRID Lab의 최영선, 백경준입니다.
저희 둘은 2020년, NIPA 오픈소스 컨트리뷰톤에서 멘토와 멘티로 처음 만났습니다.
그때 SQLAlchemy에 기여하면서 오픈소스를 배웠고,
Gitter에서 창시자 Mike Bayer와 대화하면서 SQLAlchemy Korea 커뮤니티도 만들었습니다.
오늘은 그 뒤 6년 동안 저희가 무엇을 만들었는지, 이야기로 들려드리겠습니다.
-->

---

<Act :n="2" />

<div class="eyebrow">발견 <span class="crit">활용성</span></div>

<div class="gap mid">
  <div class="share">
    <span class="num">13.24<small>%</small></span>
    <p class="big">한국 공공부문 DBMS 점유율 <b>2위</b></p>
    <p class="muted">2,367개 설치 · Oracle 다음 · 2025년 말</p>
    <p class="src">행정안전부·NIA 「2026년도 범정부EA기반 공공부문 정보자원 현황 통계보고서」</p>
  </div>

  <div class="dead">
    <h2>그런데 Python으로 가는 길은<br><span class="seal">2014년에 멈춰 있었습니다</span></h2>
    <div class="row"><span class="d seal">2012</span><div><b>zzzeek/sqlalchemy_cubrid</b><p class="muted">Mike Bayer가 만든 방언 — 이후 방치</p></div></div>
    <div class="row"><span class="d seal">2014-05-15</span><div><b>공식 Python 드라이버</b><p class="muted">마지막 릴리스 — C 확장 · asyncio · SQLAlchemy 2.x 미지원</p></div></div>
  </div>
</div>

<EvidenceFooter claim="cubrid-public-sector, official-driver-2014" />

<style>
.gap { display: grid; grid-template-columns: 1fr 1.15fr; gap: 44px; align-items: start; }
.share { display: grid; gap: 8px; padding-top: 6px; }
.share .num { font-size: 5.6rem; color: var(--blue); }
.share .num small { font-size: 0.45em; margin-left: 4px; letter-spacing: 0; }
.share .big { font-size: 1.25rem; font-weight: 650; }
.share .src { margin-top: 10px; max-width: 30ch; }
.dead { display: grid; gap: 14px; }
.dead h2 { font-size: 1.75rem; line-height: 1.25; margin-bottom: 4px; }
.row { display: grid; grid-template-columns: 104px 1fr; gap: 14px; align-items: baseline; border-top: 1px solid var(--line); padding-top: 12px; }
.row .d { font-weight: 800; font-size: 0.95rem; font-variant-numeric: tabular-nums; }
.row b { font-size: 0.95rem; }
.row p { font-size: 0.8rem; margin-top: 2px; }
</style>

<!--
[0:45–1:30 · 45초]
그러다 이상한 걸 하나 발견했습니다.
CUBRID는 한국 공공부문 DBMS 점유율 2위입니다. 13.24%, 2천 3백 개가 넘게 설치돼 있습니다.
그런데 Python에서 이 데이터베이스를 쓰려고 하니,
Mike Bayer가 2012년에 만든 방언은 멈춰 있었고, 공식 드라이버의 마지막 릴리스는 2014년이었습니다.
asyncio도, SQLAlchemy 2도 쓸 수 없었습니다. 그래서, 저희가 고쳐보기로 했습니다.
-->

---

<Act :n="3" />

<div class="eyebrow">만들기 <span class="crit">PT</span></div>

## 방언을 고치려다, 드라이버부터 다시 만들게 됐습니다

<div class="chain mid">
  <div class="tl"><span class="dot">1</span><span class="yr">2021–22</span><span class="name">sqlalchemy-cubrid</span><span class="what">2012년 방언을 SQLAlchemy 2.0 기준으로 처음부터 다시 썼습니다</span><span class="why">그런데 밑의 드라이버가 멈춰 있었고 →</span></div>
  <div class="tl"><span class="dot">2</span><span class="yr">2025</span><span class="name">pycubrid</span><span class="what">순수 Python 드라이버 · 의존성 0</span><span class="why">만들고 나니 쓰는 법을 보여줘야 했고 →</span></div>
  <div class="tl"><span class="dot">3</span><span class="yr">2026</span><span class="name">cubrid-cookbook</span><span class="what">68 예제 + 7 템플릿 · 매일 밤 실서버에서 실행</span><span class="why">그리고 AI가 데이터를 묻는 시대가 왔습니다 →</span></div>
  <div class="tl now"><span class="dot">4</span><span class="yr">2026</span><span class="name">cubrid-mcp-server</span><span class="what">AI가 자연어로 CUBRID에 질의 · 세계 최초 CUBRID MCP</span></div>
</div>

<EvidenceFooter claim="mcp-world-first" />

<style>
.chain { display: grid; grid-template-columns: repeat(4, 1fr); position: relative; }
.chain::before { content: ""; position: absolute; left: 0; right: 0; top: 11px; height: 2px; background: var(--line); }
.chain .why { font-size: 0.74rem; font-weight: 650; color: var(--blue); margin-top: 6px; line-height: 1.45; }
</style>

<!--
[1:30–2:30 · 60초]
처음엔 방언 하나만 고치려고 했습니다. Mike Bayer의 2012년 방언을 SQLAlchemy 2.0 기준으로 처음부터 다시 썼죠.
그런데 방언 밑에 있는 드라이버가 2014년에 멈춘 C 확장이었습니다. 그래서 드라이버부터 새로 만들었습니다.
드라이버를 만들고 나니, 사람들이 실제로 쓰는 법을 보여줘야 했습니다. 그게 cookbook이고, 매일 밤 실서버에서 돌면서 드라이버 버그를 가장 먼저 잡습니다.
그리고 AI가 데이터를 묻는 시대가 와서, 세계 최초의 CUBRID MCP 서버까지 만들었습니다.
하나를 고치면 다음 문제가 보였고, 그걸 따라가다 보니 생태계가 됐습니다.
-->

---

<Act :n="3" />

<div class="eyebrow">만들기 — 가장 어려웠던 순간</div>

<p class="say">문서가 없었습니다.<br><span class="accent">그래서 두 드라이버의 소스를 나란히 놓고 읽었습니다.</span></p>

<div class="proto mid">
  <div class="sources">
    <div class="src-card"><b>node-cubrid</b><span>Node.js 드라이버 · BSD</span></div>
    <span class="x">×</span>
    <div class="src-card"><b>공식 C 드라이버</b><span>CAS 클라이언트 소스</span></div>
  </div>

  <div class="packet">
    <div><b>4B</b><span>length</span></div>
    <div><b>4B</b><span>cas_info</span></div>
    <div><b>payload</b><span>CAS 바이너리 프로토콜 v8 · TCP 33000</span></div>
  </div>

  <div class="stats three">
    <div class="stat"><span class="num">18</span><span class="k">패킷 타입</span></div>
    <div class="stat"><span class="num">27</span><span class="k">데이터 타입</span></div>
    <div class="stat hl"><span class="num">0</span><span class="k">런타임 의존성</span></div>
  </div>
</div>

<style>
.proto { display: grid; gap: 18px; }
.stats.three { grid-template-columns: repeat(3, 1fr); }
.stats.three .num { font-size: 2.2rem; }
</style>

<!--
[2:30–3:00 · 30초]
드라이버를 만들 때 가장 어려웠던 건, CUBRID의 CAS 프로토콜 문서가 없다는 점이었습니다.
그래서 BSD 라이선스인 node-cubrid와 공식 C 드라이버 소스를 나란히 놓고 한 줄씩 비교했습니다.
그렇게 18개 패킷 타입과 27개 데이터 타입을 해독했고, 결과물은 의존성이 하나도 없는 순수 Python 드라이버입니다.
-->

---

<Act :n="4" />

<div class="eyebrow">방법 <span class="crit">커뮤니티 5점</span></div>

## 두 사람이 어떻게 4개를? — AI가 쓰고, 사람이 책임집니다

<div class="flow mid">
  <div class="step human"><span class="who">사람</span><span class="t">AGENTS.md</span><span class="d">규칙을 씁니다</span></div>
  <div class="arrow">→</div>
  <div class="step"><span class="who">AI</span><span class="t">구현</span><span class="d">코드 · 테스트 · 문서</span></div>
  <div class="arrow">→</div>
  <div class="step human"><span class="who">사람</span><span class="t">리뷰</span><span class="d">모든 PR을 읽습니다</span></div>
  <div class="arrow">→</div>
  <div class="step"><span class="who">CI</span><span class="t">게이트</span><span class="d">타입 · 커버리지 · 라이브 DB</span></div>
  <div class="arrow">→</div>
  <div class="step human"><span class="who">사람</span><span class="t">릴리스</span><span class="d">태그는 사람만</span></div>
</div>

<div class="work">
  <div class="stat hl"><span class="num">450</span><span class="k">Merged PRs</span><span class="v">CI 게이트 통과 후 병합</span></div>
  <p class="aside">컨트리뷰톤에서 배운 멘토–멘티 방식 그대로입니다. AI가 멘티처럼 구현하고, 저희가 멘토처럼 리뷰합니다. 한국어 문서 동기화, 릴리스마다 SBOM까지 CI가 지킵니다.</p>
</div>

<style>
.work { display: grid; grid-template-columns: 200px 1fr; gap: 28px; align-items: center; margin-top: 22px; }
.work .num { font-size: 2.6rem; }
</style>

<!--
[3:00–4:00 · 60초]
여기서 이런 질문이 드실 겁니다. 두 사람이 어떻게 4개 프로젝트를 만들었냐고요.
답은, AI가 쓰고 사람이 책임지는 구조입니다.
사람이 AGENTS.md에 규칙을 쓰고, AI가 구현하고, 모든 PR은 사람이 리뷰하고, CI 게이트를 통과해야만 병합됩니다. 릴리스 태그는 사람만 찍습니다.
사실 이건 저희가 컨트리뷰톤에서 배운 멘토-멘티 방식 그대로입니다. 이렇게 450개 PR이 병합됐습니다.
-->

---

<Act :n="4" />

<div class="eyebrow">방법 <span class="crit">기능테스트 10점</span></div>

## "AI가 쓴 코드를 믿을 수 있나요?" — 통과 못 하면 머지되지 않습니다

<div class="qa mid">
  <div class="lead">
    <span class="num">2,200</span>
    <p class="big">개의 테스트</p>
    <p class="muted">품질은 목표가 아니라 전제 조건입니다.</p>
  </div>
  <ul class="checks">
    <li><div><b>mypy --strict</b><span>타입 오류 0</span></div></li>
    <li><div><b>Coverage ≥ 95%</b><span>미달이면 머지 불가</span></div></li>
    <li><div><b>hypothesis</b><span>랜덤 입력으로 엣지 케이스 탐색</span></div></li>
    <li><div><b>api-baseline.json</b><span>공개 API가 몰래 바뀌면 실패</span></div></li>
    <li><div><b>Golden tests · 45</b><span>매일 밤 CUBRID 11.2 + 11.4 실서버</span></div></li>
    <li><div><b>SQLAlchemy 공식 스위트 · 720</b><span>방언 호환성</span></div></li>
    <li><div><b>CodeQL</b><span>모든 PR 보안 스캔</span></div></li>
    <li><div><b>Python 5 × CUBRID 4</b><span>20조합 라이브 DB (드라이버·방언)</span></div></li>
  </ul>
</div>

<style>
.qa { display: grid; grid-template-columns: 0.7fr 1.5fr; gap: 36px; align-items: center; }
.qa .lead { display: grid; gap: 8px; }
.qa .lead .num { font-size: 4.4rem; color: var(--blue); }
.qa .big { font-size: 1.3rem; font-weight: 700; margin-top: -4px; }
.qa .muted { font-size: 0.88rem; line-height: 1.5; }
</style>

<!--
[4:00–5:00 · 60초]
그러면 당연히 다음 질문이 나옵니다. AI가 쓴 코드를 믿을 수 있냐.
그래서 저희는 믿지 않아도 되게 만들었습니다. 테스트가 2,200개이고, 이 게이트들을 통과하지 못하면 머지 자체가 안 됩니다.
타입 검사, 커버리지 95%, 랜덤 입력 테스트, 공개 API 변경 감지,
그리고 매일 밤 실제 CUBRID 서버에서 45개 예제를 돌립니다.
품질은 목표가 아니라, 머지의 전제 조건입니다.
-->

---

<Act :n="4" />

<div class="eyebrow">방법 <span class="crit">기능테스트</span></div>

## 니치 시장에는 성능을 알려줄 사용자가 없습니다. 그래서 직접 쟀습니다.

<div class="perf mid"><SnapshotMetrics category="performance" /></div>

<p class="repro">재현: <b>github.com/cubrid-lab/cubrid-benchmark</b></p>

<style>
.perf .stat .num { font-size: 2.6rem; }
.repro { font-size: 0.8rem; color: var(--muted); }
.repro b { color: var(--ink); font-family: var(--mono); font-weight: 600; }
</style>

<!--
[5:00–5:45 · 45초]
큰 오픈소스는 사용자가 성능 문제를 알려줍니다. 니치 시장은 그렇지 않습니다.
그래서 벤치마크 저장소를 따로 만들고, 프로파일링으로 병목을 직접 찾았습니다.
연결 확인은 기존 SELECT 1 방식보다 처리량이 280%, SQLAlchemy 풀 체크는 588% 늘었고,
대량 INSERT와 조회도 각각 12%, 20% 빨라졌습니다. 모두 저장소에서 재현할 수 있습니다.
-->

---

<Act :n="5" />

<div class="eyebrow">증명 <span class="crit">활용성 15점</span></div>

## 쓰는 사람에게는 5분이면 충분해야 합니다

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
    <span class="chip on">FastAPI</span>
    <span class="chip on">Django</span>
    <span class="chip on">Streamlit 대시보드</span>
    <span class="chip on">AI 에이전트 · MCP</span>
    <span class="chip">Celery</span>
    <span class="chip">Pandas ETL</span>
    <span class="chip">Flask</span>
  </div>
  <div class="docs">
    <div><span class="num">4</span><span class="muted">문서 사이트</span></div>
    <div><span class="num">34</span><span class="muted">한국어 페이지</span></div>
  </div>
</div>
</div>

<style>
.dx { display: grid; grid-template-columns: 1.25fr 1fr; gap: 28px; align-items: center; }
.dx .side { display: grid; gap: 14px; }
.dx .h { font-size: 0.95rem; font-weight: 700; }
.docs { display: flex; gap: 28px; }
.docs div { display: grid; gap: 2px; }
.docs .num { font-size: 2.2rem; color: var(--blue); }
.docs .muted { font-size: 0.75rem; }
</style>

<!--
[5:45–6:30 · 45초]
이제 쓰는 사람 입장에서 보겠습니다. pip install 한 줄이면 끝납니다. C 컴파일러도 필요 없습니다.
FastAPI, Django, Streamlit 대시보드, AI 에이전트까지 7개 템플릿을 복사해서 바로 시작할 수 있고,
문서는 4개 사이트, 한국어로 34페이지를 준비했습니다.
그럼, 실제로 어떻게 쓰이는지 직접 보여드리겠습니다.
-->

---
class: navy
---

<Act :n="5" />

<div class="eyebrow">증명 · Live Demo <span class="crit">데모 10점 · 2분</span></div>

## 직접 보여드리겠습니다 — 온나라 데이터로

<p class="lede">행안부 전자결재(온나라) 시나리오 — CUBRID 위의 공공 업무 데이터, 지금까지는 Java 중심.</p>

<div class="timing"><span>대시보드 15s</span><span class="core">Claude + MCP 90s</span><span>터미널 15s</span></div>

<div class="asks mid">
  <div class="ask"><span class="n">1</span><span class="q">"이 DB에 어떤 테이블이 있어?"</span><span class="beat">탐색</span></div>
  <div class="ask star"><span class="n">2</span><span class="q">"결재가 지연된 문서 TOP 5는? 평균 처리일과 대기 수로"</span><span class="beat">AI 운영 분석</span></div>
  <div class="ask"><span class="n">3</span><span class="q">"기밀 문서는 부처별로 몇 개야? 내용은 보지 말고 집계만"</span><span class="beat">집계만 질의</span></div>
  <div class="ask reject"><span class="n">4</span><span class="q">"결재 대기 문서를 전부 승인 처리해줘"</span><span class="stamp">반려</span></div>
</div>

<p class="note">MCP 서버는 기본이 읽기 전용 — 쓰기 도구는 노출되지 않고, 쓰기 SQL은 화이트리스트에서 거부됩니다.</p>

<style>
.asks { margin-top: 0; }
.asks .ask:last-child { padding-block: 4px; }
.note { font-size: 0.78rem; color: var(--on-navy-muted); }
</style>

<!--
[6:30–8:30 · 2분 · DEMO_RUNBOOK.md]
행안부 온나라는 47개 부처가 쓰는 CUBRID 기반 전자결재 시스템입니다. 지금까지는 Java 중심이었습니다.
이 데이터를 Python과 AI로 다뤄보겠습니다. 대시보드부터 보시죠.
(#2 후) AI가 데이터를 읽기만 하는 게 아니라, 평균 처리일과 대기 수로 결재 병목을 스스로 분석했습니다.
(#4 후) 결재 대기 문서를 전부 승인하라는 AI 명령이 서버에서 반려됐습니다.
MCP 서버는 기본이 읽기 전용이라 쓰기 도구가 노출조차 되지 않고, 쓰기 SQL은 화이트리스트에서 거부됩니다.
-->

---

<Act :n="6" />

<div class="eyebrow">신뢰 <span class="crit">OSS 적절성 15점</span></div>

## 저희끼리 정한 규칙이 아니라, 표준 위에 올렸습니다

<div class="std mid">
  <div class="stat"><span class="k accent">PEP 249 · DB-API 2.0</span><span class="t">pycubrid 완전 준수</span><span class="v">1,147 테스트</span></div>
  <div class="stat"><span class="k accent">PEP 561 · 타입</span><span class="t">py.typed · mypy strict 0</span><span class="v">CI 강제</span></div>
  <div class="stat"><span class="k accent">SQLAlchemy Dialect API</span><span class="t">공식 테스트 스위트 통합</span><span class="v">53 feature flags</span></div>
  <div class="stat"><span class="k accent">Model Context Protocol</span><span class="t">Tools · Resources · Prompts</span><span class="v">세계 최초 CUBRID MCP</span></div>
</div>

<p class="stackh">어깨를 빌린 오픈소스</p>
<div class="chips">
  <span class="chip">SQLAlchemy · MIT</span>
  <span class="chip">zzzeek/sqlalchemy_cubrid · MIT</span>
  <span class="chip">node-cubrid · BSD</span>
  <span class="chip">MCP · MIT</span>
  <span class="chip">pytest · hypothesis</span>
  <span class="chip">CodeQL · Dependabot</span>
</div>

<EvidenceFooter claim="pep249-compliance" />

<style>
.std { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.std .t { font-size: 0.95rem; font-weight: 700; line-height: 1.35; }
.std .k { font-size: 0.7rem; letter-spacing: 0.02em; }
.stackh { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin: 0 0 8px; }
</style>

<!--
[8:30–9:30 · 60초]
저희가 만든 건 저희끼리만 통하는 규칙이 아닙니다.
드라이버는 Python 표준인 PEP 249를 완전히 따르고, 타입 정보도 표준대로 제공합니다.
방언은 SQLAlchemy 공식 테스트 스위트를 통과하고, AI 서버는 MCP 표준을 따릅니다.
그리고 저희도 SQLAlchemy, node-cubrid 같은 오픈소스의 어깨 위에서 만들었습니다.
-->

---

<Act :n="6" />

<div class="eyebrow">신뢰 <span class="crit">라이선스 5점</span></div>

<div class="lic mid">
  <div>
    <p class="say">누구나 가져다 쓸 수 있게</p>
    <span class="num">MIT × 4</span>
    <p class="muted">4개 패키지 모두 MIT · 의존성 트리에도 GPL 없음</p>
  </div>
  <div class="cards">
    <div class="stat"><span class="k">우리 패키지</span><span class="v">독립 wire-protocol 클라이언트 — CUBRID 서버 코드를 포함하지 않음</span></div>
    <div class="stat"><span class="k">CUBRID 서버</span><span class="v">Apache-2.0 엔진 · BSD 커넥터 — 업스트림 COPYING 직접 확인</span></div>
    <div class="stat"><span class="k">배포물</span><span class="v">THIRD_PARTY_LICENSES · NOTICE · SPDX SBOM</span></div>
  </div>
</div>

<style>
.lic { display: grid; grid-template-columns: 1fr 1.2fr; gap: 44px; align-items: center; }
.lic .say { font-size: 1.4rem; margin-bottom: 8px; }
.lic .num { font-size: 4.4rem; color: var(--blue); }
.lic .muted { font-size: 0.85rem; margin-top: 10px; }
.lic .cards { display: grid; gap: 10px; }
</style>

<!--
[9:30–9:50 · 20초]
라이선스는 짧게 말씀드리겠습니다. 4개 모두 MIT이고, 의존성 어디에도 GPL은 없습니다.
CUBRID 서버의 라이선스도 업스트림 원문을 직접 확인했습니다.
-->

---

<Act :n="6" />

<div class="eyebrow">신뢰 <span class="crit">기능테스트</span></div>

## 저희 말 대신, 직접 확인해 보세요

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
.ver { display: grid; grid-template-columns: 1.2fr 1fr; gap: 28px; align-items: center; }
.ver pre.slidev-code { font-size: 0.9rem !important; }
.steps { display: grid; gap: 8px; }
.steps .h { font-size: 1rem; font-weight: 700; }
.steps .muted { font-size: 0.85rem; line-height: 1.55; }
</style>

<!--
[9:50–10:10 · 20초]
오늘 말씀드린 내용은 심사위원분들이 직접 확인하실 수 있습니다.
명령어 한 줄로 AI 서버를 띄울 수 있고, VERIFY.md에 단계별 명령과 기대 결과를 모두 적어 두었습니다.
-->

---

<Act :n="6" />

<div class="eyebrow">신뢰 <span class="crit">활용성</span></div>

## 부풀리지 않은 숫자만 가져왔습니다

<div class="adopt mid"><SnapshotMetrics category="adoption" /></div>

<p class="honest">GitHub 클론 수는 CI 러너의 checkout이 대부분이라, 채택 지표로 쓰지 않았습니다.</p>

<style>
.adopt .stat .num { font-size: 2.5rem; }
.honest { font-size: 0.78rem; color: var(--muted); }
</style>

<!--
[10:10–10:40 · 30초]
숫자는 검증할 수 있는 것만 가져왔습니다. 병합된 PR 450개, 테스트 2,200개, 20개 조합의 CI, 릴리스 35번.
사실 클론 수가 더 커 보이는 숫자였는데, 측정해 보니 대부분 저희 CI였습니다. 그래서 뺐습니다.
-->

---

<Act :n="7" />

<div class="eyebrow">다음 <span class="crit">커뮤니티 + 발전가능성</span></div>

## Python에서 검증한 순서를, 다른 언어로

<div class="langs mid">
  <div class="stat hl"><span class="k">Python · 완성</span><span class="t">pycubrid v1.7.1</span><span class="t">sqlalchemy-cubrid v1.7.1</span></div>
  <div class="stat"><span class="k">TypeScript · 진행</span><span class="t">cubrid-client v1.1.0</span><span class="t">drizzle-cubrid v0.2.1</span></div>
  <div class="stat"><span class="k">Go · 진행</span><span class="t">cubrid-go v0.2.1</span><span class="t">gorm-cubrid v0.1.0</span></div>
  <div class="stat"><span class="k">Rust · 진행</span><span class="t">cubrid-rs v0.1.0</span><span class="t">sea-orm-cubrid v0.1.0</span></div>
</div>

<p class="aside">드라이버 → ORM → 예제 → AI. 그리고 SQLAlchemy Korea를 6년째 운영해 온 방식 그대로 — 문서, 예제, 멘토링이 붙은 good-first-issue로 사람을 모읍니다.</p>

<style>
.langs { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.langs .t { font-family: var(--mono); font-size: 0.78rem; font-weight: 600; }
.langs .stat.hl .t { color: #fff; }
.aside { max-width: none; }
</style>

<!--
[10:40–11:10 · 30초]
Python은 끝이 아니라 레퍼런스입니다. 드라이버, ORM, 예제, AI로 이어지는 같은 순서를
TypeScript, Go, Rust에서도 진행하고 있습니다.
커뮤니티는 SQLAlchemy Korea를 운영해 온 방식 그대로, 문서와 예제, 멘토링이 붙은 이슈로 키우겠습니다.
-->

---
class: navy
---

<Act :n="7" />

<div class="eyebrow">다음</div>

<div class="close mid">
  <div>
    <h1>6년 전 저희가 받은 것을,<br><span class="accent">다음 사람에게</span></h1>
    <ol class="wheel">
      <li>컨트리뷰톤에서 배웠고</li>
      <li>Mike Bayer와 대화했고</li>
      <li>멈춘 방언에서 다시 시작해</li>
      <li>드라이버부터 생태계까지 만들었습니다</li>
      <li class="next">이제 다음 기여자를 기다립니다</li>
    </ol>
  </div>
  <div class="right">
    <p class="thanks">감사합니다</p>
    <div class="links">
      <div><span>GitHub</span>github.com/cubrid-lab</div>
      <div><span>설치</span>pip install pycubrid</div>
      <div><span>AI</span>uvx cubrid-mcp-server</div>
      <div><span>문서</span>cubrid-lab.github.io/pycubrid</div>
    </div>
    <p class="sig">CUBRID Lab — 최영선 · 백경준</p>
  </div>
</div>

<style>
.close { display: grid; grid-template-columns: 1.25fr 1fr; gap: 40px; align-items: center; }
.close h1 { font-size: 2.4rem; line-height: 1.2; }
.wheel { list-style: none; padding: 0; margin: 22px 0 0; display: grid; gap: 8px; counter-reset: w; }
.wheel li { counter-increment: w; margin: 0; padding: 0; font-size: 1rem; font-weight: 600; display: grid; grid-template-columns: 26px 1fr; align-items: baseline; color: var(--on-navy); }
.wheel li::before { content: counter(w); font-size: 0.75rem; font-weight: 800; color: #7fb0ec; }
.wheel li.next { color: #7fb0ec; }
.close .right { display: grid; gap: 18px; }
.thanks { font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; }
.sig { font-size: 0.8rem; color: var(--on-navy-muted); }
</style>

<!--
[11:10–11:40 · 30초]
6년 전 컨트리뷰톤에서, 저희는 오픈소스로부터 많은 것을 받았습니다.
오늘은 그때 받은 것을 생태계로 돌려드리러 왔습니다.
다음 컨트리뷰톤 어딘가에서, 저희 프로젝트를 이어갈 누군가를 기다리겠습니다. 감사합니다.
-->
