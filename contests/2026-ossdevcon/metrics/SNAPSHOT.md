# Metrics Snapshot — 2026-09-12

> Re-measure on presentation day. Commands at bottom.

## Ecosystem Totals

| Metric | pycubrid | sqlalchemy-cubrid | cubrid-mcp-server | cubrid-cookbook | **Total** |
|---|---:|---:|---:|---:|---:|
| GitHub stars | 29 | 36 | 29 | 25 | **119** |
| Merged PRs | 159 | 151 | 84 | 56 | **450** |
| Unique clones (14d, per-repo, **CI-dominated**)¹ | 363 | 268 | ~200 | ~95 | ~926² |
| PyPI releases | 16 | 19 | — | — | **35** |
| Tests | 1,147 | 769 | 284 | — | **2,200** |
| Docs pages | 20 | 14 | 7 | 22 | **63** |
| Korean docs | 13 | 14 | 5+ko | 2 | **34** |

## Quality Gates

| Gate | Value |
|---|---|
| CI matrix (live DB) | Python 5 × CUBRID 4 = **20 combinations** |
| CI matrix (offline) | (Ubuntu + macOS) × Python 5 = **10 combinations** |
| Coverage floor | **95%** (CI-enforced) |
| Type safety | mypy strict, **0 errors** |
| API compatibility | api-baseline.json gate |
| SQLAlchemy suite | Official test suite integrated |
| SBOM | SPDX on every GitHub Release |

## Performance

| Optimization | Result |
|---|---|
| Native ping (CHECK_CAS) | **+280% throughput** |
| SA pool_pre_ping | **+588% throughput** |
| Bulk insert (1000 rows) | **12.3% faster** |
| Query select-all | **19.9% faster** |

¹ Per-repo unique clones reported by GitHub Traffic API individually. Mostly CI
  runners — see "Clone traffic is CI" below. Not used as an adoption metric.
² Sum of per-repo figures; the same person cloning multiple repos is counted
  once per repo, so cross-repo overlap is **not removed** from this total.

## ⚠️ Clone traffic is CI (measured 2026-09-27)

`actions/checkout` does a real git fetch and each hosted runner is a distinct
cloner, so clone counts track CI activity, not users. (An earlier version of
this file claimed CI was excluded; that was wrong.)

| Repo | Unique cloners (14d) | Total clones (14d) | CI workflow runs (14d) |
|---|---:|---:|---:|
| pycubrid | 495 | 4,969 | 700 |
| sqlalchemy-cubrid | 547 | 5,742 | 1,103 |
| cubrid-mcp-server | 277 | 1,493 | 96 |
| cubrid-cookbook-python | 184 | 1,018 | 335 |

PyPI downloads also include CI (~20-50/day). For adoption, cite merged PRs,
releases, and stars.

```bash
# CI runs in the same 14-day window
gh api "repos/cubrid-lab/$r/actions/runs?created=>=$(date -u -d '14 days ago' +%F)&per_page=1" --jq .total_count
```

## Re-measurement Commands

```bash
# Stars + PRs
for r in pycubrid sqlalchemy-cubrid cubrid-mcp-server cubrid-cookbook-python; do
  gh repo view cubrid-lab/$r --json stargazerCount --jq .stargazerCount
  gh pr list -R cubrid-lab/$r --state merged --limit 1000 --json number --jq 'length'
done

# Unique clones (14d)
gh api "repos/cubrid-lab/$r/traffic/clones?per=week" --jq '.uniques'

# PyPI
curl -s "https://pypistats.org/api/packages/pycubrid/recent" | jq '.data'
```
