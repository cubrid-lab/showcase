# Metrics Snapshot — 2026-09-12

> Re-measure on presentation day using the commands in the main repo.

## Ecosystem Totals

| Metric | pycubrid | sqlalchemy-cubrid | cubrid-mcp-server | cubrid-cookbook | **Total** |
|---|---:|---:|---:|---:|---:|
| GitHub stars | 27 | 34 | 27 | 23 | **111** |
| Merged PRs | 159 | 151 | 84 | 56 | **450** |
| Unique clones (14d) | 305 | 225 | 198 | 94 | **822** |
| PyPI releases | 16 | 19 | — | — | **35** |
| Tests | 1,147 | 769 | 284 | — | **2,200** |
| Docs pages | 20 | 14 | 7 | 22 | **63** |
| Korean docs | 13 | 14 | 5+ko | 2 | **34** |

## Performance Optimizations

| Optimization | Result |
|---|---|
| Native ping (CHECK_CAS) | +280% throughput |
| SA pool_pre_ping | +588% throughput |
| Bulk insert (1000 rows) | 12.3% faster |
| Query select-all | 19.9% faster |

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
| Security | CodeQL, Dependabot, audit logging |

## Features

| Feature | Count |
|---|---|
| MCP tools | 12 (11 read + 1 opt-in write) |
| MCP skill resources | 7 (2 schema + 5 domain knowledge) |
| MCP prompts | 9 (4 basic + 5 expert workflows) |
| Cookbook examples | 75 |
| Application templates | 7 (FastAPI, Flask, Django, Streamlit, Celery, ETL, AI agent) |
| Golden-verified examples | 45 (CI on 11.2 + 11.4) |
| Supported CUBRID versions | 10.2, 11.0, 11.2, 11.4 |
| Supported Python versions | 3.10, 3.11, 3.12, 3.13, 3.14 |

## Licensing

All 4 repos: MIT. THIRD_PARTY_LICENSES.md + NOTICE in every repo.
SPDX SBOM attached to releases. No GPL dependencies.

## Documentation

4 mkdocs-material sites (six-tab unified IA), all live:
- cubrid-lab.github.io/pycubrid/
- cubrid-lab.github.io/sqlalchemy-cubrid/
- cubrid-lab.github.io/cubrid-mcp-server/
- cubrid-lab.github.io/cubrid-cookbook-python/

## ⚠️ PyPI Download Caveat

Our CI (cookbook smoke + integration tests) generates ~20-50 downloads/day.
Use "GitHub unique clones" (822/14d) as the primary adoption metric —
GitHub Actions' `actions/checkout` uses tarball API and is automatically
excluded from clone statistics.

## Re-measurement Commands

```bash
# Stars + PRs
for r in pycubrid sqlalchemy-cubrid cubrid-mcp-server cubrid-cookbook-python; do
  gh repo view cubrid-lab/$r --json stargazerCount --jq .stargazerCount
  gh pr list -R cubrid-lab/$r --state merged --limit 1000 --json number --jq 'length'
done

# Unique clones (14d)
gh api "repos/cubrid-lab/$r/traffic/clones?per=week" --jq '.uniques'

# PyPI releases
curl -s "https://pypi.org/pypi/pycubrid/json" | jq '.releases | length'
```
