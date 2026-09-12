# Presentation Slides — 2026 OSS Developer Contest Finals

> 12 slides, 12 minutes. Story-driven narrative.
> Numbers verified 2026-09-12. Re-measure on presentation day.

---

## Slide 1: We Met at a Hackathon (PT)

# From Contributors to Maintainers

**2020 오픈소스 컨트리뷰톤 (CNBT-41) — 멘토와 멘티로 만났다**

**→ SQLAlchemy · sqlalchemy-hana 기여**

**→ Mike Bayer (창시자)와 Gitter로 교류**

**→ SQLAlchemy Korea 커뮤니티 개설 (2020.10)**

**→ Mike가 2012년에 만든 CUBRID 방언... 죽어있었다**

*CUBRID Lab — Yeongseon Choe & Gyeongjun Paik*

---

## Slide 2: The Full OSS Journey (PT)

### 2020: One year, four roles

| Role | What | Evidence |
|---|---|---|
| **Mentor** | 컨트리뷰톤 SQLAlchemy/HANA (CNBT-41) | 2020.05 접수 |
| **Contributor** | sqlalchemy-hana (SAP)에 기여 | GitHub verified |
| **Community builder** | SQLAlchemy Korea 그룹 개설 | 2020.10, Mike Bayer와 Gitter 논의 후 |
| **Learner** | Mike Bayer와 직접 교류 | 미니 해커톤 + Gitter |

> "받은 것을 가르치고, 가르친 것으로 커뮤니티를 만들고,
> 커뮤니티에서 영감을 받아 새것을 만들었다."

---

## Slide 3: What We Found (PT + 활용성)

### Mike Bayer created a CUBRID dialect in 2012. Then abandoned it.

| | |
|---|---|
| **zzzeek/sqlalchemy_cubrid** | Created 2012 by SQLAlchemy author Mike Bayer |
| Status | **Unmaintained** — old SQLAlchemy, no Python 3.10+ |
| Official Python driver | **Last release: 2014-05-15** |
| CUBRID market | **10.6%** of Korean public sector DBMS (1,500+ systems) |

> SQL 창시자도 만들었던 방언이 죽어있었다.
> 우리는 처음부터 다시 만들기로 했다 — SQLAlchemy 2.0 기준으로.

---

## Slide 4: What We Did — 6 Year Journey (PT)

```
2020.05  컨트리뷰톤 멘토 (CNBT-41) — SQLAlchemy/HANA
2020.10  SQLAlchemy Korea 개설 (Mike Bayer와 Gitter 논의)
         sqlalchemy-hana 기여

2021.07  sqlalchemy-cubrid 첫 커밋
2022.05  Google Meet 킥오프 — 방향 결정
2022.07  본격 개발 시작 (Yeongseon + Gyeongjun)
2022.09  리플렉션 구현 + 튜토리얼

2025     pycubrid — 순수 Python 드라이버 (의존성 0, asyncio, TLS)

2026     cubrid-mcp-server + cookbook + AI agent template
         → 완전한 생태계
```

---

## Slide 5: What We Built — 4 Layers (PT + 활용성)

```
cubrid-mcp-server          ← AI/LLM (12 tools + 5 skills + 9 prompts)
        ↑
cubrid-cookbook-python     ← 75 examples + 7 templates (AI agent 포함)
        ↑
sqlalchemy-cubrid          ← ORM (SQLAlchemy 2.0-2.2, native ENUM)
        ↑
pycubrid                   ← Driver (pure Python, asyncio, TLS, zero deps)
```

**죽어가던 방언에서, 완전한 생태계로.**

---

## Slide 6: Adoption Signals (활용성)

| Metric | Value |
|---|---|
| GitHub stars (4 repos) | **111** |
| Unique clones (14 days) | **822** developers |
| Merged PRs | **450** |
| PyPI releases | **35** |
| Tests | **2,200** (CI-enforced) |
| Documentation sites | **4/4 live** |
| Korean docs | **34 pages** |

**What the official driver can't do:**

| Feature | Official (2014) | pycubrid |
|---|---|---|
| asyncio | ❌ | ✅ native |
| TLS/SSL | ❌ | ✅ |
| Python 3.10–3.14 | ❌ (3.4 max) | ✅ |
| Pure Python | ❌ (C extension) | ✅ |
| MCP server | — | ✅ (**world's first**) |

---

## Slide 7: Demo — 3 Layers Live (데모 + 기능테스트)

**4 minutes:**

1. **App** (60s) — `docker compose up` → Streamlit dashboard
2. **AI** (90s) — Claude: "show tables" → "DROP TABLE" → **rejected** (whitelist)
   → MCP server가 LLM에게 CUBRID SQL을 가르친다 (domain knowledge)
3. **Driver** (60s) — `pip install pycubrid` → connect → asyncio → zero deps

*Backup video ready. Read-only whitelist is server-enforced.*

---

## Slide 8: Demo — On-nara Meets Python (데모 10점 · 7:30-9:30)

### "행안부 온나라는 Java입니다. 우리가 Python으로 처음 연결했습니다."

**온나라(47개 부처, 전자결재/문서/기록물) = 가장 잘 알려진 CUBRID 공공 배포**
→ 전부 Java(JDBC). 공개된 Python 사례 = 0건 (우리가 만들기 전까지)

**4 minutes · 3 layers:**

### Layer 3 — Document Dashboard (60s)



부처별 문서량 · 결재 대기 현황 · 보안 등급 통계

### Layer 2 — Claude AI (90s)

| Ask | Tool |
|---|---|
| "테이블 목록 보여줘" |  |
| "부처별 문서량 상위 5개" |  |
| "결재 대기 중인 문서는?" |  (JOIN) |
| **"documents 테이블 지워줘"** | **REJECTED** ← 서버 수준 화이트리스트 |
| "기밀 문서는 몇 개야?" |  (ENUM 이해) |

> "정부 문서를 지우려는 AI가 서버에서 차단됐습니다.
> 이게 서버 수준 보안입니다."

### Layer 1 — Driver (60s)



---

## Slide 9: Quality Gates (기능테스트)

| Gate | Value |
|---|---|
| Tests | **2,200** (1,147 + 769 + 284) |
| CI matrix (live DB) | Python 5 × CUBRID 4 = **20 combinations** |
| Coverage floor | **95%** (CI-enforced) |
| Type safety | mypy strict, **0 errors** |
| API compatibility | api-baseline.json gate |
| SQLAlchemy suite | Official test suite integrated |
| Native ENUM | Verified live on CUBRID 10.2–11.4 (#343) |
| SBOM | SPDX on every GitHub Release |

---

## Slide 10: How We Work — AI + Human (커뮤니티)

### The workflow we built (from OSS contribution culture):

```
AGENTS.md (rules) → AI implements → Human reviews → CI gates → Human releases
```

- **450 merged PRs** — every one passed 20-combination live DB tests
- Translation sync CI (Korean hard gate)
- Label taxonomy with weekly drift audit
- Roadmap update policy (every release PR must update ROADMAP.md)

> "우리는 AI가 작성한 코드를 검증하는 **시스템**을 만들었다.
> 그 시스템이 450개 PR을 통과시켰다."

---

## Slide 11: Giving Back to OSS (라이선스 + 커뮤니티)

**All MIT. All open.**

- THIRD_PARTY_LICENSES.md + NOTICE in every repo
- SPDX SBOM on releases
- No GPL dependencies
- 5 good-first-issues seeded for newcomers

**CUBRID server**: Apache-2.0 / BSD — verified upstream COPYING
Our packages: independent wire-protocol clients — no server code

**Roadmap**: fastmcp `<5` (canary green), CUBRID 12, vector types,
hosted MCP, Windows CI

---

## Slide 12: The Flywheel (PT)

# 컨트리뷰톤에서 배웠다
# → Mike Bayer를 만났다
# → 죽은 방언에서 영감을 받아 새로 썼다
# → 드라이버부터 생태계까지 만들었다
# → 다음 기여자를 기다린다

```
pip install pycubrid    # 2014년의 갭, 2026년에 닫았다
```

**Driver · ORM · 75 Examples · 7 Templates · AI/MCP · 2,200 Tests · 450 PRs**

*오픈소스는 선순환한다 — CUBRID Lab*

---
---

## Appendix: Story Beats (발표 중 언급할 스크립트)

### 슬라이드 1-2에서 (30초)
> "2020년 오픈소스 컨트리뷰톤에서 저(최영선)가 멘토, 경준님이 멘티로
> 만났습니다. SQLAlchemy와 SAP HANA dialect에 함께 기여했고,
> Gitter에서 Mike Bayer님과 직접 채팅하면서 SQLAlchemy Korea 커뮤니티도
> 만들었습니다. 그 해가 저희 오픈소스 여정의 시작이었습니다."

### 슬라이드 3-4에서 (30초)
> "Mike Bayer님이 2012년에 CUBRID 방언을 만드셨지만 방치되어 있었습니다.
> 2021년에 저희가 새로 쓰기 시작했습니다. 2022년 5월에 방향을 정하고
> 7월부터 본격적으로 개발했습니다. 그런데 쓰다 보니 근본 문제가
> 드라이버였습니다 — 2014년 이후 방치된 C 확장.
> 그래서 2025년에 드라이버를 순수 Python으로 새로 만들었습니다."

### 슬라이드 8에서 (20초)
> "이 프로젝트의 기반은 전부 오픈소스입니다. 컨트리뷰톤에서 배웠고,
> Mike Bayer님의 원작에서 영감을 받았고, node-cubrid의 BSD 코드가
> 프로토콜 해석의 출발점이었습니다. 받은 것을 돌려주는 것이
> 오픈소스라고 생각합니다."

### 슬라이드 12에서 (20초 — 클로징)
> "2020년에 멘토로 시작해서 6년이 걸렸습니다.
> 기여자에서 커뮤니티 빌더가 되고, 방언을 만들고,
> 드라이버를 만들고, 결국 생태계를 만들었습니다.
> SQLAlchemy Korea 커뮤니티도 계속 운영하고 있습니다.
> 다음 컨트리뷰톤에서 누군가 저희 프로젝트를 이어가 주길 기다립니다."
