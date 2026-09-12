# Appendix — Technical Reference for Q&A

> Judges may ask for details. This appendix has architecture diagrams,
> performance data, adoption trends, and per-repo technical specifics.

---

## A. Architecture (Per-Repo)

### pycubrid — Pure Python Driver

```
┌─────────────────────────────────────────────┐
│              Application                    │
├─────────────────────────────────────────────┤
│  pycubrid (DB-API 2.0 / PEP 249)          │
│  ├── Connection (TCP, TLS/STARTTLS)        │
│  ├── Cursor (execute, fetch, executemany)  │
│  ├── Lob (BLOB/CLOB)                       │
│  └── aio/ (asyncio native)                 │
├─────────────────────────────────────────────┤
│  protocol.py (18 CAS packet types)         │
│  packet.py (PacketReader/PacketWriter)     │
│  constants.py (41 function codes,          │
│    27+ data types)                         │
├─────────────────────────────────────────────┤
│  CAS Binary Protocol v8 (TCP:33000)        │
│  [4B length][4B cas_info][payload]         │
└─────────────────────────────────────────────┘
```

**Key design decisions:**
- Zero runtime dependencies (`dependencies = []`)
- Driver-side literal binding (not server-side prepared statements)
- `no_backslash_escapes` auto-negotiation via live server probe
- Transparent CAS reconnect on broker redirect
- Memory-bounded fetch (default batch: 100 rows)

### sqlalchemy-cubrid — SQLAlchemy Dialect

```
┌─────────────────────────────────────────────┐
│  SQLAlchemy ORM / Core                     │
├─────────────────────────────────────────────┤
│  sqlalchemy_cubrid                         │
│  ├── dialect.py (reflection, isolation)    │
│  ├── compiler.py (SQL/DDL/Type compilers)  │
│  ├── types.py (CUBRID type system)         │
│  ├── dml.py (MERGE, ODKU, REPLACE)         │
│  ├── alembic_impl.py (migrations)          │
│  └── requirements.py (53 SA test flags)    │
├─────────────────────────────────────────────┤
│  pycubrid (or CUBRIDdb legacy driver)      │
└─────────────────────────────────────────────┘
```

**Key design decisions:**
- Supports 3 driver URLs: `cubrid+pycubrid://`, `cubrid+aiopycubrid://`, `cubrid+cubriddb://`
- Official SQLAlchemy test suite integrated (53 feature flags)
- Non-transactional DDL handling (CUBRID auto-commits DDL)
- `insertmanyvalues` batch optimization (SA 2.x)

### cubrid-mcp-server — AI/LLM Access

```
┌─────────────────────────────────────────────┐
│  Claude / Cursor / Any MCP Client          │
├─────────────────────────────────────────────┤
│  cubrid-mcp-server (stdio)                 │
│  ├── 12 Tools (11 read + 1 opt-in write)  │
│  ├── 7 Resources (2 schema + 5 domain)     │
│  ├── 9 Prompts (4 basic + 5 expert)        │
│  ├── Read-only whitelist (sqlparse)        │
│  ├── Multi-connection (per-conn isolation) │
│  └── Audit logging (no raw SQL)            │
├─────────────────────────────────────────────┤
│  fastmcp (Apache-2.0) + pycubrid (MIT)     │
└─────────────────────────────────────────────┘
```

**Key design decisions:**
- Domain knowledge packs teach LLMs CUBRID SQL (LIMIT, SHOW TRACE, SET)
- Server-enforced whitelist (not prompt-based safety)
- Write mode off by default, single DML atomic txn only
- fastmcp pin opened to `<5` (canary 3× green)

### cubrid-cookbook-python — Dogfooding Platform

```
┌─────────────────────────────────────────────┐
│  Templates (7)                             │
│  ├── api-service-fastapi (12 recipes)      │
│  ├── flask (11 recipes)                    │
│  ├── django                                │
│  ├── dashboard (Streamlit, one-command)    │
│  ├── async-worker (Celery)                 │
│  ├── batch-etl (Pandas)                    │
│  └── ai-agent (MCP + RAG metadata)        │
├─────────────────────────────────────────────┤
│  Fundamentals (68 examples)                │
│  ├── connect, crud, transactions           │
│  ├── parameterized, error handling, LOB   │
│  ├── orm-basics, pycubrid (22), sqlalchemy│
│  ├── pandas (6), async, alembic, json     │
│  └── isolation-levels                      │
├─────────────────────────────────────────────┤
│  Nightly CI: 45 golden-verified examples  │
│  on CUBRID 11.2 + 11.4 (docker)           │
└─────────────────────────────────────────────┘
```

---

## B. Performance Data

### pycubrid vs PyMySQL (C extension) — Synthetic Baseline

| Scenario | pycubrid | PyMySQL | Ratio |
|---|---:|---:|---:|
| insert_sequential (10K rows) | 10.47s | 1.74s | 6.0x |
| select_by_pk (10K lookups) | 15.99s | 3.52s | 4.5x |
| select_full_scan (10K rows) | 10.31s | 1.86s | 5.5x |
| update_indexed (10K rows) | 10.70s | 2.19s | 4.9x |
| delete_sequential (10K rows) | 10.75s | 2.10s | 5.1x |

*Note: Pure Python vs C extension — this gap is expected. The trade-off is zero-install (no compiler), cross-platform, and asyncio. What matters is the improvement trend, shown below.*

### Optimization Results (Before → After)

| Optimization | Before | After | Improvement |
|---|---:|---:|---:|
| Native ping (CHECK_CAS vs SELECT 1) | — | — | **+280% throughput** |
| SQLAlchemy pool_pre_ping | — | — | **+588% throughput** |
| Bulk insert 100 rows | 370.3ms | 356.1ms | **3.9% faster** |
| Bulk insert 1000 rows | 2,865ms | 2,512ms | **12.3% faster** |
| Query select-all | 39.8ms | 31.8ms | **19.9% faster** |
| Fetch optimization (10K rows) | 96ms | 78ms | **−19% latency** |

### Benchmark Infrastructure

- Repo: [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark)
- Environment: Intel i5-9400F, Linux x86_64, Docker CUBRID 11.4
- Workload: 10,000 rows × 5 rounds (mean)
- Profiling scripts: `profile_connect.py`, `profile_execute.py`, `profile_fetch.py`
- All numbers reproducible via benchmark repo

---

## C. Adoption Trends

### GitHub Stars (as of 2026-09-12)

| Repo | Created | Stars | Growth |
|---|---|---|---|
| sqlalchemy-cubrid | 2022-07 | ⭐36 | 4 years, steady |
| pycubrid | 2026-03 | ⭐29 | 6 months, rapid |
| cubrid-mcp-server | 2026-04 | ⭐29 | 5 months, rapid |
| cubrid-cookbook-python | 2026-03 | ⭐25 | 6 months |
| **Total** | — | **⭐119** | — |

### Unique Clones (14-day, GitHub Traffic API)

| Repo | Unique Cloners | Trend |
|---|---|---|
| pycubrid | **363** | ↑ from 305 last week |
| sqlalchemy-cubrid | **268** | ↑ from 225 |
| cubrid-mcp-server | ~200 | stable |
| cubrid-cookbook-python | ~95 | stable |
| **Total** | **~926** | **↑ 14% week-over-week** |

### PyPI Downloads

| Package | Day | Week | Month | Note |
|---|---:|---:|---:|---|
| pycubrid | 129 | 653 | **3,778** | ~125/day organic |
| sqlalchemy-cubrid | 0* | 84 | **420** | *CI-inflated excluded |
| cubrid-mcp-server | — | — | — | Pending PyPI (#154) |

*Note: Our CI (cookbook smoke + integration tests) generates ~20-50 downloads/day. Use "GitHub unique clones" as the primary adoption metric — GitHub Actions' checkout uses tarball API and is automatically excluded.*

### Merged PRs (Collaboration Evidence)

| Repo | Merged PRs | Contributors | AI+Human PRs |
|---|---:|---|---|
| pycubrid | 159 | 2 humans + AI | 100% CI-gated |
| sqlalchemy-cubrid | 151 | 2 humans + AI | 100% CI-gated |
| cubrid-mcp-server | 84 | 2 humans + AI | 100% CI-gated |
| cubrid-cookbook-python | 56 | 2 humans + AI | 100% CI-gated |
| **Total** | **450** | | |

---

## D. Multi-Language Ecosystem

| Language | Driver | Version | ORM | Version | Status |
|---|---|---|---|---|---|
| **Python** | pycubrid | v1.7.0 | sqlalchemy-cubrid | v1.7.0 | **Complete** |
| TypeScript | cubrid-client | v1.1.0 | drizzle-cubrid | v0.2.1 | In progress |
| Go | cubrid-go | v0.2.1 | gorm-cubrid | v0.1.0 | In progress |
| Rust | cubrid-rs | v0.1.0 | sea-orm-cubrid | v0.1.0 | In progress |

---

## E. License Compliance Summary

| Item | Status |
|---|---|
| All 4 repos | MIT |
| THIRD_PARTY_LICENSES.md | Every repo (pip-licenses generated) |
| NOTICE | Every repo |
| SPDX SBOM | Every GitHub Release |
| GPL dependencies | **Zero** (runtime + dev) |
| CUBRID server license | Apache-2.0 / BSD (upstream COPYING verified) |
| Our packages | Independent wire-protocol clients, no server code |
