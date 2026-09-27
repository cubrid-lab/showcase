# Metrics Snapshot — 2026-09-12

> Re-measure on presentation day. Commands at bottom.

## Ecosystem Totals

| Metric | pycubrid | sqlalchemy-cubrid | cubrid-mcp-server | cubrid-cookbook | **Total** |
|---|---:|---:|---:|---:|---:|
| GitHub stars | 29 | 36 | 29 | 25 | **119** |
| Merged PRs | 159 | 151 | 84 | 56 | **450** |
| Unique clones (14d) | 363 | 268 | ~200 | ~95 | **~926** |
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

## ⚠️ PyPI Download Caveat

Our CI generates ~20-50 downloads/day. Use "GitHub unique clones" (926/14d)
as the primary adoption metric — GitHub Actions' checkout is excluded.

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
