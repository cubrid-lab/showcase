# Presentation Tooling — Slidev

Shared Slidev tooling for the [showcase presentations](../README.md).
`slides.md` remains the 2026 OSS Developer Contest deck; its existing commands
and scripts continue to use that entry.

The Operator uses `operator-first-validation.ko.md` and
`operator-first-validation.en.md` as thin entry files. They import the
[event's web slide sources](decks/2026-builder-season4/01-validation/)
inside the Slidev project root and share its installed theme and tooling.
See the [event brief](../events/2026-builder-season4/01-validation/) for
requirements. Edit the deck sources for content
and the entry frontmatter for presentation configuration.

## Published HTML presentations

Open the [showcase viewer](https://cubrid-lab.github.io/showcase/) to select a
presentation. The root README and event briefs link directly to each HTML deck.

```bash
npm ci
npm run build:site
```

This builds all three decks into `../site-dist/` with their own URL base paths,
plus a landing page. `PAGES_BASE_PATH` defaults to `/showcase`; set it to an
empty string for a domain-root deployment. Slide navigation uses hash routes.

The Pages workflow rebuilds and deploys when presentation sources or site
build files change on `main`, and supports manual dispatch. It uses the
existing package lock; no additional npm dependency is required. PDFs and
PPTX remain separate exports from the same web sources.

## Operator: web → PDF / PPTX

Run these commands from `presentation/` with Node.js 22.12 or newer:

```bash
npm ci
npm run dev:operator:ko       # Korean web presentation
npm run dev:operator:en       # English web presentation
npm run build:operator       # Both static web presentations
```

The build outputs are `dist/operator-first-validation/operator-first-validation.ko/`
and `dist/operator-first-validation/operator-first-validation.en/`. Each can be
served as its own static site. Use `--base /your/path/` when building for a
hosting subpath; publishing is a separate step.

CLI export requires Slidev's optional `playwright-chromium` peer and its browser.
Install it locally for export without changing the package manifest or lockfile:

```bash
npm install --no-save playwright-chromium
npm run export:operator:pdf
npm run export:operator:pptx
```

The optional install must be repeated after `npm ci`. If Chromium requires
system libraries, follow the [Playwright browser setup guide](https://playwright.dev/docs/browsers#install-system-dependencies).
For an existing browser, append `-- --executable-path /path/to/chrome` to an
export command. Slidev also provides a browser export screen in the dev server.

Both languages are exported to this directory as
`operator-first-validation.{ko,en}.{pdf,pptx}`. The web sources are the source
of truth: make changes there and regenerate the artifacts. Generated files
and `dist/` are ignored by Git; preserve final deliverables as release attachments.

The default PPTX uses an image per slide for visual consistency; its text is
not directly editable, and web interactions/animations become static. Both
formats use `--with-clicks false` so one source slide becomes one exported page.
Slidev 53 also supports `--format pptx-editable` when native text/shapes are
needed, with separate layout review. See the [official export guide](https://sli.dev/guide/exporting).

The Operator talk contains eighteen matched slides per language, speaker notes and
[event Q&A preparation](../events/2026-builder-season4/01-validation/EXPECTED_QA.ko.md).
The [delivery record](../events/2026-builder-season4/01-validation/DELIVERY.md)
records exported artifacts and checks. Build/export checks do not certify a
human rehearsal, desktop PowerPoint inspection or Discord submission.

## Development

```bash
npm install
npm run dev        # Opens browser with live reload
```

## Build

```bash
npm run build      # Static HTML -> dist/
npm run export     # PDF export
```

## Architecture

- `slides.md` — Narrative + speaker notes (Slidev Markdown)
- `deck.json` — Points to the active metrics snapshot
- `snapshots/*.json` — Immutable metrics snapshots with provenance
- `references.json` — Evidence mapping for claims
- `components/` — Vue components for metrics display + evidence

## Workflow

1. Edit `slides.md` for narrative changes
2. Run `python ../scripts/collect_snapshot.py` to create a new snapshot (when needed)
3. Update `deck.json` to point to the new snapshot
4. Preview with `npm run dev`
5. Build final with `npm run build`

## Finals Build

### Preparation version (continuous improvement)

```bash
./scripts/build_final.sh
```

### Finals version (frozen for submission)

```bash
./scripts/build_final.sh --finals
```

This stamps `manifest.json` with the current commit SHA and build timestamp.

### PDF export

```bash
./scripts/export_pdf.sh
```

### Offline verification

```bash
cd presentation/dist
python3 -m http.server 8080
# Disconnect network, open http://localhost:8080
# All slides should render without external resources
```

### Version manifest

`manifest.json` records what was used for the final presentation:
- `presentationCommit`: Git SHA of the frozen content
- `snapshot`: Which metrics snapshot was active
- `demoVersions`: Package versions used in the live demo
- `builtAt`: When the finals build was created
