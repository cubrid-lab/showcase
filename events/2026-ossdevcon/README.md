# 2026 OSS Developer Contest

## Presentation

- **[View slides (HTML)](https://cubrid-lab.github.io/showcase/contests/2026-ossdevcon/)** — latest version, rebuilt from `main`; opens in the browser
- **[Download PDF, 2026-10-25 release](https://github.com/cubrid-lab/showcase/releases/download/ossdevcon-2026-presentation-2026-10-25/ossdevcon.pdf)** · **[Download PowerPoint (PPTX)](https://github.com/cubrid-lab/showcase/releases/download/ossdevcon-2026-presentation-2026-10-25/ossdevcon.pptx)** · [HTML ZIP of the same version](https://github.com/cubrid-lab/showcase/releases/download/ossdevcon-2026-presentation-2026-10-25/ossdevcon-html.zip) (unzip and serve with `python3 -m http.server`)
- [Release `ossdevcon-2026-presentation-2026-10-25`](https://github.com/cubrid-lab/showcase/releases/tag/ossdevcon-2026-presentation-2026-10-25) — version record: source commit, export workflow run, metrics snapshot and SHA-256 checksums

| Format | Role |
|---|---|
| [`presentation/decks/2026-ossdevcon/slides.md`](../../presentation/decks/2026-ossdevcon/slides.md) | Editable Slidev source of the slides and speaker notes; edit this file. Deck settings are in the entry [`presentation/2026-ossdevcon.md`](../../presentation/2026-ossdevcon.md) |
| [SLIDES.md](SLIDES.md) | Speaker script collected from the speaker notes in `slides.md`; not the slide source |
| HTML | Published from `slides.md` on every qualifying push to `main` |
| PDF | Exported from `slides.md`; one page per slide |
| PPTX | One static image per slide for presenting; text and shapes are not editable |

The PDF and PPTX in the release were exported from commit `3feb210` with metrics
snapshot 2026-10-25. The HTML deck follows `main`, so it can be newer than the
release files after later slide changes.

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
| SLIDES.md | Current 32-slide speaker script, collected from the speaker notes in `presentation/decks/2026-ossdevcon/slides.md` |
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
[`presentation/decks/2026-ossdevcon/slides.md`](../../presentation/decks/2026-ossdevcon/slides.md), with its generated
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
- [Benchmark rerun 2026-10-25](metrics/benchmark-2026-10-25/README.md) — versions, environment, commands and raw output of the performance numbers on the deck
- [English one-pager](../../projects/cubrid-python-ecosystem/press-kit/ONE_PAGER.md)
- [Korean one-pager](../../projects/cubrid-python-ecosystem/press-kit/ONE_PAGER.ko.md)

The active metrics snapshot is [2026-10-25](../../presentation/snapshots/2026-10-25.json); the 2026-09-12 snapshot remains for historical comparison.
Clone traffic includes CI activity and is not an adoption metric; see the
[measurement notes](metrics/SNAPSHOT.md) before reusing any traffic figures.
