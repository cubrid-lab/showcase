# Scripts

## collect_snapshot.py

Collects current metrics from the 4 cubrid-lab repos and saves a dated JSON snapshot.

### Prerequisites

- `gh` CLI authenticated (`gh auth login`)
- `GITHUB_TOKEN` with `repo` scope (for traffic API / unique clones)
- `curl` (for PyPI API)

### Usage

```bash
python scripts/collect_snapshot.py
```

### Output

Creates `presentation/snapshots/YYYY-MM-DD.json` with:
- Per-repo and total metrics (stars, PRs, clones, PyPI releases)
- Provenance fields (source, period, collection timestamp)
- Stale flags for any failed API calls (never replaces real values with 0)

### Notes

- Does not overwrite existing snapshots (appends timestamp if date exists)
- Clone data requires push access to each repo
- PyPI download counts are not collected (CI-inflated, not reliable as adoption metric)
