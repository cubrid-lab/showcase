# Presentation Slides — 2026 OSS Developer Contest Finals

> 14 slides, 12 minutes. Every scoring criterion has a dedicated slide.
> Numbers verified 2026-09-12. Re-measure on presentation day.

---

## Slide 1: Opening — 2020, Two People Met (PT · 0:00-0:45)

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

## Slide 2: The Gap — Why This Matters (활용성 · 0:45-1:30)

### 한국 공공부문 DBMS 10.6%가 CUBRID — 그런데 Python은 죽어있었다

| | |
|---|---|
| **zzzeek/sqlalchemy_cubrid** | Mike Bayer가 2012년 제작 → 방치 |
| **공식 Python 드라이버** | 마지막 릴리스 2014-05-15 |
| **G-Cloud 표준 DBMS** | 600+ 시스템 · 국방·행안부·지자체 |
| **영향받는 개발자** | 1,500+ 시스템 유지보수 인력 |

> **"방언도 죽어가고, 드라이버도 죽어있었다.
> 방언을 살리려니 — 드라이버부터 새로 만들어야 했다."**

---

## Slide 3: What We Built — 4 Projects (PT · 1:30-3:00)

### 연대기: 각 단계가 다음 단계를 자연스럽게 낳았다

**① sqlalchemy-cubrid (2021-22)** — ORM dialect, 공식 테스트 스위트 통합
**② pycubrid (2025)** — 순수 Python 드라이버, CAS 프로토콜 해독, 의존성 0
**③ cubrid-cookbook (2026)** — 75 예제 + 7 템플릿, dogfooding 플랫폼
**④ cubrid-mcp-server (2026)** — 세계 최초 CUBRID MCP, AI/LLM 접근

> **"각 단계가 다음 단계를 자연스럽게 낳았다."**

---

## Slide 4: Developer Experience (활용성 15점 · 3:00-4:00)

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

---

## Slide 5: Code Quality — How We Ensure It (기능테스트 10점 · 4:00-5:00)

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

---

## Slide 6: Performance — Benchmark-Driven (기능테스트 · 5:00-6:00)

### 니치 시장에서는 사용자가 성능을 알려주지 않는다 — 직접 측정한다

| Optimization | Before | After | Improvement |
|---|---|---|---|
| Native ping (CHECK_CAS) | SELECT 1 | CAS packet | **+280%** |
| SA pool_pre_ping | SQL 왕복 | native ping | **+588%** |
| Bulk insert (1000행) | 2,865ms | 2,512ms | **12.3%** |
| Query select-all | 39.8ms | 31.8ms | **19.9%** |

재현: [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark)

---

## Slide 7: Standards & Open Source (OSS 적절성 15점 · 6:00-7:30)

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

---

## Slide 8: Demo — Public Service Dashboard (데모 10점 · 7:30-9:30)

**4 minutes · 3 layers · "공공 행정 시스템" 시나리오**

### Layer 3 — App (60s): Streamlit 대시보드

```bash
cd templates/dashboard && docker compose up -d
```

**지역별 민원 처리 현황 대시보드** (공공부문 CUBRID 실제 사용 패턴)

### Layer 2 — AI (90s): Claude Desktop

1. *"이 DB에 어떤 테이블이 있어?"* → `all_table_names`
2. *"민원 데이터 구조 보여줘"* → `describe_table`
3. *"지역별 민원 상위 5개"* → `execute_query` (SELECT)
4. **"민원 테이블 지워줘"** → **거부** ← 서버 수준 화이트리스트
5. *"긴급 민원만 보여줘"* → SET 타입 (MCP가 CUBRID 타입 가르침)

### Layer 3 — Driver (60s): 터미널

```python
import pycubrid  # pip install 한 줄, C 컴파일러 불필요
conn = pycubrid.connect(host="localhost", port=33000,
                        database="demodb", user="dba")
```

*(백업 영상 준비 — 동일 런북 사전 녹화)*

---

## Slide 9: How We Work — AI + Human (커뮤니티 5점 · 9:30-10:15)

```
AGENTS.md (rules) → AI implements → Human reviews → CI gates → Human releases
```

- **450 PRs** — 모두 20조합 CI 통과
- Translation sync CI (한국어 하드 게이트)
- Label taxonomy + weekly drift audit
- SBOM + SPDX on every release

> "AI가 작성한 코드를 검증하는 **시스템**을 만들었다."

---

## Slide 10: Licensing (라이선스 5점 · 10:15-10:30)

**MIT × 4** · THIRD_PARTY_LICENSES · NOTICE · SPDX SBOM · No GPL

CUBRID server: Apache-2.0 / BSD (COPYING 검증)
Our packages: 독립 wire-protocol 클라이언트 — 서버 코드 포함 안 함

---

## Slide 11: Ecosystem Vision (커뮤니티 + 발전가능성 · 10:30-11:15)

### Python이 레퍼런스 — TypeScript, Go, Rust도 진행 중

| Language | Driver | ORM | Status |
|---|---|---|---|
| **Python** | pycubrid v1.7.0 | sqlalchemy-cubrid v1.7.0 | **완성** |
| TypeScript | cubrid-client v1.1.0 | drizzle-cubrid v0.2.1 | 진행 |
| Go | cubrid-go v0.2.1 | gorm-cubrid v0.1.0 | 진행 |
| Rust | cubrid-rs v0.1.0 | sea-orm-cubrid v0.1.0 | 진행 |

### 커뮤니티: SQLAlchemy Korea 경험으로
### 지속가능성: MIT, 문서화된 governance, AI/MCP = 다음 세대 개발자

---

## Slide 12: Judge Verification (기능테스트 · 11:15-11:30)

```bash
uvx cubrid-mcp-server          # PyPI (등록 후)
# or
docker compose up && make verify   # GitHub Release (지금)
```

**VERIFY.md** — 단계별 검증 가이드

---

## Slide 13: Adoption Metrics (활용성 · 11:30-11:45)

| Metric | Value | Meaning |
|---|---|---|
| Stars | 119 | Community interest |
| **Unique clones** (14d) | **926** | **Developers downloading code** |
| **Merged PRs** | **450** | **Validated AI+Human workflow** |
| PyPI releases | 35 | Sustained maintenance |
| **Tests** | **2,200** | **Quality gate** |
| CI combinations | 20 | **Compatibility** |

---

## Slide 14: Closing — The Flywheel (PT · 11:45-12:00)

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

## Scoring Criteria → Slide Mapping

| Criterion | Points | Dedicated Slides |
|---|---|---|
| **활용성** | 15 | Slide 2 (시장), Slide 4 (DX), Slide 13 (지표) |
| **OSS 적절성** | 15 | Slide 7 (표준 + OSS 스택) |
| **PT** | 10 | Slide 1 (오프닝), 3 (여정), 14 (클로징) |
| **데모** | 10 | Slide 8 (공공 행정 데모) |
| **기능테스트** | 10 | Slide 5 (품질 게이트), 6 (성능), 12 (검증) |
| **커뮤니티** | 5 | Slide 9 (워크플로우), 11 (비전) |
| **라이선스** | 5 | Slide 10 (MIT, SBOM, Apache) |

---

## Appendix: Speaking Scripts

### 슬라이드 1 (오프닝, 30초)
> "2020년, NIPA가 운영하는 오픈소스 컨트리뷰톤에서 두 사람이 만났습니다.
> 멘토와 멘티로요. 저희입니다.
> 그때 SQLAlchemy를 배웠고, Gitter에서 창시자 Mike Bayer님과 대화하면서
> 한국 커뮤니티도 만들었습니다. 6년 후, 하나의 생태계를 들고 왔습니다."

### 슬라이드 4 (Developer Experience, 45초)
> "개발자가 이 생태계를 시작하는 데 5분이면 됩니다.
> pip install 한 줄, C 컴파일러도 필요 없습니다.
> 7개 프로덕션 템플릿이 있어서 복사해서 바로 수정하면 됩니다.
> FastAPI, Django, Streamlit 대시보드, 심지어 AI 에이전트 템플릿까지.
> 문서는 4개 사이트에 한국어 34페이지, 데모 GIF도 모든 README에 있습니다."

### 슬라이드 5 (Code Quality, 45초)
> "2,200개 테스트는 우연이 아닙니다. 품질 게이트 시스템이 있습니다.
> mypy strict 모드로 타입 오류 0개를 CI에서 강제합니다.
> 커버리지 95% 이상이 아니면 머지가 안 됩니다.
> hypothesis로 랜덤 입력 테스트를 돌리고,
> api-baseline.json으로 공개 API가 의도치 않게 바뀌는 것을 감지합니다.
> 45개 골든 테스트는 매일 밤 실서버 CUBRID에서 실행됩니다.
> AI가 작성한 코드가 이 모든 게이트를 통과해야 머지됩니다."

### 슬라이드 8 (데모 소개, 15초)
> "공공 행정 시스템 시나리오로 데모하겠습니다.
> CUBRID가 가장 많이 쓰이는 실제 사용 패턴입니다.
> 민원 처리 현황 대시보드부터 시작합니다."

### 슬라이드 14 (클로징, 20초)
> "2020년에 멘토로 시작해서 6년이 걸렸습니다.
> 기여자에서 커뮤니티 빌더가 되고, 방언을 만들고,
> 드라이버를 만들고, 결국 생태계를 만들었습니다.
> SQLAlchemy Korea도 계속 운영하고 있습니다.
> 다음 컨트리뷰톤에서 누군가 저희 프로젝트를 이어가 주길 기다립니다."
