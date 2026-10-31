# Expected Q&A — 2026 OSS Developer Contest Finals

> 18 anticipated questions with prepared spoken answers (30-60 seconds each).
> Evidence and sources are in [APPENDIX.md](APPENDIX.md); commands to reproduce are in
> [VERIFY.md](VERIFY.md). Repository metrics are dated 2026-10-25, outside contributors
> 2026-10-28 (UTC); clone and CI figures are from 2026-09-27.

---

## Q0: Tell us about your team's background.

We are the PyCUBRID team (파이큐브리드팀). We met at the 2020 OSS Contribution
Hackathon as mentor and mentee. We contributed to SQLAlchemy and sqlalchemy-hana, connected with Mike
Bayer via Gitter, and started the SQLAlchemy Korea community. Mike Bayer
had built a CUBRID dialect in 2012 but abandoned it. We rebuilt from
scratch for SQLAlchemy 2.0, then built the pure Python driver, then the
full ecosystem, including a CUBRID MCP server for AI tools. As of 2026-11-01, 67 people outside the team have had 153 pull requests merged
(maintainers and bots excluded).

## Q1: Why not just use the official CUBRID Python driver?

The official driver's last PyPI release was May 2014 — 12 years ago.
Newer versions (up to v11.3.0.51, September 2025) are published only as
GitHub releases of a C extension you build yourself, and it has no
asyncio support. Our pycubrid is pure Python,
works on 3.10-3.14, and `pip install pycubrid` just works. We also
support the old driver via `cubrid+cubriddb://` URLs in our dialect.

## Q2: Why are there so many AI-generated commits?

We use AI coding tools, and we do not trust them blindly. AGENTS.md defines
the rules, humans review, every PR is merged only after CI gates pass
(driver and dialect PRs run the 20-combination live DB matrix with a 95%
coverage floor), and only humans push release tags. As of 2026-10-25, the four repositories have 1,553 merged PRs in total;
that counts all authors and is repository activity, not people.

## Q3: Stars are low — is anyone actually using this?

We're early, and we don't inflate it. We deliberately don't quote clone
counts: GitHub clone traffic is dominated by our own CI runners (pycubrid:
~700 workflow runs vs ~5,000 clones in the same 14 days). What we can show
is 67 outside contributors with 153 merged PRs (2026-11-01), 61 published GitHub
Releases across the three package repositories, and 129 stars across the four
repositories (2026-10-25). The market is real: CUBRID
ranks second among the top five Korean public-sector DBMS vendors
(2,367 installations; 13.24% of their combined total at end of
2025, MOIS/NIA report), and before us it had no Python driver you could
`pip install` from a current PyPI release.

## Q4: Isn't CUBRID GPL? Does your MIT license conflict?

No. We verified CUBRID's upstream COPYING: server engine is Apache-2.0,
connectors are BSD. The often-cited GPL v2+ no longer applies. Our
packages are independent wire-protocol clients with zero server code.
No GPL anywhere in our dependency trees.

## Q5: How does performance compare to C extensions?

We measured it on 2026-10-28 against the official C driver on the same
CUBRID 11.4.6 server: pycubrid 1.15.0 is about 1.04x the time on a primary-key
SELECT, 1.17x on fetching 10,000 rows and 1.04x on inserting 10,000 rows
with executemany (within the noise for that one). It is a little slower, because it
is pure Python. In return you get `pip install` without a compiler,
cross-platform use, native asyncio and TLS. Caveat: one shared host,
so the ratios are more reliable than absolute times
([APPENDIX 2](APPENDIX.md#2-performance-evidence)).

## Q5.5: How did you approach performance optimization?

We built cubrid-benchmark (separate repo) for reproducible comparison,
then used profiling scripts to find bottlenecks. Earlier results (not
rerun; run date and versions not recorded) include native ping +280%
throughput and pool_pre_ping +588%; treat them as history, not a current
measurement. The current numbers are the 2026-10-28 same-server comparison
above ([APPENDIX 2](APPENDIX.md#2-performance-evidence)). In a niche market,
you benchmark yourself.

## Q6: What about CUBRID 12 support?

No CUBRID 12 release or schedule has been announced; the latest releases
are 11.4.6 (2026-09-10) and 11.3.6 (2026-10-20). Our CI already tests 10.2,
11.0, 11.2 and 11.4 (20 combinations). Any new CUBRID version is added to the
matrix when it ships.

## Q7: Vector types for AI workloads?

Not yet. A native VECTOR type is still being developed in the CUBRID
repository (the `cubvec` branches and PR CUBRID/cubrid#7076, not merged as of
2026-11-01). We will look at driver support once it is in a CUBRID release.

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
Plus 9 prompts for common workflows. Claude can write correct
CUBRID SQL without prior knowledge — because the server teaches it.

## Q10: You mentioned contributing to SQLAlchemy — tell us more.

We contributed to SQLAlchemy and sqlalchemy-hana during a hackathon.
Mike Bayer (SQLAlchemy creator) had built zzzeek/sqlalchemy_cubrid in
2012 but abandoned it. We met Mike via Gitter. We didn't fork his
code — we wrote a new dialect from scratch targeting SQLAlchemy 2.0.

## Q10.5: Is this just for Python?

Python is complete and is the contest entry. TypeScript, Go and Rust
ecosystems are in progress, using the same approach
([APPENDIX 5](APPENDIX.md#5-other-languages)).

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
2,367 installations, second among the top five vendors after Oracle.
The reported 13.24% is CUBRID's share of those five vendors' combined
17,883 installations, not of all public-sector DBMS installations.
See [printed page 57, table 46](https://www.data.go.kr/data/3038513/fileData.do).
