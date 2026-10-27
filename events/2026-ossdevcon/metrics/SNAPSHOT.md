# Metrics Snapshot — 2026-10-25

> Repository metrics and current release versions were re-measured on 2026-10-25.
> Re-measure once more immediately before the final presentation.

## Ecosystem Totals

| Metric | pycubrid | sqlalchemy-cubrid | cubrid-mcp-server | cubrid-cookbook | **Total** |
|---|---:|---:|---:|---:|---:|
| GitHub stars | 31 | 38 | 32 | 28 | **129** |
| Merged PRs | 537 | 529 | 236 | 251 | **1,553** |
| Published GitHub Releases | 29 | 23 | 9 | — | **61** |
| Current release | v1.13.3 | v1.11.5 | v0.5.4 | — | — |

Sources: GitHub REST/Search/Releases APIs, measured 2026-10-25.

## Why there is no single test-count total anymore

The old 2026-09-12 snapshot summed three fixed pytest counts into **2,200 tests**.
That is no longer a stable apples-to-apples metric: the repositories now use
different parameterized suites, offline/live lanes, integration matrices and
result-reporting contracts. A selected-test count can change with the workflow
without changing product quality.

For the presentation, cite the enforced gates instead:

- repository-local test suites must pass before merge;
- pycubrid, sqlalchemy-cubrid and cubrid-mcp-server enforce a **95% coverage floor**;
- driver/dialect validation includes live CUBRID integration matrices;
- sqlalchemy-cubrid includes the official SQLAlchemy dialect suite;
- cookbook live verification records PASS/FAIL/INCOMPLETE evidence by lane.

Do not revive a fixed ecosystem-wide test total unless it is redefined with one
consistent collection method across all four repositories.

## Adoption metric policy

Clone traffic and PyPI downloads remain useful operational signals but are not
presented as unique-user adoption metrics because project CI can generate both.

The presentation uses three auditable repository metrics:

1. GitHub stars
2. merged PRs
3. published GitHub Releases

Cookbook has no package release count, so the release chart intentionally omits it.

## Historical clone traffic — 2026-09-27 only

These figures are retained only to explain why clone traffic is excluded from
the adoption slide.

| Repo | Unique cloners (14d) | Total clones (14d) | CI workflow runs (14d) |
|---|---:|---:|---:|
| pycubrid | 495 | 4,969 | 700 |
| sqlalchemy-cubrid | 547 | 5,742 | 1,103 |
| cubrid-mcp-server | 277 | 1,493 | 96 |
| cubrid-cookbook-python | 184 | 1,018 | 335 |

## Performance evidence retained from the benchmark snapshot

| Optimization | Result |
|---|---|
| Native ping (CHECK_CAS) | **+280% throughput** |
| SA pool_pre_ping | **+588% throughput** |
| Bulk insert (1000 rows) | **12.3% faster** |
| Query select-all | **19.9% faster** |

These benchmark numbers were not re-run during this documentation refresh.
Keep the benchmark environment and reproduction instructions attached whenever
they are quoted.

## Re-measurement commands

```bash
for r in pycubrid sqlalchemy-cubrid cubrid-mcp-server cubrid-cookbook-python; do
  gh repo view cubrid-lab/$r --json stargazerCount --jq .stargazerCount
  gh api "search/issues?q=repo:cubrid-lab/$r+is:pr+is:merged&per_page=1" --jq .total_count
done

for r in pycubrid sqlalchemy-cubrid cubrid-mcp-server; do
  gh api "repos/cubrid-lab/$r/releases?per_page=100" \
    --jq '[.[] | select(.draft == false and .published_at != null)] | length'
  gh api "repos/cubrid-lab/$r/releases/latest" --jq .tag_name
done
```

Historical baseline: [2026-09-12](../../../presentation/snapshots/2026-09-12.json).
Current presentation snapshot: [2026-10-25](../../../presentation/snapshots/2026-10-25.json).
