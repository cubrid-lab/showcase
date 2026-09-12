# Presentation Slides — 2026 OSS Developer Contest Finals

> 12 slides, 12 minutes. Each slide maps to a scoring criterion.
> Numbers verified 2026-09-12. Re-measure on presentation day.

---

## Slide 1: One-Line Summary (PT)

# CUBRID Python Ecosystem
## Driver → ORM → Recipes → AI

**Pure Python · Zero C Extensions · 4 Packages · 450+ Merged PRs**

*CUBRID Lab — Yeongseon Choe & Gyeongjun Paik*

---

## Slide 2: Why This Matters (PT + 활용성)

### Korean public sector DBMS: **10.6%** is CUBRID

| | |
|---|---|
| G-Cloud standard DBMS | 600+ government systems |
| Defense, MoIAC, local govts | 1,500+ systems · 2,300+ DB instances |
| **Official Python driver** | **Last release: 2014-05-15** |

> **12 years** without: asyncio, SQLAlchemy 2.x, Python 3.10+, `pip install`

---

## Slide 3: Four-Layer Architecture (PT)

```
cubrid-mcp-server          ← AI/LLM (MCP, 12 tools, read-only)
        ↑
cubrid-cookbook-python     ← Examples (75 recipes, 7 templates)
        ↑
sqlalchemy-cubrid          ← ORM (SQLAlchemy 2.0-2.2, Alembic)
        ↑
pycubrid                   ← Driver (pure Python, asyncio, TLS)
```

Each layer depends only on the layer below. All MIT licensed.

---

## Slide 4: Usability ① — Real Applications Run (활용성)

**7 production-shaped templates:**

| Template | Stack |
|---|---|
| FastAPI service | REST API + Docker |
| Streamlit dashboard | One-command `docker compose up` |
| Django app | Full ORM + admin |
| AI agent | MCP toolchain + RAG metadata |
| Celery worker | Async task processing |
| Pandas ETL | Batch data pipeline |
| Flask app | Classic web patterns |

All install from PyPI. Demo GIFs on every README.

---

## Slide 5: Usability ② — Adoption Signals (활용성)

| Metric | Value |
|---|---|
| GitHub stars (4 repos) | **111** |
| Unique clones (14 days) | **822** developers |
| Merged PRs | **450** |
| PyPI releases | **35** |
| Documentation sites | **4/4 live** |
| Korean docs | **34 pages** |
| Tests | **2,200** (CI-enforced) |

**What the official driver can't do:**

| Feature | Official (2014) | pycubrid |
|---|---|---|
| asyncio | ❌ | ✅ native |
| TLS/SSL | ❌ | ✅ |
| Python 3.10–3.14 | ❌ (3.4 max) | ✅ |
| Pure Python install | ❌ (C extension) | ✅ |
| MCP server | — | ✅ (**world's first**) |

---

## Slide 6: Demo (데모 + 기능테스트)

**3 layers live (4 minutes):**

1. **App** (60s) — `docker compose up` → Streamlit dashboard
2. **AI** (90s) — Claude: "show tables" → "DROP TABLE" → **rejected** (whitelist)
3. **Driver** (60s) — `pip install pycubrid` → connect → asyncio → zero deps

*Backup video ready. Read-only whitelist is server-enforced.*

---

## Slide 7: OSS Appropriateness (OSS 적절성)

**Standards compliance:**
- PEP 249 (DB-API 2.0), PEP 561 (typed package)
- SQLAlchemy Dialect API
- MCP specification (Tools, Resources, Prompts)

**OSS stack:**

| Layer | Tools | License |
|---|---|---|
| Testing | pytest, hypothesis, mypy strict, ruff | MIT/MPL |
| CI | CodeQL, Dependabot, SBOM (SPDX) | GitHub |
| Integration | cubrid/cubrid Docker (10.2–11.4) | CUBRID |
| Reference | node-cubrid (protocol reference) | BSD |

---

## Slide 8: Quality Gates (기능테스트)

| Gate | Value |
|---|---|
| Tests | **2,200** (1,147 + 769 + 284) |
| CI matrix (live DB) | Python 5 × CUBRID 4 = **20 combinations** |
| CI matrix (offline) | (Ubuntu + macOS) × Python 5 = **10 combinations** |
| Coverage floor | **95%** (CI-enforced) |
| Type safety | mypy strict, **0 errors** |
| API compatibility | api-baseline.json gate |
| SQLAlchemy suite | Official test suite integrated |
| Native ENUM | CUBRID ENUM('a','b') verified on 10.2–11.4 (#343) |

---

## Slide 9: Management + AI Workflow (커뮤니티)

- PR-based: **450 merged PRs** across 4 repos
- Labels, milestones, stale bot, Dependabot, CodeQL
- Translation sync CI (Korean hard gate)
- Weekly label drift audit
- **Roadmap update policy** (release PRs must update ROADMAP.md)

**AI Agent Workflow:**
- AGENTS.md → AI implements → Human reviews → CI gates → Human releases
- "We built a **system to validate AI-written code**, not just AI-written code."
- **450 PRs** prove the system works

---

## Slide 10: Licensing (라이선스)

- **MIT** × 4 repositories
- `THIRD_PARTY_LICENSES.md` in every repo (pip-licenses generated)
- `NOTICE` in every repo
- SPDX **SBOM** on every GitHub Release
- No GPL dependencies (runtime or dev)

**CUBRID server**: Apache-2.0 (engine) / BSD (connectors) — verified upstream COPYING
Our packages: **independent wire-protocol clients** — no server code included

---

## Slide 11: Roadmap (커뮤니티 + 발전가능성)

| Item | Status |
|---|---|
| fastmcp 4.x | **Pin opened to `<5`**, canary 3× green |
| Native ENUM | **Shipped** (#343) |
| IS DISTINCT FROM | **Shipped** via `<=>` (#344) |
| MCP Skills | **Shipped** — 5 domain knowledge + 5 expert prompts (#162) |
| PyPI (mcp-server) | Release shipped, publish pending (#154) |
| CUBRID 12 | Tracking upstream |
| Vector types | cubvec branch analyzed |
| Windows CI | macOS + Linux active |
| good-first-issues | 5 seeded |

---

## Slide 12: Closing (PT)

# 2014 → 2026

**The gap in CUBRID's Python ecosystem is closed.**

```bash
pip install pycubrid    # one command, pure Python
```

**Driver · ORM · 75 Examples · 7 Templates · AI/MCP · 2,200 Tests**

*Thank you — CUBRID Lab*
