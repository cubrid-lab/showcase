# Presentation Slides — 2026 OSS Developer Contest Finals

> 12 slides, 12 minutes. Story-driven narrative.
> Numbers verified 2026-09-12. Re-measure on presentation day.

---

## Slide 1: Opening — 2020, Two People Met (PT + 팀 소개)

**(텍스트가 순서대로 등장)**

# 2020년, 두 사람이 만났다

**멘토 최영선 × 멘티 백경준**
(오픈소스 컨트리뷰톤 CNBT-41)

| | |
|---|---|
| **배운 것** | SQLAlchemy |
| **만난 사람** | Mike Bayer (창시자, Gitter) |
| **만든 커뮤니티** | SQLAlchemy Korea |

# 6년 후 — 하나의 생태계를 들고 돌아왔다

---

## Slide 2: The Full OSS Journey (PT)

### 2020년 한 해, 네 가지 역할

| Role | What | Evidence |
|---|---|---|
| **Mentor** | 컨트리뷰톤 SQLAlchemy/HANA (CNBT-41) | 2020.05 접수 |
| **Contributor** | sqlalchemy-hana (SAP) 기여 | GitHub verified |
| **Community builder** | SQLAlchemy Korea 개설 | 2020.10, Mike Bayer와 Gitter 논의 후 |
| **Learner** | Mike Bayer와 직접 교류 | Gitter 채팅 |

> "받은 것을 가르치고, 가르친 것으로 커뮤니티를 만들고,
> 커뮤니티에서 영감을 받아 새것을 만들었다."

---

## Slide 3: The Gap We Found (PT + 활용성)

### CUBRID had a SQLAlchemy dialect. Mike Bayer made it. Then abandoned it.

| | |
|---|---|
| **zzzeek/sqlalchemy_cubrid** | Created 2012 by Mike Bayer (SQLAlchemy 창시자) |
| Status | **Unmaintained** — old SQLAlchemy, no Python 3.10+ |
| Official Python driver | **Last release: 2014-05-15** |
| CUBRID market | **10.6%** of Korean public sector (1,500+ systems) |

> **"방언도 죽어가고, 드라이버도 죽어있었다.
> 방언을 살리려니 — 드라이버부터 새로 만들어야 했다."**

---

## Slide 4: The Journey — What We Built & How (PT)

### ① sqlalchemy-cubrid (2021-22) — "우리가 아는 것부터"

**난제:** Mike Bayer의 방언이 SA 1.x 시절 구조로 죽어있었다
**해결:** SA 2.0 Dialect API로 처음부터 작성 — 공식 테스트 스위트 통합

| 기술 성과 | 내용 |
|---|---|
| 스키마 리플렉션 | 테이블·컬럼·PK·FK·인덱스·뷰·코멘트 전부 |
| DML 확장 | ON DUPLICATE KEY UPDATE, MERGE, REPLACE |
| Native ENUM | CUBRID 10.2–11.4 실증 후 구현 (#343) |
| Alembic | 비트랜잭션 DDL 처리 + autogenerate 지원 |

### ② pycubrid (2025) — "드라이버가 없어서 직접 만들었다"

**난제:** CAS 바이너리 프로토콜 문서가 없었다
**해결:** node-cubrid(BSD) + 공식 C 드라이버 소스 역분석으로 프로토콜 해독

```python
# 우리가 해독한 CAS 프로토콜 구조
# [4B data_length][4B cas_info][payload]
# 18개 패킷 타입 · 27개 데이터 타입 · big-endian
# TLS STARTTLS 업그레이드 · 브로커 리다이렉트 · 자동 재연결
```

| 기술 성과 | 내용 |
|---|---|
| 순수 Python | C 확장 없음, 의존성 0개, 크로스 플랫폼 |
| asyncio 네이티브 | pycubrid.aio — 동시성 쿼리 지원 |
| TLS/SSL | STARTTLS 방식 업그레이드 |
| 이스케이프 협상 | no_backslash_escapes 자동 감지 |
| **벤치마킹 기반 최적화** | 프로파일링 → 개선 → 검증 (아래) |

### ③ cubrid-cookbook (2026) — "우리가 직접 써보자 (dogfooding)"

**역할:** 예제집 + 최전선 통합 테스트
**증거:** pycubrid 1.7.0 이스케이프 버그를 cookbook이 가장 먼저 감지

### ④ cubrid-mcp-server (2026) — "AI 시대니까"

**난제:** LLM이 CUBRID SQL 구문을 모른다 (LIMIT, SHOW TRACE, SET 타입)
**해결:** 도메인 지식 팩을 서버에 내장 — LLM에게 CUBRID를 가르친다

```
12 tools + 5 domain-knowledge resources + 9 expert prompts
→ LLM이 CUBRID를 몰라도 올바른 SQL을 생성
→ 읽기 전용 화이트리스트로 DROP TABLE도 서버가 거부
→ 세계 최초의 CUBRID MCP 서버
```

---

## Slide 5: Technical Architecture (PT)

### 프로토콜부터 AI까지 — 전부 직접 구현

```
         ┌─────────────────────────────────┐
         │   cubrid-mcp-server (AI/LLM)    │
         │   · MCP protocol (JSON-RPC)     │
         │   · 12 tools + domain knowledge │
         │   · read-only whitelist         │
         ├─────────────────────────────────┤
         │   cubrid-cookbook (dogfooding)  │
         │   · 75 examples = 75 tests     │
         │   · nightly live DB execution   │
         ├─────────────────────────────────┤
         │   sqlalchemy-cubrid (ORM)       │
         │   · SQLAlchemy Dialect API      │
         │   · reflection + DML + Alembic  │
         ├─────────────────────────────────┤
         │   pycubrid (driver)             │
         │   · CAS binary protocol v8      │
         │   · 18 packet types decoded     │
         │   · pure Python, zero deps     │
         ├─────────────────────────────────┤
         │   CUBRID Server (TCP:33000)     │
         └─────────────────────────────────┘
```

**각 계층이 아래 계층만 의존 — 순환 없음, 전부 MIT**

---

## Slide 5.5: Performance — 벤치마킹으로 측정하고 최적화했다 (기능테스트)

### 과학적 방법: 벤치마크 → 프로파일 → 최적화 → 검증

**[cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark) 저장소** — 재현 가능한 비교 벤치마크

| 최적화 | Before | After | 개선 |
|---|---|---|---|
| **Native ping()** (vs SELECT 1) | — | — | **+280% 처리량** |
| **SA pool_pre_ping** | — | — | **+588% 처리량** |
| **bulk insert 1000행** | 2,865ms | 2,512ms | **12.3% faster** |
| **query select-all** | 39.8ms | 31.8ms | **19.9% faster** |
| **fetch 최적화** | 96ms | 78ms | **-19% latency** |

### 프로파일링 도구 (demos/ + scripts/)

```bash
# 병목을 찾고 → 수정하고 → 재측정
scripts/profile_connect.py    # 핸드셰이크 병목 분석
scripts/profile_execute.py    # DML 경로 분석
scripts/profile_fetch.py      # fetch 병목 분석
# + enable_timing=True (드라이버 내장 계측)
```

> **"니치 시장에서는 사용자가 성능 문제를 알려주지 않는다.
> 우리가 직접 벤치마크하고, 프로파일하고, 최적화했다."**

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
| Predecessor | zzzeek/sqlalchemy_cubrid | MIT | Mike Bayer's original — inspiration for our rebuild |
| Protocol reference | node-cubrid | BSD | CAS wire protocol decoding |
| MCP protocol | Model Context Protocol | MIT | AI/LLM access (world's first for CUBRID) |
| Testing | pytest, hypothesis | MIT/MPL | 2,200 tests |
| CI/CD | CodeQL, Dependabot | GitHub | 20-combination matrix |
| Benchmark | cubrid/cubrid Docker | CUBRID | Live DB testing 10.2–11.4 |

> "오픈소스 기여로 배우고, 죽은 프로젝트에서 영감을 받고, 새 생태계를 만들었다."

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

## Slide 12: The Flywheel — Closing (PT)

# 컨트리뷰톤에서 배웠다
# → Mike Bayer를 만났다
# → 죽은 방언에서 영감을 받아 새로 썼다
# → 드라이버부터 생태계까지 만들었다
# → 다음 기여자를 기다린다

```bash
pip install pycubrid    # 2014년의 갭, 2026년에 닫았다
```

**Driver · ORM · 75 Examples · 7 Templates · AI/MCP · 2,200 Tests · 450 PRs**

*오픈소스는 선순환한다 — CUBRID Lab*

---
---

## Appendix: Story Beats (발표 스크립트)

### 슬라이드 1 (오프닝 + 팀 소개, 30초)
> "2020년, NIPA가 운영하는 오픈소스 컨트리뷰톤에서 두 사람이 만났습니다.
> 멘토와 멘티로요. 저희입니다.
> 그때 SQLAlchemy를 배웠고, Gitter에서 창시자 Mike Bayer님과 대화하면서
> 한국 커뮤니티도 만들었습니다. 6년 후, 하나의 생태계를 들고 왔습니다."

### 슬라이드 2 (여정, 30초)
> "2020년 한 해에 저희는 네 가지 역할을 했습니다.
> 컨트리뷰톤 멘토, SAP sqlalchemy-hana 기여자,
> Mike Bayer와 Gitter에서 대화한 학습자,
> 그리고 SQLAlchemy Korea 커뮤니티 빌더.
> 이 네 가지가 지금 프로젝트의 기반입니다."

### 슬라이드 3 (갭 발견, 20초)
> "Mike Bayer님이 2012년에 CUBRID 방언을 만드셨지만 방치되어 있었습니다.
> 드라이버는 더 심각했습니다 — 2014년 이후 죽어있었으니까."

### 슬라이드 4 (프로젝트 소개, 60초 — 연대기 순)
> "첫 번째로 sqlalchemy-cubrid를 만들었습니다. Mike Bayer님이 만들다
> 버린 방언을 SQLAlchemy 2.0 기준으로 처음부터 썼습니다.
>
> 두 번째, 방언을 만들다 보니 드라이버가 문제였습니다.
> 2014년 이후 방치된 C 확장. 그래서 pycubrid를 순수 Python으로
> 만들었습니다. 의존성 0개, pip install 한 줄.
>
> 세 번째, cookbook을 만들었습니다. 단순한 예제집이 아니라
> 우리 드라이버를 실제 애플리케이션에서 직접 써보는 dogfooding입니다.
> 75개 예제가 매일 밤 실서버에서 실행되고,
> 드라이버에 버그가 있으면 cookbook이 가장 먼저 잡습니다.
> 실제로 pycubrid 1.7.0의 이스케이프 버그를 cookbook이 잡았습니다.
>
> 네 번째, MCP 서버를 만들었습니다. 세계 최초입니다.
> 각 단계가 다음 단계를 자연스럽게 낳았습니다."

### 슬라이드 5.5 (성능, 30초)
> "벤치마킹을 통해 성능을 개선했습니다. cubrid-benchmark라는 별도
> 저장소를 만들어 재현 가능한 비교 환경을 구축했고,
> 프로파일링 스크립트로 병목을 찾아 최적화했습니다.
>
> 대표적인 결과: native ping을 구현해서 SELECT 1 폴백 대비
> 280% 처리량 향상, SQLAlchemy pool_pre_ping 시나리오에서는
> 588% 향상을 달성했습니다. 대량 INSERT도 12% 빨라졌습니다.
>
> 이게 니치 시장에서 성능을 개선하는 방법입니다 —
> 사용자가 알려줄 때까지 기다리지 않고 직접 측정합니다."

### 슬라이드 4-5 (기술 심화, 90초)
> "pycubrid의 가장 어려웠던 부분은 CAS 바이너리 프로토콜 해독이었습니다.
> 공식 문서가 없어서 node-cubrid의 BSD 코드와 C 드라이버 소스를
> 교차 분석해서 18개 패킷 타입과 27개 데이터 타입을 해독했습니다.
>
> sqlalchemy-cubrid는 Mike Bayer님이 만들다 버린 방언을
> SQLAlchemy 2.0 기준으로 처음부터 썼습니다. 스키마 리플렉션,
> MERGE, ON DUPLICATE KEY UPDATE, native ENUM까지 지원합니다.
>
> MCP 서버는 단순히 도구를 노출하는 게 아니라, 도메인 지식 팩을
> 내장해서 LLM이 CUBRID 구문을 모르더라도 올바른 SQL을
> 생성할 수 있게 했습니다. 이게 세계 최초의 CUBRID MCP 서버입니다."

### 슬라이드 8 (OSS 스택, 20초)
> "이 프로젝트의 기반은 전부 오픈소스입니다. 컨트리뷰톤에서 배웠고,
> Mike Bayer님의 원작에서 영감을 받았고, node-cubrid의 BSD 코드가
> 프로토콜 해석의 출발점이었습니다."

### 슬라이드 12 (클로징, 20초)
> "2020년에 멘토로 시작해서 6년이 걸렸습니다.
> 기여자에서 커뮤니티 빌더가 되고, 방언을 만들고,
> 드라이버를 만들고, 결국 생태계를 만들었습니다.
> SQLAlchemy Korea 커뮤니티도 계속 운영하고 있습니다.
> 다음 컨트리뷰톤에서 누군가 저희 프로젝트를 이어가 주길 기다립니다."
