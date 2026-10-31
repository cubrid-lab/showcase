# Appendix — Source-Linked Technical Evidence

> Reference for judges and Q&A. This page holds evidence and links, not the talk.
> Spoken answers are in [EXPECTED_QA.md](EXPECTED_QA.md). Commands to reproduce
> anything here are only in [VERIFY.md](VERIFY.md). The slides are in
> [`slides.md`](../../presentation/decks/2026-ossdevcon/slides.md).

## Index

| Looking for | Go to |
|---|---|
| How the four repositories fit together | [1. Architecture and compatibility](#1-architecture-and-compatibility) |
| pycubrid against the official C driver | [2. Performance evidence](#2-performance-evidence) |
| Contributors, merged PRs, stars, CI and releases | [3. Community and reliability evidence](#3-community-and-reliability-evidence) |
| Licenses and SBOM | [4. License checklist](#4-license-checklist) |
| Other languages | [5. Other languages](#5-other-languages) |
| Raw data and sources | [6. References](#6-references) |

---

## 1. Architecture and compatibility

```
 Application                    Claude / Cursor / any MCP client
     │                                      │
 SQLAlchemy ORM / Core              cubrid-mcp-server (stdio)
     │                                      │
 sqlalchemy-cubrid (dialect)                │
     │                                      │
     └──────────────┬───────────────────────┘
                    │
        pycubrid (DB-API 2.0, sync + asyncio)
                    │
        CUBRID CAS binary protocol over TCP (broker port 33000)
```

[cubrid-cookbook-python](https://github.com/cubrid-lab/cubrid-cookbook-python) is not
part of this stack. It is a separate repository of examples and templates that uses
the three packages above and runs them against live CUBRID in CI.

| Repository | Role | What sets it apart | Authoritative docs |
|---|---|---|---|
| [pycubrid](https://github.com/cubrid-lab/pycubrid) | Pure Python driver | No runtime dependencies; speaks the CAS protocol directly (20 packet types, 30 data types); sync and `pycubrid.aio`; TLS; no compiler needed | [repo](https://github.com/cubrid-lab/pycubrid) |
| [sqlalchemy-cubrid](https://github.com/cubrid-lab/sqlalchemy-cubrid) | SQLAlchemy 2.x dialect | URLs `cubrid+pycubrid://`, `cubrid+aiopycubrid://` and `cubrid+cubriddb://` (the official C driver); runs SQLAlchemy's own dialect test suite; Alembic support; MERGE, ON DUPLICATE KEY UPDATE and REPLACE; handles CUBRID auto-committing DDL | [repo](https://github.com/cubrid-lab/sqlalchemy-cubrid) |
| [cubrid-mcp-server](https://github.com/cubrid-lab/cubrid-mcp-server) | MCP server for AI tools | 11 read-only tools by default plus 1 opt-in write tool; keyword whitelist enforced by the server, not by the prompt; write mode off by default (single INSERT/UPDATE/DELETE only); optional audit log without raw SQL; domain guides and prompts that teach CUBRID SQL | [repo](https://github.com/cubrid-lab/cubrid-mcp-server) |
| [cubrid-cookbook-python](https://github.com/cubrid-lab/cubrid-cookbook-python) | Examples and templates | 50+ examples (connection, CRUD, transactions, LOB, async, pandas, Alembic); 7 app templates (FastAPI, Flask, Django, Streamlit dashboard, Celery worker, Pandas ETL, AI agent); nightly golden-verified run on CUBRID 11.4, weekly on 11.2 | [repo](https://github.com/cubrid-lab/cubrid-cookbook-python) |

Design choices worth knowing (details in each repository's docs):

- pycubrid binds parameters on the driver side rather than using server-side prepared
  statements, and probes the server to detect `no_backslash_escapes`.
- The MCP server's safety comes from the server-side whitelist and the database
  account's grants, not from instructions to the model.
- Compatibility matrix in CI: Python 3.10-3.14 against CUBRID 10.2, 11.0, 11.2 and 11.4
  (20 combinations) for the driver and dialect, with a 95% coverage floor.

---

## 2. Performance evidence

**Headline: the 2026-10-28 same-server comparison.** Full provenance, raw output and
environment freeze files are in
[metrics/benchmark-2026-10-28](metrics/benchmark-2026-10-28/README.md). It repeats the
method of the [2026-10-25 rerun](metrics/benchmark-2026-10-25/README.md), which is kept
unchanged.

Measured 2026-10-28 13:39-14:57 UTC with the unmodified
[cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark) harnesses at commit
`831d495` (harness files byte-identical to the 2026-10-25 run). Both drivers ran against one CUBRID 11.4.6 server (Docker `cubrid/cubrid:11.4`)
on one host (Intel i5-9400F, 6 cores, 31 GiB, Ubuntu 22.04.5), CPython 3.12.13,
`autocommit=False`, 10,000 seeded rows, 5 trials per driver in rotating order, warm-up
discarded, every iteration verified. Driver versions: pycubrid 1.15.0 (PyPI) and CUBRIDdb
from cubrid-python `v11.3.0.51` (C extension over CCI). Pooled medians; lower is faster.

| Operation | pycubrid 1.15.0 | CUBRIDdb | pycubrid ÷ CUBRIDdb | 2026-10-25 (1.13.5) |
|---|---:|---:|---:|---:|
| connect + close | 1.71 ms | 1.20 ms | 1.43× | 1.40× |
| SELECT by primary key | 0.735 ms | 0.709 ms | 1.04× | 1.12× |
| `fetchall`, 10,000 rows | 48.7 ms | 41.5 ms | 1.17× | 1.25× |
| `executemany` 10,000 rows + commit | 3,772 ms | 3,612 ms | 1.04× (95% CI 0.97–1.20) | 1.20× |

- Concurrency (SELECT by primary key, 8 workers, one connection each): pycubrid sync
  4,533 and `pycubrid.aio` 3,958 queries/s against CUBRIDdb 747 queries/s.
- pycubrid 1.15.0 against 1.10.0 in the same run: no regression by the harness's rule
  (median more than 5% slower with non-overlapping IQRs).
- Caveat: the host was shared (1-minute load average 2-15 on 6 cores, lighter than the
  6-25 of 2026-10-25), with one server and localhost networking. Part of the change
  from 2026-10-25 may come from the lighter load, not only from the newer driver. Trust the ratios more than the
  absolute times. The full table (95% intervals, more operations) and the pycubrid-only
  Tier 1 workload are in the benchmark README.

**Historical results (archive, not the headline).** Earlier numbers are kept as
recorded and were not rerun. Do not compare them with the table above: the versions,
CUBRID version and workloads differ.

| Record | What it is | Status |
|---|---|---|
| pycubrid vs PyMySQL, 2026-03-16 | Run `2026-03-16_initial` in cubrid-benchmark: pycubrid 0.5.0 against CUBRID 11.2, PyMySQL against a **MySQL 8.0** server. PyMySQL is a pure Python driver, not a C extension. This compares two database engines as well as two drivers, so it does not isolate driver overhead. It predates a pycubrid `fetchall` fix and an autocommit correction. | [Run directory](https://github.com/cubrid-lab/cubrid-benchmark/tree/b002085822054fdd48075a97b52c75921a73fda3/experiments/baseline-multilang/runs/2026-03-16_initial); not quoted in the talk |
| Optimization results (native ping +280% throughput, SQLAlchemy `pool_pre_ping` +588%, bulk insert 1,000 rows 12.3% faster, select-all 19.9% faster, fetch 10,000 rows 96 → 78 ms) | Earlier profiling-driven changes. Run date, harness and library versions are **not recorded**, so they are not a current measurement. | Kept here as recorded; no longer shown on the slides (since 2026-11-01 the performance slide shows only the 2026-10-28 comparison with CUBRIDdb) |

Tracking and any future rerun: [issue #44](https://github.com/cubrid-lab/showcase/issues/44).

---

## 3. Community and reliability evidence

**Definitions.**

- *Maintainer*: the two team members, `yeongseon` and `paikend`.
- *Outside contributor*: a human GitHub account other than the maintainers, not a bot or
  automation account, that authored at least one merged PR in the four repositories.
- *Bots and automation*: dependabot, GitHub Actions, review bots and AI agent accounts.
  They are not counted as contributors.
- *Repository merged-PR total*: every merged PR in a repository whoever authored it,
  including the maintainers' own AI-assisted PRs. It measures repository activity, not
  the number of people or users.

**Outside contributors, as of 2026-11-01 (UTC):**
**67 people with 153 merged PRs** across the four repositories. By repository, merged
outside PRs: pycubrid 34, sqlalchemy-cubrid 35, cubrid-mcp-server 42,
cubrid-cookbook-python 42. Method, exclusions and per-PR links are in
[metrics/contributors-2026-11-01.json](metrics/contributors-2026-11-01.json), generated by
`scripts/collect_contributors.py`. The earlier snapshot
([metrics/contributors-2026-10-28.json](metrics/contributors-2026-10-28.json): 62 people,
137 PRs) is kept; cutting the new data off at its timestamp reproduces it exactly.

**Repository activity, as of 2026-10-25 (UTC)**, from
[metrics/SNAPSHOT.md](metrics/SNAPSHOT.md):

| Repository | Stars | Merged PRs (all authors) | Published GitHub Releases |
|---|---:|---:|---:|
| pycubrid | 31 | 537 | 29 |
| sqlalchemy-cubrid | 38 | 529 | 23 |
| cubrid-mcp-server | 32 | 236 | 9 |
| cubrid-cookbook-python | 28 | 251 | none (examples) |
| **Total** | **129** | **1,553** | **61** |

**Not used as adoption evidence.** GitHub clone traffic and PyPI downloads include our
own CI (for example, pycubrid had about 700 workflow runs and 4,969 clones in the 14
days measured on 2026-09-27). They say little about how many people use the packages,
so the talk does not cite them. The 2026-09-27 table is kept in
[metrics/SNAPSHOT.md](metrics/SNAPSHOT.md).

**Reliability gates.** Merging requires passing CI. pycubrid, sqlalchemy-cubrid and
cubrid-mcp-server enforce a 95% coverage floor; the driver and dialect run the live
CUBRID matrix; sqlalchemy-cubrid also runs the official SQLAlchemy dialect suite. Only
humans push release tags. See each repository's Actions page (links in
[VERIFY.md](VERIFY.md)).

**Release versions are point-in-time.** pycubrid 1.13.3 and sqlalchemy-cubrid 1.11.5
were the latest on 2026-10-24 and appear in the 2026-10-25 snapshot, which was not
refreshed after later releases. The current benchmark (2026-10-28) used pycubrid 1.15.0; the 2026-10-25 run used
1.13.5 (released 2026-10-25 02:10 UTC, before that run). Newer releases have shipped since; check the
[pycubrid](https://pypi.org/project/pycubrid/),
[sqlalchemy-cubrid](https://pypi.org/project/sqlalchemy-cubrid/) and
[cubrid-mcp-server](https://pypi.org/project/cubrid-mcp-server/) pages for the latest.

---

## 4. License checklist

| Item | Status | Evidence |
|---|---|---|
| Our four repositories | MIT | `LICENSE` in each repository |
| Third-party licenses | `THIRD_PARTY_LICENSES.md` and `NOTICE` in every repository | files in each repository root |
| SPDX SBOM | Attached to recent GitHub Releases, not the earliest | Releases page of each repository |
| GPL dependencies | None, runtime or development, in the generated license reports | `THIRD_PARTY_LICENSES.md` |
| CUBRID server license | Apache-2.0 for the engine, BSD for connectors, per the upstream `COPYING` | [CUBRID COPYING](https://github.com/CUBRID/cubrid/blob/develop/COPYING) |
| Relationship to CUBRID | Independent wire-protocol clients; no CUBRID server code | repository source |

---

## 5. Other languages

Python is the complete, reference ecosystem and the contest entry. The same approach is
under way for TypeScript (`cubrid-client`, `drizzle-cubrid`), Go (`cubrid-go`,
`gorm-cubrid`) and Rust (`cubrid-rs`, `sea-orm-cubrid`), all in progress at 0.x-1.x
versions. Treat versions as of 2026-10-25 and check each repository's releases for the
current status.

---

## 6. References

- [EXPECTED_QA.md](EXPECTED_QA.md): prepared spoken answers
- [VERIFY.md](VERIFY.md): commands to reproduce and verify
- [metrics/SNAPSHOT.md](metrics/SNAPSHOT.md): repository metrics, 2026-10-25
- [metrics/contributors-2026-11-01.json](metrics/contributors-2026-11-01.json): outside contributors, 2026-11-01 (current)
- [metrics/contributors-2026-10-28.json](metrics/contributors-2026-10-28.json): outside contributors, 2026-10-28
- [metrics/benchmark-2026-10-28](metrics/benchmark-2026-10-28/README.md): current benchmark rerun, raw data
- [metrics/benchmark-2026-10-25](metrics/benchmark-2026-10-25/README.md): previous benchmark rerun, raw data
- [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark): harnesses and earlier runs
