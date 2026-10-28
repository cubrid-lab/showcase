# Benchmark Rerun — 2026-10-28

> New measurement for [issue #95](https://github.com/cubrid-lab/showcase/issues/95).
> It repeats the method of the [2026-10-25 rerun](../benchmark-2026-10-25/README.md) with the
> current pycubrid release and does not change that record. It does **not** replace the
> historical numbers in the deck and in [APPENDIX.md section B](../../APPENDIX.md#b-performance-data).
> Those were measured with other driver versions, another CUBRID version and other
> workloads, and are not comparable with this run.

Two existing harnesses from
[cubrid-lab/cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark) were run
unmodified from a clean checkout of `main` at
[`831d495403a934b3c6bb2c2a2485e77bc0423dbb`](https://github.com/cubrid-lab/cubrid-benchmark/tree/831d495403a934b3c6bb2c2a2485e77bc0423dbb),
against one local CUBRID 11.4 container. Since the 2026-10-25 checkout (`b002085`), that
repository changed only documentation (`AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md`,
`README.md`); the harness files below have the same SHA-256 as on 2026-10-25.

1. **Driver baseline** —
   [`experiments/pycubrid-release-baseline`](https://github.com/cubrid-lab/cubrid-benchmark/tree/831d495403a934b3c6bb2c2a2485e77bc0423dbb/experiments/pycubrid-release-baseline):
   pycubrid against the official `CUBRIDdb` C driver on the same server, plus pycubrid
   1.10.0 for release-to-release continuity. Raw output: [`driver-baseline/`](driver-baseline/).
2. **Tier 1 workload** —
   [`experiments/tier1-python-workload`](https://github.com/cubrid-lab/cubrid-benchmark/tree/831d495403a934b3c6bb2c2a2485e77bc0423dbb/experiments/tier1-python-workload):
   the five scenarios named in the historical table (`insert_sequential`, `select_by_pk`,
   `select_full_scan`, `update_indexed`, `delete_sequential`), pycubrid only. Raw output:
   [`tier1/`](tier1/).

## Slide summary: pycubrid time relative to CUBRIDdb = 100

The three numbers used on the performance slide. Each is the pooled-median ratio
pycubrid ÷ CUBRIDdb from the `pycubrid main vs CUBRIDdb` table of
[`derived/summary.md`](driver-baseline/derived/summary.md), multiplied by 100 and rounded,
exactly as the 2026-10-25 values (1.118 → 112, 1.249 → 125, 1.197 → 120) were derived.
Higher means pycubrid takes longer.

| Operation | 2026-10-28, pycubrid 1.15.0 | ratio (95% CI) | 2026-10-25, pycubrid 1.13.5 |
|---|---:|---|---:|
| SELECT by primary key (execute + fetchone) | **104** | 1.037 (1.025–1.048) | 112 |
| `fetchall`, 10,000 rows | **117** | 1.173 (1.155–1.186) | 125 |
| `executemany` 10,000 rows + commit | **104** | 1.044 (0.965–1.197) | 120 |

The `executemany` confidence interval includes 1.0: in this run that case cannot tell
pycubrid apart from CUBRIDdb with confidence. The PK lookup and `fetchall` intervals do not
include 1.0.

## Run metadata

| Item | Value |
|---|---|
| Date (UTC) | Driver baseline 2026-10-28 13:39:38Z – 14:42:14Z; Tier 1 2026-10-28 14:43:12Z – 14:57:18Z |
| Host | Intel Core i5-9400F @ 2.90 GHz, 6 cores (1 thread per core), 31 GiB RAM, x86_64 (same machine as 2026-10-25) |
| OS | Ubuntu 22.04.5 LTS, Linux 5.15.0-198-generic |
| Docker | 29.2.1, container port 33000 published on `127.0.0.1:33951` |
| CUBRID | 11.4.6 (`11.4.6.1963-0e7d3c1`, `cubrid_rel`), image `cubrid/cubrid:11.4` `sha256:1248b77ad39888df9e064655937188ab99fe056ed7e35b57d06155a015dc1791` (same digest as 2026-10-25), database `testdb`, default broker (`MAX_NUM_APPL_SERVER=40`) |
| Python | CPython 3.12.13 (uv 0.11.7 venvs, one per driver) |
| pycubrid (current) | 1.15.0 from PyPI, the latest release on the run date (tag `v1.15.0` = `838620b5817648bd96975409fb39a6611f418c7a`) |
| pycubrid (continuity) | 1.10.0 from PyPI (tag `v1.10.0` = `d383be79e55a5f164b2569a0edb44eace9bb7e50`) |
| CUBRIDdb | CUBRID/cubrid-python tag `v11.3.0.51` (`c63ab9c51353e5c80e02dd2c1a19d4640acb29f5`, cci-src `7d1eb8f40f04089b8218d08e36e2c24a2de11b24`), built from source with GCC 11.4.0 and CMake 3.22.1 as in the harness README; dist name `cubrid-python 11.3.0.1` |
| Tier 1 tools | pytest 9.1.1 (pinned, see [Deviations](#deviations-from-the-2026-10-25-method)), pytest-benchmark 5.3.0 (SQLAlchemy 2.1.6 and sqlalchemy-cubrid 1.12.1 were installed from `python/requirements.txt` but not used by these benchmarks) |
| Harness file SHA-256 | `scripts/driver_baseline_bench.py` `99d370ef76dfbd36066c9cf75efda394f5ea2cb2e90296c1cbc784124055bb74`; `experiments/pycubrid-release-baseline/run.sh` `15f0b05ce2ba2f00c408e60a11c59e6913a1b4f167d556c01b520fd0c6223e3b`; `python/bench_pycubrid.py` `bc9b734fc5fd953fb3debd203925b09711d9dd0d5d8ccb60dcd620842ab88c1f` (workload revision `tier1-explicit-keys-v2`); also recorded: `scripts/summarize_driver_baseline.py` `de9b847eaa6231b8131cf75496c819e67b11e7be5e19deb1b392828cf8b86fda`, `experiments/tier1-python-workload/cubrid_only_plugin.py` `0f6d25f414357884d59175ac591c8b549a35316a3843108b5bc3da77044ae75e` ([`env/harness.sha256`](env/harness.sha256)) |
| Installed packages | [`env/`](env/) (`uv pip freeze` of each venv; [`env/run.txt`](env/run.txt) and [`env/host.txt`](env/host.txt) hold the version strings and host details) |
| Host load | **Shared host**: 16 logged-in users and a 1-minute load average of 2.2–14.8 on 6 cores during the driver baseline, 3.4–12.8 during Tier 1 ([driver](driver-baseline/raw/loadavg.log), [Tier 1](tier1/raw/loadavg.log)). Lighter than on 2026-10-25 (6–25), but still noisy. |

The server container was created for this run and removed afterwards. Before the
measurement it served one `--quick` smoke run of each driver (tables created and dropped).

## Commands

```bash
# cubrid-benchmark clean checkout at 831d495403a934b3c6bb2c2a2485e77bc0423dbb
docker run -d --name showcase95-bench-cubrid114 -e CUBRID_DB=testdb \
  -p 127.0.0.1:33951:33000 cubrid/cubrid:11.4

uv venv -p 3.12 venv-1150 && uv pip install -p venv-1150/bin/python pycubrid==1.15.0
uv venv -p 3.12 venv-1100 && uv pip install -p venv-1100/bin/python pycubrid==1.10.0
git clone --branch v11.3.0.51 --depth 1 --recurse-submodules \
  https://github.com/CUBRID/cubrid-python.git cubrid-python
(cd cubrid-python/cci-src && mkdir -p build_x86_64_release && cd build_x86_64_release \
  && cmake ../ && make -j3)
printf '#!/bin/bash\nexit 0\n' > cubrid-python/build_cci.sh
uv venv -p 3.12 venv-cubriddb && uv pip install -p venv-cubriddb/bin/python setuptools ./cubrid-python

# 1. Driver baseline: 5 trials per driver, driver order rotated every trial
PATH=$PWD/venv-1150/bin:$PATH CUBRID_PORT=33951 \
PY_MAIN=$PWD/venv-1150/bin/python PY_REL=$PWD/venv-1100/bin/python \
PY_CUBRIDDB=$PWD/venv-cubriddb/bin/python \
MAIN_SHA="pypi:1.15.0 (tag v1.15.0 = 838620b5817648bd96975409fb39a6611f418c7a)" \
CUBRIDDB_SHA="c63ab9c51353e5c80e02dd2c1a19d4640acb29f5 (cci-src 7d1eb8f40f04089b8218d08e36e2c24a2de11b24)" \
experiments/pycubrid-release-baseline/run.sh <run-dir> 5

# 2. Tier 1: 3 back-to-back trials (pytest pinned to the 2026-10-25 version)
uv venv -p 3.12 venv-tier1 && uv pip install -p venv-tier1/bin/python \
  -r python/requirements.txt pycubrid==1.15.0 pytest==9.1.1
cd python && for t in 1 2 3; do
  CUBRID_PORT=33951 CUBRID_DB=testdb PYTHONPATH=../experiments/tier1-python-workload \
    ../venv-tier1/bin/python -m pytest --noconftest -p cubrid_only_plugin bench_pycubrid.py \
    --benchmark-json=<run-dir>/raw/cubrid114_t$t.json -v
done
```

`run.sh` hard-codes its label for the current driver as `pycubrid-main`. In this run that
label is **pycubrid 1.15.0 from PyPI**, not a `main` checkout; the raw JSON records the
installed version (`metadata.driver.version`) and the commit string above. Wherever
`derived/summary.md` says "main", read "1.15.0".

## Deviations from the 2026-10-25 method

- **pytest pinned to 9.1.1 for Tier 1.** `python/requirements.txt` only asks for
  `pytest>=8.0`, so the first Tier 1 attempt installed pytest 9.2.0, released after the
  2026-10-25 run. pytest-benchmark 5.3.0 fails with it before any timing
  (`AttributeError: 'Function' object has no attribute '_nodeid'` in
  `pytest_benchmark/fixture.py`; all 5 tests errored in 0.13 s, nothing was measured; log:
  [`tier1/failed-attempt-pytest-9.2.0.log`](tier1/failed-attempt-pytest-9.2.0.log)). Tier 1
  was rerun from a fresh venv with `pytest==9.1.1`, the version used on 2026-10-25. No
  harness file was changed.
- sqlalchemy-cubrid resolved to 1.12.1 instead of 1.11.7 (unpinned in `requirements.txt`);
  it is not used by these benchmarks.
- Different host port (33951 instead of 33650) and container name. Nothing else differs.

## Method and aggregation

**Driver baseline** (`driver-baseline/`). Every connection uses `autocommit=False`
(pycubrid `connect(autocommit=False)`, CUBRIDdb its setter) and writes commit explicitly.
The server holds 10,000 rows of `(INT PK, VARCHAR(100), VARCHAR(200), INT)`. Each driver ran
5 trials, with the driver order rotated every trial; warm-up iterations are discarded and
every measured iteration is checked for the right row counts and values. Times are
milliseconds per operation, timed with `time.perf_counter_ns()`. Samples of all trials are
pooled per driver, and the report gives the pooled median, p95, IQR and the range of the
per-trial medians. The ratio is pycubrid median ÷ CUBRIDdb median (>1 means pycubrid is
slower), with a bootstrap 95% confidence interval. The full output is
[`derived/summary.md`](driver-baseline/derived/summary.md), generated by the harness's
`scripts/summarize_driver_baseline.py` from [`raw/`](driver-baseline/raw/).

**Tier 1** (`tier1/`). pytest-benchmark pedantic mode: per trial, 1 warm-up round and 5
measured rounds per scenario, 1 iteration per round. An untimed setup rebuilds the table with
explicit keys 1–10,000 before every round, and an untimed teardown verifies every row and row
count; all 15 runs passed. The timed region is the measured statements plus, for writes, one
final `commit()`. The table reports, as the experiment's README does, the median of the three
per-trial median round times, in seconds, and rows per second at that median.

## Results: pycubrid 1.15.0 against CUBRIDdb, same server

Pooled medians, milliseconds per operation (lower is faster).

| Operation | pycubrid 1.15.0 | CUBRIDdb (C, CCI) | pycubrid ÷ CUBRIDdb | 95% CI |
|---|---:|---:|---:|---|
| connect + close | 1.709 | 1.196 | 1.43× | 1.40–1.46 |
| SELECT by primary key (execute + fetchone) | 0.735 | 0.709 | 1.04× | 1.03–1.05 |
| `fetchall`, 10,000 rows | 48.7 | 41.5 | 1.17× | 1.16–1.19 |
| `fetchmany(100)` loop, 10,000 rows | 48.3 | 41.6 | 1.16× | 1.13–1.18 |
| `executemany` 10,000 rows + commit | 3,772 | 3,612 | 1.04× | 0.97–1.20 |
| `executemany` 1,000 rows + commit | 417 | 432 | 0.97× | 0.87–1.11 |
| INSERT 1 row, execute only | 5.41 | 4.69 | 1.15× | 1.02–1.27 |

Single-row writes with `commit()` measured 42–50 ms at the median for every driver, close to
the 33–41 ms recorded on 2026-10-11 and far below the 120–184 ms of 2026-10-25. They remain
commit-bound and are not used as a driver comparison here. The execute-only single-row
phases are 3.5–6.5 ms at the median for every driver (1.2–1.5 ms on 2026-10-25), with very
wide IQRs (about 2–5 ms) and per-trial medians from about 1.1 to 7.0 ms, so those cases are
noisy in this run; see `derived/summary.md` for the full table.

**Concurrency** (SELECT by PK, one connection per worker): with 8 workers pycubrid sync
threads reached 4,533 queries/s and `pycubrid.aio` tasks 3,958 queries/s, against 747 for
CUBRIDdb threads; with 32 workers 4,339, 4,127 and 825.

**pycubrid 1.15.0 against 1.10.0**: the harness's regression rule (median more than 5%
slower *and* non-overlapping IQRs) found **no regression** in any case, including the six
concurrency cases. The rule can only detect slowdowns of roughly 5–8% for the fetch cases, 26–30% for `executemany` of 10,000 rows,
22–94% for connects and the PK lookup, and far more for single-row commits and execute-only
phases (the `min detectable` column).

## Results: Tier 1 workload, pycubrid 1.15.0

| Scenario | Rows per round | Per-trial median round (s) | Median (s) | Rows/s at median |
|---|---:|---|---:|---:|
| insert_sequential | 10,000 | 7.530 / 7.308 / 6.948 | 7.308 | 1,368 |
| select_by_pk | 10,000 | 7.208 / 7.472 / 6.402 | 7.208 | 1,387 |
| select_full_scan | 10,000 | 0.0406 / 0.0345 / 0.0357 | 0.0357 | 281,000 |
| update_indexed | 1,000 | 0.763 / 0.686 / 0.605 | 0.686 | 1,458 |
| delete_sequential | 1,000 | 0.761 / 0.638 / 0.624 | 0.638 | 1,568 |

This uses the corrected `tier1-explicit-keys-v2` workload. The historical table in
APPENDIX.md section B came from the earlier workload, whose SELECT/UPDATE/DELETE rounds
addressed keys that no longer existed and whose rounds also timed the re-seed (see the
experiment's README), so the two tables measure different quantities and must not be
compared. There is no CUBRIDdb counterpart in this harness, and no PyMySQL/MySQL run was
made: a comparison across database engines mixes server differences with driver overhead.

## Known limitations

- One shared machine, under lighter load than on 2026-10-25. Medians and ratios between
  drivers measured in the same rotated trials are the robust part; absolute times are not.
  The change from the 2026-10-25 ratios mixes the driver change (1.13.5 → 1.15.0) with the
  different host load, so the size of the improvement cannot be attributed to the driver
  alone from these two runs.
- One server container, one host, localhost networking. No other CUBRID version was run.
- The deck's historical optimization rows (native ping, `pool_pre_ping`, bulk insert,
  select-all, fetch) were not rerun: their source harness and run are not recorded.
