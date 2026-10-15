# 2026 OSS Developer Contest

## Entry

pycubrid · sqlalchemy-cubrid · cubrid-cookbook-python · cubrid-mcp-server

## Background

In 2020, we joined the OSS Contribution Hackathon (컨트리뷰톤, CNBT-41) as
mentor (Yeongseon) and mentee (Gyeongjun). We contributed to SQLAlchemy
and sqlalchemy-hana, connected with SQLAlchemy creator Mike Bayer via
Gitter, and started the SQLAlchemy Korea community. Then we asked:
"Why is CUBRID's Python ecosystem dead?" — and built the answer.

## Schedule

- Round 1 (written): Passed
- Round 2 (presentation): Q4 2026

## Scoring

Usability 15 · OSS 15 · PT 10 · Demo 10 · Testing 10 · Community 5 · License 5

## Contents

| File | Purpose |
|---|---|
| SLIDES.md | 14-slide presentation (Oracle-reviewed, On-nara demo) |
| APPENDIX.md | Technical reference for Q&A |
| EXPECTED_QA.md | 12 anticipated questions + answers |
| DEMO_RUNBOOK.md | On-nara demo script (4 min) + checklist |
| VERIFY.md | Judge verification guide |
| seed_demo_data.py | On-nara e-approval demo data (agencies/documents/approvals) |
| seed_demo_data_products.py | Alternative product catalog demo data |
| cubrid-corp-outreach.md | CUBRID Corp outreach email draft |
| blog-post-draft.md | Tech blog post draft |
| metrics/SNAPSHOT.md | Verified metrics snapshot (re-measure on presentation day) |
| captures/ | Demo rehearsal scripts + backup recording |

## Consolidation Note

This folder was consolidated from two earlier versions:
- `2026-ossdevcon/` (original, product-based demo)
- `2026-ossdevon/` (evolved, Oracle-reviewed On-nara demo)

The On-nara version (14 slides) is now canonical. The product-based seed
script is preserved as `seed_demo_data_products.py`.

## VHS Demo Scripts

Terminal demo GIFs are generated from VHS (.tape) scripts in each repo:

| Repo | Script | Renders |
|---|---|---|
| pycubrid | `demos/pycubrid-demo.tape` | `docs/demo.gif` |
| sqlalchemy-cubrid | `demos/orm-demo.tape` | `docs/demo.gif` |
| cubrid-mcp-server | `demos/mcp-demo.tape` | `docs/demo.gif` |
| cubrid-cookbook | `demos/agent-state.tape` | `docs/demo-agent-state.gif` |
| cubrid-cookbook | `demos/mcp-toolchain.tape` | `docs/demo-mcp-toolchain.gif` |

## Presentation and supporting evidence

- [Slidev presentation](../../presentation/README.md) — development and export instructions
- [Metrics snapshot](metrics/SNAPSHOT.md) — provenance and measurement details
- [English one-pager](../../press-kit/ONE_PAGER.md)
- [Korean one-pager](../../press-kit/ONE_PAGER.ko.md)

### Historical ecosystem context (2026-09-12)

The following tables were moved from the showcase homepage. They preserve
the context of this contest entry; they are not current organization-wide
metrics or evidence for the Kubernetes Operator. Re-verify claims before reuse.

| Metric | Value |
|---|---|
| GitHub stars | 119 |
| Unique clones (14d, per-repo sum) | ~926 |
| Merged PRs | 450 |
| PyPI releases | 35 |
| Tests | 2,200 (CI-enforced) |
| CI combinations | Python 5 × CUBRID 4 = 20 |
| Docs sites | 4/4 live |
| Korean docs | 34 pages |

### Ecosystem

| Language | Driver | ORM | Status |
|---|---|---|---|
| **Python** | pycubrid v1.7.0 | sqlalchemy-cubrid v1.7.0 | **Complete** |
| TypeScript | cubrid-client v1.1.0 | drizzle-cubrid v0.2.1 | In progress |
| Go | cubrid-go v0.2.1 | gorm-cubrid v0.1.0 | In progress |
| Rust | cubrid-rs v0.1.0 | sea-orm-cubrid v0.1.0 | In progress |
