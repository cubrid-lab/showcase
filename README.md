# CUBRID Lab — Showcase

Presentations, contest entries, program submissions, demos, and supporting
materials for [cubrid-lab](https://github.com/cubrid-lab) projects, including
the CUBRID client ecosystem and the CUBRID Kubernetes Operator.

## Presentations and submissions

| Event / program | Project | Presentation sources | Overview |
|---|---|---|---|
| 2026 OSS Developer Contest | CUBRID Python ecosystem | [Slides](presentation/slides.md) · [Talk script](contests/2026-ossdevcon/SLIDES.md) | [Contest materials](contests/2026-ossdevcon/) |
| 2026 Builder Season 4 | CUBRID Kubernetes Operator | First validation: [한국어](presentation/decks/2026-builder-season4/01-validation/SLIDES.ko.md) · [English](presentation/decks/2026-builder-season4/01-validation/SLIDES.en.md) | [Program and presentation rounds](events/2026-builder-season4/) |

The links above open slide sources on GitHub. A hosted web slide viewer is
not deployed yet. The Operator sources are seven-slide writing scaffolds;
see the [first-validation brief](events/2026-builder-season4/01-validation/)
for their preparation state and local preview commands.

## Repository layout

| Path | Purpose |
|---|---|
| [events/](events/) | Event briefs and presentation milestones, regardless of event type |
| [contests/](contests/) | Existing contest materials, with their original paths preserved |
| [programs/](programs/) | Program submissions, validation presentations, and application examples |
| [presentation/](presentation/) | Shared Slidev tooling and deck entry files for web, PDF, and PPTX |
| [demo-videos/](demo-videos/) | Demo video materials |
| [press-kit/](press-kit/) | Existing CUBRID Python ecosystem one-pagers |
| [scripts/](scripts/) | Build, PDF export, and metrics collection for the existing contest deck |

## Adding a presentation

1. Add new material under `events/<year>-<event>/<milestone>/`, whether it
   is a contest, program, conference, or meetup. Keep existing contest paths
   intact. Use the index to identify the project and describe the event type.
2. For a recurring program, include an event-level `README.md` linking its
   presentation rounds. Each milestone gets a `README.md` with the project,
   audience, event date, submission deadline, required formats, and source
   of the requirements. Add future rounds when preparation starts.
3. Keep the event brief and supporting evidence in that event folder. Put
   web slide sources in `presentation/decks/<year>-<event>/<milestone>/`
   as `SLIDES.ko.md` and `SLIDES.en.md`, with entry files in `presentation/`.
   This keeps imports within the Slidev project root and reuses its tooling.
   Link the sources from the event brief, and generate PDF and PPTX from
   those sources. Mark preparation and submission separately.
4. Add a row to the presentation index above. Keep project-specific metrics,
   biographies, and claims in the corresponding event materials with sources.
5. Check the required delivery format for each event. Follow the
   [Operator workflow](events/2026-builder-season4/01-validation/#웹-원본에서-발표와-내보내기)
   for web preview, static builds, and Korean/English PDF and PPTX export.
   Generated files stay out of Git; keep final submissions as event release
   attachments, with the source commit recorded in the event brief.

## License

MIT (same as the code projects).
