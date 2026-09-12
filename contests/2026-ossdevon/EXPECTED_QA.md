# Expected Q&A — 2026 OSS Developer Contest Finals

> 12 anticipated questions with prepared answers (30-60 seconds each).
> Numbers verified 2026-09-12.

---

## Q0: Tell us about your team's background.

We met at the 2020 OSS Contribution Hackathon as mentor and mentee.
We contributed to SQLAlchemy and sqlalchemy-hana, connected with Mike
Bayer via Gitter, and started the SQLAlchemy Korea community. Mike Bayer
had built a CUBRID dialect in 2012 but abandoned it. We rebuilt from
scratch for SQLAlchemy 2.0, then built the pure Python driver, then the
full ecosystem including the world's first CUBRID MCP server.

## Q1: Why not just use the official CUBRID Python driver?

The official driver's last PyPI release was May 2014 — 12 years ago.
It's a C extension requiring a compiler toolchain, doesn't support
asyncio, and only works up to Python 3.4. Our pycubrid is pure Python,
works on 3.10-3.14, and `pip install pycubrid` just works. We also
support the old driver via `cubrid+cubriddb://` URLs in our dialect.

## Q2: Why are there so many AI-generated commits?

We built a system where AI agents write code and humans review it —
the same mentor-mentee model we learned from OSS contribution culture.
AGENTS.md defines the rules, every PR passes 20-combination live DB
tests with 95% coverage, and only humans push release tags. 450 merged
PRs prove the system works.

## Q3: Stars are low — is anyone actually using this?

We're early. But 926 developers cloned our repos in the last 14 days
(GitHub Traffic API, CI actions excluded). We're the only modern Python
driver for a database with 10.6% of Korean public sector market share.
The market exists — 1,500+ systems are waiting for this tooling.

## Q4: Isn't CUBRID GPL? Does your MIT license conflict?

No. We verified CUBRID's upstream COPYING: server engine is Apache-2.0,
connectors are BSD. The often-cited GPL v2+ no longer applies. Our
packages are independent wire-protocol clients with zero server code.
No GPL anywhere in our dependency trees.

## Q5: How does performance compare to C extensions?

C extensions will always have an edge in raw throughput. But what you
gain: zero installation friction, cross-platform, native asyncio, TLS.
For 95% of use cases, install simplicity outweighs the throughput gap.
We improved bulk insert 12.3% and query 19.9% through profiling.

## Q5.5: How did you approach performance optimization?

We built cubrid-benchmark (separate repo) for reproducible comparison,
then used profiling scripts to find bottlenecks. Key results: native
ping +280%, pool_pre_ping +588%, bulk insert 12.3% faster. In a niche
market, you benchmark yourself.

## Q6: What about CUBRID 12 support?

CUBRID 12 hasn't shipped yet. Our CI already tests 10.2, 11.0, 11.2,
11.4 (20 combinations). When 12 releases, we add it to the matrix.

## Q7: Vector types for AI workloads?

CUBRID's cubvec branch is under development upstream. We've analyzed
the wire format and HNSW index structure. Prototype planned once the
server releases.

## Q8: Is the MCP write mode dangerous?

It's off by default and requires explicit opt-in. Even then, only single
DML statements in atomic transactions — no DDL. We demonstrate the
safety live: asking Claude to "DROP TABLE" gets rejected by the
server-level whitelist.

## Q9: How do you handle CUBRID-specific SQL differences?

Our MCP server ships with 5 domain-knowledge guide documents that teach
LLMs about CUBRID's LIMIT syntax, SHOW TRACE, collection types, etc.
Plus 5 expert prompts for common workflows. Claude can write correct
CUBRID SQL without prior knowledge — because the server teaches it.

## Q10: You mentioned contributing to SQLAlchemy — tell us more.

We contributed to SQLAlchemy and sqlalchemy-hana during a hackathon.
Mike Bayer (SQLAlchemy creator) had built zzzeek/sqlalchemy_cubrid in
2012 but abandoned it. We met Mike via Gitter. We didn't fork his
code — we wrote a new dialect from scratch targeting SQLAlchemy 2.0.

## Q10.5: Is this just for Python?

cubrid-lab has 4 language ecosystems: Python (complete, contest entry),
TypeScript, Go, Rust. Python is the reference. Same playbook applies.

## Q10.7: How will you grow the community?

We run SQLAlchemy Korea (since 2020). Same methodology: docs sites,
cookbook onboarding, good-first-issues with mentoring, community
building. Full circle: we were mentees, now we mentor.

## Q11: What's your sustainability plan after the contest?

Infrastructure is built for longevity: translation sync CI, label
taxonomy, SBOM automation, API compatibility gates, 5 good-first-issues.
MIT licensed — anyone can continue. We hope the next contribution
hackathon mentee finds our project and continues the cycle.
