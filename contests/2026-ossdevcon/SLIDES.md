# Presentation Slides — 2026 OSS Developer Contest Finals

> 12 slides, 12 minutes. Story-driven narrative.
> Numbers verified 2026-09-12. Re-measure on presentation day.

---

## Slide 1: We Met at a Hackathon (PT)

# From Mentees to Creators

**오픈소스 컨트리뷰톤 — 멘토와 멘티로 만났다**

**→ SQLAlchemy · sqlalchemy-hana에 기여**

**→ "우리 DB는 왜 없지?"**

*CUBRID Lab — Yeongseon Choe & Gyeongjun Paik*

---

## Slide 2: What We Learned (PT)

### Contributing to SQLAlchemy & sqlalchemy-hana

| What we did | What we learned |
|---|---|
| SQLAlchemy core patches | Dialect API internals |
| sqlalchemy-hana (SAP HANA dialect) | How to build a production dialect |
| Code review culture | AGENTS.md-driven AI workflow |
| Test-driven development | 95% coverage discipline |

> "기여하면서 배웠다. 이제 우리 차례."

---

## Slide 3: The Gap We Found (PT + 활용성)

### Korean public sector DBMS: **10.6%** is CUBRID

| | |
|---|---|
| G-Cloud standard DBMS | 600+ government systems |
| Defense, MoIAC, local govts | 1,500+ systems |
| **Official Python driver** | **Last release: 2014-05-15** |

> SQLAlchemy 지식이 있는데, CUBRID엔 dialect조차 없었다.
> dialect를 만들려니 — 드라이버부터 없었다.

---

## Slide 4: So We Built Both (PT)

### The journey: ORM → Driver → Ecosystem

```
2021: sqlalchemy-cubrid 시작
   → C 확장 드라이버의 한계 발견 (컴파일, 플랫폼 제약)
   
2025: pycubrid 탄생
   → 순수 Python, asyncio, TLS, 의존성 0
   → "pip install 한 줄"로 해결
   
2026: 생태계 완성
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

**The mentor-mentee pair became a builder team.**

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

**We didn't build from scratch — we stand on the shoulders of:**

| Layer | OSS | License | How we use it |
|---|---|---|---|
| ORM framework | SQLAlchemy | MIT | Dialect API (learned by contributing) |
| Async framework | asyncio | PSF | Native driver support |
| MCP protocol | Model Context Protocol | MIT | AI/LLM access (world's first for CUBRID) |
| Testing | pytest, hypothesis | MIT/MPL | 2,200 tests |
| Type safety | mypy strict | MIT | 0 errors |
| CI/CD | CodeQL, Dependabot | GitHub | 20-combination matrix |
| Protocol reference | node-cubrid | BSD | CAS wire protocol decoding |
| Benchmark target | cubrid/cubrid Docker | CUBRID | Live DB testing 10.2–11.4 |

> "오픈소스 기여로 배워서, 오픈소스로 갚았다."

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

### The workflow we built (learned from OSS contribution culture):

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
# → CUBRID 생태계를 만들었다
# → 다음 기여자를 기다린다

```
pip install pycubrid    # 2014년의 갭, 2026년에 닫았다
```

**Driver · ORM · 75 Examples · 7 Templates · AI/MCP · 2,200 Tests · 450 PRs**

*오픈소스는 선순환한다 — CUBRID Lab*

---
---

## Appendix: Story Beats (발표 중 언급할 스토리 포인트)

### 슬라이드 1-2에서 (30초)
> "저희는 작년 오픈소스 컨트리뷰톤에서 멘토-멘티로 만났습니다.
> SQLAlchemy와 SAP HANA dialect에 기여하면서 방언 API를 배웠습니다.
> 그런데 '우리가 쓰는 CUBRID에는 왜 dialect가 없지?'라는 질문이
> 이 프로젝트의 시작이었습니다."

### 슬라이드 4에서 (30초)
> "sqlalchemy-cubrid를 만들다가 C 확장 드라이버의 한계를 발견했습니다.
> 컴파일러가 필요하고, asyncio가 없고, Python 3.10+이 안 됐습니다.
> 그래서 드라이버부터 다시 만들기로 했습니다 — 순수 Python으로."

### 슬라이드 8에서 (20초)
> "이 프로젝트의 모든 기술은 오픈소스에서 왔습니다.
> SQLAlchemy를 기여하며 배운 지식, node-cubrid의 BSD 코드가
> 프로토콜 해석의 출발점이었습니다. 오픈소스 기여로 배워서
> 오픈소스로 갚은 것입니다."

### 슬라이드 12에서 (20초 — 클로징)
> "저희는 멘토-멘티로 만나서 기여자가 되었고, 기여자에서
> 생태계를 만드는 크리에이터가 되었습니다. 다음 컨트리뷰톤에서
> 누군가 저희 프로젝트에 기여해주길 기다립니다."
