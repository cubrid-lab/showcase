---
theme: default
title: "CUBRID Python Ecosystem — From Contributors to Maintainers"
info: "2026 OSS Developer Contest Finals"
author: "CUBRID Lab — Yeongseon Choe & Gyeongjun Paik"
drawings:
  persist: false
transition: fade
# Finals run offline: no Google Fonts / CDN favicon
fonts:
  provider: none
favicon: /favicon.svg
# Hash routes (/#/5) survive a refresh on any static server, no SPA fallback needed
routerMode: hash
---

# 2020년, 두 사람이 만났다

**멘토 최영선 × 멘티 백경준**
(오픈소스 컨트리뷰톤 CNBT-41)

| | |
|---|---|
| **배운 것** | SQLAlchemy |
| **만난 사람** | Mike Bayer (창시자, Gitter) |
| **만든 커뮤니티** | SQLAlchemy Korea |

# 6년 후 — 하나의 생태계를 들고 돌아왔다

<!--
2020년, NIPA가 운영하는 오픈소스 컨트리뷰톤에서 두 사람이 만났습니다.
멘토와 멘티로요. 저희입니다.
그때 SQLAlchemy를 배웠고, Gitter에서 창시자 Mike Bayer님과 대화하면서
한국 커뮤니티도 만들었습니다. 6년 후, 하나의 생태계를 들고 왔습니다.
-->

---

## The Gap — Why This Matters

### 한국 공공부문 DBMS 2위 CUBRID (13.24%) — 그런데 Python은 죽어있었다

| | |
|---|---|
| **zzzeek/sqlalchemy_cubrid** | Mike Bayer가 2012년 제작 → 방치 |
| **공식 Python 드라이버** | 마지막 릴리스 2014-05-15 |
| **공공 DBMS 점유율** | 13.24% · 2,367개 설치 · Oracle 다음 2위 (2025년 말) |

<sub>출처: 행정안전부·NIA 「2026년도 범정부EA기반 공공부문 정보자원 현황 통계보고서」 (2025년 말 기준)</sub>

> **"방언도 죽어가고, 드라이버도 죽어있었다.
> 방언을 살리려니 — 드라이버부터 새로 만들어야 했다."**

<EvidenceFooter claim="cubrid-public-sector, official-driver-2014" />

---

## What We Built — 4 Projects

### 연대기: 각 단계가 다음 단계를 자연스럽게 낳았다

**① sqlalchemy-cubrid (2021-22)** — ORM dialect, 공식 테스트 스위트 통합

**② pycubrid (2025)** — 순수 Python 드라이버, CAS 프로토콜 해독, 의존성 0

**③ cubrid-cookbook (2026)** — 68 예제 + 7 템플릿, dogfooding 플랫폼

**④ cubrid-mcp-server (2026)** — 세계 최초 CUBRID MCP, AI/LLM 접근

> **"각 단계가 다음 단계를 자연스럽게 낳았다."**

<EvidenceFooter claim="mcp-world-first" />

---

## Developer Experience

### 개발자가 5분 안에 시작하는 방법

```bash
pip install pycubrid                    # 1초, C 컴파일러 불필요
```

```python
import pycubrid
conn = pycubrid.connect(host="localhost", port=33000,
                        database="demodb", user="dba")
cur = conn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())  # (1,)
```

**7개 프로덕션 템플릿** — 복사해서 바로 수정:

| Template | Stack |
|---|---|
| FastAPI 서비스 | REST API + Docker |
| Django 앱 | ORM + Admin |
| Streamlit 대시보드 | 원커맨드 `docker compose up` |
| AI 에이전트 | MCP + RAG metadata |
| Celery 워커 | 비동기 작업 처리 |
| Pandas ETL | 배치 파이프라인 |
| Flask 웹앱 | 클래식 패턴 |

**문서**: 4개 사이트 (한국어 34페이지) · Demo GIF 모든 README · GETTING_STARTED.md

<!--
개발자가 이 생태계를 시작하는 데 5분이면 됩니다.
pip install 한 줄, C 컴파일러도 필요 없습니다.
7개 프로덕션 템플릿이 있어서 복사해서 바로 수정하면 됩니다.
FastAPI, Django, Streamlit 대시보드, 심지어 AI 에이전트 템플릿까지.
문서는 4개 사이트에 한국어 34페이지, 데모 GIF도 모든 README에 있습니다.
-->

---

## Code Quality — How We Ensure It

### "2,200개 테스트는 우연이 아니다 — 품질 게이트 시스템"

```
┌─────────────────────────────────────────┐
│         Quality Gate System             │
├─────────────────────────────────────────┤
│ Type Safety    mypy --strict, 0 errors │
│ Coverage       ≥95% (CI 강제)           │
│ Lint/Format    ruff check + format     │
│ Property Test  hypothesis (난수 기반)   │
│ API Compat     api-baseline.json 게이트 │
│ Security       CodeQL + 감사 로그      │
│ Golden Tests   45 예제, 매일 밤 실서버  │
│ SA Test Suite  720 tests (공식 스위트)  │
└─────────────────────────────────────────┘
```

| Gate | Value | How |
|---|---|---|
| **mypy --strict** | 0 errors | CI 강제 — 타입 안전성 |
| **Coverage ≥95%** | CI 강제 | 커버리지 미달 시 머지 불가 |
| **hypothesis** | Property-based | 랜덤 입력으로 엣지 케이스 발견 |
| **api-baseline.json** | API 호환성 | 공개 API 변경 감지 |
| **Golden Tests** | 45 examples | 매일 밤 CUBRID 11.2+11.4 실서버 |
| **CodeQL** | 보안 스캔 | 모든 PR에서 자동 실행 |

> "AI가 작성한 코드가 이 게이트를 통과해야 머지됩니다.
> 품질은 목표가 아니라 전제 조건입니다."

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

## Performance — Benchmark-Driven

### 니치 시장에서는 사용자가 성능을 알려주지 않는다 — 직접 측정한다

<SnapshotMetrics category="performance" />

재현: [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark)

---

## Standards & Open Source

### "폐쇄형 데모가 아니라, 개방형 표준 위의 상호운용 OSS 인프라"

| Standard | Compliance | Evidence |
|---|---|---|
| **PEP 249** (DB-API 2.0) | pycubrid 완전 준수 | 1,147 테스트 |
| **PEP 561** (Type Safety) | py.typed, mypy strict 0 errors | CI 강제 |
| **SQLAlchemy Dialect API** | 공식 테스트 스위트 통합 | 53 feature flags |
| **MCP Specification** | Tools + Resources + Prompts | 세계 최초 CUBRID MCP |

### 오픈소스 스택:

| Layer | OSS | License |
|---|---|---|
| ORM | SQLAlchemy | MIT |
| Predecessor | zzzeek/sqlalchemy_cubrid | MIT |
| Protocol ref | node-cubrid | BSD |
| MCP | Model Context Protocol | MIT |
| Testing | pytest, hypothesis | MIT/MPL |
| CI/CD | CodeQL, Dependabot | GitHub |

> "오픈소스 기여로 배우고, 죽은 프로젝트에서 영감을 받고, 새 생태계를 만들었다."

<EvidenceFooter claim="pep249-compliance" />

---

## Demo — On-nara Meets Python + AI

### "CUBRID 공공 업무는 Java 중심이었습니다.
### 저희가 Python, 대시보드, AI 질의, 안전한 실행 정책까지 연결했습니다."

**2 min · 온나라(행안부 전자결재) 시나리오** — Dashboard 15s · **Claude/MCP 90s** · Terminal 15s

| # | Ask | Story |
|---|---|---|
| 1 | "이 DB에 어떤 테이블이 있어?" | 탐색 |
| 2 | **"결재가 지연된 문서 TOP 5는? 평균 처리일과 대기 수로"** | ★ **AI 운영 분석** |
| 3 | "기밀 문서는 부처별로 몇 개야? 내용은 보지 말고 집계만" | 집계만 질의 |
| 4 | **"결재 대기 문서를 전부 승인 처리해줘"** | ★★ **쓰기 차단** |

> **기본 읽기 전용** — 쓰기 도구는 노출되지 않고, 쓰기 SQL은 화이트리스트에서 거부

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

## How We Work — AI + Human

```
AGENTS.md (rules) → AI implements → Human reviews → CI gates → Human releases
```

- **450 PRs** — CI 게이트 통과 후 병합 (드라이버·방언: 20조합 라이브 DB)
- Translation sync CI (한국어 하드 게이트)
- Label taxonomy + weekly drift audit
- SBOM + SPDX on every release

> "AI가 작성한 코드를 검증하는 **시스템**을 만들었다."

---

## Licensing

**MIT × 4** · THIRD_PARTY_LICENSES · NOTICE · SPDX SBOM · No GPL

CUBRID server: Apache-2.0 / BSD (COPYING 검증)

Our packages: 독립 wire-protocol 클라이언트 — 서버 코드 포함 안 함

---

## Ecosystem Vision

### Python이 레퍼런스 — TypeScript, Go, Rust도 진행 중

| Language | Driver | ORM | Status |
|---|---|---|---|
| **Python** | pycubrid v1.7.1 | sqlalchemy-cubrid v1.7.1 | **완성** |
| TypeScript | cubrid-client v1.1.0 | drizzle-cubrid v0.2.1 | 진행 |
| Go | cubrid-go v0.2.1 | gorm-cubrid v0.1.0 | 진행 |
| Rust | cubrid-rs v0.1.0 | sea-orm-cubrid v0.1.0 | 진행 |

### 커뮤니티: SQLAlchemy Korea 경험으로

### 지속가능성: MIT, 문서화된 governance, AI/MCP = 다음 세대 개발자

---

## Judge Verification

```bash
uvx cubrid-mcp-server          # PyPI (v0.4.0)
# or
docker compose up && make verify   # GitHub Release (지금)
```

**VERIFY.md** — 단계별 검증 가이드

---

## Adoption Metrics

<SnapshotMetrics category="adoption" />

---

## Closing — The Flywheel

# 컨트리뷰톤에서 배웠다
# → Mike Bayer를 만났다
# → 죽은 방언에서 영감을 받아 새로 썼다
# → 드라이버부터 생태계까지 만들었다
# → 다음 기여자를 기다린다

```bash
pip install pycubrid    # 2014년의 갭, 2026년에 닫았다
```

**Driver · ORM · 68 Examples · 7 Templates · AI/MCP · 2,200 Tests · 450 PRs**

*오픈소스는 선순환한다 — CUBRID Lab*

<!--
2020년에 멘토로 시작해서 6년이 걸렸습니다.
기여자에서 커뮤니티 빌더가 되고, 방언을 만들고,
드라이버를 만들고, 결국 생태계를 만들었습니다.
SQLAlchemy Korea도 계속 운영하고 있습니다.
다음 컨트리뷰톤에서 누군가 저희 프로젝트를 이어가 주길 기다립니다.
-->
