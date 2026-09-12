# Expected Q&A — 2026 OSS Developer Contest Finals

> Prepare answers for likely judge questions. Practice delivering these
> concisely (30-60 seconds each). Numbers verified 2026-09-12.

---

## Q1: "Why not just use the official CUBRID Python driver?"

**A:** The official driver's last PyPI release was **May 2014** — 12 years ago.
It's a C extension requiring a compiler toolchain, doesn't support asyncio,
doesn't support Python 3.5+ (we support 3.10-3.14), and has no TLS support.
Our pycubrid is pure Python — `pip install pycubrid` just works. And for
users who still need the old driver, sqlalchemy-cubrid supports both via
`cubrid+cubriddb://` URLs. We're not replacing it — we're filling the gap.

---

## Q2: "Why are there so many AI-generated commits?"

**A:** We built a system where AI agents write code and humans review it.
AGENTS.md defines the rules, AI implements, every PR goes through the same
CI gates (20-combination live DB tests, 95% coverage, mypy strict), and
only humans push release tags. Slide 9 shows: "We built a system to validate
AI-written code, not just AI-written code." The 450 merged PRs are evidence
the system works — every one passed the same quality gates.

---

## Q3: "Stars are low — is anyone actually using this?"

**A:** We're early — that's honest. But look at the signals beyond stars:
**822 developers cloned our repos in the last 14 days** (GitHub Traffic API,
CI actions excluded). That's people downloading and experimenting with the
code, not just starring and leaving. Also: we're the **only** modern Python
driver for a database that holds **10.6%** of Korean public sector DBMS
market share. The market exists — 1,500+ systems are waiting for this tooling.

---

## Q4: "Isn't CUBRID GPL? Does your MIT license conflict?"

**A:** No. We verified CUBRID's upstream COPYING directly: the server engine
is **Apache License 2.0** and official APIs/connectors are **BSD** — the
often-cited GPL v2+ no longer applies. And even under the old GPL regime,
our packages are independent wire-protocol clients with zero server code.
All our THIRD_PARTY_LICENSES are generated with pip-licenses — no GPL
anywhere in our dependency trees. This is documented in every repo.

---

## Q5: "How does performance compare to C extensions?"

**A:** Honestly — C extensions will always have an edge in raw throughput.
Our benchmarks show pycubrid at 4.5-6.0x vs PyMySQL in synthetic workloads.
But what you gain: zero installation friction (no compiler), cross-platform
(Ubuntu + macOS + any OS with Python), native asyncio, and TLS. For the
95% of use cases that aren't latency-critical bulk inserts, the install
simplicity outweighs the throughput gap. And we're actively optimizing —
19% fetch improvement shipped in the current release.

---

## Q6: "What about CUBRID 12 support?"

**A:** CUBRID 12 hasn't shipped yet. We're tracking it — our CI already
tests against 10.2, 11.0, 11.2, and 11.4 (20 Python×CUBRID combinations).
When 12 releases, we add it to the matrix and fix any issues. The CAS
wire protocol has been stable since 10.2.

---

## Q7: "Vector types for AI workloads?"

**A:** CUBRID's `cubvec` branch is under active development upstream. We've
already analyzed the wire format, type codes, and HNSW index structure.
Once the server releases, we'll prototype behind an experimental flag.
This is on our roadmap (slide 11) but outside the current contest scope.

---

## Q8: "Is the MCP write mode dangerous?"

**A:** It's **off by default** and requires explicit opt-in via
`CUBRID_MCP_WRITE=1`. Even then, it only allows single DML statements
(INSERT/UPDATE/DELETE) in atomic transactions — no DDL, no multi-statement.
And the database user should still be SELECT-only (defense in depth).
We demonstrate the safety in our demo: asking Claude to "DROP TABLE"
gets **rejected by the server-level whitelist**.

---

## Q9: "How do you handle CUBRID-specific SQL differences?"

**A:** Our MCP server now ships with **domain knowledge resources** —
5 guide documents (`cubrid://agent-guide`, `cubrid://guide/sql-dialect`,
`cubrid://guide/types`, etc.) that teach LLMs about CUBRID's LIMIT syntax,
SHOW TRACE vs EXPLAIN, collection types, and more. Plus 5 expert prompts
that guide common workflows. This means Claude can write correct CUBRID
SQL without prior knowledge — because the server teaches it.

---

## Q10: "What's your sustainability plan after the contest?"

**A:** The infrastructure is already built for longevity: translation sync
CI, label taxonomy with weekly drift audit, automated SBOM generation,
1.x release policy with API compatibility gates. We have 5 good-first-issues
seeded for external contributors. The CUBRID Corporation sponsorship of
this contest signals ecosystem alignment. And the code is MIT — anyone
can fork and continue.
