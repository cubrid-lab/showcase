---
title: "CUBRID, 이제 Python으로 — 파이큐브리드팀"
---

<p class="kicker event-corner">2026 오픈소스 개발자대회</p>

<div class="cover">
  <h1>CUBRID, 이제 Python으로</h1>
  <p class="lead">feat. CUBRID Python 생태계 구축기</p>
  <div class="products">
    <div><BrandMark name="pycubrid" alt="pycubrid 아이콘" :height="46" /><span>pycubrid</span></div>
    <div><BrandMark name="sqlalchemy-cubrid" alt="sqlalchemy-cubrid 아이콘" :height="46" /><span>sqlalchemy-cubrid</span></div>
    <div><BrandMark name="cubrid-cookbook-python" alt="cubrid-cookbook 아이콘" :height="46" /><span>cubrid-cookbook</span></div>
    <div><BrandMark name="cubrid-mcp-server" alt="cubrid-mcp-server 아이콘" :height="46" /><span>cubrid-mcp-server</span></div>
  </div>
  <div class="who">
    <b>파이큐브리드팀</b>
    <span>최영선 · 백경준</span>
  </div>
</div>

<style>
.event-corner { position: absolute; top: 28px; left: 72px; margin: 0; }
.cover { display: grid; gap: 20px; }
.cover h1 { font-size: 3.4rem; line-height: 1.12; white-space: nowrap; }
.cover .lead { font-size: 1.45rem; font-weight: 700; letter-spacing: -0.02em; }
.products { display: flex; gap: 26px; margin-top: 4px; }
.products > div { display: grid; justify-items: center; gap: 6px; }
.products span { font-family: var(--mono); font-size: 0.7rem; color: var(--muted); }
.who { display: flex; gap: 14px; align-items: baseline; margin-top: 8px; padding-top: 16px; border-top: 2px solid var(--ink); width: fit-content; }
.who b { font-size: 1.1rem; }
.who span { font-size: 1.05rem; color: var(--ink); }
</style>

<!--
[15초 · PT]
안녕하세요. 파이큐브리드팀의 최영선, 백경준입니다. 오늘은 Python에서 CUBRID를 제대로 쓸 수 없던 상황을, 저희가 어떻게 바꿨는지 말씀드리겠습니다. 제목 아래 네 프로젝트가 그 결과입니다.
-->

---

<p class="kicker">목차</p>
<h2 class="one">오늘 말씀드릴 네 가지</h2>

<div class="agenda">
  <div><span>01</span><b>왜 시작했는가</b><p>오픈소스 기여 경험과 멈춰 있던 CUBRID dialect</p></div>
  <div><span>02</span><b>무엇을 만들었는가</b><p>Python 드라이버부터 ORM · 예제 · AI 연결까지</p></div>
  <div><span>03</span><b>어떻게 믿고 쓸 수 있게 했는가</b><p>사람의 리뷰 · CI · 성능 실측 · 표준과 공개</p></div>
  <div><span>04</span><b>어떻게 이어갈 것인가</b><p>외부 기여 성과와 오픈소스 생태계 확장</p></div>
</div>

<style>
.agenda { display: grid; gap: 0; }
.agenda > div { display: grid; grid-template-columns: 56px 290px minmax(0, 1fr); align-items: baseline; padding: 14px 0; border-top: 2px solid var(--line); }
.agenda > div:last-child { border-bottom: 2px solid var(--line); }
.agenda span { color: var(--blue); font-size: 1.5rem; font-weight: 800; font-variant-numeric: tabular-nums; }
.agenda b { font-size: 1.3rem; }
.agenda p { color: var(--muted); font-size: 1rem; white-space: nowrap; }
</style>

<!--
[15초 · PT]
오늘은 네 가지 질문에 답하겠습니다. 왜 시작했는지, 무엇을 만들었는지, 어떻게 믿고 쓸 수 있게 했는지, 마지막으로 이 오픈소스 생태계를 어떻게 이어갈 것인지 말씀드리겠습니다.
-->

---

<ChapterDivider number="01" title="왜 시작했는가" subtitle="오픈소스 기여 경험에서 출발한 CUBRID Python 문제" />

<!--
[0초 · 챕터 전환 · 문제의 발견]
시각적 구분 페이지입니다. 별도 설명 없이 다음 장의 본문으로 진행합니다.
-->

---

<p class="kicker">2020년 오픈소스 컨트리뷰톤</p>
<h2 class="one">SQLAlchemy팀에서 멘토와 멘티로 만났습니다</h2>

<div class="split meet">
  <div class="stack">
    <ul class="explain">
      <li><b>SQLAlchemy · sqlalchemy-hana</b>에 PR</li>
      <li><b>Mike Bayer</b>와 대화</li>
      <li><b>SQLAlchemy Korea</b> 개설</li>
    </ul>
  </div>
  <div class="stack meet-side">
    <div class="frame"><Photo src="/photos/team-2020.jpg" label="2020 컨트리뷰톤 사진" /></div>
    <a class="group-card" href="https://www.facebook.com/groups/sqlalchemykorea/" target="_blank"><img src="/photos/sqlalchemy-korea.png" alt="SQLAlchemy Korea 페이스북 공개 그룹, 멤버 29명"><span>facebook.com/groups/sqlalchemykorea</span></a>
  </div>
</div>

<style>
.meet { grid-template-columns: 1.5fr 1fr; }
.meet-side { justify-content: center; }
.group-card { display: inline-flex; flex-direction: column; gap: 4px; margin-top: 0; padding: 8px 12px 8px; border: 1.5px solid var(--line); border-radius: 12px; border-bottom-width: 1.5px; width: fit-content; }
.group-card img { width: 250px; display: block; }
.group-card span { font-size: 0.7rem; color: var(--muted); }
.frame { height: 270px; }
</style>

<!--
[25초 · PT · 커뮤니티]
저희 둘은 2020년 오픈소스 컨트리뷰톤의 SQLAlchemy 프로젝트에서 멘토와 멘티로 만났습니다. SQLAlchemy와 sqlalchemy-hana에 PR을 보내면서, 데이터베이스마다 붙는 dialect가 어떻게 만들어지는지 배웠습니다.
창시자 Mike Bayer와도 이야기를 나눴고, 그 뒤 SQLAlchemy Korea 커뮤니티를 만들었습니다. 이 경험이 있었기에 다음 장의 저장소를 알아볼 수 있었습니다.
-->

---

<p class="kicker">dialect를 공부하다가 찾은 저장소</p>
<h2 class="one">CUBRID dialect는 있었지만, <span class="seal">멈춰 있었습니다.</span></h2>

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

<ChapterDivider number="02" title="무엇을 만들었는가" subtitle="드라이버 · ORM · 예제 · MCP로 이어지는 연결 구조" />

<!--
[0초 · 챕터 전환 · Python 생태계 구축]
시각적 구분 페이지입니다. 별도 설명 없이 다음 장의 본문으로 진행합니다.
-->

---

<p class="kicker">구조</p>
<h2>CUBRID Python 생태계의 연결 구조</h2>

<div class="arch eco">
  <div class="path">
    <span class="label">애플리케이션에서</span>
    <div class="cook">
      <div class="cook-head"><BrandMark name="cubrid-cookbook-python" alt="cubrid-cookbook 아이콘" :height="22" /><b>cubrid-cookbook</b><small>예제·템플릿</small></div>
      <div class="chips"><span>FastAPI</span><span>Django</span><span>Flask</span><span>pandas</span></div>
    </div>
    <div class="down">↓</div>
    <div class="sa">
      <div class="sa-head"><b>SQLAlchemy</b><small>Python ORM</small></div>
      <div class="node ours"><span class="ic"><BrandMark name="sqlalchemy-cubrid" alt="sqlalchemy-cubrid 아이콘" :height="22" />sqlalchemy-cubrid</span><small>dialect 플러그인</small></div>
    </div>
    <div class="down">↓</div>
    <div class="node ours"><span class="ic"><BrandMark name="pycubrid" alt="pycubrid 아이콘" :height="22" />pycubrid</span><small>드라이버 (DB-API)</small></div>
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

<style>
.eco { grid-template-columns: 1.4fr 1fr; gap: 24px; }
.eco .down { font-size: 0.6rem; }
.eco .node, .eco .sa, .eco .cook { padding-top: 4px; padding-bottom: 4px; }
.eco .node { padding: 5px 12px; }
.eco .ic { display: flex; align-items: center; gap: 8px; }
.eco .cook { border: 1.5px dashed var(--blue); border-radius: 10px; padding: 7px 12px; display: grid; gap: 6px; }
.eco .cook-head { display: flex; align-items: center; gap: 8px; }
.eco .cook-head b { color: var(--blue); font-size: 0.92rem; white-space: nowrap; }
.eco .ic { white-space: nowrap; }
.eco .cook-head small, .eco .sa-head small { font-size: 0.72rem; color: var(--muted); margin-left: auto; }
.eco .chips { display: flex; gap: 6px; }
.eco .chips span { border: 1px solid var(--line); border-radius: 6px; padding: 2px 8px; font-size: 0.8rem; font-weight: 650; background: #fff; }
.eco .sa { border: 1.5px solid var(--line); border-radius: 10px; padding: 6px 10px 8px; display: grid; gap: 6px; }
.eco .sa-head { display: flex; align-items: baseline; gap: 8px; font-size: 0.95rem; }
</style>


<!--
[30초 · 활용성 · OSS 적절성]
전체 구조부터 보여드리겠습니다. 애플리케이션은 저희 dialect를 끼운 SQLAlchemy를 거쳐, 드라이버로 CUBRID에 연결합니다. AI 도구는 MCP 서버를 거쳐 같은 드라이버를 씁니다.
애플리케이션 자리에는 cookbook이 있습니다. FastAPI, Django, Flask, pandas로 만든 예제와 템플릿이 모두 이 길로 CUBRID에 연결되고, 매일 실서버에서 실제로 동작하는지 확인합니다. dialect는 SQLAlchemy 안에 끼우는 플러그인이라 따로 떨어진 계층이 아닙니다. 하나씩 보겠습니다.
-->

---


<p class="kicker proj"><BrandMark name="sqlalchemy-cubrid" alt="" :height="28" />sqlalchemy-cubrid</p>
<h2 class="one">CUBRID용 SQLAlchemy dialect를 새로 구현했습니다</h2>

<p class="sub" style="white-space: nowrap">dialect: SQLAlchemy가 CUBRID SQL을 만들고 읽게 하는 플러그인</p>

<ul class="explain">
  <li><b>SQLAlchemy 2.0 기준</b>으로 처음부터 작성</li>
  <li><b>SQLAlchemy 공식 호환성 테스트</b>를 실제 CUBRID에서 실행</li>
  <li>지원하지 않는 기능은 <b>feature flag 60여 개</b>로 명시</li>
  <li><b>MERGE · ON DUPLICATE KEY · REPLACE</b> · Alembic · 비동기</li>
</ul>

<!--
[30초 · OSS 적절성 · 기능테스트]
첫 번째는 sqlalchemy-cubrid입니다. dialect는 SQLAlchemy가 CUBRID 문법으로 SQL을 만들고 결과를 읽게 해 주는 계층입니다. Mike의 코드는 동작하지 않았기 때문에 SQLAlchemy 2.0 기준으로 처음부터 새로 만들었습니다.
SQLAlchemy는 외부 dialect가 같은 동작을 보장하는지 확인하라고 공통 테스트 묶음을 제공합니다. 저희는 이 테스트를 실제 CUBRID에서 돌리고, CUBRID가 지원하지 않는 기능은 feature flag로 명시해 건너뜁니다.
-->

---


<p class="kicker proj"><BrandMark name="sqlalchemy-cubrid" alt="" :height="28" />sqlalchemy-cubrid</p>

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
.slidev-layout.contest-deck pre.slidev-code { font-size: 0.8rem !important; line-height: 1.45 !important; padding: 14px 20px !important; }
</style>

<!--
[15초 · 활용성]
쓰는 법은 다른 데이터베이스와 같습니다. 연결 URL만 바꾸면 SQLAlchemy 코드가 그대로 CUBRID에서 돕니다. 그런데 이 코드 아래에 둘 드라이버가 문제였습니다.
-->

---

<p class="kicker">dialect 아래에 둘 드라이버를 찾아보니</p>
<h2 class="one">공식 드라이버에 더하고 싶었던 것: 간편한 설치와 비동기</h2>

<ul class="explain wide">
  <li><b>C 확장</b> — 일부 Python 버전만 wheel, 나머지는 컴파일러로 직접 빌드</li>
  <li><b>PyPI에는 2014년 9.3.0만</b> — 최신 v11.3.0.51은 GitHub 릴리스</li>
  <li><b>asyncio 미지원</b> — 비동기 서버에서는 스레드로 감싸야 함</li>
</ul>
<p class="note-line">공식 드라이버는 잘 동작하고, 성능 비교도 이 드라이버와 했습니다</p>

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


<p class="kicker proj"><BrandMark name="pycubrid" alt="" :height="28" />pycubrid</p>
<h2 class="one">C 라이브러리 없이, 서버 통신을 직접 구현했습니다</h2>
<p class="sub" style="max-width: none; font-size: 1rem;">그래서 브로커(CAS)와 주고받는 바이너리 메시지를 Python이 직접 만들고 읽습니다</p>

<div class="packet">
  <div><b>4B</b><span>length<br>본문 길이</span></div>
  <div><b>4B</b><span>cas_info<br>서버 상태</span></div>
  <div><b>payload</b><span>요청·응답 본문 · CAS 바이너리 프로토콜 · TCP 33000</span></div>
</div>

<ul class="explain">
  <li><a href="https://github.com/CUBRID/node-cubrid" target="_blank"><b>CUBRID/node-cubrid</b></a> — 순수 JavaScript라 요청 순서와 패킷 형식이 그대로 보임</li>
  <li><b>공식 C 드라이버</b>와 동작을 하나씩 대조 — 둘 다 참고 자료, 의존성 아님</li>
</ul>

<p class="facts"><b>20</b> 패킷 타입 · <b>30</b> 데이터 타입 · 런타임 의존성 <b class="accent">0</b></p>

<style>
.facts { font-size: 1.2rem; font-weight: 650; }
.facts b { font-size: 1.6rem; font-weight: 800; }
</style>

<!--
[30초 · OSS 적절성 · 라이선스]
그래서 순수 Python 드라이버 pycubrid를 만들었습니다. C 라이브러리를 쓰지 않으니, 서버와 주고받는 통신을 Python으로 직접 구현해야 했습니다. CUBRID에서는 이 통신을 CAS 프로토콜이라고 부릅니다. 먼저 node-cubrid를 읽었습니다. 순수 JavaScript로 되어 있어서 서버에 어떤 순서로 무엇을 보내는지가 코드에 그대로 보였습니다. 그다음 같은 동작을 공식 C 드라이버 소스와 하나씩 맞춰 봤습니다.
모든 요청과 응답은 길이, 서버 상태, 본문이라는 같은 틀을 따릅니다. 이렇게 20개 패킷 타입과 30개 데이터 타입을 구현했고, 런타임 의존성은 하나도 없습니다.
-->

---


<p class="kicker proj"><BrandMark name="pycubrid" alt="" :height="28" />pycubrid</p>
<h2 class="one">C 컴파일러 없이, 한 줄이면 끝납니다</h2>

<div class="split even">
  <div class="stack">

```bash
pip install pycubrid
```

  </div>
  <ul class="explain">
    <li><b>PEP 249</b> — Python 표준 DB-API 그대로</li>
    <li><b>asyncio 지원</b> — 비동기 서버에서 바로</li>
    <li><b>TLS</b> 연결 · <b>BLOB · CLOB</b></li>
    <li>CAS broker 자동 재연결 · batch fetch</li>
    <li><b>커버리지 95%</b> · mypy strict 0</li>
  </ul>
</div>

<!--
[25초 · 활용성 · 기능테스트]
그 결과가 pycubrid입니다. pip install 한 줄이면 끝나고, C 컴파일러가 필요 없습니다. Python 표준 DB-API를 따르니 다른 데이터베이스와 쓰는 법이 같고, asyncio를 지원해서 FastAPI 같은 비동기 서버에서 바로 쓸 수 있습니다.
TLS 암호화와 대용량 데이터도 지원하고, 테스트와 커버리지 기준은 CI에서 강제합니다.
-->

---


<p class="kicker proj"><BrandMark name="cubrid-cookbook-python" alt="" :height="28" />cubrid-cookbook</p>
<h2 class="one">만들고 나니, 쓰는 법이 필요했습니다</h2>

<div class="split">
  <div class="stack">
    <ul class="explain">
      <li><b>예제 50여 개</b> — 연결부터 async · Alembic까지</li>
      <li><b>템플릿 7개</b> — FastAPI · Django · Flask 등</li>
      <li><b>문서 4개 사이트</b> · 한국어 포함</li>
    </ul>
  </div>
  <div class="docs-grid">
    <figure class="shot"><img src="/shots/docs-pycubrid.jpg" alt="pycubrid 문서 사이트"></figure>
    <figure class="shot"><img src="/shots/docs-sqlalchemy-cubrid.jpg" alt="sqlalchemy-cubrid 문서 사이트"></figure>
    <figure class="shot"><img src="/shots/docs-mcp.jpg" alt="cubrid-mcp-server 문서 사이트"></figure>
    <figure class="shot"><img src="/shots/docs-cookbook.jpg" alt="cubrid-cookbook-python 문서 사이트"></figure>
  </div>
</div>

<style>
.docs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.docs-grid .shot { box-shadow: 0 8px 18px -10px rgba(15, 27, 45, 0.35); border-radius: 8px; }
</style>

<!--
[20초 · 활용성]
드라이버를 만들고 나니, 실제로 쓰는 법을 보여줘야 했습니다. 그래서 cookbook에 연결부터 비동기, pandas까지 50여 개 예제와, FastAPI, Django, 대시보드, AI 에이전트 같은 템플릿 7개를 만들었습니다. 문서는 4개 사이트로 만들고 한국어 문서도 함께 씁니다.
-->

---


<p class="kicker proj"><BrandMark name="cubrid-cookbook-python" alt="" :height="28" />cubrid-cookbook</p>
<h2 class="one">cookbook 예제로 드라이버를 매일 검증합니다</h2>

<div class="nightly">
  <div class="node">매일 GitHub Actions</div><span class="arr">→</span>
  <div class="node db">CUBRID 11.4 컨테이너</div><span class="arr">→</span>
  <div class="node">최신 릴리스 드라이버로<br>모든 예제 실행</div><span class="arr">→</span>
  <div class="node ours">출력이 기대 결과와<br>다르면 실패</div>
</div>

<p class="sub">월요일엔 CUBRID 11.2에서도 · 드라이버가 깨지면 이 검사가 먼저 실패합니다.</p>

<style>
.nightly { display: flex; align-items: center; gap: 8px; }
.nightly .node { font-size: 0.82rem; padding: 6px 10px; line-height: 1.35; }
.nightly .arr { color: var(--muted); }
.nightly + .sub { max-width: none; white-space: nowrap; font-size: 1.05rem; }
</style>

<!--
[20초 · 기능테스트]
이 예제들은 문서로 끝나지 않습니다. 매일 GitHub Actions에서 CUBRID 11.4 컨테이너를 띄우고, PyPI에 올라간 최신 드라이버로 모든 예제를 실행해 출력을 기대 결과와 비교합니다. 템플릿 테스트도 함께 돌고, 월요일에는 11.2에서도 확인합니다. 드라이버에 문제가 생기면 사용자보다 이 검사가 먼저 잡습니다.
-->

---


<p class="kicker proj"><BrandMark name="cubrid-mcp-server" alt="" :height="28" />cubrid-mcp-server</p>
<h2 class="one">AI가 CUBRID에 직접 물어볼 수 있게</h2>

<div class="split">
  <div class="stack">
    <p class="sub" style="white-space: nowrap">MCP: AI 도구용 공개 프로토콜</p>
    <ul class="explain">
      <li><b>tool 11개</b> — 스키마 · 인덱스 · 쿼리 등</li>
      <li><b>기본 읽기 전용</b> — 쓰기는 켤 때만</li>
      <li><b>감사 로그</b> — tool 사용 기록</li>
    </ul>
  </div>
  <figure class="shot clip"><img src="/shots/docs-mcp.jpg" alt="cubrid-mcp-server 문서 사이트"></figure>
</div>

<!--
[20초 · 활용성 · OSS 적절성]
이제 AI가 데이터를 묻는 일이 많아졌습니다. MCP는 Claude 같은 AI 도구가 외부 데이터에 접근하는 공개 프로토콜입니다. CUBRID용 MCP 서버를 만들었고, 테이블 목록, 스키마, 인덱스, 실행 계획, 쿼리 실행까지 11개 도구를 제공합니다. 기본은 읽기 전용입니다.
-->

---


<p class="kicker proj"><BrandMark name="cubrid-mcp-server" alt="" :height="28" />cubrid-mcp-server</p>
<h2>그래서 서버가 먼저 알려 줍니다</h2>

<ul class="explain wide">
  <li><b>domain knowledge 5종</b> — LIMIT 문법 · 컬렉션 타입 · SHOW TRACE 같은 차이</li>
  <li><b>prompt 9종</b> — 스키마 점검 · 인덱스 후보 · 실행 계획 해석</li>
  <li><b>schema resource</b> — 쿼리 전에 테이블 구조부터 읽게 함</li>
</ul>

<p class="note-line">AI가 CUBRID 문법을 몰라도, 서버가 차이를 먼저 알려 줍니다.</p>

<!--
[15초 · 활용성]
AI 모델은 CUBRID 문법을 잘 모릅니다. 그래서 서버가 먼저 알려 줍니다. CUBRID 문법의 차이를 문서로, 자주 하는 작업을 prompt로 제공해서, AI가 쿼리를 쓰기 전에 차이부터 읽게 했습니다.
-->

---


<p class="kicker proj"><BrandMark name="cubrid-mcp-server" alt="" :height="28" />cubrid-mcp-server</p>
<h1 class="one">"지워버리면요?" 기본은 <span class="accent">읽기 전용</span>입니다</h1>

<ul class="explain wide2">
  <li><b>쓰기 tool은 보이지도 않습니다</b> — 기본 모드에서는 등록 자체가 안 됨</li>
  <li><b>조회만 허용</b> — SELECT · SHOW · DESC · WITH만, 여러 문장은 거부</li>
  <li><b>쓰기는 운영자가 켤 때만</b> — 그때도 한 문장씩, DDL은 불가</li>
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

<ChapterDivider number="03" title="어떻게 믿고 쓸 수 있게 했는가" subtitle="사람의 리뷰와 CI, 성능 실측, 표준을 따른 공개" />

<!--
[0초 · 챕터 전환 · 검증과 품질]
시각적 구분 페이지입니다. 별도 설명 없이 다음 장의 본문으로 진행합니다.
-->

---

<p class="kicker">두 사람이 네 저장소를 어떻게 운영하나</p>
<h2 class="one">에이전트와 개발하고, <span class="accent">책임은 사람이 집니다</span></h2>

<div class="roles">
  <div><b>사람</b><span>문제 선택 · 규칙 작성 · 머지 결정</span></div>
  <div><b>코딩 에이전트</b><span>구현 · 테스트 · 문서의 초안 작성</span></div>
  <div><b>CI</b><span>필수 검사를 통과해야만 머지</span></div>
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

<p class="kicker">“AI와 함께 쓴 코드를 믿을 수 있나요?”</p>
<h1 class="one"><span class="accent">CI</span>를 통과해야 머지됩니다</h1>

<div class="split even">
  <div class="stack">
  </div>
  <ul class="explain">
    <li><b>타입 오류 0</b> — mypy strict</li>
    <li><b>커버리지 95%</b> — 전체 오프라인 회귀 검사 기준</li>
    <li><b>property-based test</b></li>
    <li><b>공개 API 변경 감지</b> — 몰래 바뀌면 실패</li>
    <li><b>SQLAlchemy 호환성 테스트</b></li>
    <li><b>20개 조합</b> — 릴리스·수동 전체 검증</li>
  </ul>
</div>

<!--
[25초 · 기능테스트]
그러면 당연히 이런 질문이 나옵니다. AI와 함께 쓴 코드를 믿을 수 있냐. 저희 답은 검사를 통과하지 못하면 머지되지 않는다는 것입니다. 타입 오류 0, 커버리지 95%, property-based test, 공개 API 변경 감지, SQLAlchemy 호환성 테스트,
PR에서는 변경 위험에 맞는 검사만 선택하고, 릴리스와 수동 전체 검증에서 Python 5개 버전과 CUBRID 4개 버전의 20개 실제 DB 조합을 확인합니다. 자세한 실행 범위는 보조 자료 C에 있습니다.
-->

---

<p class="kicker">무엇을 쟀나 · 같은 서버에서 같은 작업에 걸린 시간</p>
<h2 class="one">조금 느리지만, 설치와 비동기를 얻었습니다</h2>

<div class="split perf">
  <div class="stack">
    <p class="chart-cap">C 드라이버 CUBRIDdb = 100 · 짧을수록 좋음</p>
    <PairChart :width="400" :label-width="150" before-name="CUBRIDdb (C)" after-name="pycubrid" :rows="[
      { label: 'PK 조회', before: 100, after: 104, beforeText: '100', afterText: '104' },
      { label: '1만 행 fetchall', before: 100, after: 117, beforeText: '100', afterText: '117' },
      { label: 'executemany 1만 행', before: 100, after: 104, beforeText: '100', afterText: '104' },
    ]" />
    <p class="small">2026-10-28 · CUBRID 11.4.6 · pycubrid 1.15.0 · Appendix B</p>
  </div>
  <div class="stack past">
    <p class="chart-cap">같은 측정 · 이전 릴리스 1.10.0 → 1.15.0</p>
    <ul class="explain">
      <li><b>19개 작업</b> — 성능 회귀 없음</li>
      <li><b>동시 접속 1·8·32</b> — 처리량 회귀 없음</li>
      <li><b>메모리</b> — 최대 40 MiB (C 37 MiB)</li>
    </ul>
    <p class="small">2026-10-28 · 같은 서버·하네스 · 드라이버당 5회 교대</p>
  </div>
</div>

<style>
.chart-cap { font-size: 0.85rem; font-weight: 700; color: var(--ink); }
.perf { align-items: start; grid-template-columns: 1.2fr 1fr; }
.past .explain li { font-size: 0.92rem; }
</style>

<!--
[30초 · 기능테스트]
성능은 무엇과 비교했는지부터 말씀드리겠습니다. 2026년 10월 28일, 같은 CUBRID 11.4.6 서버에서 공식 C 드라이버와 최신 pycubrid 1.15.0이 같은 작업에 걸린 시간을 쟀습니다. C 드라이버를 100으로 놓으면 pycubrid는 PK 조회 104, 1만 행 조회 117, 1만 행 일괄 입력 104입니다. 순수 Python이라 조금 느리지만, 격차가 크지 않습니다.
대신 설치와 비동기, 이식성을 얻었습니다. 오른쪽은 같은 날 같은 방법으로 이전 릴리스 1.10.0과 비교한 결과입니다. 연결, 조회, 쓰기 19개 작업과 동시 접속 1개, 8개, 32개에서 성능 회귀가 없었습니다. 기능을 늘리면서 느려지지 않았다는 뜻입니다.
-->

---

<p class="kicker">표준과 라이선스</p>
<h2 class="one">표준을 따르고, <span class="accent">누구나 쓸 수 있게 공개합니다</span></h2>

<div class="split even trust" style="align-items: start">
  <div class="stack">
    <p class="chart-cap">따르는 표준</p>
    <ul class="explain">
      <li><b>PEP 249</b> DB-API — pycubrid</li>
      <li><b>PEP 561</b> 타입 정보 — 세 패키지</li>
      <li><b>SQLAlchemy dialect API</b></li>
      <li><b>MCP</b> 표준 형식 — cubrid-mcp-server</li>
    </ul>
  </div>
  <div class="stack">
    <p class="chart-cap">공개 사용 조건</p>
    <ul class="explain">
      <li><b>네 저장소 모두 MIT</b> · 의존성에 GPL 없음</li>
      <li><b>서드파티 라이선스 · NOTICE</b> — 네 저장소</li>
      <li><b>SPDX SBOM</b> — 세 패키지 릴리스마다</li>
      <li>CUBRID 서버 라이선스 원문 확인</li>
    </ul>
  </div>
</div>
<p class="note-line">기반 오픈소스: SQLAlchemy · node-cubrid(참고) · FastMCP · pytest · hypothesis</p>

<style>
.trust .explain li { font-size: 0.96rem; }
</style>

<!--
[20초 · OSS 적절성 · 라이선스]
저희끼리만 통하는 규칙이 아니라 표준을 따릅니다. 드라이버는 Python DB-API, dialect는 SQLAlchemy의 dialect API, AI 서버는 MCP 형식을 따릅니다.
네 저장소 모두 MIT 라이선스이고, 의존성에 GPL은 없습니다. 서드파티 라이선스 목록을 저장소마다 두고, 패키지 릴리스마다 SBOM을 붙입니다.
-->

---

<ChapterDivider number="04" title="어떻게 이어갈 것인가" subtitle="외부 기여자와 함께 확장하는 오픈소스 생태계" />

<!--
[0초 · 챕터 전환 · 성과와 다음 단계]
시각적 구분 페이지입니다. 별도 설명 없이 다음 장의 본문으로 진행합니다.
-->

---

<h2 class="one">팀 밖의 <span class="accent">67명</span>이 보낸 PR <span class="accent">153개</span>가 머지됐습니다</h2>

<div class="people">
  <a href="https://github.com/WilliamK112" target="_blank" title="WilliamK112"><img src="/contributors/WilliamK112.jpg" alt="WilliamK112"></a>
  <a href="https://github.com/Enard52" target="_blank" title="Enard52"><img src="/contributors/Enard52.jpg" alt="Enard52"></a>
  <a href="https://github.com/soyeladice-svg" target="_blank" title="soyeladice-svg"><img src="/contributors/soyeladice-svg.jpg" alt="soyeladice-svg"></a>
  <a href="https://github.com/HarshRajSinghania" target="_blank" title="HarshRajSinghania"><img src="/contributors/HarshRajSinghania.jpg" alt="HarshRajSinghania"></a>
  <a href="https://github.com/kcncb" target="_blank" title="kcncb"><img src="/contributors/kcncb.jpg" alt="kcncb"></a>
  <a href="https://github.com/CloudCorpRecords" target="_blank" title="CloudCorpRecords"><img src="/contributors/CloudCorpRecords.jpg" alt="CloudCorpRecords"></a>
  <a href="https://github.com/rahul05ranjan" target="_blank" title="rahul05ranjan"><img src="/contributors/rahul05ranjan.jpg" alt="rahul05ranjan"></a>
  <a href="https://github.com/WATSONSK14" target="_blank" title="WATSONSK14"><img src="/contributors/WATSONSK14.jpg" alt="WATSONSK14"></a>
  <a href="https://github.com/awss1i" target="_blank" title="awss1i"><img src="/contributors/awss1i.jpg" alt="awss1i"></a>
  <a href="https://github.com/KeuqS" target="_blank" title="KeuqS"><img src="/contributors/KeuqS.jpg" alt="KeuqS"></a>
  <a href="https://github.com/tayfuryldz" target="_blank" title="tayfuryldz"><img src="/contributors/tayfuryldz.jpg" alt="tayfuryldz"></a>
  <a href="https://github.com/Vieta100-omo" target="_blank" title="Vieta100-omo"><img src="/contributors/Vieta100-omo.jpg" alt="Vieta100-omo"></a>
  <a href="https://github.com/Aaqibhafeezkhan" target="_blank" title="Aaqibhafeezkhan"><img src="/contributors/Aaqibhafeezkhan.jpg" alt="Aaqibhafeezkhan"></a>
  <a href="https://github.com/bfs2021" target="_blank" title="bfs2021"><img src="/contributors/bfs2021.jpg" alt="bfs2021"></a>
  <a href="https://github.com/bh-official" target="_blank" title="bh-official"><img src="/contributors/bh-official.jpg" alt="bh-official"></a>
  <a href="https://github.com/Mr-Neutr0n" target="_blank" title="Mr-Neutr0n"><img src="/contributors/Mr-Neutr0n.jpg" alt="Mr-Neutr0n"></a>
  <a href="https://github.com/rushikeshraghatate90" target="_blank" title="rushikeshraghatate90"><img src="/contributors/rushikeshraghatate90.jpg" alt="rushikeshraghatate90"></a>
  <a href="https://github.com/ryanduguid" target="_blank" title="ryanduguid"><img src="/contributors/ryanduguid.jpg" alt="ryanduguid"></a>
  <a href="https://github.com/thymeed" target="_blank" title="thymeed"><img src="/contributors/thymeed.jpg" alt="thymeed"></a>
  <a href="https://github.com/UsmanGhias" target="_blank" title="UsmanGhias"><img src="/contributors/UsmanGhias.jpg" alt="UsmanGhias"></a>
  <a href="https://github.com/VeldanDev" target="_blank" title="VeldanDev"><img src="/contributors/VeldanDev.jpg" alt="VeldanDev"></a>
  <a href="https://github.com/abhishekjoshi13" target="_blank" title="abhishekjoshi13"><img src="/contributors/abhishekjoshi13.jpg" alt="abhishekjoshi13"></a>
  <a href="https://github.com/Ai-Siiii" target="_blank" title="Ai-Siiii"><img src="/contributors/Ai-Siiii.jpg" alt="Ai-Siiii"></a>
  <a href="https://github.com/alperensumeroglu" target="_blank" title="alperensumeroglu"><img src="/contributors/alperensumeroglu.jpg" alt="alperensumeroglu"></a>
  <a href="https://github.com/anaylab" target="_blank" title="anaylab"><img src="/contributors/anaylab.jpg" alt="anaylab"></a>
  <a href="https://github.com/anush-933" target="_blank" title="anush-933"><img src="/contributors/anush-933.jpg" alt="anush-933"></a>
  <a href="https://github.com/anyingiit" target="_blank" title="anyingiit"><img src="/contributors/anyingiit.jpg" alt="anyingiit"></a>
  <a href="https://github.com/AuraFamerCode" target="_blank" title="AuraFamerCode"><img src="/contributors/AuraFamerCode.jpg" alt="AuraFamerCode"></a>
  <a href="https://github.com/Bryandero98" target="_blank" title="Bryandero98"><img src="/contributors/Bryandero98.jpg" alt="Bryandero98"></a>
  <a href="https://github.com/chenzeyan54-commits" target="_blank" title="chenzeyan54-commits"><img src="/contributors/chenzeyan54-commits.jpg" alt="chenzeyan54-commits"></a>
  <a href="https://github.com/dannyward630" target="_blank" title="dannyward630"><img src="/contributors/dannyward630.jpg" alt="dannyward630"></a>
  <a href="https://github.com/Dikshant-Neupane" target="_blank" title="Dikshant-Neupane"><img src="/contributors/Dikshant-Neupane.jpg" alt="Dikshant-Neupane"></a>
  <a href="https://github.com/goktugekin" target="_blank" title="goktugekin"><img src="/contributors/goktugekin.jpg" alt="goktugekin"></a>
  <a href="https://github.com/itsdevcode" target="_blank" title="itsdevcode"><img src="/contributors/itsdevcode.jpg" alt="itsdevcode"></a>
  <a href="https://github.com/jackgedge" target="_blank" title="jackgedge"><img src="/contributors/jackgedge.jpg" alt="jackgedge"></a>
  <a href="https://github.com/Jah-yee" target="_blank" title="Jah-yee"><img src="/contributors/Jah-yee.jpg" alt="Jah-yee"></a>
  <a href="https://github.com/Jaysanghani08" target="_blank" title="Jaysanghani08"><img src="/contributors/Jaysanghani08.jpg" alt="Jaysanghani08"></a>
  <a href="https://github.com/kragent66-glitch" target="_blank" title="kragent66-glitch"><img src="/contributors/kragent66-glitch.jpg" alt="kragent66-glitch"></a>
  <a href="https://github.com/laozhej" target="_blank" title="laozhej"><img src="/contributors/laozhej.jpg" alt="laozhej"></a>
  <a href="https://github.com/MugdhoAI" target="_blank" title="MugdhoAI"><img src="/contributors/MugdhoAI.jpg" alt="MugdhoAI"></a>
  <a href="https://github.com/Muhtasim-Munif-Fahim" target="_blank" title="Muhtasim-Munif-Fahim"><img src="/contributors/Muhtasim-Munif-Fahim.jpg" alt="Muhtasim-Munif-Fahim"></a>
  <a href="https://github.com/Nandankumarjv" target="_blank" title="Nandankumarjv"><img src="/contributors/Nandankumarjv.jpg" alt="Nandankumarjv"></a>
  <a href="https://github.com/nightcityblade" target="_blank" title="nightcityblade"><img src="/contributors/nightcityblade.jpg" alt="nightcityblade"></a>
  <a href="https://github.com/Ochibueze474" target="_blank" title="Ochibueze474"><img src="/contributors/Ochibueze474.jpg" alt="Ochibueze474"></a>
  <a href="https://github.com/OpenDeernet" target="_blank" title="OpenDeernet"><img src="/contributors/OpenDeernet.jpg" alt="OpenDeernet"></a>
  <a href="https://github.com/Oscar-Williams" target="_blank" title="Oscar-Williams"><img src="/contributors/Oscar-Williams.jpg" alt="Oscar-Williams"></a>
  <a href="https://github.com/PandaHUN777" target="_blank" title="PandaHUN777"><img src="/contributors/PandaHUN777.jpg" alt="PandaHUN777"></a>
  <a href="https://github.com/Parth-Vasave" target="_blank" title="Parth-Vasave"><img src="/contributors/Parth-Vasave.jpg" alt="Parth-Vasave"></a>
  <a href="https://github.com/petrovicistefan" target="_blank" title="petrovicistefan"><img src="/contributors/petrovicistefan.jpg" alt="petrovicistefan"></a>
  <a href="https://github.com/pratham8499" target="_blank" title="pratham8499"><img src="/contributors/pratham8499.jpg" alt="pratham8499"></a>
  <a href="https://github.com/pratipc" target="_blank" title="pratipc"><img src="/contributors/pratipc.jpg" alt="pratipc"></a>
  <a href="https://github.com/rahemoth" target="_blank" title="rahemoth"><img src="/contributors/rahemoth.jpg" alt="rahemoth"></a>
  <a href="https://github.com/randomcodeross" target="_blank" title="randomcodeross"><img src="/contributors/randomcodeross.jpg" alt="randomcodeross"></a>
  <a href="https://github.com/SHIL0018" target="_blank" title="SHIL0018"><img src="/contributors/SHIL0018.jpg" alt="SHIL0018"></a>
  <a href="https://github.com/srijavuppala" target="_blank" title="srijavuppala"><img src="/contributors/srijavuppala.jpg" alt="srijavuppala"></a>
  <a href="https://github.com/Srikanthmadhan" target="_blank" title="Srikanthmadhan"><img src="/contributors/Srikanthmadhan.jpg" alt="Srikanthmadhan"></a>
  <a href="https://github.com/SuellenQwQ" target="_blank" title="SuellenQwQ"><img src="/contributors/SuellenQwQ.jpg" alt="SuellenQwQ"></a>
  <a href="https://github.com/tnalbant" target="_blank" title="tnalbant"><img src="/contributors/tnalbant.jpg" alt="tnalbant"></a>
  <a href="https://github.com/tyza66" target="_blank" title="tyza66"><img src="/contributors/tyza66.jpg" alt="tyza66"></a>
  <a href="https://github.com/varshith84" target="_blank" title="varshith84"><img src="/contributors/varshith84.jpg" alt="varshith84"></a>
  <a href="https://github.com/xuu33030" target="_blank" title="xuu33030"><img src="/contributors/xuu33030.jpg" alt="xuu33030"></a>
  <a href="https://github.com/yotam1001" target="_blank" title="yotam1001"><img src="/contributors/yotam1001.jpg" alt="yotam1001"></a>
  <a href="https://github.com/sarankumar1325" target="_blank" title="sarankumar1325"><img src="/contributors/sarankumar1325.jpg" alt="sarankumar1325"></a>
  <a href="https://github.com/Vamsi-2581" target="_blank" title="Vamsi-2581"><img src="/contributors/Vamsi-2581.jpg" alt="Vamsi-2581"></a>
  <a href="https://github.com/a3643605788" target="_blank" title="a3643605788"><img src="/contributors/a3643605788.jpg" alt="a3643605788"></a>
  <a href="https://github.com/Chaitanya-code0" target="_blank" title="Chaitanya-code0"><img src="/contributors/Chaitanya-code0.jpg" alt="Chaitanya-code0"></a>
  <a href="https://github.com/inmassat" target="_blank" title="inmassat"><img src="/contributors/inmassat.jpg" alt="inmassat"></a>
</div>
<p class="note-line">2026-11-01 기준 · 네 저장소에 PR이 머지된 외부 기여자 전원 · 메인테이너·봇 제외</p>

<style>
.people { display: grid; grid-template-columns: repeat(14, 1fr); gap: 8px 6px; justify-items: center; }
.people a { display: block; border: 0; }
.people img { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; border: 2px solid var(--line); display: block; }
</style>

<!--
[25초 · 커뮤니티]
2026년 11월 1일 기준으로, 팀 밖의 67명이 보낸 PR 153개가 네 저장소에 머지됐습니다. 메인테이너와 봇은 뺀 숫자입니다.
화면의 얼굴이 그 67명입니다. 테스트를 보강한 PR이 가장 많고, 문서와 버그 수정이 뒤를 잇습니다. 둘이 시작한 저장소를 이제 여러 사람이 함께 고치고 있습니다.
-->

---

<p class="kicker">드라이버 → ORM → 예제 → AI</p>
<h2 class="one">다음 계획: Python에 집중합니다</h2>
<p class="sub">이미 공개한 네 저장소를 더 단단하게 만듭니다.</p>

<ul class="explain plans">
  <li><b>pycubrid · sqlalchemy-cubrid</b> — 새 CUBRID 버전이 나오면 호환성 테스트와 필요한 수정</li>
  <li><b>cubrid-mcp-server</b> — 보안 검증 · 관찰성 · 실무 예제 보강</li>
  <li><b>CUBRID 공식 저장소</b> — 작업 중 찾은 문제를 cubrid · cubrid-python에 이슈와 PR로 전달</li>
  <li><b>국내 개발자 커뮤니티</b> — 파이콘 한국 등에서 발표하고 사용자 의견 모으기</li>
</ul>

<style>
.plans li { font-size: 1rem; }
</style>

<!--
[20초 · 커뮤니티 · 발전가능성]
다음 계획입니다. Python에 집중해 이미 공개한 네 저장소를 더 단단하게 만들겠습니다. 새 CUBRID 버전이 나오면 드라이버와 dialect의 호환성을 바로 시험하고 고치겠습니다. MCP 서버는 보안 검증과 관찰성, 실무 예제를 보강하겠습니다. 드라이버와 dialect를 만들며 찾은 문제는 CUBRID 공식 저장소에도 이슈와 PR로 전달하겠습니다. 파이콘 한국 같은 국내 개발자 커뮤니티에서도 발표하며 실제 사용자의 의견을 모으려고 합니다.
-->

---

<p class="kicker">CUBRID, 이제 Python으로</p>
<h2 class="one">감사합니다</h2>
<p class="sub" style="white-space: nowrap">멈춰 있던 dialect에서 시작해, 이제는 여러 사람이 함께 고치는 생태계가 됐습니다.</p>

<div class="split even">
  <div class="stack">
    <p class="thanks">파이큐브리드팀 최영선 · 백경준</p>
  </div>
  <div class="frame"><Photo src="/photos/team-now.jpg" label="지금의 두 사람 사진" /></div>
</div>

<style>
.frame { height: 200px; }
.thanks { font-size: 1.15rem; font-weight: 700; }
</style>

<!--
[20초 · PT · 커뮤니티]
처음에 보여드린 README의 한 줄, "관심 있는 사람이 있다면"에 저희가 답했습니다. 멈춰 있던 dialect에서 시작한 일이 이제 드라이버와 ORM, 예제, AI 도구까지 이어졌고, 여러 사람이 함께 고치는 생태계가 됐습니다. 네 저장소 모두 열려 있습니다. 들어 주셔서 감사합니다.
-->

---

<ChapterDivider number="Q&amp;A" title="질의응답" />

<!--
[0초 · Q&A · 발표 시간 외]
질문을 받습니다. 질문에 맞는 보조 자료로 이동할 때는 g 키를 누르고 쪽 번호를 입력합니다. 28 공식 드라이버 비교 · 29 CAS 프로토콜 직접 구현 · 30 버전 호환성과 CI · 31 실측 성능 결과 · 32 MCP 서버 보안 · 33 라이선스와 외부 기여 · 34 채택 지표의 해석 · 35 공공 업무 연계 시나리오 · 36 로드맵과 유지보수. 각 보조 자료 아래의 "Q&A로 돌아가기"를 누르면 이 화면으로 돌아옵니다.
-->

---

<p class="kicker">보조 자료 · 드라이버 비교</p>
<h2 class="one">왜 공식 C 드라이버를 대체하지 않고 보완했나요?</h2>
<p class="proof-lead">차이는 <b>설치 방식과 네이티브 비동기 지원</b>입니다. 공식 드라이버도 dialect에서 계속 선택할 수 있습니다.</p>
<table class="proof-table">
<thead><tr><th style="width:22%">확인 항목</th><th style="width:39%">CUBRIDdb · C 확장</th><th>pycubrid · 순수 Python</th></tr></thead>
<tbody>
<tr><td>설치 요건</td><td>CCI와 C 빌드 또는 호환 바이너리 필요</td><td><code>pip install pycubrid</code> · CUBRID 네이티브 라이브러리 불필요</td></tr>
<tr><td>배포 경로</td><td>PyPI 9.3.x (2015년 마지막 업로드) · 최신 소스는 GitHub</td><td>현재 PyPI 릴리스와 범용 Python wheel</td></tr>
<tr><td>비동기</td><td>네이티브 asyncio API 없음</td><td><code>pycubrid.aio</code> · <code>cubrid+aiopycubrid://</code></td></tr>
<tr><td>SQLAlchemy</td><td><code>cubrid+cubriddb://</code></td><td><code>cubrid+pycubrid://</code> · 비동기 URL</td></tr>
</tbody>
</table>
<div class="proof-line"><b>선택의 기준:</b> C 확장은 유지하고, 간편한 설치·비동기 워크로드에 순수 Python 선택지를 추가했습니다. SQLAlchemy asyncio의 <code>greenlet</code>은 별도 의존성입니다.</div>
<div class="proof-source">근거 · <a href="https://pypi.org/project/CUBRID-Python/">공식 패키지 PyPI</a> · <a href="https://pypi.org/project/pycubrid/">pycubrid PyPI</a> · <a href="https://github.com/cubrid-lab/sqlalchemy-cubrid/blob/main/docs/DRIVER_COMPAT.md">드라이버 호환성</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
공식 C 드라이버 자체가 불량하다는 주장은 아닙니다. 최신 CUBRIDdb는 소스 빌드 경로로 사용 가능하고, sqlalchemy-cubrid에서도 선택할 수 있습니다. 순수 Python 드라이버는 설치 경험과 네이티브 비동기 API를 추가하는 역할입니다.
-->

---

<p class="kicker">보조 자료 · 프로토콜 구현</p>
<h2 class="one">기존 C 드라이버를 감싼 것 아닌가요?</h2>
<p class="proof-lead">아닙니다. Python에서 <b>CAS 바이너리 프로토콜을 직접 인코딩·디코딩</b>하며, CCI 런타임에 의존하지 않습니다.</p>
<div class="proof-flow">
  <div class="step">Python 애플리케이션<br />DB-API / asyncio</div><span class="arrow">→</span>
  <div class="step accent">pycubrid<br />패킷 생성·파싱</div><span class="arrow">→</span>
  <div class="step">CUBRID Broker / CAS<br />TCP 33000 예시</div><span class="arrow">→</span>
  <div class="step">CUBRID DB 서버</div>
</div>
<div class="proof-grid three">
  <div class="proof-card"><div class="proof-stat">20</div><h3>패킷 타입</h3><p>요청·응답 메시지를 Python에서 구현</p></div>
  <div class="proof-card"><div class="proof-stat">30</div><h3>데이터 타입</h3><p>CUBRID 타입과 Python 값 간 변환</p></div>
  <div class="proof-card"><div class="proof-stat">0</div><h3>런타임 의존성</h3><p>드라이버에 별도 CCI 링크 불필요</p></div>
</div>
<div class="proof-line"><b>소스 검증:</b> <code>node-cubrid</code>에서 패킷 흐름을 연구하고 공식 CCI 동작과 대조했지만, 두 구현을 런타임에 불러오지는 않습니다.</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/pycubrid">pycubrid 소스</a> · <a href="https://github.com/CUBRID/node-cubrid">node-cubrid</a> · <a href="https://github.com/CUBRID/cubrid-python">공식 C 드라이버</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
순수 Python 구현이란 실제 데이터베이스 통신 패킷을 Python이 생성하고 파싱한다는 뜻입니다. CUBRID 서버와 Broker는 별도로 필요하지만, 클라이언트 측 CCI 라이브러리 종속성을 제거했습니다. TCP 33000은 예시 Broker 포트입니다.
-->

---

<p class="kicker">보조 자료 · 테스트 범위</p>
<h2 class="one">20개 조합은 매 PR마다 실행하나요?</h2>
<p class="proof-lead"><b>아닙니다.</b> 지원 매트릭스와 실행 빈도를 구분합니다. 전체 20개 실서버 조합은 수동 검증과 릴리스에서 실행합니다.</p>
<table class="proof-table">
<thead><tr><th style="width:24%">Python / CUBRID</th><th>10.2</th><th>11.0</th><th>11.2</th><th>11.4</th></tr></thead>
<tbody>
<tr><td>3.11</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
<tr><td>3.12</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
<tr><td>3.13</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
<tr><td>3.14</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
<tr><td>3.15</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr>
</tbody>
</table>
<div class="proof-grid three">
  <div class="proof-card"><h3>PR</h3><p>변경 위험에 맞춘 오프라인·대표 실서버 검사</p></div>
  <div class="proof-card"><h3>main / 주간</h3><p>오래된·최신 Python 및 CUBRID 대표 조합 검사</p></div>
  <div class="proof-card"><h3>수동·릴리스</h3><p>전체 5 × 4 실서버 매트릭스와 릴리스 게이트</p></div>
</div>
<div class="proof-line"><b>검증의 한계:</b> PR이 통과했다고 20개 조합 전체를 그 PR에서 실행했다는 뜻은 아닙니다. pycubrid PR 일반 smoke와 dialect PR 95% 커버리지 정책도 다릅니다.</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/pycubrid/blob/main/docs/CI_POLICY.md">pycubrid CI 정책</a> · <a href="https://github.com/cubrid-lab/sqlalchemy-cubrid/blob/main/docs/CI_POLICY.md">dialect CI 정책</a> · <a href="https://github.com/cubrid-lab/pycubrid/actions">Actions</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
2026년 10월 현재 지원 범위는 Python 3.11부터 3.15, CUBRID 10.2부터 11.4까지입니다. 일상 PR은 변경 유형에 맞게 검사를 선택하고, 모든 20개 실서버 조합은 명시적 전체 실행 또는 릴리스 게이트에 포함됩니다. pycubrid의 일상 PR smoke에 95% 전체 커버리지를 주장하지 않습니다.
-->

---

<p class="kicker">보조 자료 · 성능 실측</p>
<h2 class="one">같은 CUBRID에서 공식 C 드라이버와 비교했습니다</h2>
<p class="proof-lead">2026-10-28 · CUBRID 11.4.6 · pycubrid 1.15.0 vs CUBRIDdb v11.3.0.51 · 낮을수록 빠름</p>
<table class="proof-table">
<thead><tr><th style="width:33%">동일 작업</th><th>CUBRIDdb</th><th>pycubrid</th><th>소요 시간 비율</th></tr></thead>
<tbody>
<tr><td>기본키 SELECT</td><td>0.709 ms</td><td>0.735 ms</td><td><b>1.04×</b></td></tr>
<tr><td>10,000행 fetchall</td><td>41.5 ms</td><td>48.7 ms</td><td><b>1.17×</b></td></tr>
<tr><td>10,000행 executemany + commit</td><td>3,612 ms</td><td>3,772 ms</td><td><b>1.04×</b></td></tr>
<tr><td>연결 + 종료</td><td>1.20 ms</td><td>1.71 ms</td><td><b>1.43×</b></td></tr>
</tbody>
</table>
<div class="proof-grid">
  <div class="proof-card"><h3>재현 설계</h3><p>동일 서버·하네스, 드라이버당 5회, 순서 교대, warm-up 제외, 작업 결과 검증</p></div>
  <div class="proof-card"><h3>해석 한계</h3><p>공유 호스트·localhost 조건. 일괄 입력의 1.04× 차이는 불확실성 범위가 겹침</p></div>
</div>
<div class="proof-line"><b>정확한 결론:</b> 이 환경의 단건 조회와 배치 작업에서 pycubrid가 대체로 더 느렸습니다. 전체 운영 워크로드에서 차이가 없다는 뜻은 아닙니다.</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/metrics/benchmark-2026-10-28/README.md">측정 보고서·원본 데이터</a> · <a href="https://github.com/cubrid-lab/cubrid-benchmark">벤치마크 하네스</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
C 기반 드라이버를 기준으로 PK SELECT는 4%, 1만 행 조회는 17% 더 오래 걸렸습니다. 연결·종료는 43% 차이가 납니다. 1만 행 입력 차이는 신뢰구간이 1을 포함하므로 유의미한 차이라고 단정하지 않습니다. 측정은 공유 호스트 한 대에서 진행돼 절대 지연시간을 일반화하면 안 됩니다.
-->

---

<p class="kicker">보조 자료 · MCP 보안</p>
<h2 class="one">MCP 읽기 전용은 데이터 유출까지 막나요?</h2>
<p class="proof-lead"><b>아닙니다.</b> 도구 차단과 데이터 접근 권한은 서로 다른 보안 계층입니다.</p>
<div class="proof-flow">
  <div class="step">AI / MCP 클라이언트</div><span class="arrow">→</span>
  <div class="step accent">MCP 서버<br />SQL 유형·단일 문장 검사</div><span class="arrow">→</span>
  <div class="step accent">CUBRID 계정 권한<br />SELECT-only · 뷰</div><span class="arrow">→</span>
  <div class="step">허용된 데이터만 조회</div>
</div>
<div class="proof-grid">
  <div class="proof-card"><h3>기본 정책 · 서버에서 강제</h3><ul><li>쓰기 도구 미등록, 조회 문장만 허용</li><li>여러 문장 및 데이터 변경형 조회 차단</li><li>쓰기 모드는 명시적으로 켜야 함</li></ul></div>
  <div class="proof-card"><h3>운영에서 반드시 추가</h3><ul><li>최소 권한 CUBRID 계정 사용</li><li>민감 열·행은 접근 가능한 뷰로 제한</li><li>감사·쿼리 제한·운영 검증 필요</li></ul></div>
</div>
<div class="proof-line"><b>잔여 위험:</b> 쓰기 모드를 허용하면 한 개의 UPDATE로 다수 행을 변경할 수 있습니다. 읽기 전용도 기밀 데이터 노출 방지를 보장하지 않습니다.</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/cubrid-mcp-server/blob/main/SECURITY.md">MCP 보안 문서</a> · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/EXPECTED_QA.md">예상 질문 Q12·Q13</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
MCP의 SQL allowlist는 문장 종류를 통제하지, 업무 승인 규칙이나 행 단위 권한을 구현하지 않습니다. 쓰기를 명시적으로 켜면 조건에 맞는 다수 행을 한 UPDATE로 갱신할 수도 있습니다. 운영에는 SELECT 전용 DB 계정 및 필요한 데이터만 노출하는 뷰가 필요합니다.
-->

---

<p class="kicker">보조 자료 · 공개·기여 근거</p>
<h2 class="one">오픈소스로 계속 운영될 근거가 있나요?</h2>
<p class="proof-lead">사람의 참여 실적과 운영 장치를 분리해서 보여드립니다. 숫자는 사용자 수가 아닌 <b>기여·유지관리 지표</b>입니다.</p>
<div class="proof-grid three">
  <div class="proof-card"><div class="proof-stat">67명</div><h3>팀 외부 기여자</h3><p>메인테이너·봇 제외, 2026-11-01</p></div>
  <div class="proof-card"><div class="proof-stat">153개</div><h3>외부 머지 PR</h3><p>4개 저장소에서 실제 병합된 PR</p></div>
  <div class="proof-card"><div class="proof-stat">MIT × 4</div><h3>독립 OSS 라이선스</h3><p>서드파티 고지 및 SBOM 운영</p></div>
</div>
<div class="proof-grid" style="margin-top:8px">
  <div class="proof-card"><h3>유지관리 체계</h3><p>필수 CI 게이트, 릴리스 검증, 공개 API 변경 감지, 문서·예제 실서버 검사</p></div>
  <div class="proof-card"><h3>통계의 범위</h3><p>67명은 저장소 간 중복을 제외한 외부 인간 기여자입니다. 153개는 그들이 병합한 PR 건수입니다.</p></div>
</div>
<div class="proof-line"><b>주장 범위:</b> 커뮤니티 참여가 확인된다는 뜻이지, 67개 조직이 서비스를 운영 중이라는 뜻은 아닙니다.</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/metrics/contributors-2026-11-01.json">기여자별 PR 원본</a> · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/APPENDIX.md">라이선스·릴리스 근거</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
실제 외부 기여자 67명과 이들이 보낸 머지 PR 153건은 2026년 11월 1일 기준 자료입니다. 네 저장소의 라이선스는 MIT이고, CI와 릴리스 게이트를 운영합니다. 개발 활동의 규모를 실제 사용자 수 또는 운영 기관 수로 바꾸어 말하지 않습니다.
-->

---

<p class="kicker">보조 자료 · 지표 해석</p>
<h2 class="one">클론·스타가 실제 사용자 수를 뜻하나요?</h2>
<p class="proof-lead"><b>아닙니다.</b> 자체 CI가 저장소를 반복 클론할 수 있어 GitHub Traffic을 채택 증거에서 제외했습니다.</p>
<div class="proof-grid">
  <div class="proof-card"><h3>측정은 됐지만 채택 근거로 쓰지 않음</h3><div class="proof-stat">4,969</div><p>pycubrid 14일 클론 수(2026-09-27 기록)</p><p class="proof-small" style="margin-top:8px">같은 시기 자체 워크플로 실행 약 700회 · 반복 자동화의 영향 가능</p></div>
  <div class="proof-card"><h3>재현 가능한 커뮤니티 근거</h3><div class="proof-stat">67 / 153</div><p>외부 기여자 / 외부 머지 PR (2026-11-01)</p><p class="proof-small" style="margin-top:8px">계정·PR별 원본 링크와 봇 제외 기준 제공</p></div>
</div>
<div class="proof-grid" style="margin-top:8px">
  <div class="proof-card"><h3>확인된 것</h3><p>오픈소스 기여·패키지 배포·테스트·릴리스 활동</p></div>
  <div class="proof-card"><h3>별도 증명이 필요한 것</h3><p>실제 운영 기관, 고유 사용자 수, 프로덕션 배포·업무 효과</p></div>
</div>
<div class="proof-line"><b>정직한 답변:</b> 개발 생태계가 활발해졌다는 증거는 제시할 수 있습니다. 검증되지 않은 고유 클로너 수나 실제 도입 기관 수는 주장하지 않습니다.</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/metrics/SNAPSHOT.md">Traffic 기록과 제외 이유</a> · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/metrics/contributors-2026-11-01.json">기여자 원본</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
이전에 이야기했던 926 Unique Clones 같은 수치는 저장소별 중복과 자체 CI 클론 때문에 실제 사람 수나 사용 기관 수로 해석하면 안 됩니다. 현재 발표는 GitHub 클론 트래픽을 사용 지표에서 제외했습니다. 대신 인간 외부 기여자와 머지 PR을 근거 링크와 함께 제시합니다.
-->

---

<p class="kicker">보조 자료 · 적용 시나리오</p>
<h2 class="one">Java 중심의 공공 시스템에 Python이 왜 필요한가요?</h2>
<p class="proof-lead">기존 Java 업무 시스템을 교체하는 제안이 아닙니다. <b>DB와 분리된 Python 분석·AI 서비스</b>를 추가하는 아키텍처 예시입니다.</p>
<div class="proof-flow">
  <div class="step">기존 Java 업무 시스템<br />변경 없이 유지</div><span class="arrow">↔</span>
  <div class="step accent">CUBRID DB<br />권한 분리·전용 뷰</div><span class="arrow">↔</span>
  <div class="step">Python 조회·분석 서비스<br />pycubrid / SQLAlchemy</div><span class="arrow">→</span>
  <div class="step">대시보드·MCP·AI</div>
</div>
<div class="proof-grid">
  <div class="proof-card"><h3>이미 확인한 범위</h3><p>연결·SQL 실행, cookbook 템플릿, MCP 읽기 도구 및 온나라 스타일 샘플 데이터의 과거 리허설</p></div>
  <div class="proof-card"><h3>실무 적용 전 필요한 검증</h3><p>기관 보안 정책, DB 계정·뷰 설계, 기존 시스템 부하, 민감 정보 처리, 배포·운영 권한</p></div>
</div>
<div class="proof-line"><b>사실관계:</b> 온나라 <em>형태를 모사한 데모</em>를 준비한 것이며, 실제 온나라 운영 시스템에 이 코드를 도입했다는 주장이 아닙니다.</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/DEMO_RUNBOOK.md">과거 온나라 데모 런북</a> · <a href="https://github.com/cubrid-lab/cubrid-cookbook-python">cookbook 템플릿</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
이 장은 실제 운영기관 도입 사례가 아니라 구조의 실현 가능성을 설명하기 위한 예시입니다. 기존 Java 애플리케이션과 CUBRID는 유지하고 Python 분석 API 또는 MCP 기반 서비스를 별도로 배치할 수 있습니다. 실제 공공기관 연계는 네트워크·권한·보안·성능 검증이 필요합니다.
-->

---

<p class="kicker">보조 자료 · 로드맵과 운영</p>
<h2 class="one">새 CUBRID 버전과 장기 유지보수는?</h2>
<p class="proof-lead">이미 제공하는 기능, 선행 조사, 출시 뒤 검증할 항목을 <b>서로 다른 상태</b>로 표시합니다.</p>
<table class="proof-table">
<thead><tr><th style="width:25%">주제</th><th style="width:30%">현재 확인된 상태</th><th>다음 작업 및 조건</th></tr></thead>
<tbody>
<tr><td>Python 드라이버·dialect</td><td>Python 3.11–3.15 · CUBRID 10.2–11.4 지원</td><td>새 CUBRID 버전이 나오면 매트릭스에 추가해 호환성 테스트·필요한 수정</td></tr>
<tr><td>Vector 타입</td><td>CUBRID 저장소에서 개발 중 (VECTOR 타입 PR #7076, 아직 머지 전)</td><td>CUBRID 릴리스에 포함되면 드라이버 지원 검토</td></tr>
<tr><td>MCP</td><td>스키마 탐색·읽기 쿼리·기본 차단 정책 구현</td><td>보안 검증·관찰성·실무 예제 지속 개선</td></tr>
</tbody>
</table>
<div class="proof-grid" style="margin-top:10px">
  <div class="proof-card"><h3>운영 장치</h3><p>main 검증 · 릴리스 전체 매트릭스 · cookbook 예제 주기 검증 · 공개 코드·MIT</p></div>
  <div class="proof-card"><h3>현재 상태</h3><p>CUBRID 12 출시 일정은 공개된 것이 없고, Vector 타입은 <b>아직 CUBRID에 들어가지 않았습니다</b>. 출시된 뒤 검증하고 나서 지원한다고 말씀드리겠습니다.</p></div>
</div>
<div class="proof-source">근거 · <a href="https://github.com/cubrid-lab/pycubrid/blob/main/docs/CI_POLICY.md">검증 운영 정책</a> · <a href="https://github.com/cubrid-lab/showcase/blob/main/events/2026-ossdevcon/EXPECTED_QA.md">로드맵 질의응답</a></div>
<div class="proof-footer"><Link to="27">← Q&amp;A로 돌아가기</Link></div>
<style>
.proof-lead { font-size: 1.12rem; line-height: 1.4; margin: 0 0 8px; color: var(--ink); }
.proof-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.proof-grid.three { grid-template-columns: repeat(3,minmax(0,1fr)); }
.proof-card { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.proof-card h3 { margin: 0 0 7px; font-size: 1.05rem; font-weight: 750; color: var(--ink); }
.proof-card p, .proof-card li { margin: 0; font-size: 0.92rem; line-height: 1.38; overflow-wrap: break-word; }
.proof-card ul { margin: 6px 0 0; padding-left: 19px; }
.proof-stat { font-size: 2.05rem; color: var(--blue); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.proof-small { font-size: 0.84rem; color: var(--muted); line-height: 1.35; }
.proof-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 0.9rem; }
.proof-table th { text-align: left; color: var(--blue); font-weight: 800; border-bottom: 2px solid var(--line); padding: 7px 8px; }
.proof-table td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; line-height: 1.35; overflow-wrap: break-word; }
.proof-table td:first-child { font-weight: 750; }
.proof-line { padding: 8px 12px; border-left: 4px solid var(--blue); background: rgba(27,98,203,0.065); border-radius: 4px; font-size: 0.96rem; line-height: 1.4; margin-top: 9px; }
.proof-source { margin-top: 7px; font-size: 0.75rem; color: var(--muted); line-height: 1.3; overflow-wrap: break-word; }
.proof-source a { color: var(--blue); text-decoration: none; }
.proof-footer { margin-top: auto; display: flex; align-items: baseline; justify-content: flex-end; gap: 12px; padding-top: 8px; font-size: 0.77rem; line-height: 1.4; }
.proof-footer a { color: var(--blue); text-decoration: none; font-weight: 700; }
.proof-flow { display: flex; align-items: stretch; gap: 8px; margin: 17px 0; }
.proof-flow .step { flex: 1; min-width: 0; display: flex; justify-content: center; align-items: center; padding: 10px 8px; border: 1.5px solid var(--line); border-radius: 10px; text-align: center; font-size: 0.88rem; font-weight: 700; line-height: 1.35; }
.proof-flow .step.accent { border-color: var(--blue); }
.proof-flow .arrow { align-self: center; color: var(--blue); font-size: 1.35rem; flex: 0 0 auto; }
.proof-band { display: grid; grid-template-columns: 110px 1fr; border-bottom: 1px solid var(--line); gap: 12px; padding: 10px 0; font-size: 0.94rem; line-height: 1.37; }
.proof-band b { color: var(--blue); }
</style>
<!--
[0초 · 보조 자료 · 발표 시간 외]
지원이 완료된 버전은 Python 3.11부터 3.15, CUBRID 10.2부터 11.4까지입니다. 새 CUBRID 버전이 나오면 매트릭스에 추가해 검증합니다. CUBRID 12의 출시 일정은 공개된 것이 없고, Vector 타입은 CUBRID 저장소에서 아직 개발 중입니다. 유지보수는 PR 정책, 릴리스 호환성 매트릭스, 실서버 예제 검증에 기반합니다.
-->
