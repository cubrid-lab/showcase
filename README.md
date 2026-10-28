# CUBRID Lab — Showcase

<!-- CUBRID-LAB-ICON:START -->
<p align="center">
  <a href="https://github.com/cubrid-lab/brand"><img src="https://raw.githubusercontent.com/cubrid-lab/brand/e55990a6a0b2c3b0d133985951d41e42b62a8588/dist/icons/showcase.svg" alt="showcase icon (CUBRID Lab brand repository)" width="120"></a>
</p>
<!-- CUBRID-LAB-ICON:END -->

Presentations, event submissions, demonstration materials and public project assets for [CUBRID Lab](https://github.com/cubrid-lab).

**[Open HTML presentations](https://cubrid-lab.github.io/showcase/)**

## Events and presentations

| Event | Project | Latest HTML (follows `main`) | Released PDF, PPTX and HTML ZIP | Source and materials |
|---|---|---|---|---|
| 2026 OSS Developer Contest | CUBRID Python ecosystem | [HTML slides](https://cubrid-lab.github.io/showcase/contests/2026-ossdevcon/) | [2026-10-25 release](https://github.com/cubrid-lab/showcase/releases/tag/ossdevcon-2026-presentation-2026-10-25): [PDF](https://github.com/cubrid-lab/showcase/releases/download/ossdevcon-2026-presentation-2026-10-25/ossdevcon.pdf) · [PPTX](https://github.com/cubrid-lab/showcase/releases/download/ossdevcon-2026-presentation-2026-10-25/ossdevcon.pptx) · [HTML ZIP](https://github.com/cubrid-lab/showcase/releases/download/ossdevcon-2026-presentation-2026-10-25/ossdevcon-html.zip) | [Contest materials](events/2026-ossdevcon/) |
| 2026 Builder Season 4 | CUBRID Kubernetes Operator | First validation: [한국어](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/ko/) · [English](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/en/) | [2026-10-28 release](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-28-r2): 한국어 [PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-28-r2/operator-first-validation.ko.pdf) · [PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-28-r2/operator-first-validation.ko.pptx) · [HTML ZIP](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-28-r2/operator-first-validation.ko-html.zip); English [PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-28-r2/operator-first-validation.en.pdf) · [PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-28-r2/operator-first-validation.en.pptx) · [HTML ZIP](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-28-r2/operator-first-validation.en-html.zip) | [Validation and submission brief](events/2026-builder-season4/01-validation/) |

The HTML slides are rebuilt from `main` on every presentation change, so they can be newer than a release's PDF and PPTX. Each release lists the source commit its files were exported from; its HTML ZIP is the HTML for that same commit (unzip and serve with `python3 -m http.server`). Earlier versions stay available on the [releases page](https://github.com/cubrid-lab/showcase/releases).

For upcoming rounds and program opportunities, see the [events index](events/).

## Project materials

| Project | Materials |
|---|---|
| CUBRID Lab | [Introduction video project](projects/cubrid-lab/intro-video/) |
| CUBRID Python ecosystem | [Press kit and one-pagers](projects/cubrid-python-ecosystem/press-kit/) |

[Browse all project materials](projects/).

## Repository structure

| Directory | Purpose |
|---|---|
| [events/](events/) | Time-bound contest entries, program submissions, speaker notes, demos and supporting evidence |
| [projects/](projects/) | Reusable project and organization promotional assets |
| [templates/](templates/) | Reusable application, presentation and demo templates |
| [presentation/](presentation/) | Shared Slidev project, canonical deck sources, themes, metrics snapshots and export configuration |
| [scripts/](scripts/) | Shared build, export and metrics tools |

Each event brief links to its source deck and supporting evidence. Deck sources live in `presentation/decks/<event>/[<round>/]`, inside the shared Slidev project, because the build needs that project root. This is a tooling constraint, not a second copy of the event material.

## Add a presentation

1. Create `events/<year>-<event>/README.md` for a new event, and an event milestone directory when there are multiple presentation rounds.
2. Record the project, audience, requirements, deadline and source of the event details in the event brief.
3. Put the canonical slide source at `presentation/decks/<year>-<event>/[<round>/]slides[.<lang>].md`, add a thin entry next to the other entries in `presentation/` ([naming rules](presentation/README.md#where-deck-sources-live)), and link the source from the brief. Keep event-specific runbooks, notes and evidence in the event directory.
4. Update the events index and, when a public viewer exists, the HTML presentation index. Derive PDF/PPTX from the same source.
5. Publish immutable deliverables as release assets with a source commit, and verify links and exports before publication.

**Compatibility:** The OSSDevCon HTML presentation keeps its existing `/contests/2026-ossdevcon/` public URL. The source materials have moved to `events/2026-ossdevcon/`; existing published release links remain unchanged.

## License

MIT (same as the code projects).
