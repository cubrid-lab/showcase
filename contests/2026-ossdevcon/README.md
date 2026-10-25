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
| SLIDES.md | Current 32-slide talk script, generated from `presentation/slides.md` |
| APPENDIX.md | Technical reference for Q&A |
| EXPECTED_QA.md | 12 anticipated questions + answers |
| DEMO_RUNBOOK.md | Historical On-nara demo script (2 min) + checklist |
| VERIFY.md | Judge verification guide |
| seed_demo_data.py | On-nara e-approval demo data (agencies/documents/approvals) |
| seed_demo_data_products.py | Alternative product catalog demo data |
| cubrid-corp-outreach.md | CUBRID Corp outreach email draft |
| blog-post-draft.md | Tech blog post draft |
| metrics/SNAPSHOT.md | Verified metrics snapshot (refreshed 2026-10-25; re-measure before delivery) |
| captures/ | Historical demo rehearsal scripts + backup recording |

## Consolidation Note

This folder was consolidated from two earlier versions:
- `2026-ossdevcon/` (original, product-based demo)
- `2026-ossdevon/` (evolved, reviewed On-nara demo)

The current canonical presentation is the 32-slide story in
[`presentation/slides.md`](../../presentation/slides.md), with its generated
speaker script in [SLIDES.md](SLIDES.md). It uses code, documentation, repository,
and PR screenshots without a live demo. Adoption charts follow the recorded
snapshot selected by [`presentation/deck.json`](../../presentation/deck.json).

The earlier On-nara and product demos remain reference resources; the demo
runbook, captures, and both seed scripts are preserved for rehearsal and reuse.

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

The active metrics snapshot is [2026-10-25](../../presentation/snapshots/2026-10-25.json); the 2026-09-12 snapshot remains for historical comparison.
Clone traffic includes CI activity and is not an adoption metric; see the
[measurement notes](metrics/SNAPSHOT.md) before reusing any traffic figures.
