# Presentation Slides — 2026 OSS Developer Contest Finals

> 12 slides, 12 minutes. Story-driven narrative.
> Numbers verified 2026-09-12. Re-measure on presentation day.

---

## Slide 1: We Met at a Hackathon (PT)

# From Contributors to Maintainers

**오픈소스 컨트리뷰톤 — 멘토와 멘티로 만났다**

**→ SQLAlchemy · sqlalchemy-hana에 기여**

**→ SQLAlchemy 창시자 Mike Bayer가 CUBRID 방언을 만들었었다**

**→ 2012년에 만들고... 유지보수가 끊겼다**

*CUBRID Lab — Yeongseon Choe & Gyeongjun Paik*

---

## Slide 2: What We Learned (PT)

### Contributing to SQLAlchemy & sqlalchemy-hana

| What we did | What we learned |
|---|---|
| SQLAlchemy core patches | Dialect API internals |
| sqlalchemy-hana (SAP HANA dialect) | How to build a production dialect |
| Mini hackathon with Mike Bayer | Direct guidance from SQLAlchemy creator |
| Code review culture | AGENTS.md-driven AI workflow |
| Test-driven development | 95% coverage discipline |

> "기여하면서 배웠다. 이제 우리 차례."

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

## Slide 4: What We Did (PT)

### Rebuild from scratch. Driver too. Then grow the ecosystem.

```
2021-22: sqlalchemy-cubrid — Mike Bayer의 작품에서 영감을 받아
   → SQLAlchemy 2.0 기준 처음부터 작성 (포크가 아닌 신규 구현)
   → C 확장 드라이버의 한계 발견 (컴파일, asyncio 불가)

2025: pycubrid — 드라이버를 순수 Python으로 새로 작성
   → 의존성 0, asyncio 네이티브, TLS, pip install 한 줄

2026: 생태계 확장
   → cookbook (75 예제, 7 템플릿)
   → cubrid-mcp-server (AI/LLM, 세계 최초)
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

## Slide 8: The OSS Stack We Stand On (OSS 적절성)

**We stand on the shoulders of giants — including the ones who came before us:**

| Layer | OSS | License | How we use it |
|---|---|---|---|
| ORM framework | SQLAlchemy | MIT | Dialect API (learned by contributing) |
| Predecessor | zzzeek/sqlalchemy_cubrid (Mike Bayer) | MIT | Inspiration — we rebuilt from scratch for SA 2.0 |
| Protocol reference | node-cubrid | BSD | CAS wire protocol decoding |
| MCP protocol | Model Context Protocol | MIT | AI/LLM access (world's first for CUBRID) |
| Testing | pytest, hypothesis | MIT/MPL | 2,200 tests |
| CI/CD | CodeQL, Dependabot | GitHub | 20-combination matrix |
| Benchmark | cubrid/cubrid Docker | CUBRID | Live DB testing 10.2–11.4 |

> "오픈소스 기여로 배우고, 죽은 프로젝트를 살리고, 새 생태계를 만들었다."

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
> "저희는 오픈소스 컨트리뷰톤에서 멘토-멘티로 만났습니다.
> SQLAlchemy와 SAP HANA dialect에 기여하면서 방언 API를 배웠습니다.
> 미니 해커톤에서 SQLAlchemy 창시자 Mike Bayer님과도 이야기할 기회가 있었습니다."

### 슬라이드 3-4에서 (30초)
> "Mike Bayer님이 2012년에 CUBRID 방언을 만드셨지만 유지보수가 끊겼습니다.
> SQLAlchemy 2.0도 안 되고, Python 3.10+도 안 됐습니다.
> 우리는 이것을 계승하는 게 아니라, SQLAlchemy 2.0 기준으로
> 처음부터 다시 쓰기로 했습니다. 그런데 쓰다 보니 근본 문제가 드라이버였습니다.
> 2014년 이후 방치된 C 확장. 그래서 드라이버를 순수 Python으로
> 새로 만들었습니다."

### 슬라이드 8에서 (20초)
> "이 프로젝트의 기반은 전부 오픈소스입니다. SQLAlchemy를 기여하며 배웠고,
> Mike Bayer님의 원작에서 영감을 받았고, node-cubrid의 BSD 코드가
> 프로토콜 해석의 출발점이었습니다. 오픈소스 커뮤니티에서 배워서
> 새 생태계를 만든 것입니다."

### 슬라이드 12에서 (20초 — 클로징)
> "저희는 멘토-멘티로 만나서 기여자가 되었고, Mike Bayer님의 작품에서
> 영감을 받아 새로 썼고, 결국 생태계 전체를 만들었습니다.
> 다음 컨트리뷰톤에서 누군가 저희 프로젝트를 이어가 주길 기다립니다."
