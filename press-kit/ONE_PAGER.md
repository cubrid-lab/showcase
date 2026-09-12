# CUBRID Python Ecosystem — One-Pager

## Our Story

We met at the 2020 OSS Contribution Hackathon (CNBT-41) as mentor and mentee.
Contributed to SQLAlchemy and sqlalchemy-hana.
Found Mike Bayer's CUBRID dialect (2012) unmaintained.
Rebuilt from scratch for SQLAlchemy 2.0, then built the driver too.

## The Problem

Korean public sector DBMS market: **10.6% is CUBRID** (1,500+ systems, 2,300+ DB instances). The official Python driver's last release was **May 2014** — no asyncio, no SQLAlchemy 2.x, no modern Python. Thousands of developers locked into a database with dead tooling.

## The Solution

Four packages, pure Python, `pip install` — done.

```
pycubrid            Driver (DB-API 2.0, asyncio, TLS, zero deps)
sqlalchemy-cubrid   ORM (SQLAlchemy 2.0-2.2, Alembic, ENUM)
cubrid-cookbook     75 examples + 7 templates (FastAPI to AI agent)
cubrid-mcp-server   AI/LLM access (12 tools, read-only whitelist, domain knowledge)
```

## Key Metrics (2026-09)

| | |
|---|---|
| GitHub stars | 111 |
| Unique clones (14d) | 822 developers |
| Merged PRs | 450 |
| PyPI releases | 35 |
| Tests | 1,916 (CI-enforced) |
| CI combinations | Python 5 × CUBRID 4 = 20 |
| Documentation | 4 sites, 33 Korean pages |
| License | MIT (all 4 repos) |

**Community**: SQLAlchemy Korea organizer (since Oct 2020, after Gitter chat with Mike Bayer)

## Performance (Benchmark-Driven)

| Optimization | Result |
|---|---|
| Native ping (CHECK_CAS) | **+280% throughput** vs SELECT 1 |
| SQLAlchemy pool_pre_ping | **+588% throughput** |
| Bulk insert (1000 rows) | **12.3% faster** |
| Query select-all | **19.9% faster** |

Reproducible benchmarks at [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark).

## Ecosystem Expansion (4 Languages)

| Language | Driver | ORM | Status |
|---|---|---|---|
| Python | pycubrid v1.7.0 | sqlalchemy-cubrid v1.7.0 | **Complete** |
| TypeScript | cubrid-client v1.1.0 | drizzle-cubrid v0.2.1 | In progress |
| Go | cubrid-go v0.2.1 | gorm-cubrid v0.1.0 | In progress |
| Rust | cubrid-rs v0.1.0 | sea-orm-cubrid v0.1.0 | In progress |

Community: Led by SQLAlchemy Korea organizer (since 2020).
Same playbook (driver -> ORM -> examples -> AI) for each language.

## What Makes It Different

1. **World's only** pure Python CUBRID driver (no C extensions)
2. **World's only** MCP server for CUBRID (AI/LLM access)
3. **Domain knowledge built-in** — MCP server teaches LLMs CUBRID SQL dialect
4. **450 PRs validated** by AI-agent workflow with human review gates
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
