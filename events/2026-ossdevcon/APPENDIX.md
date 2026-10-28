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
│  protocol.py (20 CAS packet types)         │
│  packet.py (PacketReader/PacketWriter)     │
│  constants.py (41 function codes,          │
│    30 data types)                          │
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
│  Fundamentals (50+ examples)               │
│  ├── connect, crud, transactions           │
│  ├── parameterized, error handling, LOB   │
│  ├── orm-basics, pycubrid (22), sqlalchemy│
│  ├── pandas (6), async, alembic, json     │
│  └── isolation-levels                      │
├─────────────────────────────────────────────┤
│  Nightly CI: golden-verified examples     │
│  on CUBRID 11.4 (11.2 weekly, docker)     │
└─────────────────────────────────────────────┘
```

---

## B. Performance Data

This section holds two separate sets of numbers. Do not compare them with each other:
they were measured with different driver versions, CUBRID versions and workloads.

- **Rerun 2026-10-25** — measured for this presentation, with full provenance and raw
  output in [metrics/benchmark-2026-10-25](metrics/benchmark-2026-10-25/README.md).
- **Historical** — earlier results, kept as they were recorded, not rerun.

### Rerun 2026-10-25: pycubrid 1.13.5 vs CUBRIDdb on the same server

Measured 2026-10-25 08:15–10:16 UTC with the unmodified
[cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark) harnesses at
`b002085`: pycubrid 1.13.5 (PyPI) and CUBRIDdb from cubrid-python `v11.3.0.51` (C
extension over CCI), CPython 3.12.13, CUBRID 11.4.6 (`11.4.6.1963-0e7d3c1`, Docker
`cubrid/cubrid:11.4`), Intel i5-9400F 6 cores, 31 GiB, Ubuntu 22.04.5 / Linux
5.15.0-198. `autocommit=False` on every connection; 10,000 seeded rows; 5 trials per
driver in rotating order, warm-up discarded, every iteration verified; pooled medians in
milliseconds (lower is faster). The host was shared and heavily loaded (1-minute load
average 6–25 on 6 cores), so the ratios are more reliable than the absolute times.

| Operation | pycubrid 1.13.5 | CUBRIDdb | pycubrid ÷ CUBRIDdb |
|---|---:|---:|---:|
| connect + close | 2.11 ms | 1.51 ms | 1.40× |
| SELECT by primary key | 0.84 ms | 0.75 ms | 1.12× |
| `fetchall`, 10,000 rows | 51.3 ms | 41.1 ms | 1.25× |
| `executemany` 10,000 rows + commit | 3,899 ms | 3,258 ms | 1.20× |

- Concurrency (SELECT by PK, 8 workers, one connection each): pycubrid sync 2,906 and
  `pycubrid.aio` 2,005 queries/s against CUBRIDdb 995 queries/s.
- pycubrid 1.13.5 against 1.10.0 in the same run: no regression detected by the
  harness's rule (median >5% slower with non-overlapping IQRs).
- Tier 1 workload (`tier1-explicit-keys-v2`, pycubrid only, median of 3 trials ×
  5 rounds): insert_sequential 8.66 s, select_by_pk 7.45 s, select_full_scan 0.043 s
  (10,000 rows each), update_indexed 0.94 s, delete_sequential 1.10 s (1,000 rows each).
  This corrected workload measures a different quantity from the historical table below.
- Not rerun: PyMySQL/MySQL (a cross-engine comparison does not isolate driver
  overhead) and the optimization rows below (their source run is not recorded).

### Historical: pycubrid vs PyMySQL (C extension) — Synthetic Baseline

| Scenario | pycubrid | PyMySQL | Ratio |
|---|---:|---:|---:|
| insert_sequential (10K rows) | 10.47s | 1.74s | 6.0x |
| select_by_pk (10K lookups) | 15.99s | 3.52s | 4.5x |
| select_full_scan (10K rows) | 10.31s | 1.86s | 5.5x |
| update_indexed (10K rows) | 10.70s | 2.19s | 4.9x |
| delete_sequential (10K rows) | 10.75s | 2.10s | 5.1x |

*Note: Pure Python vs C extension — this gap is expected. The trade-off is zero-install (no compiler), cross-platform, and asyncio. What matters is the improvement trend, shown below.*

### Historical: Optimization Results (Before → After)

| Optimization | Before | After | Improvement |
|---|---:|---:|---:|
| Native ping (CHECK_CAS vs SELECT 1) | — | — | **+280% throughput** |
| SQLAlchemy pool_pre_ping | — | — | **+588% throughput** |
| Bulk insert 100 rows | 370.3ms | 356.1ms | **3.9% faster** |
| Bulk insert 1000 rows | 2,865ms | 2,512ms | **12.3% faster** |
| Query select-all | 39.8ms | 31.8ms | **19.9% faster** |
| Fetch optimization (10K rows) | 96ms | 78ms | **−19% latency** |

### Historical provenance and status

> **Historical results — not rerun for the 2026-10-25 presentation refresh.**
> The values above are retained as previously recorded results, not as a benchmark
> of the latest driver/library versions. Fields that could not be traced to a run log
> are marked **not recorded** rather than inferred. The current measurement is the
> 2026-10-25 rerun above.

- Repo: [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark)
- *pycubrid vs PyMySQL* table — traced on 2026-10-25 to cubrid-benchmark
  [`experiments/baseline-multilang/runs/2026-03-16_initial`](https://github.com/cubrid-lab/cubrid-benchmark/tree/b002085822054fdd48075a97b52c75921a73fda3/experiments/baseline-multilang/runs/2026-03-16_initial)
  (`raw/python_tier1.json` means match the table): run 2026-03-16 12:30 UTC, pycubrid
  0.5.0, PyMySQL version not recorded, CPython 3.10.12, CUBRID **11.2** against a
  **MySQL 8.0** server (a cross-engine comparison), Intel i5-9400F, Linux
  5.15.0-171, 5 rounds × 1 iteration, mean. That experiment's README notes that these
  rows predate a pycubrid `fetchall` fix and an autocommit correction. The earlier
  statement "Docker CUBRID 11.4" for this table was wrong.
- *Optimization Results* table — original execution date, harness and
  `pycubrid` / SQLAlchemy versions or commit SHAs: **not recorded**.
- Profiling scripts as previously stated (not verified against a run log): `profile_connect.py`, `profile_execute.py`, `profile_fetch.py`
- Tracking: [Issue #44](https://github.com/cubrid-lab/showcase/issues/44).

---

## C. Adoption Trends

### GitHub Stars (as of 2026-10-25)

| Repo | Created | Stars | Growth |
|---|---|---|---|
| sqlalchemy-cubrid | 2022-07 | ⭐38 | 4 years, steady |
| pycubrid | 2026-03 | ⭐31 | 7 months |
| cubrid-mcp-server | 2026-04 | ⭐32 | 6 months |
| cubrid-cookbook-python | 2026-03 | ⭐28 | 7 months |
| **Total** | — | **⭐129** | — |

### GitHub Clone Traffic — not an adoption metric

> Measured 2026-09-27. `actions/checkout` performs a real git fetch, and every
> GitHub-hosted runner counts as a distinct cloner, so clone traffic is
> dominated by our own CI (matrix jobs × runs). We no longer quote it as
> adoption. Earlier drafts claimed CI was excluded — that was wrong.

| Repo | Unique cloners (14d) | Total clones (14d) | CI workflow runs (14d) |
|---|---:|---:|---:|
| pycubrid | 495 | 4,969 | 700 |
| sqlalchemy-cubrid | 547 | 5,742 | 1,103 |
| cubrid-mcp-server | 277 | 1,493 | 96 |
| cubrid-cookbook-python | 184 | 1,018 | 335 |

### PyPI Downloads

| Package | Day | Week | Month | Note |
|---|---:|---:|---:|---|
| pycubrid | 129 | 653 | **3,778** | includes CI installs |
| sqlalchemy-cubrid | 0 | 84 | **420** | includes CI installs |
| cubrid-mcp-server | — | — | — | Published on PyPI (v0.4.0); stats not yet collected |

*Note: Our CI (cookbook smoke + integration tests) generates ~20-50 downloads/day, so PyPI counts include CI. Neither PyPI downloads nor clone traffic is a clean adoption signal; we cite merged PRs, releases, and stars instead.*

### Merged PRs (Collaboration Evidence)

| Repo | Merged PRs | Contributors | AI+Human PRs |
|---|---:|---|---|
| pycubrid | 537 | 2 humans + AI | CI-gated |
| sqlalchemy-cubrid | 529 | 2 humans + AI | CI-gated |
| cubrid-mcp-server | 236 | 2 humans + AI | CI-gated |
| cubrid-cookbook-python | 251 | 2 humans + AI | CI-gated |
| **Total** | **1,553** | | |

---

## D. Multi-Language Ecosystem

| Language | Driver | Version | ORM | Version | Status |
|---|---|---|---|---|---|
| **Python** | pycubrid | v1.13.3 | sqlalchemy-cubrid | v1.11.5 | **Complete** (versions as of the 2026-10-25 snapshot) |
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
| SPDX SBOM | Recent GitHub Releases (not attached to the earliest ones) |
| GPL dependencies | **Zero** (runtime + dev) |
| CUBRID server license | Apache-2.0 / BSD (upstream COPYING verified) |
| Our packages | Independent wire-protocol clients, no server code |
