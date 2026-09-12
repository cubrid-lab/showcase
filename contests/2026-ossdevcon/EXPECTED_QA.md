# Expected Q&A — 2026 OSS Developer Contest Finals

> Prepare answers for likely judge questions. Practice delivering these
> concisely (30-60 seconds each). Numbers verified 2026-09-12.

---

## Q0: "Tell us about your team's background." (새로 추가 — 스토리 질문)

**A:** We met at an open source contribution hackathon (컨트리뷰톤) as mentor
and mentee. We contributed to SQLAlchemy core and sqlalchemy-hana (SAP HANA
dialect), learning the dialect API from the inside. That's when we asked:
"Why doesn't CUBRID have this?" We started with sqlalchemy-cubrid, discovered
the official driver was dead since 2014, and ended up building the entire
stack — driver, ORM, examples, and AI/MCP server.

---

## Q0.5: "You mentioned SQLAlchemy Korea — tell us about that."

**A:** In October 2020, after discussing with Mike Bayer via Gitter, I opened
the SQLAlchemy Korea Facebook group to build a local community for Korean
SQLAlchemy users. It's still active today. That experience — building a
community around an open source tool — directly informed how we structured
the CUBRID ecosystem: documentation in Korean, translation sync CI, and
good-first-issues for newcomers. Community isn't an afterthought; it's
designed into our workflow.

---

## Q1: "Why not just use the official CUBRID Python driver?"

**A:** The official driver's last PyPI release was **May 2014** — 12 years ago.
It's a C extension requiring a compiler toolchain, doesn't support asyncio,
doesn't support Python 3.5+ (we support 3.10-3.14), and has no TLS support.
Our pycubrid is pure Python — `pip install pycubrid` just works. And for
users who still need the old driver, sqlalchemy-cubrid supports both via
`cubrid+cubriddb://` URLs. We're not replacing it — we're filling the gap
that SQLAlchemy and sqlalchemy-hana taught us how to fill.

---

## Q2: "Why are there so many AI-generated commits?"

**A:** We built a system where AI agents write code and humans review it —
the same mentor-mentee model we learned from OSS contribution culture.
AGENTS.md defines the rules, AI implements, every PR goes through the same
CI gates (20-combination live DB tests, 95% coverage, mypy strict), and
only humans push release tags. 450 merged PRs are evidence the system works.

---

## Q3: "Stars are low — is anyone actually using this?"

**A:** We're early — that's honest. But **822 developers cloned our repos
in the last 14 days** (GitHub Traffic API, CI actions excluded). That's
people downloading and experimenting. Also: we're the **only** modern Python
driver for a database that holds **10.6%** of Korean public sector DBMS
market share. The market exists — 1,500+ systems are waiting for this tooling.

---

## Q4: "Isn't CUBRID GPL? Does your MIT license conflict?"

**A:** No. We verified CUBRID's upstream COPYING directly: the server engine
is **Apache License 2.0** and official APIs/connectors are **BSD** — the
often-cited GPL v2+ no longer applies. And even under the old GPL regime,
our packages are independent wire-protocol clients with zero server code.
All our THIRD_PARTY_LICENSES are generated with pip-licenses — no GPL
anywhere in our dependency trees.

---

## Q5: "How does performance compare to C extensions?"

**A:** Honestly — C extensions will always have an edge in raw throughput.
But what you gain: zero installation friction (no compiler), cross-platform,
native asyncio, and TLS. For the 95% of use cases that aren't latency-critical
bulk inserts, install simplicity outweighs the throughput gap. And we're
actively optimizing — 19% fetch improvement shipped in the current release.

---

## Q5.5: How did you approach performance optimization?

We built cubrid-benchmark (separate repo) for reproducible comparison, then used profiling scripts to find bottlenecks. Key results: native ping +280%, pool_pre_ping +588%, bulk insert 12.3% faster, select-all 19.9% faster. In a niche market, you benchmark yourself.

## Q6: "What about CUBRID 12 support?"

**A:** CUBRID 12 hasn't shipped yet. Our CI already tests against 10.2, 11.0,
11.2, and 11.4 (20 Python×CUBRID combinations). When 12 releases, we add it
to the matrix and fix any issues. The CAS wire protocol has been stable
since 10.2.

---

## Q7: "Vector types for AI workloads?"

**A:** CUBRID's `cubvec` branch is under development upstream. We've analyzed
the wire format, type codes, and HNSW index structure. Once the server
releases, we'll prototype behind an experimental flag. On our roadmap.

---

## Q8: "Is the MCP write mode dangerous?"

**A:** It's **off by default** and requires explicit opt-in. Even then, it
only allows single DML statements in atomic transactions — no DDL, no
multi-statement. The database user should still be SELECT-only (defense in
depth). We demonstrate the safety live: asking Claude to "DROP TABLE" gets
**rejected by the server-level whitelist**.

---

## Q9: "How do you handle CUBRID-specific SQL differences?"

**A:** Our MCP server ships with **domain knowledge resources** — 5 guide
documents that teach LLMs about CUBRID's LIMIT syntax, SHOW TRACE vs EXPLAIN,
collection types, and more. Plus 5 expert prompts for common workflows.
This means Claude can write correct CUBRID SQL without prior knowledge —
because the server teaches it. This is a pattern we haven't seen in other
MCP servers.

---

## Q10: "You mentioned contributing to SQLAlchemy — tell us more."

**A:** (Backing up Q0) We contributed to SQLAlchemy core and sqlalchemy-hana
(SAP HANA dialect) during an OSS contribution hackathon. That experience
taught us:
1. The Dialect API — how to implement visit_* methods, type compilers,
   reflection
2. Testing discipline — the official SQLAlchemy test suite (which we now
   run against CUBRID)
3. Code review culture — which we applied to our AI-agent workflow

Without that contribution experience, this project wouldn't exist. It's
the OSS flywheel in action: learn from existing projects → build for your
ecosystem → open the door for the next contributor.

---

## Q11: "What's your sustainability plan after the contest?"

**A:** The infrastructure is built for longevity: translation sync CI,
label taxonomy with weekly drift audit, automated SBOM generation, 1.x
release policy with API compatibility gates, 5 good-first-issues seeded.
The code is MIT — anyone can fork and continue. And we hope the next
컨트리뷰톤 mentee finds our project and continues the cycle.
