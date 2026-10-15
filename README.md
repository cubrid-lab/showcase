# CUBRID Lab — Showcase

Presentations, contest entries, program submissions, demos, and supporting
materials for [cubrid-lab](https://github.com/cubrid-lab) projects, including
the CUBRID client ecosystem and the CUBRID Kubernetes Operator.

## Presentations and submissions

| Event / program | Project | Materials |
|---|---|---|
| 2026 OSS Developer Contest | CUBRID Python ecosystem | [Contest brief, slides, Q&A, demo, and evidence](contests/2026-ossdevcon/) · [Slidev deck](presentation/) |
| 2026 Builder Season 4 — First Validation | CUBRID Kubernetes Operator | [Presentation brief and Korean / English outlines](programs/2026-builder-season4/first-validation/) |

## Repository layout

| Path | Purpose |
|---|---|
| [contests/](contests/) | Contest-specific entries and presentation materials |
| [programs/](programs/) | Program submissions, validation presentations, and application examples |
| [presentation/](presentation/) | Existing Slidev deck for the 2026 OSS Developer Contest |
| [demo-videos/](demo-videos/) | Demo video materials |
| [press-kit/](press-kit/) | Existing CUBRID Python ecosystem one-pagers |
| [scripts/](scripts/) | Build, PDF export, and metrics collection for the existing contest deck |

## Adding a presentation

1. Add the event under `contests/<year>-<event>/` for a contest or
   `programs/<year>-<program>/<milestone>/` for a program milestone.
   Standalone talks can use `talks/<year>-<event>/` when needed.
2. Include a `README.md` with the project, audience, event date, submission
   deadline, required formats, and source of the requirements.
3. Keep language variants and supporting evidence together in that event
   folder. For example, use `SLIDES.ko.md` and `SLIDES.en.md` for outlines,
   and `slides.ko.pptx` and `slides.en.pptx` for the corresponding deliverables.
   An outline is not a submitted deck; mark preparation and submission separately.
4. Add a row to the presentation index above. Keep project-specific metrics,
   biographies, and claims in the corresponding event materials with sources.
5. Check the required delivery format for each event. The existing Slidev
   scripts build the contest deck and export PDF; they do not produce PPTX.

## License

MIT (same as the code projects).
