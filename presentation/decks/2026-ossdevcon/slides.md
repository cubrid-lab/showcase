---
title: "멈춰 있던 연결을 다시 잇다 — 파이큐브리드팀"
---

<div class="cover">
  <div class="products">
    <div><BrandMark name="pycubrid" alt="pycubrid 아이콘" :height="46" /><span>pycubrid</span></div>
    <div><BrandMark name="sqlalchemy-cubrid" alt="sqlalchemy-cubrid 아이콘" :height="46" /><span>sqlalchemy-cubrid</span></div>
    <div><BrandMark name="cubrid-cookbook-python" alt="cubrid-cookbook 아이콘" :height="46" /><span>cubrid-cookbook</span></div>
    <div><BrandMark name="cubrid-mcp-server" alt="cubrid-mcp-server 아이콘" :height="46" /><span>cubrid-mcp-server</span></div>
  </div>
  <p class="kicker">2026 오픈소스 개발자대회</p>
  <h1>멈춰 있던 연결을<br>다시 잇다</h1>
  <p class="lead">파이큐브리드팀의 CUBRID Python 생태계 구축기</p>
  <div class="who">
    <b>최영선 · 백경준</b>
    <span>파이큐브리드팀</span>
  </div>
</div>

<style>
.cover { display: grid; gap: 20px; }
.cover h1 { font-size: 3.8rem; line-height: 1.12; }
.cover .lead { font-size: 1.45rem; font-weight: 700; letter-spacing: -0.02em; }
.products { display: flex; gap: 26px; margin-bottom: 6px; }
.products > div { display: grid; justify-items: center; gap: 6px; }
.products span { font-family: var(--mono); font-size: 0.7rem; color: var(--muted); }
.who { display: flex; gap: 14px; align-items: baseline; margin-top: 18px; padding-top: 16px; border-top: 2px solid var(--ink); width: fit-content; }
.who b { font-size: 1.1rem; }
.who span { font-size: 0.9rem; color: var(--muted); }
</style>

<!--
[15초 · PT]
안녕하세요. 파이큐브리드팀의 최영선, 백경준입니다. 오늘은 오랫동안 멈춰 있던 CUBRID와 Python 사이의 연결을 어떻게 다시 이었는지 말씀드리겠습니다. 위에 보이는 네 프로젝트가 그 결과입니다.
-->

---

<div class="split meet">
  <div class="stack">
    <p class="kicker">2020년 오픈소스 컨트리뷰톤</p>
    <h2>SQLAlchemy에서<br>멘토와 멘티로 만났습니다</h2>
    <ul class="explain">
      <li><b>SQLAlchemy</b>와 <b>sqlalchemy-hana</b>에 PR을 보내며 데이터베이스별 dialect가 어떻게 만들어지는지 배웠습니다</li>
      <li>창시자 <b class="nw">Mike Bayer</b>와 Gitter에서 이야기를 나눴고, <b class="nw">SQLAlchemy Korea</b> 커뮤니티를 만들었습니다</li>
    </ul>
    <p class="note-line">PR 예: <a class="nw" href="https://github.com/SAP/sqlalchemy-hana/pull/61" target="_blank">SAP/sqlalchemy-hana#61</a> · <a class="nw" href="https://github.com/sqlalchemy/sqlalchemy/pull/5570" target="_blank">sqlalchemy/sqlalchemy#5570</a></p>
  </div>
  <div class="frame"><Photo src="/photos/team-2020.jpg" label="2020 컨트리뷰톤 사진" /></div>
</div>

<style>
.meet { grid-template-columns: 1.35fr 1fr; }
.meet h2 { font-size: 2rem; }
.frame { height: 330px; }
</style>

<!--
[25초 · PT · 커뮤니티]
저희 둘은 2020년 오픈소스 컨트리뷰톤의 SQLAlchemy 프로젝트에서 멘토와 멘티로 만났습니다. SQLAlchemy와 sqlalchemy-hana에 PR을 보내면서, 데이터베이스마다 붙는 dialect가 어떻게 만들어지는지 배웠습니다.
창시자 Mike Bayer와도 이야기를 나눴고, 그 뒤 SQLAlchemy Korea 커뮤니티를 만들었습니다. 이 경험이 있었기에 다음 장의 저장소를 알아볼 수 있었습니다.
-->

---

<p class="kicker">dialect를 공부하다가 찾은 저장소</p>
<h2>CUBRID dialect는 있었지만,<br><span class="seal">멈춰 있었습니다.</span></h2>

<div class="repo">
  <div class="repo-head"><a href="https://github.com/zzzeek/sqlalchemy_cubrid" target="_blank"><b>github.com/zzzeek/sqlalchemy_cubrid</b></a><span>2012년 생성 · 커밋 4개 · 코드 변경은 2012년이 마지막</span></div>
  <div class="readme">
    "…there is not actually anything working here. … if someone were to be interested in this, i will gladly transfer this repo over to them."
    <span class="cite">— Mike Bayer, README (2019)</span>
  </div>
</div>
<p class="then">“관심 있는 사람이 있다면” — 저희가 그 사람이 되기로 했습니다.</p>

<style>
.repo { border: 1.5px solid var(--line); border-radius: 12px; overflow: hidden; }
.repo-head { display: flex; justify-content: space-between; gap: 12px; align-items: baseline; padding: 10px 18px; background: #f6f8fa; border-bottom: 1px solid var(--line); }
.repo-head a { color: var(--ink); text-decoration: none; border: 0; }
.repo-head b { font-family: var(--mono); font-size: 0.9rem; }
.repo-head span { font-size: 0.78rem; color: var(--muted); }
.readme { padding: 18px 22px; font-size: 1.15rem; line-height: 1.55; display: grid; gap: 10px; }
.readme .cite { font-size: 0.85rem; color: var(--muted); }
.then { font-size: 1.3rem; font-weight: 700; line-height: 1.4; border-left: 4px solid var(--blue); padding-left: 16px; }
</style>

<!--
[30초 · 활용성 · 커뮤니티]
sqlalchemy-hana를 고치면서 다른 dialect를 찾아보다가, Mike Bayer의 저장소에서 CUBRID dialect를 발견했습니다. 2012년에 만들어진 뒤 멈춰 있었고, README에는 Mike가 이렇게 적어 두었습니다.
"여기엔 실제로 동작하는 게 없다. 관심 있는 사람이 있다면 기꺼이 넘기겠다." 저희가 그 관심 있는 사람이 되기로 했습니다. 오늘 발표 제목도 이 문장에서 나왔습니다.
-->

---

<h2>CUBRID Python 생태계의 연결 구조</h2>

<div class="arch eco">
  <div class="path">
    <span class="label">애플리케이션에서</span>
    <div class="level">
      <div class="node app"><span>FastAPI · Django · Flask · pandas</span><small>여러분의 코드</small></div>
      <div class="node aside"><BrandMark name="cubrid-cookbook-python" alt="cubrid-cookbook 아이콘" :height="22" /><span><b>cubrid-cookbook</b><small>예제·템플릿 · 실행 경로 밖</small></span></div>
    </div>
    <div class="down">↓</div>
    <div class="node">SQLAlchemy <small>Python ORM</small></div>
    <div class="down">↓</div>
    <div class="node ours"><span class="ic"><BrandMark name="sqlalchemy-cubrid" alt="sqlalchemy-cubrid 아이콘" :height="22" />sqlalchemy-cubrid</span><small>dialect</small></div>
    <div class="down">↓</div>
    <div class="node ours"><span class="ic"><BrandMark name="pycubrid" alt="pycubrid 아이콘" :height="22" />pycubrid</span><small>드라이버</small></div>
    <div class="down">↓</div>
    <div class="node db">CUBRID <small>CAS 프로토콜 · TCP 33000</small></div>
  </div>
  <div class="path">
    <span class="label">AI 도구에서</span>
    <div class="node">Claude · Cursor <small>MCP 클라이언트</small></div>
    <div class="down">↓</div>
    <div class="node ours"><span class="ic"><BrandMark name="cubrid-mcp-server" alt="cubrid-mcp-server 아이콘" :height="22" />cubrid-mcp-server</span><small>MCP 서버</small></div>
    <div class="down">↓</div>
    <div class="node ours"><span class="ic"><BrandMark name="pycubrid" alt="pycubrid 아이콘" :height="22" />pycubrid</span><small>같은 드라이버</small></div>
    <div class="down">↓</div>
    <div class="node db">CUBRID</div>
  </div>
</div>
<p class="note-line">cookbook은 런타임 의존성이 아니라, 애플리케이션 계층의 예제·템플릿이자 매일 도는 실서버 검증입니다.</p>

<style>
.eco { grid-template-columns: 1.45fr 1fr; gap: 22px; }
.eco .node { padding: 5px 12px; }
.eco .level { display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 8px; }
.eco .node.aside b { white-space: nowrap; }
.eco .node.aside { border-style: dashed; border-color: var(--blue); justify-content: flex-start; align-items: center; }
.eco .node.aside span { display: grid; gap: 2px; }
.eco .node.aside b { color: var(--blue); font-size: 0.9rem; }
.eco .node.app { font-size: 0.88rem; flex-direction: column; align-items: flex-start; gap: 2px; }
.eco .ic { display: flex; align-items: center; gap: 8px; }
</style>

<!--
[30초 · 활용성 · OSS 적절성]
전체 구조부터 보여드리겠습니다. 애플리케이션은 SQLAlchemy를 거쳐 저희 dialect, 그리고 드라이버로 CUBRID에 연결합니다. AI 도구는 MCP 서버를 거쳐 같은 드라이버를 씁니다.
cookbook은 실행 경로에 들어가지 않습니다. 애플리케이션 계층 옆에서 예제와 템플릿을 제공하고, 매일 실서버에서 이 경로들이 실제로 동작하는지 확인합니다. 하나씩 보겠습니다.
-->

---

<div class="split dialect">
  <div class="stack">
    <p class="kicker proj"><BrandMark name="sqlalchemy-cubrid" alt="" :height="24" />sqlalchemy-cubrid</p>
    <h2>CUBRID용<br>SQLAlchemy dialect를<br>새로 구현했습니다</h2>
    <p class="sub">dialect는 SQLAlchemy가 CUBRID 문법으로 SQL을 만들고 결과를 읽게 해 주는 계층입니다.</p>
  </div>
  <ul class="explain">
    <li><b>SQLAlchemy 2.0 기준</b>으로 처음부터 작성했습니다. 2012년 코드는 쓰지 않았습니다</li>
    <li><b>SQLAlchemy가 제공하는 dialect 호환성 테스트</b>를 실제 CUBRID에서 돌립니다. 타입 · 조회 · 트랜잭션 · 리플렉션 같은 공통 동작을 검사합니다 (<code>sqlalchemy.testing.suite</code>)</li>
    <li>CUBRID가 지원하지 않는 기능은 <b>feature flag 60여 개</b>로 명시해 건너뜁니다</li>
    <li>schema reflection · <b class="nw">MERGE</b> · <b class="nw">ON DUPLICATE KEY</b> · <b class="nw">REPLACE</b> · Alembic 마이그레이션 · 동기·비동기 연결</li>
  </ul>
</div>

<style>
.dialect { grid-template-columns: 0.85fr 1.15fr; }
.dialect h2 { font-size: 2rem; }
</style>

<!--
[30초 · OSS 적절성 · 기능테스트]
첫 번째는 sqlalchemy-cubrid입니다. dialect는 SQLAlchemy가 CUBRID 문법으로 SQL을 만들고 결과를 읽게 해 주는 계층입니다. Mike의 코드는 동작하지 않았기 때문에 SQLAlchemy 2.0 기준으로 처음부터 새로 만들었습니다.
SQLAlchemy는 외부 dialect가 같은 동작을 보장하는지 확인하라고 공통 테스트 묶음을 제공합니다. 저희는 이 테스트를 실제 CUBRID에서 돌리고, CUBRID가 지원하지 않는 기능은 feature flag로 명시해 건너뜁니다.
-->

---

<p class="kicker">sqlalchemy-cubrid — 이렇게 씁니다</p>

```python
from sqlalchemy import create_engine, MetaData, Table, select, func

engine = create_engine(
    "cubrid+pycubrid://dba@localhost:33000/demodb")
agencies = Table("agencies", MetaData(),
                 autoload_with=engine)          # schema reflection

with engine.connect() as conn:
    stmt = (select(agencies.c.region, func.count())
            .group_by(agencies.c.region))
    print(conn.execute(stmt).all())   # [('서울', 2), ('세종', 10)]
```

<p class="then">그런데 이 코드 아래에 둘 <span class="seal">드라이버</span>가 문제였습니다.</p>

<style>
.then { font-size: 1.3rem; font-weight: 700; line-height: 1.4; border-left: 4px solid var(--seal); padding-left: 16px; }
pre.slidev-code { font-size: 0.9rem !important; }
</style>

<!--
[15초 · 활용성]
쓰는 법은 다른 데이터베이스와 같습니다. 연결 URL만 바꾸면 SQLAlchemy 코드가 그대로 CUBRID에서 돕니다. 그런데 이 코드 아래에 둘 드라이버가 문제였습니다.
-->

---

<p class="kicker">dialect 아래에 둘 드라이버를 찾아보니</p>
<h2>공식 드라이버는 C 확장이라,<br>설치와 비동기가 걸림돌이었습니다</h2>

<ul class="explain wide">
  <li><b>CUBRIDdb</b>(CUBRID-Python)는 C 확장입니다. Python 3.6 · 3.10–3.12용 wheel은 CUBRID 배포 서버에서 받고, 그 밖의 버전은 컴파일러(Windows는 Visual Studio 2017, Linux는 GCC 8 이상)로 직접 빌드합니다</li>
  <li><b>PyPI에는 2014년 버전(9.3.0)만 있습니다</b> — 최신 버전은 GitHub 릴리스(v11.3.0.51, 2025-09)로 배포됩니다</li>
  <li><b>asyncio를 지원하지 않습니다</b> — FastAPI 같은 비동기 서버에서는 스레드로 감싸야 합니다</li>
</ul>
<p class="note-line">공식 드라이버는 잘 동작하며, 뒤의 성능 비교도 이 드라이버와 했습니다. PyPI의 CUBRID-Python 9.3.0은 2014-05-15에 올라왔습니다. 2026-10-28 확인.</p>

<style>
.wide { max-width: 66ch; }
.wide li { font-size: 1.08rem; }
</style>

<!--
[25초 · 활용성]
dialect 아래에 둘 드라이버를 찾아봤습니다. 공식 드라이버 CUBRIDdb는 C 확장입니다. 몇몇 Python 버전은 CUBRID 배포 서버에서 wheel로 받을 수 있지만, 나머지는 컴파일러로 직접 빌드해야 합니다. PyPI에는 2014년 버전만 있어서 pip install로 최신 드라이버를 받을 수 없고, asyncio도 지원하지 않습니다.
드라이버 자체는 잘 동작합니다. 다만 pip install 한 줄로 설치하고 비동기 서버에서 바로 쓰려면, 순수 Python 드라이버가 필요했습니다.
-->

---

<p class="kicker proj"><BrandMark name="pycubrid" alt="" :height="24" />pycubrid · 2026</p>
<h2 class="cas">필요한 CAS 통신 동작을 기존 드라이버 소스와 대조해 확인했습니다</h2>

<div class="packet">
  <div><b>4B</b><span>length<br>본문 길이</span></div>
  <div><b>4B</b><span>cas_info<br>서버 상태</span></div>
  <div><b>payload</b><span>요청·응답 본문 · CAS 바이너리 프로토콜 · TCP 33000</span></div>
</div>

<ul class="explain">
  <li><a href="https://github.com/CUBRID/node-cubrid" target="_blank"><b>CUBRID/node-cubrid</b></a>를 먼저 읽었습니다. 순수 JavaScript라 요청 순서와 패킷 형식이 코드에 그대로 드러납니다</li>
  <li>같은 동작을 <b>공식 C 드라이버</b> 소스와 하나씩 맞춰 봤습니다. 두 저장소는 참고 자료일 뿐, pycubrid의 의존성이 아닙니다</li>
</ul>

<p class="facts"><b>20</b> 패킷 타입 · <b>30</b> 데이터 타입 · 런타임 의존성 <b class="accent">0</b></p>

<style>
.cas { font-size: 1.75rem; }
.facts { font-size: 1.2rem; font-weight: 650; }
.facts b { font-size: 1.6rem; font-weight: 800; }
</style>

<!--
[25초 · OSS 적절성 · 라이선스]
그래서 순수 Python 드라이버 pycubrid를 만들었습니다. 먼저 node-cubrid를 읽었습니다. 순수 JavaScript로 되어 있어서 서버에 어떤 순서로 무엇을 보내는지가 코드에 그대로 보였습니다. 그다음 같은 동작을 공식 C 드라이버 소스와 하나씩 맞춰 봤습니다.
모든 요청과 응답은 길이, 서버 상태, 본문이라는 같은 틀을 따릅니다. 이렇게 20개 패킷 타입과 30개 데이터 타입을 구현했고, 런타임 의존성은 하나도 없습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker proj"><BrandMark name="pycubrid" alt="" :height="24" />pycubrid</p>

```bash
pip install pycubrid
```

  <h2>C 컴파일러 없이,<br>한 줄이면 끝납니다</h2>
  </div>
  <ul class="explain">
    <li><b>PEP 249</b> — Python 표준 DB-API 그대로</li>
    <li><b>asyncio 지원</b> — <code>pycubrid.aio</code> 모듈로 FastAPI 같은 비동기 서버에서 바로</li>
    <li><b>TLS</b> 암호화 연결, <b>BLOB · CLOB</b> 대용량 데이터</li>
    <li>CAS broker 자동 재연결 · batch fetch</li>
    <li><b>커버리지 95%</b> CI 게이트 · mypy strict 오류 0</li>
  </ul>
</div>

<!--
[25초 · 활용성 · 기능테스트]
그 결과가 pycubrid입니다. pip install 한 줄이면 끝나고, C 컴파일러가 필요 없습니다. Python 표준 DB-API를 따르니 다른 데이터베이스와 쓰는 법이 같고, asyncio를 지원해서 FastAPI 같은 비동기 서버에서 바로 쓸 수 있습니다.
TLS 암호화와 대용량 데이터도 지원하고, 테스트와 커버리지 기준은 CI에서 강제합니다.
-->

---

<div class="split">
  <div class="stack">
    <p class="kicker proj"><BrandMark name="cubrid-cookbook-python" alt="" :height="24" />cubrid-cookbook · 2026</p>
    <h2>만들고 나니,<br>쓰는 법이 필요했습니다</h2>
    <ul class="explain">
      <li><b>fundamentals 50여 개</b> — 연결 · CRUD · 트랜잭션 · LOB · pandas · async · Alembic</li>
      <li><b>프로덕션 템플릿 7개</b> — FastAPI · Django · Flask · Streamlit 대시보드 · Celery · pandas ETL · AI 에이전트</li>
      <li><b>문서 4개 사이트</b> · 한국어 문서 포함</li>
    </ul>
  </div>
  <figure class="shot clip"><img src="/shots/docs-pycubrid.jpg" alt="pycubrid 문서 사이트"></figure>
</div>

<!--
[20초 · 활용성]
드라이버를 만들고 나니, 실제로 쓰는 법을 보여줘야 했습니다. 그래서 cookbook에 연결부터 비동기, pandas까지 50여 개 예제와, FastAPI, Django, 대시보드, AI 에이전트 같은 템플릿 7개를 만들었습니다. 문서는 4개 사이트로 만들고 한국어 문서도 함께 씁니다.
-->

---

<p class="kicker proj"><BrandMark name="cubrid-cookbook-python" alt="" :height="24" />cubrid-cookbook — 예제가 곧 테스트입니다</p>
<h2>cookbook 예제로<br>드라이버의 동작을 매일 검증합니다</h2>

<div class="nightly">
  <div class="node">매일 GitHub Actions</div><span class="arr">→</span>
  <div class="node db">CUBRID 11.4 컨테이너</div><span class="arr">→</span>
  <div class="node">최신 릴리스 드라이버로<br>모든 예제 실행</div><span class="arr">→</span>
  <div class="node ours">출력이 기대 결과와<br>다르면 실패</div>
</div>

<p class="sub">템플릿 테스트와 FastAPI 빠른 시작도 같은 실행에서 확인합니다. 월요일에는 CUBRID 11.2에서도 돌립니다. 드라이버가 깨지면 사용자보다 이 검사가 먼저 실패합니다.</p>

<style>
.nightly { display: flex; align-items: center; gap: 8px; }
.nightly .node { font-size: 0.82rem; padding: 6px 10px; line-height: 1.35; }
.nightly .arr { color: var(--muted); }
.nightly + .sub { max-width: 54ch; }
</style>

<!--
[20초 · 기능테스트]
이 예제들은 문서로 끝나지 않습니다. 매일 GitHub Actions에서 CUBRID 11.4 컨테이너를 띄우고, PyPI에 올라간 최신 드라이버로 모든 예제를 실행해 출력을 기대 결과와 비교합니다. 템플릿 테스트도 함께 돌고, 월요일에는 11.2에서도 확인합니다. 드라이버에 문제가 생기면 사용자보다 이 검사가 먼저 잡습니다.
-->

---

<div class="split">
  <div class="stack">
    <p class="kicker proj"><BrandMark name="cubrid-mcp-server" alt="" :height="24" />cubrid-mcp-server · 2026</p>
    <h2>AI가 CUBRID에<br>직접 물어볼 수 있게</h2>
    <p class="sub">MCP는 AI 도구가 외부 데이터와 도구에 접근하는 공개 프로토콜입니다.</p>
    <ul class="explain">
      <li><b>tool 11개</b> — 테이블 목록 · 스키마 · 인덱스 · 실행 계획 · 쿼리 실행</li>
      <li><b>기본 읽기 전용</b> — 쓰기 tool은 운영자가 켤 때만 추가됩니다</li>
      <li><b>감사 로그</b> — 켜 두면 어떤 tool이 언제 쓰였는지 남깁니다</li>
    </ul>
  </div>
  <figure class="shot clip"><img src="/shots/repo-mcp.jpg" alt="cubrid-mcp-server 저장소"></figure>
</div>

<!--
[20초 · 활용성 · OSS 적절성]
이제 AI가 데이터를 묻는 일이 많아졌습니다. MCP는 Claude 같은 AI 도구가 외부 데이터에 접근하는 공개 프로토콜입니다. CUBRID용 MCP 서버를 만들었고, 테이블 목록, 스키마, 인덱스, 실행 계획, 쿼리 실행까지 11개 도구를 제공합니다. 기본은 읽기 전용입니다.
-->

---

<p class="kicker proj"><BrandMark name="cubrid-mcp-server" alt="" :height="24" />cubrid-mcp-server — AI는 CUBRID SQL을 잘 모릅니다</p>
<h2>그래서 서버가 먼저 알려 줍니다</h2>

<ul class="explain wide">
  <li><b>domain knowledge 5종</b> — CUBRID의 LIMIT 문법, 컬렉션 타입, SHOW TRACE 같은 차이를 문서로 제공</li>
  <li><b>prompt 9종</b> — 스키마 점검, 인덱스 후보 찾기, 실행 계획 해석 같은 자주 하는 작업</li>
  <li><b>schema resource</b> — AI가 쿼리를 쓰기 전에 테이블 구조부터 읽게 합니다</li>
</ul>

<p class="note-line">AI가 CUBRID 문법을 몰라도, 쿼리를 쓰기 전에 서버가 차이를 먼저 알려 줍니다.</p>

<!--
[15초 · 활용성]
AI 모델은 CUBRID 문법을 잘 모릅니다. 그래서 서버가 먼저 알려 줍니다. CUBRID 문법의 차이를 문서로, 자주 하는 작업을 prompt로 제공해서, AI가 쿼리를 쓰기 전에 차이부터 읽게 했습니다.
-->

---

<p class="kicker proj"><BrandMark name="cubrid-mcp-server" alt="" :height="24" />cubrid-mcp-server — AI에게 DB를 열어 줄 때 첫 질문</p>
<h1>"지워버리면요?"<br>기본은 <span class="accent">읽기 전용</span>입니다</h1>

<ul class="explain wide2">
  <li><b>쓰기 tool은 보이지도 않습니다</b> — 기본 모드에서는 <code>execute_write</code>가 AI에게 등록되지 않습니다</li>
  <li><b>조회만 허용</b> — <code>execute_query</code>는 SELECT · SHOW · DESC · WITH만 실행하고, 여러 문장을 한 번에 보내면 거부합니다. 실행 계획은 <code>explain_query</code>로 봅니다</li>
  <li><b>쓰기는 운영자가 연결별로 직접 켤 때만</b> — 그때도 INSERT · UPDATE · DELETE 한 문장씩만, DDL은 불가</li>
</ul>
<p class="note-line">실제 운영에서는 SELECT 권한만 가진 DB 계정으로 연결하기를 권합니다.</p>

<style>
.wide2 { max-width: 66ch; }
.wide2 li { font-size: 1.06rem; }
</style>

<!--
[20초 · 활용성 · 기능테스트]
AI에게 데이터베이스를 열어 주면 제일 먼저 나오는 질문이 "지워버리면 어떡하냐"입니다. 그래서 기본은 읽기 전용입니다. 기본 모드에서는 쓰기 도구가 AI에게 보이지도 않고, 쿼리 도구는 조회 문장만, 그것도 한 문장씩만 허용합니다.
쓰기는 운영자가 연결별로 직접 켤 때만 가능합니다. 실제 운영에서는 조회 권한만 가진 계정을 권합니다.
-->

---

<p class="kicker">두 사람이 네 저장소를 어떻게 운영하나</p>
<h2>에이전트와 함께 개발하고,<br><span class="accent">책임은 사람이 집니다</span></h2>

<div class="roles">
  <div><b>사람</b><span>풀 문제를 고르고 <code>AGENTS.md</code>에 규칙을 씁니다. 변경을 확인하고 머지와 릴리스를 결정합니다</span></div>
  <div><b>코딩 에이전트</b><span>구현 · 테스트 · 문서의 초안을 씁니다</span></div>
  <div><b>CI</b><span>필수 검사를 통과해야만 머지됩니다</span></div>
</div>
<figure class="shot wide-shot"><img src="/shots/merged-prs.jpg" alt="pycubrid의 병합된 PR 목록 — 각 PR 옆에 CI 통과 표시"></figure>

<style>
.roles { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px; }
.roles > div { display: grid; gap: 6px; border-top: 3px solid var(--blue); padding-top: 8px; }
.roles b { font-size: 1.05rem; color: var(--blue); }
.roles span { font-size: 0.88rem; line-height: 1.45; color: var(--ink); }
.wide-shot { max-height: 205px; }
.wide-shot img { width: 100%; height: auto; }
</style>

<!--
[30초 · 커뮤니티 · 기능테스트]
그럼 두 사람이 네 저장소를 어떻게 운영할까요. 코딩 에이전트와 함께 개발합니다. 어떤 문제를 풀지는 사람이 고르고, 저장소마다 AGENTS.md에 규칙을 써 둡니다. 에이전트는 구현과 테스트, 문서의 초안을 쓰고, 사람은 그 변경을 확인한 뒤 머지와 릴리스를 결정합니다.
그리고 어떤 변경이든 필수 CI 검사를 통과해야만 머지됩니다. 아래는 실제 PR 목록이고, PR마다 CI 통과 표시가 붙어 있습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">“AI와 함께 쓴 코드를 믿을 수 있나요?”</p>
    <h1 class="ci-gate"><span class="accent">CI</span>를 통과해야<br>머지됩니다</h1>
    <p class="small">테스트 수는 파라미터화와 workflow lane에 따라 달라져 고정 합계로 제시하지 않습니다.</p>
  </div>
  <ul class="explain">
    <li><b>타입 오류 0</b> — mypy strict</li>
    <li><b>커버리지 95% 이상</b> — 전체 검증에서 미달이면 실패</li>
    <li><b>property-based test</b> — hypothesis로 경계 사례 탐색</li>
    <li><b>공개 API 변경 감지</b> — 몰래 바뀌면 실패</li>
    <li><b>SQLAlchemy dialect 호환성 테스트</b> — 실제 CUBRID에서</li>
    <li><b>20개 조합</b> — 전체 라이브 검증, <span class="nw">Python 5 × CUBRID 4</span></li>
  </ul>
</div>

<style>
.ci-gate { font-size: 3rem; line-height: 1.15; }
</style>

<!--
[25초 · 기능테스트]
그러면 당연히 이런 질문이 나옵니다. AI와 함께 쓴 코드를 믿을 수 있냐. 저희 답은 검사를 통과하지 못하면 머지되지 않는다는 것입니다. 타입 오류 0, 커버리지 95%, property-based test, 공개 API 변경 감지, SQLAlchemy 호환성 테스트,
그리고 Python 5개 버전과 CUBRID 4개 버전, 20개 조합의 실제 DB에서 검증합니다.
-->

---

<p class="kicker">무엇을 쟀나 · 같은 서버에서 같은 작업에 걸린 시간</p>
<h2>C 드라이버보다 조금 느리지만,<br>설치와 비동기를 얻었습니다</h2>

<div class="split perf">
  <div class="stack">
    <p class="chart-cap">C 드라이버 CUBRIDdb = 100 · 짧을수록 좋음</p>
    <PairChart :width="400" :label-width="150" before-name="CUBRIDdb (C)" after-name="pycubrid" :rows="[
      { label: 'PK 조회', before: 100, after: 112, beforeText: '100', afterText: '112' },
      { label: '1만 행 fetchall', before: 100, after: 125, beforeText: '100', afterText: '125' },
      { label: 'executemany 1만 행', before: 100, after: 120, beforeText: '100', afterText: '120' },
    ]" />
    <p class="small">2026-10-25 · CUBRID 11.4.6 · pycubrid 1.13.5 · 환경과 원본 결과: Appendix B</p>
  </div>
  <div class="stack past">
    <p class="chart-cap">pycubrid 안에서 바꾼 것 (과거 측정)</p>
    <ul class="explain">
      <li><b>ping</b>: SELECT 1 대신 CAS 명령 CHECK_CAS — 처리량 3.8배</li>
      <li><b>pool_pre_ping</b> — 처리량 6.9배</li>
      <li><b>bulk insert 1,000행</b> — 2,865 → 2,512ms</li>
      <li><b>select-all</b> — 39.8 → 31.8ms</li>
    </ul>
    <p class="small">재측정하지 않았고, 측정 날짜와 버전은 기록되지 않았습니다.</p>
  </div>
</div>

<style>
.chart-cap { font-size: 0.85rem; font-weight: 700; color: var(--ink); }
.perf { align-items: start; grid-template-columns: 1.2fr 1fr; }
.past .explain li { font-size: 0.92rem; }
</style>

<!--
[30초 · 기능테스트]
성능은 무엇과 비교했는지부터 말씀드리겠습니다. 2026년 10월 25일, 같은 CUBRID 11.4.6 서버에서 공식 C 드라이버와 같은 작업에 걸린 시간을 쟀습니다. C 드라이버를 100으로 놓으면 pycubrid는 PK 조회 112, 1만 행 조회 125입니다. 순수 Python이라 조금 느립니다.
대신 설치와 비동기, 이식성을 얻었습니다. 오른쪽은 pycubrid 안에서 ping 방식 등을 바꿔 개선한 과거 측정값입니다. 날짜와 버전이 기록되지 않아서, 참고로만 보여드립니다.
-->

---

<h2>표준을 따르고,<br><span class="accent">누구나 쓸 수 있게 공개합니다</span></h2>

<div class="split even trust" style="align-items: start">
  <div class="stack">
    <p class="chart-cap">따르는 표준</p>
    <ul class="explain">
      <li><b>PEP 249</b> DB-API — pycubrid</li>
      <li><b>PEP 561</b> 타입 정보(py.typed) — 세 패키지 모두</li>
      <li><b>SQLAlchemy dialect API</b> — sqlalchemy-cubrid</li>
      <li><b>MCP</b> — tool · resource · prompt를 표준 형식으로 제공 · cubrid-mcp-server</li>
    </ul>
  </div>
  <div class="stack">
    <p class="chart-cap">공개 사용 조건</p>
    <ul class="explain">
      <li><b>네 저장소 모두 MIT</b> · 의존성에 GPL 없음</li>
      <li><b>THIRD_PARTY_LICENSES · NOTICE</b> — 네 저장소 모두</li>
      <li><b>SPDX SBOM</b> — 세 패키지의 최근 릴리스마다 첨부</li>
      <li>CUBRID 서버 라이선스도 원문으로 확인 (Apache-2.0 엔진 · BSD 커넥터)</li>
    </ul>
  </div>
</div>
<p class="note-line">기반 오픈소스: <span class="nw">SQLAlchemy (MIT)</span> · <span class="nw">node-cubrid (프로토콜 참고)</span> · FastMCP · pytest · hypothesis</p>

<style>
.trust .explain li { font-size: 0.96rem; }
</style>

<!--
[20초 · OSS 적절성 · 라이선스]
저희끼리만 통하는 규칙이 아니라 표준을 따릅니다. 드라이버는 Python DB-API, dialect는 SQLAlchemy의 dialect API, AI 서버는 MCP 형식을 따릅니다.
네 저장소 모두 MIT 라이선스이고, 의존성에 GPL은 없습니다. 서드파티 라이선스 목록을 저장소마다 두고, 패키지 릴리스마다 SBOM을 붙입니다.
-->

---

<h2>저희 말 대신,<br><span class="accent">직접 확인해 보세요</span></h2>

```bash
uvx cubrid-mcp-server          # PyPI 최신 릴리스
make docker-up && make verify  # cookbook 저장소에서, 전체 스택
```

<p class="sub"><b>VERIFY.md</b> — <span class="nw">드라이버 연결</span> → ORM → <span class="nw">MCP 서버</span> → <span class="nw">실서버 golden test</span> → <span class="nw">SBOM · 라이선스</span>.<br>단계마다 명령과 기대 결과를 적어 두었습니다.</p>

<!--
[15초 · 기능테스트]
오늘 말씀드린 내용은 직접 확인하실 수 있습니다. 명령 한 줄로 AI 서버를 띄울 수 있고, VERIFY.md에 단계별 명령과 기대 결과를 모두 적어 두었습니다.
-->

---

<SnapshotAdoptionCharts />

<!--
[20초 · 활용성 · 커뮤니티]
지금 이 저장소들이 얼마나 움직이고 있는지 보여드리겠습니다. 스냅숏 날짜 기준의 GitHub star, 머지된 PR, GitHub 릴리스 수입니다. 이 숫자는 개발 활동을 보여 줄 뿐, 사용자 수가 아닙니다. 클론 수는 CI와 실제 사용자를 구분할 수 없어 쓰지 않았습니다.
그리고 이 PR 가운데에는 저희 둘이 아닌 사람들이 보낸 것도 많습니다.
-->

---

<p class="kicker">외부 기여 · 2026-10-28 12:20 UTC 기준</p>
<h2>팀 밖의 <span class="accent">62명</span>이 보낸<br>PR <span class="accent">137개</span>가 머지됐습니다</h2>

<div class="people">
  <a href="https://github.com/WilliamK112" target="_blank"><img src="/contributors/WilliamK112.jpg" alt=""><b>WilliamK112</b><span>PR 17</span></a>
  <a href="https://github.com/Enard52" target="_blank"><img src="/contributors/Enard52.jpg" alt=""><b>Enard52</b><span>PR 16</span></a>
  <a href="https://github.com/soyeladice-svg" target="_blank"><img src="/contributors/soyeladice-svg.jpg" alt=""><b>soyeladice-svg</b><span>PR 8</span></a>
  <a href="https://github.com/HarshRajSinghania" target="_blank"><img src="/contributors/HarshRajSinghania.jpg" alt=""><b>HarshRajSinghania</b><span>PR 6</span></a>
  <a href="https://github.com/kcncb" target="_blank"><img src="/contributors/kcncb.jpg" alt=""><b>kcncb</b><span>PR 6</span></a>
  <a href="https://github.com/CloudCorpRecords" target="_blank"><img src="/contributors/CloudCorpRecords.jpg" alt=""><b>CloudCorpRecords</b><span>PR 5</span></a>
  <a href="https://github.com/rahul05ranjan" target="_blank"><img src="/contributors/rahul05ranjan.jpg" alt=""><b>rahul05ranjan</b><span>PR 4</span></a>
  <a href="https://github.com/WATSONSK14" target="_blank"><img src="/contributors/WATSONSK14.jpg" alt=""><b>WATSONSK14</b><span>PR 4</span></a>
  <a href="https://github.com/awss1i" target="_blank"><img src="/contributors/awss1i.jpg" alt=""><b>awss1i</b><span>PR 3</span></a>
  <a href="https://github.com/KeuqS" target="_blank"><img src="/contributors/KeuqS.jpg" alt=""><b>KeuqS</b><span>PR 3</span></a>
  <a href="https://github.com/tayfuryldz" target="_blank"><img src="/contributors/tayfuryldz.jpg" alt=""><b>tayfuryldz</b><span>PR 3</span></a>
  <div class="more"><b>+51</b><span>PR 1–2개</span></div>
</div>
<p class="note-line">네 저장소에 머지된 PR 기준 · 메인테이너와 봇 제외 · 사진은 PR 3개 이상이고 계정이 30일 넘은 사람. 전체 명단과 근거: <span class="nw">events/2026-ossdevcon/metrics/contributors-2026-10-28.json</span></p>

<style>
.people { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px 10px; }
.people a, .people .more { display: grid; justify-items: center; gap: 3px; text-decoration: none; border: 0; color: var(--ink); }
.people img { width: 62px; height: 62px; border-radius: 50%; object-fit: cover; border: 2px solid var(--line); }
.people b { font-size: 0.68rem; font-weight: 700; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.people span { font-size: 0.64rem; color: var(--muted); }
.people .more b { width: 62px; height: 62px; border-radius: 50%; display: grid; place-items: center; background: var(--blue-soft); color: var(--blue); font-size: 1.05rem; }
</style>

<!--
[25초 · 커뮤니티]
저희가 가장 보여드리고 싶은 장입니다. 2026년 10월 28일 기준으로, 팀 밖의 62명이 보낸 PR 137개가 네 저장소에 머지됐습니다. 메인테이너와 봇은 뺀 숫자입니다.
사진은 PR을 세 개 이상 보낸 분들입니다. 테스트를 보강한 PR이 가장 많고, 문서와 버그 수정이 뒤를 잇습니다. 둘이 시작한 저장소를 이제 여러 사람이 함께 고치고 있습니다.
-->

---

<h2>드라이버 → ORM → 예제 → AI</h2>
<p class="sub">Python에서 검증한 이 순서를 다른 언어에도 그대로 적용하고 있습니다.</p>

<ul class="explain langs">
  <li><b>Python</b> — pycubrid · sqlalchemy-cubrid <span class="muted">PyPI 공개</span></li>
  <li><b>TypeScript</b> — cubrid-client · drizzle-cubrid <span class="muted">진행 중</span></li>
  <li><b>Go</b> — cubrid-go · gorm-cubrid <span class="muted">진행 중</span></li>
  <li><b>Rust</b> — cubrid-rs · sea-orm-cubrid <span class="muted">진행 중</span></li>
</ul>
<p class="note-line"><b>처음 기여하기</b> — 네 저장소에 <b>good first issue 46개</b>가 열려 있습니다(2026-10-28). 저장소마다 CONTRIBUTING.md에 절차를 적어 두었습니다.</p>

<style>
.langs li { font-size: 1.12rem; }
</style>

<!--
[20초 · 커뮤니티 · 발전가능성]
Python은 끝이 아니라 기준입니다. 드라이버, ORM, 예제, AI로 이어지는 같은 순서를 TypeScript, Go, Rust에서도 진행하고 있습니다. 처음 기여하실 분을 위해 good first issue를 46개 열어 두었고, 저장소마다 기여 절차를 적어 두었습니다.
-->

---

<div class="split even">
  <div class="stack">
    <p class="kicker">멈춰 있던 연결을 다시 잇다</p>
    <h1>이제, <span class="accent">함께</span><br>이어 주세요.</h1>
    <p class="sub">2019년 README의 “if someone were interested”에 저희가 답했고, 지금은 62명이 함께 잇고 있습니다.</p>
    <div class="links">
      <div><span>GitHub</span>github.com/cubrid-lab</div>
      <div><span>설치</span>pip install pycubrid</div>
      <div><span>AI</span>uvx cubrid-mcp-server</div>
    </div>
    <p class="thanks">감사합니다 — 파이큐브리드팀 최영선 · 백경준</p>
  </div>
  <div class="stack">
    <div class="frame"><Photo src="/photos/team-now.jpg" label="지금의 두 사람 사진" /></div>
    <p class="notice">파이큐브리드팀은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 오픈소스 팀입니다. CUBRID는 해당 권리자의 상표입니다.</p>
  </div>
</div>

<style>
.frame { height: 320px; }
.thanks { font-size: 1.15rem; font-weight: 700; margin-top: 8px; }
.notice { max-width: none; margin: 0; font-size: 0.62rem; line-height: 1.5; color: var(--muted); }
</style>

<!--
[20초 · PT · 커뮤니티]
처음에 보여드린 README의 한 줄, "관심 있는 사람이 있다면"에 저희가 답했습니다. 그리고 지금은 62명이 함께 이 연결을 잇고 있습니다.
이제 여러분 차례입니다. 네 저장소 모두 열려 있습니다. 감사합니다.
-->
