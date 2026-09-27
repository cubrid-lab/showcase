# Expected Q&A — 2026 OSS Developer Contest Finals

> 18 anticipated questions with prepared answers (30-60 seconds each).
> Numbers verified 2026-09-12; market share and clone/CI figures 2026-09-27.

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
AGENTS.md defines the rules, every PR is merged only after CI gates pass
(driver and dialect PRs run the 20-combination live DB matrix with a 95%
coverage floor), and only humans push release tags. 450 merged PRs
prove the system works.

## Q3: Stars are low — is anyone actually using this?

We're early, and we don't inflate it. We deliberately don't quote clone
counts: GitHub clone traffic is dominated by our own CI runners (pycubrid:
~700 workflow runs vs ~5,000 clones in the same 14 days). What we can show
is 450 merged PRs, 35 PyPI releases, 119 stars — and a real market: CUBRID
is #2 in Korean public-sector DBMS (13.24%, 2,367 installations at end of
2025, MOIS/NIA report), and before us it had no maintained Python driver.

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

It's off by default. In default mode the `execute_write` tool isn't even
registered, and any non-read statement sent to `execute_query` is rejected
by a keyword whitelist — that's the rejection you saw in the demo. Write
mode needs an explicit per-connection opt-in (`CUBRID_MCP_WRITE=1`) and then
allows only a single INSERT/UPDATE/DELETE — no DDL, no multi-statement.
Audit logging is available (`CUBRID_MCP_AUDIT_LOG=1`).

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

## Q12: So if write mode is on, could the AI mass-approve documents?

Yes — a single `UPDATE ... WHERE status='pending'` is one statement, so write
mode would allow it. The MCP whitelist controls *what kind* of statement
runs; it is not a business-rule engine. The real boundary is the database
account: connect the MCP server with a CUBRID user that has only SELECT
grants, and keep write mode off in production. That's our recommendation.

## Q13: Can a read-only query still expose confidential rows?

Yes. Read-only is not row-level security. In the demo Claude aggregated
because we *asked* it to; the server doesn't mask rows. For sensitive data,
use CUBRID's own privileges — a dedicated user granted SELECT only on views
that expose aggregates. The MCP server limits statement types; the
database decides what data is visible.

## Q14: Isn't the CUBRID market figure just vendor marketing?

It's from the government's own statistics: MOIS/NIA's 2026 government-wide
EA public-sector information resources report (end-2025 data) — CUBRID
13.24%, 2,367 installations, second only to Oracle. The previous edition
had it at 10.58%, third.
