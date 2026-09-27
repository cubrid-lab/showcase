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
  <p class="sub">CUBRID Python 생태계 — pycubrid · sqlalchemy-cubrid · cubrid-cookbook · cubrid-mcp-server</p>
  <div class="who">
    <b>최영선 · 백경준</b>
    <span>CUBRID Lab</span>
  </div>
</div>

<style>
.cover { display: grid; gap: 22px; }
.cover h1 { font-size: 3.8rem; line-height: 1.12; }
.cover .sub { max-width: none; font-size: 1.05rem; }
.who { display: flex; gap: 14px; align-items: baseline; margin-top: 26px; padding-top: 18px; border-top: 2px solid var(--ink); width: fit-content; }
.who b { font-size: 1.1rem; }
.who span { font-size: 0.9rem; color: var(--muted); }
</style>

<!--
[10초 · PT]
안녕하세요. "공공 DBMS에 Python 문을 열다", CUBRID Lab의 최영선, 백경준입니다.
-->

---

<div class="chapter"><span class="no">01</span><h1>만남과 발견</h1><span class="of">왜 만들었나</span></div>

<!--
[4초] (넘기면서) 먼저, 저희가 왜 이걸 만들었는지부터 말씀드리겠습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">2020년, 오픈소스 컨트리뷰톤</p>
    <h1>두 사람이<br>만났습니다</h1>
    <p class="sub">멘토 최영선, 멘티 백경준. NIPA 오픈소스 컨트리뷰톤에서 SQLAlchemy 프로젝트로 처음 만났습니다.</p>
  </div>
  <div class="frame"><Photo src="/photos/team-2020.jpg" label="2020 컨트리뷰톤 사진" /></div>
</div>

<style>
.frame { height: 380px; }
</style>

<!--
[15초 · PT · 커뮤니티]
저희 둘은 2020년, NIPA 오픈소스 컨트리뷰톤에서 멘토와 멘티로 처음 만났습니다.
-->

---

<ul class="lines big-lines">
  <li>SQLAlchemy에 기여하며 오픈소스를 배웠고,</li>
  <li>Gitter에서 창시자 <span class="accent">Mike Bayer</span>와 대화했고,</li>
  <li><span class="accent">SQLAlchemy Korea</span> 커뮤니티를 만들었습니다.</li>
</ul>
<p class="note-line">이 경험이 뒤에 나올 모든 것 — 방언, 드라이버, 리뷰 방식, 커뮤니티 — 의 출발점입니다.</p>

<style>
.big-lines li { font-size: 2rem; }
</style>

<!--
[15초 · 커뮤니티]
그때 SQLAlchemy에 기여하면서 오픈소스를 배웠고, Gitter에서 창시자 Mike Bayer와 대화했고,
SQLAlchemy Korea라는 커뮤니티도 만들었습니다. 오늘 이야기는 여기서 시작합니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">한국 공공부문 DBMS 점유율</p>
    <h2>CUBRID는 이제<br><span class="accent">공공 DBMS 2위</span>입니다</h2>
    <ul class="explain">
      <li><b>13.24%</b> — 공공기관 2,367곳에 설치 (2025년 말)</li>
      <li><b>Microsoft를 넘었습니다</b> — 국산 DBMS로는 처음</li>
      <li><b>5년째 상승</b> — 7.80% → 13.24%</li>
    </ul>
    <p class="small">출처: 행정안전부·NIA 「범정부EA기반 공공부문 정보자원 현황 통계보고서」 (각 전년 말 기준) · 2021–2023년 값은 큐브리드 보도자료 인용</p>
  </div>
  <div class="stack charts">
    <BarChart :width="400" :label-width="100" :rows="[
      { label: 'Oracle', value: 59.87, text: '59.87%' },
      { label: 'CUBRID', value: 13.24, text: '13.24%', hl: true },
      { label: 'Microsoft', value: 12.59, text: '12.59%' },
      { label: 'Tmax', value: 9.62, text: '9.62%' },
      { label: 'MariaDB', value: 4.67, text: '4.67%' },
    ]" />
    <p class="chart-cap">CUBRID 점유율 추이</p>
    <TrendColumns :width="380" :height="150" unit="%" :points="[
      { x: '2021', y: 7.80 }, { x: '2022', y: 8.27 }, { x: '2023', y: 9.13 }, { x: '2024', y: 10.58 }, { x: '2025', y: 13.24 },
    ]" />
  </div>
</div>

<style>
.charts { gap: 12px; }
.chart-cap { font-size: 0.8rem; font-weight: 700; color: var(--muted); margin-top: 10px; }
</style>

<!--
[25초 · 활용성]
그러다 한 가지를 알게 됐습니다. CUBRID는 지금 한국 공공부문 DBMS 점유율 2위입니다.
2025년 말 기준 13.24%, 2천 3백 곳이 넘는 공공기관에서 쓰고, 국산 DBMS로는 처음으로 Microsoft를 앞질렀습니다.
그리고 5년째 계속 오르고 있습니다.
-->

---

<p class="kicker">그런데 Python에서는</p>
<h1><span class="seal">2014년 5월 15일.</span></h1>
<p class="sub">공식 Python 드라이버의 마지막 릴리스입니다.</p>
<ul class="explain">
  <li><b>C 확장</b> — 설치하려면 컴파일러와 빌드 도구가 필요</li>
  <li><b>asyncio 없음</b> — FastAPI 같은 비동기 서버에서 쓰기 어려움</li>
  <li><b>SQLAlchemy 2 없음</b> — Mike Bayer의 2012년 방언도 멈춰 있었음</li>
</ul>

<!--
[15초 · 활용성]
그런데 Python에서 이 데이터베이스를 쓰려고 하니, 공식 드라이버의 마지막 릴리스가 2014년 5월이었습니다.
C 확장이라 설치부터 어렵고, asyncio도, SQLAlchemy 2도 쓸 수 없었습니다.
-->

---

<h1>그래서,<br><span class="accent">고쳐보기로 했습니다.</span></h1>

<!--
[5초 · PT]
그래서 저희가 고쳐보기로 했습니다.
-->

---

<div class="chapter"><span class="no">02</span><h1>만든 것</h1><span class="of">네 개의 프로젝트, 하나의 생태계</span></div>

<!--
[4초] (넘기면서) 저희가 만든 네 가지를 보여드리겠습니다.
-->

---

<h2>한 장으로 보면</h2>

<div class="arch">
  <div class="path">
    <span class="label">애플리케이션에서</span>
    <div class="node">FastAPI · Django · Flask · pandas <small>여러분의 코드</small></div>
    <div class="down">↓</div>
    <div class="node">SQLAlchemy <small>Python 표준 ORM</small></div>
    <div class="down">↓</div>
    <div class="node ours">sqlalchemy-cubrid <small>방언 · 2021</small></div>
    <div class="down">↓</div>
    <div class="node ours">pycubrid <small>드라이버 · 2025</small></div>
    <div class="down">↓</div>
    <div class="node db">CUBRID <small>CAS 프로토콜 · TCP 33000</small></div>
  </div>
  <div class="path">
    <span class="label">AI에서</span>
    <div class="node">Claude · Cursor <small>MCP 클라이언트</small></div>
    <div class="down">↓</div>
    <div class="node ours">cubrid-mcp-server <small>AI 접근 · 2026</small></div>
    <div class="down">↓</div>
    <div class="node ours">pycubrid <small>같은 드라이버</small></div>
    <div class="down">↓</div>
    <div class="node db">CUBRID</div>
  </div>
</div>
<div class="cook">
  <b>cubrid-cookbook</b> <small>2026</small> — 이 모든 경로를 예제 68개 · 템플릿 7개로 보여주고, 매일 밤 실서버에서 검증합니다
</div>

<style>
.cook { border-top: 2px solid var(--blue); padding-top: 10px; font-size: 0.95rem; color: var(--muted); }
.cook b { color: var(--blue); }
.cook small { font-size: 0.75rem; }
</style>

<!--
[25초 · 활용성 · OSS 적절성]
한 장으로 보면 이렇습니다. 애플리케이션은 SQLAlchemy를 거쳐 저희 방언과 드라이버로 CUBRID에 닿고,
AI는 저희 MCP 서버를 거쳐 같은 드라이버로 닿습니다. 모든 길의 바닥에는 pycubrid가 있습니다.
그리고 cookbook이 이 모든 경로를 예제로 보여주고, 매일 밤 실서버에서 검증합니다. 하나씩 보겠습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">프로젝트 1 · sqlalchemy-cubrid · 2021–22</p>
    <h2>Mike Bayer의 방언을<br>처음부터 다시 썼습니다</h2>
    <p class="sub">방언은 SQLAlchemy가 CUBRID의 SQL을 말하게 해 주는 번역기입니다.</p>
  </div>
  <ul class="explain">
    <li><b>SQLAlchemy 2.0 기준</b>으로 새로 작성 — 2012년 코드는 가져오지 않았습니다</li>
    <li><b>공식 테스트 스위트 통합</b> — 호환 플래그 53개로 지원 범위를 명시</li>
    <li><b>스키마 리플렉션</b>, CUBRID 전용 <b>MERGE · ON DUPLICATE KEY · REPLACE</b></li>
    <li><b>Alembic 마이그레이션</b>, 동기·<b>비동기</b> 드라이버 URL 모두 지원</li>
  </ul>
</div>

<!--
[25초 · OSS 적절성]
첫 번째는 sqlalchemy-cubrid입니다. 방언은 SQLAlchemy가 CUBRID의 SQL을 말하게 해 주는 번역기입니다.
Mike Bayer의 2012년 방언을 가져다 고친 게 아니라, SQLAlchemy 2.0 기준으로 처음부터 다시 썼습니다.
SQLAlchemy 공식 테스트 스위트를 붙였고, 스키마 리플렉션과 CUBRID 전용 MERGE 문, Alembic 마이그레이션까지 지원합니다.
-->

---

<p class="kicker">프로젝트 1 · sqlalchemy-cubrid — 이렇게 씁니다</p>

```python
from sqlalchemy import create_engine, MetaData, Table, select, func

engine = create_engine("cubrid+pycubrid://dba@localhost:33000/demodb")
agencies = Table("agencies", MetaData(),
                 autoload_with=engine)          # 스키마 리플렉션

with engine.connect() as conn:
    stmt = (select(agencies.c.region, func.count())
            .group_by(agencies.c.region))
    print(conn.execute(stmt).all())   # [('서울', 2), ('세종', 10)]
```

<p class="then">그런데 방언 밑의 드라이버가 <span class="seal">2014년에 멈춘 C 확장</span>이었습니다.</p>

<style>
.then { font-size: 1.35rem; font-weight: 700; line-height: 1.4; border-left: 4px solid var(--seal); padding-left: 16px; }
pre.slidev-code { font-size: 0.9rem !important; }
</style>

<!--
[15초 · 활용성]
쓰는 법은 다른 데이터베이스와 똑같습니다. URL 하나 바꾸면 SQLAlchemy 코드가 그대로 CUBRID에서 돕니다.
그런데 문제가 있었습니다. 방언 밑의 드라이버가 2014년에 멈춘 C 확장이었습니다.
-->

---

<h1>드라이버를 만들려고 보니,<br><span class="seal">프로토콜 문서가 없었습니다.</span></h1>

<!--
[10초 · PT]
그래서 드라이버를 새로 만들기로 했는데, 가장 큰 벽은 CUBRID 통신 프로토콜 문서가 없다는 것이었습니다.
-->

---

<p class="kicker">프로젝트 2 · pycubrid — 문서 대신 두 드라이버의 소스를 나란히 놓고 읽었습니다</p>

<div class="packet">
  <div><b>4B</b><span>length — 본문 길이</span></div>
  <div><b>4B</b><span>cas_info — 서버 상태</span></div>
  <div><b>payload</b><span>요청·응답 본문 · CAS 바이너리 프로토콜 · TCP 33000</span></div>
</div>

<ul class="explain">
  <li><b>node-cubrid</b>(Node.js, BSD)와 <b>공식 C 드라이버</b> 소스를 한 줄씩 대조했습니다</li>
  <li>모든 요청과 응답이 위 한 가지 형식을 따른다는 걸 확인하고, 읽기·쓰기 계층을 따로 만들었습니다</li>
</ul>

<div class="figures">
  <div><b>18</b><span>패킷 타입</span></div>
  <div><b>27</b><span>데이터 타입</span></div>
  <div><b class="accent">0</b><span>런타임 의존성</span></div>
</div>

<!--
[20초 · OSS 적절성 · 라이선스]
그래서 BSD 라이선스인 node-cubrid와 공식 C 드라이버 소스를 나란히 놓고 한 줄씩 비교했습니다.
모든 요청과 응답이 길이, 서버 상태, 본문이라는 한 가지 형식을 따른다는 걸 찾아냈고,
그렇게 18개 패킷 타입과 27개 데이터 타입을 해독해서, 의존성이 하나도 없는 순수 Python 드라이버를 만들었습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">프로젝트 2 · pycubrid · 2025</p>

```bash
pip install pycubrid
```

  <h2>C 컴파일러 없이,<br>한 줄이면 끝납니다</h2>
  </div>
  <ul class="explain">
    <li><b>PEP 249</b> — Python 표준 DB-API. 다른 DB 드라이버와 같은 사용법</li>
    <li><b>asyncio 네이티브</b> — <code>pycubrid.aio</code>로 FastAPI 같은 비동기 서버에서 바로</li>
    <li><b>TLS</b> 암호화 연결, <b>BLOB · CLOB</b> 대용량 데이터</li>
    <li><b>브로커 재연결 자동 처리</b>, 메모리를 넘기지 않는 분할 fetch</li>
    <li><b>테스트 1,147개</b> · 타입 정보 제공 (mypy strict 오류 0)</li>
  </ul>
</div>

<!--
[25초 · 활용성 · 기능테스트]
그 결과가 pycubrid입니다. pip install 한 줄이면 끝나고, C 컴파일러도 필요 없습니다.
Python 표준 DB-API를 따르니 다른 데이터베이스와 쓰는 법이 같고, asyncio를 기본 지원해서 FastAPI 같은 비동기 서버에서 바로 쓸 수 있습니다.
TLS 암호화와 대용량 데이터도 지원하고, 테스트는 1,147개입니다.
-->

---

<div class="split">
  <div class="stack">
    <p class="kicker">프로젝트 3 · cubrid-cookbook · 2026</p>
    <h2>만들고 나니,<br>쓰는 법을 보여줘야 했습니다</h2>
    <ul class="explain">
      <li><b>기초 예제 68개</b> — 연결 · CRUD · 트랜잭션 · LOB · pandas · async · Alembic</li>
      <li><b>프로덕션 템플릿 7개</b> — FastAPI · Django · Flask · Streamlit 대시보드 · Celery · pandas ETL · AI 에이전트</li>
      <li><b>문서 4개 사이트</b> · 한국어 34페이지</li>
    </ul>
  </div>
  <figure class="shot clip"><img src="/shots/docs-pycubrid.jpg" alt="pycubrid 문서 사이트"></figure>
</div>

<!--
[25초 · 활용성]
드라이버를 만들고 나니, 사람들이 실제로 쓰는 법을 보여줘야 했습니다.
그래서 cookbook에 연결부터 비동기, pandas까지 68개 기초 예제와, FastAPI, Django, 대시보드, AI 에이전트 같은 7개 템플릿을 만들었습니다.
문서는 4개 사이트, 한국어로 34페이지를 썼습니다.
-->

---

<p class="kicker">프로젝트 3 · cubrid-cookbook — 예제가 곧 테스트입니다</p>
<h2>매일 밤, cookbook이 드라이버를 먼저 씁니다</h2>

<div class="nightly">
  <div class="node">매일 밤 CI</div><span class="arr">→</span>
  <div class="node">골든 예제 45개 실행</div><span class="arr">→</span>
  <div class="node db">실서버 CUBRID 11.2 · 11.4</div><span class="arr">→</span>
  <div class="node ours">결과가 기대값과 다르면 실패</div>
</div>

<p class="sub">니치 시장에서는 사용자가 버그를 알려주지 않습니다. 그래서 저희가 첫 번째 사용자가 됩니다 — 드라이버에 문제가 생기면 cookbook이 가장 먼저 잡습니다.</p>

<style>
.nightly { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.nightly .arr { color: var(--muted); }
.nightly + .sub { max-width: 52ch; }
</style>

<!--
[15초 · 기능테스트]
이 예제들은 문서로 끝나지 않습니다. 매일 밤 45개 골든 예제를 실제 CUBRID 11.2와 11.4 서버에서 돌리고, 결과가 기대값과 다르면 실패합니다.
그래서 드라이버에 문제가 생기면 사용자보다 cookbook이 먼저 잡습니다.
-->

---

<div class="split">
  <div class="stack">
    <p class="kicker">프로젝트 4 · cubrid-mcp-server · 2026</p>
    <h2>AI가 CUBRID에<br>직접 물어볼 수 있게</h2>
    <p class="sub">MCP는 Claude 같은 AI가 외부 도구와 데이터에 접근하는 표준 프로토콜입니다.</p>
    <ul class="explain">
      <li><b>도구 12개</b> — 테이블 목록 · 스키마 · 인덱스 · 실행 계획 · 쿼리 실행</li>
      <li><b>기본 읽기 전용</b> — 쓰기는 운영자가 켤 때만</li>
      <li>저희가 찾아본 범위에서 <b>세계 최초의 CUBRID MCP 서버</b>, PyPI v0.4.0</li>
    </ul>
  </div>
  <figure class="shot clip"><img src="/shots/repo-mcp.jpg" alt="cubrid-mcp-server 저장소"></figure>
</div>

<!--
[25초 · 활용성 · OSS 적절성]
그리고 AI가 데이터를 묻는 시대가 왔습니다. MCP는 Claude 같은 AI가 외부 도구에 접근하는 표준 프로토콜인데,
CUBRID용 MCP 서버를 만들었습니다. 테이블 목록, 스키마, 인덱스, 실행 계획, 쿼리 실행까지 12개 도구를 제공하고, 기본은 읽기 전용입니다.
저희가 찾아본 범위에서 세계 최초의 CUBRID MCP 서버입니다.
-->

---

<p class="kicker">프로젝트 4 · cubrid-mcp-server — AI는 CUBRID SQL을 모릅니다</p>
<h2>그래서 서버가 AI에게 가르칩니다</h2>

<ul class="explain wide">
  <li><b>도메인 지식 5종</b> — CUBRID의 LIMIT 문법, 컬렉션 타입, SHOW TRACE 같은 차이를 문서로 제공</li>
  <li><b>전문가 프롬프트 5종</b> — 스키마 점검, 인덱스 후보 찾기, 실행 계획 해석 같은 자주 하는 작업</li>
  <li><b>스키마 리소스</b> — AI가 쿼리를 쓰기 전에 테이블 구조부터 읽게 합니다</li>
</ul>

<p class="note-line">사전 지식 없는 AI도 올바른 CUBRID SQL을 씁니다 — 서버가 알려주니까요.</p>

<style>
.wide { max-width: 64ch; }
.wide li { font-size: 1.12rem; }
</style>

<!--
[15초 · 활용성]
그런데 AI는 CUBRID SQL을 잘 모릅니다. 그래서 서버가 가르칩니다.
CUBRID 문법의 차이를 도메인 지식 문서로, 자주 하는 작업을 전문가 프롬프트로 제공해서, 사전 지식 없는 AI도 올바른 SQL을 쓰게 만들었습니다.
-->

---

<div class="chapter"><span class="no">03</span><h1>만든 방법</h1><span class="of">두 사람이, 어떻게 네 개를?</span></div>

<!--
[4초 · PT]
여기서 이런 질문이 드실 겁니다. 두 사람이 어떻게 이걸 다 만들었냐고요.
-->

---

<div class="split">
  <div class="stack">
    <h2>AI가 쓰고,<br><span class="accent">사람이 책임집니다</span></h2>
    <ul class="explain">
      <li><b>규칙</b>은 사람이 <code>AGENTS.md</code>에 씁니다</li>
      <li><b>구현</b>은 AI가 — 코드 · 테스트 · 문서</li>
      <li><b>리뷰</b>는 사람이 — 모든 PR</li>
      <li><b>병합</b>은 CI 검사를 모두 통과한 뒤에만</li>
      <li><b>릴리스 태그</b>는 사람만</li>
    </ul>
    <p class="small">컨트리뷰톤에서 배운 멘토–멘티 방식 그대로: AI가 구현하고, 저희가 리뷰합니다.</p>
  </div>
  <figure class="shot clip"><img src="/shots/merged-prs.jpg" alt="병합된 PR 목록 — 모든 PR에 CI 30/30 통과"></figure>
</div>

<!--
[30초 · 커뮤니티]
답은 AI가 쓰고, 사람이 책임지는 구조입니다.
사람이 AGENTS.md에 규칙을 쓰고, AI가 구현하고, 모든 PR은 사람이 리뷰하고, CI를 통과해야만 병합되고, 릴리스 태그는 사람만 찍습니다.
오른쪽이 실제 PR 목록입니다. 컨트리뷰톤에서 배운 멘토-멘티 방식 그대로입니다.
-->

---

<h1>"AI가 쓴 코드를<br>믿을 수 있나요?"</h1>

<!--
[5초 · 기능테스트]
그럼 당연히 다음 질문이 나옵니다. AI가 쓴 코드를 믿을 수 있냐.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">믿지 않아도 되게 만들었습니다</p>
    <p class="huge sm">2,200</p>
    <h2>개의 테스트를 통과 못 하면,<br>머지되지 않습니다</h2>
    <BarChart :width="360" :label-width="130" :bar="18" :gap="10" :rows="[
      { label: 'pycubrid', value: 1147, text: '1,147', hl: true },
      { label: 'sqlalchemy-cubrid', value: 769, text: '769' },
      { label: 'mcp-server', value: 284, text: '284' },
    ]" />
  </div>
  <ul class="explain">
    <li><b>타입 오류 0</b> — mypy strict</li>
    <li><b>커버리지 95% 이상</b> — 미달이면 머지 불가</li>
    <li><b>랜덤 입력 테스트</b> — hypothesis로 엣지 케이스 탐색</li>
    <li><b>공개 API 변경 감지</b> — 몰래 바뀌면 실패</li>
    <li><b>SQLAlchemy 공식 스위트</b> — 방언 호환성</li>
    <li><b>20개 조합</b> — Python 5 × CUBRID 4 라이브 DB</li>
  </ul>
</div>

<style>
.huge.sm { font-size: 5rem; }
</style>

<!--
[25초 · 기능테스트]
저희는 믿지 않아도 되게 만들었습니다. 테스트가 2,200개이고, 통과하지 못하면 머지 자체가 안 됩니다.
타입 오류 0, 커버리지 95%, 랜덤 입력 테스트, 공개 API 변경 감지,
그리고 Python 5개 버전과 CUBRID 4개 버전, 20개 조합의 실제 DB에서 검증합니다.
-->

---

<p class="kicker">니치 시장엔 성능을 알려줄 사용자가 없습니다. 그래서 직접 쟀습니다.</p>

<div class="split even perf">
  <div class="stack">
    <p class="chart-cap">처리량 — 기존 방식 = 1×</p>
    <PairChart :width="380" :label-width="130" before-name="기존" after-name="최적화" :rows="[
      { label: '연결 확인', before: 1, after: 3.8, beforeText: '1×', afterText: '3.8×' },
      { label: '연결 풀 체크', before: 1, after: 6.88, beforeText: '1×', afterText: '6.9×' },
    ]" />
    <p class="small">연결 확인: SELECT 1 대신 프로토콜 수준의 CHECK_CAS 사용</p>
  </div>
  <div class="stack">
    <p class="chart-cap">걸린 시간 — 짧을수록 좋음</p>
    <PairChart :width="380" :label-width="130" :rows="[
      { label: 'INSERT 1,000행', before: 100, after: 2512 / 2865 * 100, beforeText: '2,865ms', afterText: '2,512ms' },
      { label: '전체 조회', before: 100, after: 31.8 / 39.8 * 100, beforeText: '39.8ms', afterText: '31.8ms' },
    ]" />
    <p class="small">막대는 행마다 개선 전을 기준으로 그렸습니다. 재현: cubrid-benchmark</p>
  </div>
</div>

<p class="note-line">순수 Python이라 C 드라이버보다는 느립니다. 대신 설치 · asyncio · 이식성을 얻었고, 그 격차를 측정하며 줄이고 있습니다.</p>

<style>
.chart-cap { font-size: 0.85rem; font-weight: 700; color: var(--ink); }
.perf { align-items: start; }
</style>

<!--
[25초 · 기능테스트]
큰 오픈소스는 사용자가 성능 문제를 알려주지만, 니치 시장은 그렇지 않아서 벤치마크 저장소를 따로 만들어 직접 쟀습니다.
연결 확인을 SELECT 1 대신 프로토콜 수준으로 바꿔 처리량이 3.8배, 연결 풀 체크는 6.9배가 됐고, 대량 INSERT와 조회도 12%, 20% 빨라졌습니다.
솔직히 순수 Python이라 C 드라이버보다는 느립니다. 대신 설치와 비동기, 이식성을 얻었고, 그 격차를 계속 줄이고 있습니다.
-->

---

<div class="chapter"><span class="no">04</span><h1>직접 보여드리겠습니다</h1><span class="of">행안부 전자결재(온나라) 데이터로</span></div>

<!--
[4초] (넘기면서) 그럼, 실제로 어떻게 쓰이는지 직접 보여드리겠습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">라이브 데모 · 2분</p>
    <h2>온나라형 데이터에<br>AI로 묻습니다</h2>
    <ul class="explain">
      <li><b>데이터</b> — 기관 12 · 결재 문서 300 · 결재 이력 753건</li>
      <li><b>경로</b> — Claude → cubrid-mcp-server → pycubrid → CUBRID</li>
      <li><b>순서</b> — 대시보드 15초 → Claude 90초 → 터미널 15초</li>
    </ul>
  </div>
  <ol class="asks">
    <li><span>"이 DB에 어떤 테이블이 있어?"</span></li>
    <li><span>"결재가 지연된 문서 TOP 5는? 평균 처리일과 대기 수로"</span></li>
    <li><span>"기밀 문서는 부처별로 몇 개야? 내용은 보지 말고 집계만"</span></li>
    <li><span>"결재 대기 문서를 전부 승인 처리해줘"</span><span class="stamp">반려</span></li>
  </ol>
</div>

<style>
.asks li { font-size: 1.05rem; }
</style>

<!--
[2분 · 데모 · DEMO_RUNBOOK.md]
행안부 온나라는 47개 부처가 쓰는 CUBRID 기반 전자결재 시스템입니다. 지금까지는 Java 중심이었습니다.
이 데이터를 Python과 AI로 다뤄보겠습니다. 대시보드부터 보시죠. (대시보드 15초 → Claude 90초 → 터미널 15초)
(#2 후) AI가 데이터를 읽기만 하는 게 아니라, 평균 처리일과 대기 수로 결재 병목을 스스로 분석했습니다.
(#4 후) 결재 대기 문서를 전부 승인하라는 명령은, 서버에서 반려됐습니다.
-->

---

<h1>기본은 <span class="accent">읽기 전용</span>입니다</h1>

<ul class="explain wide2">
  <li><b>쓰기 도구는 보이지도 않습니다</b> — 기본 모드에서는 AI에게 쓰기 도구 자체가 등록되지 않습니다</li>
  <li><b>허용 목록</b> — 쿼리 도구는 SELECT · SHOW · DESC · EXPLAIN · WITH만 실행하고, 여러 문장을 이어 붙이면 거부합니다</li>
  <li><b>쓰기는 운영자가 연결별로 직접 켤 때만</b> — 그때도 INSERT · UPDATE · DELETE 한 문장씩만, DDL은 불가</li>
</ul>
<p class="note-line">실제 운영에서는 SELECT 권한만 가진 DB 계정으로 연결하기를 권합니다.</p>

<style>
.wide2 { max-width: 66ch; }
.wide2 li { font-size: 1.1rem; }
</style>

<!--
[15초 · 데모 · 기능테스트]
방금 보신 반려는 이렇게 동작합니다. 기본 모드에서는 쓰기 도구가 AI에게 보이지도 않고, 쿼리 도구는 조회 문장만 허용합니다.
쓰기는 운영자가 연결별로 직접 켤 때만 가능하고, 그때도 한 문장씩만입니다. 실제 운영에서는 조회 권한만 가진 계정을 권합니다.
-->

---

<div class="chapter"><span class="no">05</span><h1>믿을 수 있는 이유</h1><span class="of">표준 · 라이선스 · 검증 · 숫자</span></div>

<!--
[4초] (넘기면서) 이제, 이걸 믿고 쓰셔도 되는 이유입니다.
-->

---

<h2>저희끼리 정한 규칙이 아니라,<br><span class="accent">표준 위에 올렸습니다</span></h2>

<ul class="lines std">
  <li>PEP 249 <span class="muted">— Python 표준 DB-API · pycubrid</span></li>
  <li>PEP 561 <span class="muted">— 타입 정보 제공 · 세 패키지 모두</span></li>
  <li>SQLAlchemy Dialect API <span class="muted">— 공식 테스트 스위트 · sqlalchemy-cubrid</span></li>
  <li>Model Context Protocol <span class="muted">— 도구 · 리소스 · 프롬프트 · cubrid-mcp-server</span></li>
</ul>
<p class="note-line">기반 오픈소스: SQLAlchemy(MIT) · node-cubrid(BSD, 프로토콜 참고) · FastMCP · pytest · hypothesis</p>

<style>
.std li { font-size: 1.3rem; }
</style>

<!--
[20초 · OSS 적절성]
저희가 만든 건 저희끼리만 통하는 규칙이 아닙니다. 드라이버는 PEP 249, 방언은 SQLAlchemy 공식 스위트, AI 서버는 MCP 표준을 따릅니다.
그리고 저희도 SQLAlchemy, node-cubrid 같은 오픈소스의 어깨 위에서 만들었습니다.
-->

---

<p class="huge">MIT × 4</p>
<h2>누구나 가져다 쓸 수 있게.</h2>
<ul class="explain">
  <li><b>네 패키지 모두 MIT</b> — 의존성 어디에도 GPL 없음</li>
  <li><b>CUBRID 서버</b>(Apache-2.0 엔진 · BSD 커넥터) 라이선스도 원문으로 확인</li>
  <li><b>모든 릴리스에 SBOM</b>(SPDX) · THIRD_PARTY_LICENSES · NOTICE</li>
</ul>

<!--
[12초 · 라이선스]
4개 패키지 모두 MIT입니다. 의존성 어디에도 GPL은 없고, CUBRID 서버 라이선스도 원문으로 확인했습니다. 모든 릴리스에는 SBOM을 붙입니다.
-->

---

<h2>저희 말 대신,<br><span class="accent">직접 확인해 보세요</span></h2>

```bash
uvx cubrid-mcp-server             # PyPI v0.4.0
docker compose up && make verify  # 전체 스택
```

<p class="sub"><b>VERIFY.md</b> — 드라이버 연결 → ORM → MCP 서버 → 실서버 골든 테스트 → SBOM · 라이선스, 단계마다 명령과 기대 결과를 적어 두었습니다.</p>

<!--
[15초 · 기능테스트]
오늘 말씀드린 내용은 직접 확인하실 수 있습니다. 명령어 한 줄로 AI 서버를 띄울 수 있고,
VERIFY.md에 단계별 명령과 기대 결과를 모두 적어 두었습니다.
-->

---

<p class="kicker">부풀리지 않은 숫자만 가져왔습니다 · 2026-09-12 기준</p>

<div class="split even nums">
  <div class="stack">
    <p class="chart-cap">병합된 PR — 총 450개</p>
    <BarChart :width="380" :label-width="150" :bar="20" :gap="12" :rows="[
      { label: 'pycubrid', value: 159, hl: true },
      { label: 'sqlalchemy-cubrid', value: 151 },
      { label: 'cubrid-mcp-server', value: 84 },
      { label: 'cubrid-cookbook', value: 56 },
    ]" />
  </div>
  <div class="stack">
    <p class="chart-cap">PyPI 릴리스 — 총 35번</p>
    <BarChart :width="380" :label-width="150" :bar="20" :gap="12" :rows="[
      { label: 'sqlalchemy-cubrid', value: 19, hl: true },
      { label: 'pycubrid', value: 16 },
    ]" />
    <p class="small">GitHub 스타 119 (네 저장소 합계)</p>
  </div>
</div>

<p class="note-line">클론 수는 뺐습니다. 재 보니 대부분 저희 CI였습니다 — 14일간 pycubrid는 클론 4,969회, 같은 기간 CI 실행 700회(실행 한 번에 여러 잡이 저장소를 받습니다).</p>

<style>
.chart-cap { font-size: 0.85rem; font-weight: 700; }
.nums { align-items: start; }
</style>

<!--
[25초 · 활용성]
숫자는 검증할 수 있는 것만 가져왔습니다. 병합된 PR 450개, PyPI 릴리스 35번.
사실 클론 수가 더 커 보이는 숫자였는데, 측정해 보니 대부분 저희 CI였습니다. 그래서 뺐습니다.
-->

---

<div class="chapter"><span class="no">06</span><h1>다음</h1><span class="of">Python에서 검증한 순서를, 다른 언어로</span></div>

<!--
[4초] (넘기면서) 마지막으로, 다음 이야기입니다.
-->

---

<h2>드라이버 → ORM → 예제 → AI</h2>
<p class="sub">Python에서 검증한 이 순서를 다른 언어에도 그대로 적용하고 있습니다.</p>

<ul class="explain langs">
  <li><b>Python</b> — pycubrid · sqlalchemy-cubrid <span class="muted">v1.7.1 · 완성</span></li>
  <li><b>TypeScript</b> — cubrid-client · drizzle-cubrid <span class="muted">진행 중</span></li>
  <li><b>Go</b> — cubrid-go · gorm-cubrid <span class="muted">진행 중</span></li>
  <li><b>Rust</b> — cubrid-rs · sea-orm-cubrid <span class="muted">진행 중</span></li>
</ul>
<p class="note-line">커뮤니티는 SQLAlchemy Korea를 운영해 온 방식 그대로 — 문서 · 예제 · 멘토링이 붙은 good-first-issue로 다음 기여자를 모읍니다.</p>

<style>
.langs li { font-size: 1.15rem; }
</style>

<!--
[20초 · 커뮤니티 · 발전가능성]
Python은 끝이 아니라 레퍼런스입니다. 드라이버, ORM, 예제, AI로 이어지는 같은 순서를 TypeScript, Go, Rust에서도 진행하고 있습니다.
커뮤니티는 SQLAlchemy Korea를 운영해 온 방식 그대로, 멘토링이 붙은 이슈로 키우겠습니다.
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
[25초 · PT · 커뮤니티]
6년 전 저희는 컨트리뷰톤에서 오픈소스로부터 많은 것을 받았습니다. 오늘은 그걸 생태계로 돌려드리러 왔습니다.
다음 컨트리뷰톤 어딘가에서, 저희 프로젝트를 이어갈 누군가를 기다리겠습니다. 감사합니다.
-->
