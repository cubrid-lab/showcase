---
theme: default
title: "공공 DBMS에 Python 문을 열다 — CUBRID Python 생태계"
info: "2026 오픈소스 개발자대회 본선"
author: "CUBRID Lab — 최영선 · 백경준"
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
---

<div class="cover">
  <p class="kicker">2026 오픈소스 개발자대회 본선</p>
  <h1>공공 DBMS에<br>Python 문을 열다</h1>
  <p class="sub">CUBRID Python 생태계 — 기여자에서 메인테이너로</p>
  <div class="who">
    <b>최영선 · 백경준</b>
    <span>CUBRID Lab</span>
  </div>
</div>

<style>
.cover { display: grid; gap: 22px; }
.cover h1 { font-size: 3.8rem; line-height: 1.12; }
.cover .sub { max-width: none; }
.who { display: flex; gap: 14px; align-items: baseline; margin-top: 26px; padding-top: 18px; border-top: 2px solid var(--ink); width: fit-content; }
.who b { font-size: 1.1rem; }
.who span { font-size: 0.9rem; color: var(--muted); }
</style>

<!--
[0:00–0:10 · 10초 · PT]
안녕하세요. "공공 DBMS에 Python 문을 열다", CUBRID Lab의 최영선, 백경준입니다.
-->

---

<div class="chapter"><span class="no">01</span><h1>만남과 발견</h1><span class="of">왜 만들었나</span></div>

<!--
[0:10–0:15 · 5초] (넘기면서) 먼저, 저희가 왜 이걸 만들었는지부터 말씀드리겠습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">2020년, 오픈소스 컨트리뷰톤</p>
    <h1>두 사람이<br>만났습니다</h1>
    <p class="sub">멘토 최영선, 멘티 백경준.</p>
  </div>
  <div class="frame"><Photo src="/photos/team-2020.jpg" label="2020 컨트리뷰톤 사진" /></div>
</div>

<style>
.frame { height: 380px; }
</style>

<!--
[0:15–0:35 · 20초 · PT · 커뮤니티]
저희 둘은 2020년, NIPA 오픈소스 컨트리뷰톤에서 멘토와 멘티로 처음 만났습니다.
-->

---

<ul class="lines big-lines">
  <li>SQLAlchemy에 기여하며 오픈소스를 배웠고,</li>
  <li>Gitter에서 창시자 <span class="accent">Mike Bayer</span>와 대화했고,</li>
  <li><span class="accent">SQLAlchemy Korea</span> 커뮤니티를 만들었습니다.</li>
</ul>

<style>
.big-lines li { font-size: 2rem; }
</style>

<!--
[0:35–0:55 · 20초 · 커뮤니티]
그때 SQLAlchemy에 기여하면서 오픈소스를 배웠고, Gitter에서 창시자 Mike Bayer와 대화했고,
SQLAlchemy Korea라는 커뮤니티도 만들었습니다. 오늘 이야기는 여기서 시작합니다.
-->

---

<p class="kicker">한국 공공부문 DBMS 점유율 2위</p>
<p class="huge">13.24%</p>
<p class="sub">CUBRID — 공공기관 2,367곳에 설치, Oracle 다음.</p>
<p class="small">출처: 행정안전부·NIA 「2026년도 범정부EA기반 공공부문 정보자원 현황 통계보고서」(2025년 말 기준)</p>

<!--
[0:55–1:20 · 25초 · 활용성]
그러다 한 가지를 알게 됐습니다. CUBRID는 한국 공공부문 DBMS 점유율 2위입니다.
2025년 말 기준 13.24%, 2천 3백 곳이 넘는 공공기관에서 쓰고 있습니다.
-->

---

<p class="kicker">그런데 Python에서는</p>
<h1><span class="seal">2014년 5월 15일.</span></h1>
<p class="sub">공식 Python 드라이버의 마지막 릴리스.<br>asyncio도, SQLAlchemy 2도 쓸 수 없었습니다.</p>

<!--
[1:20–1:40 · 20초 · 활용성]
그런데 Python에서 이 데이터베이스를 쓰려고 하니, 공식 드라이버의 마지막 릴리스가 2014년 5월이었습니다.
그 사이 Python은 asyncio와 SQLAlchemy 2의 시대가 됐는데, CUBRID는 그대로 멈춰 있었습니다.
-->

---

<h1>그래서,<br><span class="accent">고쳐보기로 했습니다.</span></h1>

<!--
[1:40–1:45 · 5초 · PT]
그래서 저희가 고쳐보기로 했습니다.
-->

---

<div class="chapter"><span class="no">02</span><h1>만든 것</h1><span class="of">하나를 고치면 다음 문제가 보였습니다</span></div>

<!--
[1:45–1:50 · 5초] (넘기면서) 하나를 고치면 다음 문제가 보였습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">첫 번째 · 2021–22</p>
    <h2>Mike Bayer의 2012년 방언을<br>처음부터 다시 썼습니다</h2>
    <p class="sub"><code>sqlalchemy-cubrid</code> — SQLAlchemy 2.0 방언, 공식 테스트 스위트 통합</p>
  </div>
  <div class="stack">
    <p class="then">그런데 그 밑의 드라이버가<br><span class="seal">2014년에 멈춘 C 확장</span>이었습니다.</p>
  </div>
</div>

<style>
.then { font-size: 1.5rem; font-weight: 700; line-height: 1.4; border-left: 4px solid var(--seal); padding-left: 18px; }
</style>

<!--
[1:50–2:15 · 25초 · OSS 적절성]
처음엔 방언 하나만 고치려고 했습니다. Mike Bayer가 2012년에 만든 CUBRID 방언을
SQLAlchemy 2.0 기준으로 처음부터 다시 썼고, SQLAlchemy 공식 테스트 스위트도 붙였습니다.
그런데 방언 밑에 있는 드라이버가 2014년에 멈춘 C 확장이었습니다.
-->

---

<h1>드라이버를 만들려고 보니,<br><span class="seal">프로토콜 문서가 없었습니다.</span></h1>

<!--
[2:15–2:25 · 10초 · PT]
그래서 드라이버를 새로 만들기로 했는데, 가장 큰 벽은 CUBRID 통신 프로토콜 문서가 없다는 것이었습니다.
-->

---

<p class="kicker">node-cubrid (BSD) 와 공식 C 드라이버 소스를 나란히 놓고 읽었습니다</p>

<div class="packet">
  <div><b>4B</b><span>length</span></div>
  <div><b>4B</b><span>cas_info</span></div>
  <div><b>payload</b><span>CAS 바이너리 프로토콜 · TCP 33000</span></div>
</div>

<div class="figures">
  <div><b>18</b><span>패킷 타입</span></div>
  <div><b>27</b><span>데이터 타입</span></div>
  <div><b class="accent">0</b><span>런타임 의존성</span></div>
</div>

<!--
[2:25–2:50 · 25초 · OSS 적절성 · 라이선스]
그래서 BSD 라이선스인 node-cubrid와 공식 C 드라이버 소스를 나란히 놓고 한 줄씩 비교했습니다.
그렇게 18개 패킷 타입과 27개 데이터 타입을 해독했고, 의존성이 하나도 없는 순수 Python 드라이버를 만들었습니다.
-->

---

```bash
pip install pycubrid
```

<h2>C 컴파일러 없이, 한 줄이면 끝납니다.</h2>
<p class="sub">두 번째 · 2025 — <code>pycubrid</code>, 순수 Python · PEP 249 · asyncio · TLS</p>

<!--
[2:50–3:10 · 20초 · 활용성]
그 결과가 pycubrid입니다. pip install 한 줄이면 끝나고, C 컴파일러도 필요 없습니다.
Python 표준 DB-API를 따르고, asyncio와 TLS도 지원합니다.
-->

---

<div class="split">
  <div class="stack">
    <p class="kicker">세 번째 · 2026</p>
    <h2>만들고 나니,<br>쓰는 법을 보여줘야 했습니다</h2>
    <p class="sub">68 예제 · 7 템플릿 · 문서 4개 사이트 · 한국어 34페이지</p>
  </div>
  <figure class="shot clip"><img src="/shots/docs-pycubrid.jpg" alt="pycubrid 문서 사이트"></figure>
</div>

<!--
[3:10–3:35 · 25초 · 활용성]
드라이버를 만들고 나니, 사람들이 실제로 쓰는 법을 보여줘야 했습니다.
그래서 cookbook에 68개 예제와 FastAPI, Django, 대시보드 같은 7개 템플릿을 만들었고,
문서는 4개 사이트, 한국어로 34페이지를 썼습니다. 이 예제들은 매일 밤 실서버에서 돌면서 드라이버 버그를 가장 먼저 잡습니다.
-->

---

<div class="split">
  <div class="stack">
    <p class="kicker">네 번째 · 2026</p>
    <h2>그리고 AI가<br>데이터를 묻기 시작했습니다</h2>
    <p class="sub"><code>cubrid-mcp-server</code> — 세계 최초의 CUBRID MCP 서버</p>
  </div>
  <figure class="shot clip"><img src="/shots/repo-mcp.jpg" alt="cubrid-mcp-server 저장소"></figure>
</div>

<!--
[3:35–4:00 · 25초 · 활용성 · OSS 적절성]
그리고 AI가 데이터를 묻는 시대가 왔습니다. 그래서 Claude 같은 AI가 자연어로 CUBRID에 질의할 수 있는
MCP 서버를 만들었습니다. 저희가 찾아본 범위에서, 세계 최초의 CUBRID MCP 서버입니다.
-->

---

<div class="chapter"><span class="no">03</span><h1>만든 방법</h1><span class="of">두 사람이, 어떻게 네 개를?</span></div>

<!--
[4:00–4:10 · 10초 · PT]
여기서 이런 질문이 드실 겁니다. 두 사람이 어떻게 이걸 다 만들었냐고요.
-->

---

<div class="split">
  <div class="stack">
    <h2>AI가 쓰고,<br><span class="accent">사람이 책임집니다</span></h2>
    <ul class="lines small-lines">
      <li>규칙은 사람이 <code>AGENTS.md</code>에</li>
      <li>구현은 AI가</li>
      <li>리뷰는 사람이, 모든 PR</li>
      <li>릴리스 태그는 사람만</li>
    </ul>
  </div>
  <figure class="shot clip"><img src="/shots/merged-prs.jpg" alt="병합된 PR 목록 — 모든 PR에 CI 30/30 통과"></figure>
</div>

<style>
.small-lines li { font-size: 1.15rem; font-weight: 600; }
</style>

<!--
[4:10–4:50 · 40초 · 커뮤니티]
답은 AI가 쓰고, 사람이 책임지는 구조입니다.
사람이 AGENTS.md에 규칙을 쓰고, AI가 구현하고, 모든 PR은 사람이 리뷰하고, 릴리스 태그는 사람만 찍습니다.
오른쪽이 실제 PR 목록인데, 하나하나 CI 30개 검사를 통과한 뒤에야 병합됐습니다.
사실 이건 저희가 컨트리뷰톤에서 배운 멘토-멘티 방식 그대로입니다. AI가 멘티처럼 구현하고, 저희가 멘토처럼 리뷰합니다.
-->

---

<h1>"AI가 쓴 코드를<br>믿을 수 있나요?"</h1>

<!--
[4:50–5:00 · 10초 · 기능테스트]
그럼 당연히 다음 질문이 나옵니다. AI가 쓴 코드를 믿을 수 있냐.
-->

---

<p class="kicker">믿지 않아도 되게 만들었습니다</p>
<p class="huge">2,200</p>
<h2>개의 테스트를 통과하지 못하면, 머지되지 않습니다.</h2>
<p class="sub gates">타입 오류 0 · 커버리지 95% · 랜덤 입력 테스트 · 공개 API 변경 감지 · 매일 밤 실서버 45개 예제 · Python 5 × CUBRID 4 = 20개 조합</p>

<style>
.gates { max-width: 52ch; font-size: 1rem; }
</style>

<!--
[5:00–5:35 · 35초 · 기능테스트]
저희는 믿지 않아도 되게 만들었습니다. 테스트가 2,200개이고, 통과하지 못하면 머지 자체가 안 됩니다.
타입 오류 0, 커버리지 95%, 랜덤 입력 테스트, 공개 API가 몰래 바뀌면 실패하는 검사,
그리고 매일 밤 실제 CUBRID 서버에서 45개 예제를 돌리고, Python 5개 버전과 CUBRID 4개 버전, 20개 조합으로 검증합니다.
-->

---

<p class="kicker">니치 시장엔 성능을 알려줄 사용자가 없습니다. 그래서 직접 쟀습니다.</p>

<div class="figures grid2">
  <div><b class="accent">+588%</b><span>SQLAlchemy 연결 풀 체크 처리량</span></div>
  <div><b>+280%</b><span>연결 확인 처리량 (SELECT 1 대비)</span></div>
  <div><b>12.3%</b><span>대량 INSERT 1,000행</span></div>
  <div><b>19.9%</b><span>전체 조회</span></div>
</div>

<p class="small">재현: github.com/cubrid-lab/cubrid-benchmark</p>

<!--
[5:35–6:05 · 30초 · 기능테스트]
큰 오픈소스는 사용자가 성능 문제를 알려주지만, 니치 시장은 그렇지 않습니다. 그래서 벤치마크 저장소를 따로 만들어 직접 쟀습니다.
SQLAlchemy 연결 풀 체크 처리량이 588%, 연결 확인은 280% 늘었고, 대량 INSERT와 전체 조회도 각각 12%, 20% 빨라졌습니다.
모두 저장소에서 재현할 수 있습니다.
-->

---

<div class="chapter"><span class="no">04</span><h1>직접 보여드리겠습니다</h1><span class="of">행안부 전자결재(온나라) 데이터로</span></div>

<!--
[6:05–6:10 · 5초] (넘기면서) 그럼, 실제로 어떻게 쓰이는지 직접 보여드리겠습니다.
-->

---

<p class="kicker">라이브 데모 · 온나라 시나리오 · 대시보드 → Claude → 터미널</p>

<ol class="asks">
  <li><span>"이 DB에 어떤 테이블이 있어?"</span></li>
  <li><span>"결재가 지연된 문서 TOP 5는? 평균 처리일과 대기 수로"</span></li>
  <li><span>"기밀 문서는 부처별로 몇 개야? 내용은 보지 말고 집계만"</span></li>
  <li><span>"결재 대기 문서를 전부 승인 처리해줘"</span><span class="stamp">반려</span></li>
</ol>

<!--
[6:10–8:10 · 2분 · 데모 · DEMO_RUNBOOK.md]
행안부 온나라는 47개 부처가 쓰는 CUBRID 기반 전자결재 시스템입니다. 지금까지는 Java 중심이었습니다.
이 데이터를 Python과 AI로 다뤄보겠습니다. 대시보드부터 보시죠. (대시보드 15초 → Claude 90초 → 터미널 15초)
(#2 후) AI가 데이터를 읽기만 하는 게 아니라, 평균 처리일과 대기 수로 결재 병목을 스스로 분석했습니다.
(#4 후) 결재 대기 문서를 전부 승인하라는 명령은, 서버에서 반려됐습니다.
-->

---

<h1>기본은 <span class="accent">읽기 전용</span>입니다.</h1>
<p class="sub">쓰기 도구는 보이지도 않고, 쓰기 SQL은 거부됩니다.<br>쓰기는 운영자가 연결별로 직접 켤 때만 가능합니다.</p>

<!--
[8:10–8:25 · 15초 · 데모 · 기능테스트]
방금 보신 것처럼, MCP 서버는 기본이 읽기 전용입니다. 쓰기 도구는 AI에게 보이지도 않고, 쓰기 SQL은 거부됩니다.
쓰기는 운영자가 연결별로 직접 켤 때만 가능합니다.
-->

---

<div class="chapter"><span class="no">05</span><h1>믿을 수 있는 이유</h1><span class="of">표준 · 라이선스 · 검증 · 숫자</span></div>

<!--
[8:25–8:30 · 5초] (넘기면서) 이제, 이걸 믿고 쓰셔도 되는 이유입니다.
-->

---

<h2>저희끼리 정한 규칙이 아니라,<br><span class="accent">표준 위에 올렸습니다</span></h2>

<ul class="lines std">
  <li>PEP 249 <span class="muted">— Python 표준 DB-API, 드라이버 테스트 1,147개</span></li>
  <li>SQLAlchemy Dialect API <span class="muted">— 공식 테스트 스위트 통과</span></li>
  <li>Model Context Protocol <span class="muted">— Tools · Resources · Prompts</span></li>
  <li>PEP 561 <span class="muted">— 타입 정보 제공, mypy strict 오류 0</span></li>
</ul>

<style>
.std li { font-size: 1.3rem; }
</style>

<!--
[8:30–9:00 · 30초 · OSS 적절성]
저희가 만든 건 저희끼리만 통하는 규칙이 아닙니다.
드라이버는 Python 표준 DB-API인 PEP 249를 따르고, 방언은 SQLAlchemy 공식 테스트 스위트를 통과하고, AI 서버는 MCP 표준을 따릅니다.
그리고 저희도 SQLAlchemy, node-cubrid 같은 오픈소스의 어깨 위에서 만들었습니다.
-->

---

<p class="huge">MIT × 4</p>
<h2>누구나 가져다 쓸 수 있게.</h2>
<p class="sub">의존성 어디에도 GPL은 없습니다. CUBRID 서버(Apache-2.0 · BSD) 라이선스도 원문으로 확인했고, 모든 릴리스에 SBOM을 붙입니다.</p>

<!--
[9:00–9:15 · 15초 · 라이선스]
4개 패키지 모두 MIT입니다. 의존성 어디에도 GPL은 없고, CUBRID 서버 라이선스도 원문으로 확인했습니다.
모든 릴리스에는 SBOM을 붙입니다.
-->

---

<h2>저희 말 대신,<br><span class="accent">직접 확인해 보세요</span></h2>

```bash
uvx cubrid-mcp-server             # PyPI v0.4.0
docker compose up && make verify  # 전체 스택
```

<p class="sub">단계별 명령과 기대 결과는 <b>VERIFY.md</b>에 모두 적어 두었습니다.</p>

<!--
[9:15–9:35 · 20초 · 기능테스트]
오늘 말씀드린 내용은 직접 확인하실 수 있습니다. 명령어 한 줄로 AI 서버를 띄울 수 있고,
VERIFY.md에 단계별 명령과 기대 결과를 모두 적어 두었습니다.
-->

---

<p class="kicker">부풀리지 않은 숫자만 가져왔습니다</p>

<div class="figures">
  <div><b class="accent">450</b><span>병합된 PR</span></div>
  <div><b>2,200</b><span>테스트</span></div>
  <div><b>35</b><span>PyPI 릴리스</span></div>
  <div><b>119</b><span>GitHub 스타</span></div>
</div>

<p class="sub">클론 수는 뺐습니다. 재 보니 대부분 저희 CI였거든요.</p>

<!--
[9:35–10:05 · 30초 · 활용성]
숫자는 검증할 수 있는 것만 가져왔습니다. 병합된 PR 450개, 테스트 2,200개, PyPI 릴리스 35번.
사실 클론 수가 더 커 보이는 숫자였는데, 측정해 보니 대부분 저희 CI였습니다. 그래서 뺐습니다.
-->

---

<div class="chapter"><span class="no">06</span><h1>다음</h1><span class="of">Python에서 검증한 순서를, 다른 언어로</span></div>

<!--
[10:05–10:10 · 5초] (넘기면서) 마지막으로, 다음 이야기입니다.
-->

---

<h2>드라이버 → ORM → 예제 → AI</h2>

<ul class="lines">
  <li>Python에서 검증한 이 순서를 <span class="accent">TypeScript · Go · Rust</span>에서 진행 중입니다.</li>
  <li class="muted">문서 · 예제 · 멘토링이 붙은 good-first-issue로 다음 기여자를 모읍니다.</li>
</ul>

<!--
[10:10–10:35 · 25초 · 커뮤니티 · 발전가능성]
Python은 끝이 아니라 레퍼런스입니다. 드라이버, ORM, 예제, AI로 이어지는 같은 순서를 TypeScript, Go, Rust에서도 진행하고 있습니다.
커뮤니티는 SQLAlchemy Korea를 운영해 온 방식 그대로, 문서와 예제, 멘토링이 붙은 이슈로 키우겠습니다.
-->

---

<div class="split even">
  <div class="stack">
    <h1>6년 전 받은 것을,<br><span class="accent">다음 사람에게.</span></h1>
    <p class="sub">다음 컨트리뷰톤에서, 저희 프로젝트를 이어갈 누군가를 기다립니다.</p>
    <div class="links">
      <div><span>GitHub</span>github.com/cubrid-lab</div>
      <div><span>설치</span>pip install pycubrid</div>
      <div><span>AI</span>uvx cubrid-mcp-server</div>
    </div>
    <p class="thanks">감사합니다 — 최영선 · 백경준</p>
  </div>
  <div class="frame"><Photo src="/photos/team-now.jpg" label="지금의 두 사람 사진" /></div>
</div>

<style>
.frame { height: 400px; }
.thanks { font-size: 1.2rem; font-weight: 700; margin-top: 8px; }
</style>

<!--
[10:35–11:05 · 30초 · PT · 커뮤니티]
6년 전 저희는 컨트리뷰톤에서 오픈소스로부터 많은 것을 받았습니다. 오늘은 그걸 생태계로 돌려드리러 왔습니다.
다음 컨트리뷰톤 어딘가에서, 저희 프로젝트를 이어갈 누군가를 기다리겠습니다. 감사합니다.
-->
