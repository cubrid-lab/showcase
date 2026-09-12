# Presentation Slides — 2026 OSS Developer Contest Finals

> 12 slides, 12 minutes. Oracle-optimized: 35% story / 45% technical / 20% impact.
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

## Slide 2: The Gap — Why This Matters (PT + 활용성 · 0:45-1:30)

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

## Slide 3: What We Built — 4 Projects, In Order (PT · 1:30-3:30)

### 연대기: 각 단계가 다음 단계를 자연스럽게 낳았다

**① sqlalchemy-cubrid (2021-22)**
- Mike Bayer의 방언 → SA 2.0 기준 재작성
- 스키마 리플렉션, MERGE, ON DUPLICATE KEY UPDATE, Native ENUM
- **SQLAlchemy 공식 테스트 스위트 통합**

**② pycubrid (2025)**
- CAS 바이너리 프로토콜 해독 (문서 없음 → 역분석)
- **PEP 249 (DB-API 2.0) 완전 준수** · 순수 Python · 의존성 0
- asyncio 네이티브 · TLS · 크로스플랫폼 (Ubuntu + macOS)

**③ cubrid-cookbook (2026)**
- **7개 프로덕션 템플릿**: FastAPI, Flask, Django, Streamlit, Celery, ETL, AI Agent
- 75 예제 = dogfooding 플랫폼 (매일 밤 실서버 검증)
- pycubrid 1.7.0 버그를 cookbook이 가장 먼저 감지

**④ cubrid-mcp-server (2026)**
- **MCP 사양 준수** — 세계 최초의 CUBRID MCP 서버
- 12 도구 + 5 도메인 지식 팩 + 9 전문가 프롬프트
- LLM이 CUBRID SQL을 몰라도 올바르게 쿼리 (서버가 가르침)

---

## Slide 4: Standards & Open Source (OSS 적절성 · 3:30-5:30)

### "폐쇄형 데모가 아니라, 개방형 표준 위의 상호운용 OSS 인프라"

| Standard | Compliance | Evidence |
|---|---|---|
| **PEP 249** (DB-API 2.0) | pycubrid 완전 준수 | 1,147 테스트 |
| **PEP 561** (Type Safety) | py.typed · mypy strict 0 errors | CI 강제 |
| **SQLAlchemy Dialect API** | 공식 테스트 스위트 통합 | 53 feature flags |
| **MCP Specification** | Tools + Resources + Prompts | 세계 최초 CUBRID MCP |

### We stand on the shoulders of giants:

| Layer | OSS | License |
|---|---|---|
| ORM Framework | SQLAlchemy | MIT |
| Predecessor | zzzeek/sqlalchemy_cubrid | MIT |
| Protocol Reference | node-cubrid | BSD |
| MCP Protocol | Model Context Protocol | MIT |
| Testing | pytest, hypothesis | MIT/MPL |
| CI/CD | CodeQL, Dependabot, SBOM | GitHub |

> "오픈소스 기여로 배우고, 죽은 프로젝트에서 영감을 받고,
> 새 생태계를 만들었다."

---

## Slide 5: Performance — Benchmark-Driven (기능테스트 · 5:30-6:30)

### 니치 시장에서는 사용자가 성능을 알려주지 않는다 — 직접 측정한다

| Optimization | Before | After | Improvement |
|---|---|---|---|
| Native ping (CHECK_CAS) | SELECT 1 fallback | CAS packet | **+280% throughput** |
| SA pool_pre_ping | SQL round-trip | native CHECK_CAS | **+588% throughput** |
| Bulk insert (1000 rows) | 2,865ms | 2,512ms | **12.3% faster** |
| Query select-all | 39.8ms | 31.8ms | **19.9% faster** |

[cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark) — 재현 가능한 비교 환경

---

## Slide 6: Adoption & Quality (활용성 + 기능테스트 · 6:30-7:30)

### 지표가 의미하는 것

| Metric | Value | 의미 |
|---|---|---|
| 111 stars | 4 repos 합산 | 커뮤니티 관심 |
| **822 unique clones** (14일) | GitHub Traffic API | **실제로 코드를 받아가는 개발자** |
| **450 merged PRs** | 전부 CI 통과 | **AI+휴먼 협업 프로세스 검증** |
| 35 PyPI releases | 16 + 19 | 지속적 유지보수 |
| **2,200 tests** | 4 repos | 품질 게이트 |
| 20 CI combinations | Py 5 × CUBRID 4 | **호환성 보장** |
| 95% coverage | CI 강제 | 코드 품질 |
| 4 docs sites | 전부 라이브 | 접근성 |
| 34 Korean pages | 번역 | 한국 사용자 배려 |

**공식 드라이버가 못 하는 것:**

| Feature | Official (2014) | pycubrid |
|---|---|---|
| asyncio | ❌ | ✅ native |
| TLS/SSL | ❌ | ✅ |
| Python 3.10-3.14 | ❌ (3.4 max) | ✅ |
| Pure Python | ❌ (C extension) | ✅ |
| MCP server | — | ✅ (world's first) |

---

## Slide 7: Demo (데모 + 기능테스트 · 7:30-9:30)

**4 minutes, 3 layers:**

1. **App** (60s) — `docker compose up` → Streamlit dashboard
   → "7개 템플릿 중 하나 — 원커맨드로 실행"

2. **AI** (90s) — Claude Desktop
   - "show tables" → `all_table_names`
   - "top 5 products" → `execute_query` (SELECT)
   - **"DROP TABLE" → 거부** ← 서버 수준 화이트리스트
   - "tags에 'sale' 있는 상품?" → SET 타입 조회 (MCP domain knowledge)

3. **Driver** (60s) — `pip install pycubrid` → connect → asyncio → zero deps
   - "PEP 249 준수, 의존성 0개, C 컴파일러 불필요"

*(백업 영상 준비됨 — 동일 런북의 사전 녹화)*

---

## Slide 8: How We Work — AI + Human (커뮤니티 · 9:30-10:15)

```
AGENTS.md (rules) → AI implements → Human reviews → CI gates → Human releases
```

- **450 PRs** — every one passed 20-combination live DB tests
- Translation sync CI (Korean hard gate)
- Label taxonomy + weekly drift audit
- SBOM on every release

> "AI가 작성한 코드를 검증하는 시스템을 만들었다.
> 그 시스템이 450개 PR을 통과시켰다."

---

## Slide 9: Licensing (라이선스 · 10:15-10:30)

**MIT × 4** · THIRD_PARTY_LICENSES · NOTICE · SPDX SBOM · No GPL

**CUBRID server**: Apache-2.0 / BSD (upstream COPYING verified)
**Our packages**: independent wire-protocol clients — no server code

---

## Slide 10: Ecosystem Vision — 4 Languages + Community (발전가능성 · 10:30-11:15)

### Python이 레퍼런스 — TypeScript, Go, Rust도 진행 중

| Language | Driver | ORM | Status |
|---|---|---|---|
| **Python** | pycubrid v1.7.0 | sqlalchemy-cubrid v1.7.0 | **완성 (출품작)** |
| TypeScript | cubrid-client v1.1.0 | drizzle-cubrid v0.2.1 | 진행 중 |
| Go | cubrid-go v0.2.1 | gorm-cubrid v0.1.0 | 진행 중 |
| Rust | cubrid-rs v0.1.0 | sea-orm-cubrid v0.1.0 | 진행 중 |

### Community: SQLAlchemy Korea 경험으로

- 코드 접근성: 4 docs sites, 34 한국어 페이지, demo GIFs
- Cookbook = 온보딩 가이드 (75 examples)
- Good-first-issues: 5 seeded + mentoring
- **SQLAlchemy Korea 운영 중 (2020.10~)**

### Sustainability

- 대가 후에도: MIT 라이선스, 문서화된 governance, CI 자동화
- AI/MCP = 다음 세대 개발자(LLM 에이전트)도 CUBRID 사용 가능

---

## Slide 11: Judge Verification (기능테스트 · 11:15-11:30)

### 심사위원이 직접 확인할 수 있는 경로

```bash
# PyPI에서 (등록 후)
uvx cubrid-mcp-server

# 또는 GitHub Release에서 (지금 가능)
git clone cubrid-cookbook-python
docker compose up -d
make verify
```

**VERIFY.md** — 단계별 검증 가이드 (showcase repo)

---

## Slide 12: Closing — The Flywheel (PT · 11:30-12:00)

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

## Appendix: Speaking Scripts (발표 스크립트)

### 슬라이드 1 (오프닝, 30초)
> "2020년, NIPA가 운영하는 오픈소스 컨트리뷰톤에서 두 사람이 만났습니다.
> 멘토와 멘티로요. 저희입니다.
> 그때 SQLAlchemy를 배웠고, Gitter에서 창시자 Mike Bayer님과 대화하면서
> 한국 커뮤니티도 만들었습니다. 6년 후, 하나의 생태계를 들고 왔습니다."

### 슬라이드 3 (프로젝트, 90초 — 연대기 순)
> "첫 번째, sqlalchemy-cubrid입니다. Mike Bayer님이 만들다 버린 방언을
> SQLAlchemy 2.0 기준으로 처음부터 썼습니다. 공식 테스트 스위트를 통합했고,
> Native ENUM도 실증해서 구현했습니다.
>
> 두 번째, 방언을 만들다 보니 드라이버가 문제였습니다.
> 2014년 이후 방치된 C 확장. 그래서 pycubrid를 순수 Python으로
> 만들었습니다. PEP 249를 완전히 준수하고, 의존성이 0개입니다.
>
> 세 번째, cookbook입니다. 7개 프로덕션 템플릿 — FastAPI부터 AI 에이전트까지.
> 이게 단순한 예제집이 아니라 dogfooding 플랫폼입니다.
> 매일 밤 75개 예제가 실서버에서 실행되고,
> 드라이버에 버그가 있으면 cookbook이 가장 먼저 잡습니다.
>
> 네 번째, MCP 서버입니다. 세계 최초의 CUBRID MCP 서버이고,
> 도메인 지식 팩을 내장해서 LLM이 CUBRID를 몰라도
> 올바른 SQL을 생성할 수 있습니다."

### 슬라이드 4 (OSS 적절성, 60초)
> "이 프로젝트는 폐쇄형 데모 앱이 아니라, 개방형 표준 위의
> 상호운용 가능한 OSS 인프라입니다.
> pycubrid는 PEP 249를 완전히 준수하고,
> sqlalchemy-cubrid는 SQLAlchemy 공식 테스트 스위트를 통합했으며,
> MCP 서버는 MCP 사양을 준수합니다.
> SQLAlchemy, pytest, CodeQL — 전부 오픈소스 위에 구축했습니다."

### 슬라이드 5 (성능, 30초)
> "니치 시장에서는 사용자가 성능 문제를 알려주지 않습니다.
> 그래서 직접 벤치마크하고, 프로파일하고, 최적화했습니다.
> Native ping 구현으로 280%, SQLAlchemy pool_pre_ping에서는
> 588% 처리량이 향상됐습니다. 전부 cubrid-benchmark에서 재현 가능합니다."

### 슬라이드 12 (클로징, 20초)
> "2020년에 멘토로 시작해서 6년이 걸렸습니다.
> 기여자에서 커뮤니티 빌더가 되고, 방언을 만들고,
> 드라이버를 만들고, 결국 생태계를 만들었습니다.
> SQLAlchemy Korea도 계속 운영하고 있습니다.
> 다음 컨트리뷰톤에서 누군가 저희 프로젝트를 이어가 주길 기다립니다."
