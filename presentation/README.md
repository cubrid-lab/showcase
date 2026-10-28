# Presentation Tooling — Slidev

Shared Slidev tooling for the [showcase presentations](../README.md).

## Where deck sources live

Every deck has one editable source under `decks/` and one thin entry file in
this directory:

| Presentation | Edit this source | Slidev entry (configuration only) |
|---|---|---|
| 2026 OSS Developer Contest | [`decks/2026-ossdevcon/slides.md`](decks/2026-ossdevcon/slides.md) | [`2026-ossdevcon.md`](2026-ossdevcon.md) |
| Builder Season 4, first validation (Korean) | [`decks/2026-builder-season4/01-validation/slides.ko.md`](decks/2026-builder-season4/01-validation/slides.ko.md) | [`2026-builder-season4-01-validation.ko.md`](2026-builder-season4-01-validation.ko.md) |
| Builder Season 4, first validation (English) | [`decks/2026-builder-season4/01-validation/slides.en.md`](decks/2026-builder-season4/01-validation/slides.en.md) | [`2026-builder-season4-01-validation.en.md`](2026-builder-season4-01-validation.en.md) |

Naming rules for a new deck, round or language:

- Source: `decks/<year>-<event>/[<round>/]slides[.<lang>].md`. It holds the
  slides and speaker notes. Its first frontmatter block only sets `title`.
- Entry: `<year>-<event>[-<round>][.<lang>].md` in this directory. It holds the
  deck-wide Slidev settings (theme, canvas width, fonts, export name) and
  `src: ./decks/...` pointing at the source, and no slides.
- Register the deck in `presentations.json` and add its `export:*` npm
  scripts and workflow export step, and link the source from the event brief.

The entry files cannot move into a subdirectory. Slidev treats the entry's
directory as the project root, so an entry elsewhere would lose the shared
`components/`, `public/`, `style.css` and theme. `scripts/check_showcase_links.py`
fails if a Markdown file at this level is not a thin entry, or if a source
under `decks/` does not follow the naming rule.

Until 2026-10-28 the OSSDevCon source was `presentation/slides.md`, and the
Builder sources were `SLIDES.ko.md`/`SLIDES.en.md` loaded by
`operator-first-validation.{ko,en}.md` (#69). Links to those paths on `main` no
longer resolve. Released files and the public HTML routes are unchanged, and
the exported files keep their names.

The supporting contest materials are in [events/2026-ossdevcon](../events/2026-ossdevcon/), while the published HTML slides deliberately retain the historical `/contests/2026-ossdevcon/` route for existing links.

See the [Builder Season 4 event brief](../events/2026-builder-season4/01-validation/)
for that deck's requirements.

## Brand marks

The decks show the CUBRID Lab emblem (the favicon), the horizontal lockup and, in the Operator deck, the Operator icon. Because the decks run offline, `public/favicon.svg` and `public/brand/*.svg` are byte-identical copies from a recorded `cubrid-lab/brand` revision (decision 6 of the brand repository's `BRAND_USAGE.md`); [`public/brand/README.md`](public/brand/README.md) records the revision and rules, and `SHA256SUMS` lets you verify them with `cd public && sha256sum -c brand/SHA256SUMS`. Use the `BrandMark` component and only scale the mark.

## Published HTML presentations

Open the [showcase viewer](https://cubrid-lab.github.io/showcase/) to select a
presentation. The root README and event briefs link directly to each HTML deck.

```bash
npm ci
npm run build:site
```

This builds every deck in `presentations.json` into `../site-dist/` with its
own URL base path, plus a landing page. `PAGES_BASE_PATH` defaults to `/showcase`; set it to an
empty string for a domain-root deployment. Slide navigation uses hash routes.

The Pages workflow rebuilds and deploys when presentation sources or site
build files change on `main`, and supports manual dispatch. It uses the
existing package lock; no additional npm dependency is required.

## Deliverables: HTML, PDF and PPTX for every deck

Each deck in [`presentations.json`](presentations.json) is published in three
formats from the same checkout. The registry gives each deck its entry, public
HTML route, export file name and release group; the site build, the export
verification, the packaging script and the layout check all read it.

| Deck | Latest HTML (follows `main`) | PDF / PPTX / HTML ZIP file names |
|---|---|---|
| 2026 OSS Developer Contest | `/contests/2026-ossdevcon/` | `ossdevcon.{pdf,pptx}`, `ossdevcon-html.zip` |
| Builder Season 4, first validation (Korean) | `/events/2026-builder-season4/01-validation/ko/` | `operator-first-validation.ko.{pdf,pptx}`, `operator-first-validation.ko-html.zip` |
| Builder Season 4, first validation (English) | `/events/2026-builder-season4/01-validation/en/` | `operator-first-validation.en.{pdf,pptx}`, `operator-first-validation.en-html.zip` |

These are the same commands the CI export workflow runs, from `presentation/`:

```bash
npm ci
HTML_BUNDLE_DIR=$PWD/exports/html PAGES_BASE_PATH=/showcase npm run build:site
npm install --no-save --package-lock=false playwright-chromium@1.64.1
npx playwright install chromium
npm run export:ossdevcon:pdf
npm run export:ossdevcon:pptx
npm run export:operator:pdf     # Korean and English
npm run export:operator:pptx    # Korean and English
python3 -m pip install --target "${TMPDIR:-/tmp}/verify-pydeps" pypdf==6.20.0
PYTHONPATH="${TMPDIR:-/tmp}/verify-pydeps" python3 scripts/verify_exports.py
(cd .. && PYTHONPATH="${TMPDIR:-/tmp}/verify-pydeps" python3 scripts/package_presentations.py \
  --html presentation/exports/html --out presentation/exports/releases)
```

`PAGES_BASE_PATH` only sets the site's URL prefix. It defaults to `/showcase`,
so set it to an empty string (`PAGES_BASE_PATH=`) for a root-hosted preview.
`HTML_BUNDLE_DIR` is optional; when set, each deck is also built with a
relative base so it can be zipped into a release.

Outputs:
- HTML site: `../site-dist/index.html` and the linked presentation pages
- PDF and PowerPoint: `exports/<export name>.{pdf,pptx}`
- Release groups: `exports/releases/<release>/` (see below)

The export commands require Slidev's optional `playwright-chromium` peer and a
Chromium browser. If Chromium requires system libraries, follow the
[Playwright browser setup guide](https://playwright.dev/docs/browsers#install-system-dependencies).
Slidev can exit successfully while a slide still shows its "Loading slide..."
placeholder, so every export command waits for network idle and then 5 seconds
before capturing. `scripts/verify_exports.py` checks every registered deck and
fails if a file is missing, a PDF page is blank or shows the placeholder, or the
PDF page count, PPTX slide count or PPTX speaker-note count differs from the
deck's slide count. The PPTX holds images only, so inspect it visually. All
exports use `--with-clicks false` so one source slide becomes one page.

### CI artifact

The CI export workflow (`.github/workflows/presentation-export.yml`) runs on
pull requests and pushes to `main` that change presentation sources, the site
build or packaging script or the workflow, and on manual dispatch. It exports
and verifies every deck, packages the release groups, and uploads the HTML site
and `exports/releases/` as one artifact named `presentations-<commit SHA>`.
On pull request runs that SHA is GitHub's test merge commit, not the branch
head, so take release deliverables from the run on `main` or from a manual
dispatch. The artifact is kept for 30 days and serves CI review only.

### Publishing a version

`scripts/package_presentations.py` writes one directory per `release` value
in the registry. Each holds every deck of that group in all three formats,
`presentation-manifest.json` and `SHA256SUMS`. The manifest records the source
commit, workflow run, tool versions, and for each deck its event, round,
language, source file and SHA-256, slide and PDF page counts, metrics snapshot
when the deck uses one, and the latest-HTML URL, which is labelled as following
`main`.

To publish:

1. Take the artifact from the `main` run (or a manual dispatch) of the commit you approve.
2. Inspect the PDF, PPTX and unzipped HTML visually.
3. Create a **new** prerelease tag named `<release>-<YYYY-MM-DD>` and upload the
   files of `releases/<release>/` unchanged. Never replace the assets of an
   existing release.
4. Link the release from the event README and the root README.

The HTML ZIP is the version-pinned HTML. Unzip it and serve the folder with any
static server (for example `python3 -m http.server`). Browsers block the deck's
scripts when `index.html` is opened directly from disk. The public Pages URLs
always show the latest `main`, so they can differ from a frozen release.

Releases made before this script existed use the older manifest format
(schema version 1). Their HTML ZIPs were built later from the same source
commit and added with a separate `HTML_SHA256SUMS`:
[`ossdevcon-2026-presentation-2026-10-25`](https://github.com/cubrid-lab/showcase/releases/tag/ossdevcon-2026-presentation-2026-10-25)
and [`builder-season4-validation-2026-10-28`](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-28).

### PPTX format

The default PPTX export uses an image per slide for visual consistency, with
speaker notes as text. It is suitable for presenting and reviewing, but slide
text and shapes are not directly editable; web interactions and animations
become static. If native PowerPoint editing is needed, evaluate Slidev's
`--format pptx-editable` export as a separate output and review its layout by
hand. See the [official export guide](https://sli.dev/guide/exporting). Export
success does not replace visual inspection of the PDF and PPTX.

## Builder Season 4 first validation: local preview

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
hosting subpath; publishing is a separate step. For an existing browser, append
`-- --executable-path /path/to/chrome` to an export command. Slidev also
provides a browser export screen in the dev server.

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

- `decks/` — Narrative + speaker notes for each deck (Slidev Markdown)
- `2026-*.md` — Thin Slidev entries, one per deck and language
- `deck.json` — Points to the active metrics snapshot
- `snapshots/*.json` — Immutable metrics snapshots with provenance
- `references.json` — Evidence mapping for claims
- `components/` — Vue components for metrics display + evidence

## Workflow

1. Edit the deck source under `decks/` for narrative changes
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
