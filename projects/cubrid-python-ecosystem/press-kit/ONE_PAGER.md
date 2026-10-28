# CUBRID Python Ecosystem — One-Pager

## Our Story

We met at the 2020 OSS Contribution Hackathon (CNBT-41) as mentor and mentee.
Contributed to SQLAlchemy and sqlalchemy-hana.
Found Mike Bayer's CUBRID dialect (2012) unmaintained.
Rebuilt from scratch for SQLAlchemy 2.0, then built the driver too.

## The Problem

CUBRID ranks **second among the top five Korean public-sector DBMS vendors**, with **2,367 installations — 13.24% of the top-five total**, after Oracle (end of 2025, [MOIS/NIA report, printed page 57, table 46](https://www.data.go.kr/data/3038513/fileData.do)). The official Python driver's last PyPI release was **May 2014**. Newer versions (up to v11.3.0.51, September 2025) are GitHub-only C extensions you build yourself, without asyncio. Teams running those systems had no Python driver they could `pip install` from a current PyPI release.

## The Solution

Four packages, pure Python, `pip install` — done.

```
pycubrid            Driver (DB-API 2.0, asyncio, TLS, zero deps)
sqlalchemy-cubrid   ORM (SQLAlchemy 2.0-2.2, Alembic, ENUM)
cubrid-cookbook     50+ examples + 7 templates (FastAPI to AI agent)
cubrid-mcp-server   AI/LLM access (11 read tools; write tool opt-in; domain knowledge)
```

## Key Metrics (2026-10-25 snapshot)

| | |
|---|---|
| GitHub stars | 129 (4 repos) |
| Merged PRs | 1,553 |
| GitHub Releases | 61 (3 package repos) |
| CI combinations | Python 5 × CUBRID 4 = 20 |
| Documentation | 4 sites, including Korean docs |
| License | MIT (all 4 repos) |

**Community**: SQLAlchemy Korea organizer (since Oct 2020, after Gitter chat with Mike Bayer)

## Performance (Benchmark-Driven)

| Optimization | Result |
|---|---|
| Native ping (CHECK_CAS) | **+280% throughput** vs SELECT 1 |
| SQLAlchemy pool_pre_ping | **+588% throughput** |
| Bulk insert (1000 rows) | **12.3% faster** |
| Query select-all | **19.9% faster** |

These are historical results, not rerun; their run date and versions are not recorded.
A 2026-10-25 rerun against the official C driver `CUBRIDdb` on the same CUBRID 11.4.6 server
measured pycubrid 1.13.5 at 1.12× its time for a primary-key SELECT and 1.25× for fetching
10,000 rows ([provenance and raw output](../../../events/2026-ossdevcon/metrics/benchmark-2026-10-25/README.md)).

Reproducible benchmarks at [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark).

## Ecosystem Expansion (4 Languages)

| Language | Driver | ORM | Status |
|---|---|---|---|
| Python | pycubrid | sqlalchemy-cubrid | **Complete** |
| TypeScript | cubrid-client | drizzle-cubrid | In progress |
| Go | cubrid-go | gorm-cubrid | In progress |
| Rust | cubrid-rs | sea-orm-cubrid | In progress |

Current versions are on each repository's releases page.

Community: Led by SQLAlchemy Korea organizer (since 2020).
Same playbook (driver -> ORM -> examples -> AI) for each language.

## What Makes It Different

1. **Pure Python** CUBRID driver (no C extensions, `pip install`)
2. **MCP server** for CUBRID (AI/LLM access, read-only by default)
3. **Domain knowledge built-in** — MCP server teaches LLMs CUBRID SQL dialect
4. **1,553 merged PRs** (2026-10-25) through an AI-agent workflow with human review and CI gates
5. **Production-ready** — 7 runnable templates, golden-verified examples

## Links

| | |
|---|---|
| Driver | github.com/cubrid-lab/pycubrid |
| ORM | github.com/cubrid-lab/sqlalchemy-cubrid |
| Examples | github.com/cubrid-lab/cubrid-cookbook-python |
| AI/MCP | github.com/cubrid-lab/cubrid-mcp-server |
| Docs | cubrid-lab.github.io/{pycubrid, sqlalchemy-cubrid, cubrid-mcp-server, cubrid-cookbook-python} |

**Team**: Yeongseon Choe & Gyeongjun Paik (CUBRID Lab)
