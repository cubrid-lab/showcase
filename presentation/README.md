# Presentation — CUBRID Python Ecosystem

Slidev-based presentation for the 2026 OSS Developer Contest Finals.

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
