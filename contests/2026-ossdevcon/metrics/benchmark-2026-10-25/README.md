# Benchmark Rerun — 2026-10-25

> New measurement for [issue #44](https://github.com/cubrid-lab/showcase/issues/44).
> It does **not** replace the historical numbers in the deck and in
> [APPENDIX.md section B](../../APPENDIX.md#b-performance-data). Those were measured with
> other driver versions, another CUBRID version and other workloads, and are not
> comparable with this run.

Two existing harnesses from
[cubrid-lab/cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark) were run
unmodified from a clean checkout of `main` at
[`b002085822054fdd48075a97b52c75921a73fda3`](https://github.com/cubrid-lab/cubrid-benchmark/tree/b002085822054fdd48075a97b52c75921a73fda3),
against one local CUBRID 11.4 container:

1. **Driver baseline** —
   [`experiments/pycubrid-release-baseline`](https://github.com/cubrid-lab/cubrid-benchmark/tree/b002085822054fdd48075a97b52c75921a73fda3/experiments/pycubrid-release-baseline):
   pycubrid against the official `CUBRIDdb` C driver on the same server, plus pycubrid
   1.10.0 for release-to-release continuity. Raw output: [`driver-baseline/`](driver-baseline/).
2. **Tier 1 workload** —
   [`experiments/tier1-python-workload`](https://github.com/cubrid-lab/cubrid-benchmark/tree/b002085822054fdd48075a97b52c75921a73fda3/experiments/tier1-python-workload):
   the five scenarios named in the historical table (`insert_sequential`, `select_by_pk`,
   `select_full_scan`, `update_indexed`, `delete_sequential`), pycubrid only. Raw output:
   [`tier1/`](tier1/).

## Run metadata

| Item | Value |
|---|---|
| Date (UTC) | Driver baseline 2026-10-25 08:15:23Z – 09:58:22Z; Tier 1 2026-10-25 09:58:45Z – 10:15:52Z |
| Host | Intel Core i5-9400F @ 2.90 GHz, 6 cores (1 thread per core), 31 GiB RAM, x86_64 |
| OS | Ubuntu 22.04.5 LTS, Linux 5.15.0-198-generic |
| Docker | 29.2.1, container port 33000 published on `127.0.0.1:33650` |
| CUBRID | 11.4.6 (`11.4.6.1963-0e7d3c1`, `cubrid_rel`), image `cubrid/cubrid:11.4` `sha256:1248b77ad39888df9e064655937188ab99fe056ed7e35b57d06155a015dc1791`, database `testdb`, default broker (`MAX_NUM_APPL_SERVER=40`) |
| Python | CPython 3.12.13 (uv 0.11.7 venvs, one per driver) |
| pycubrid (current) | 1.13.5 from PyPI (tag `v1.13.5` = `35ea9198094787893e7cbd967c1abca4577810dd`) |
| pycubrid (continuity) | 1.10.0 from PyPI (tag `v1.10.0` = `d383be79e55a5f164b2569a0edb44eace9bb7e50`) |
| CUBRIDdb | CUBRID/cubrid-python tag `v11.3.0.51` (`c63ab9c51353e5c80e02dd2c1a19d4640acb29f5`, cci-src `7d1eb8f40f04089b8218d08e36e2c24a2de11b24`), built from source with GCC 11.4.0 and CMake 3.22.1 as in the harness README; dist name `cubrid-python 11.3.0.1` |
| Tier 1 tools | pytest 9.1.1, pytest-benchmark 5.3.0 (SQLAlchemy 2.1.6 and sqlalchemy-cubrid 1.11.7 were installed from `python/requirements.txt` but not used by these benchmarks) |
| Harness file SHA-256 | `scripts/driver_baseline_bench.py` `99d370ef76dfbd36066c9cf75efda394f5ea2cb2e90296c1cbc784124055bb74`; `experiments/pycubrid-release-baseline/run.sh` `15f0b05ce2ba2f00c408e60a11c59e6913a1b4f167d556c01b520fd0c6223e3b`; `python/bench_pycubrid.py` `bc9b734fc5fd953fb3debd203925b09711d9dd0d5d8ccb60dcd620842ab88c1f` (workload revision `tier1-explicit-keys-v2`) |
| Installed packages | [`env/`](env/) (`uv pip freeze` of each venv) |
| Host load | **Shared, heavily loaded host**: 16–19 logged-in users and a 1-minute load average of 6–25 on 6 cores during the run ([driver](driver-baseline/raw/loadavg.log), [Tier 1](tier1/raw/loadavg.log)). Treat the absolute times as noisy. |

The server container was created for this run and removed afterwards. Before the
measurement it served one `--quick` smoke run of each driver (tables created and dropped).

## Commands

```bash
# cubrid-benchmark clean checkout at b002085822054fdd48075a97b52c75921a73fda3
docker run -d --name showcase44-bench-cubrid114 -e CUBRID_DB=testdb \
  -p 127.0.0.1:33650:33000 cubrid/cubrid:11.4

uv venv -p 3.12 venv-1135 && uv pip install -p venv-1135/bin/python pycubrid==1.13.5
uv venv -p 3.12 venv-1100 && uv pip install -p venv-1100/bin/python pycubrid==1.10.0
git clone --branch v11.3.0.51 --depth 1 --recurse-submodules \
  https://github.com/CUBRID/cubrid-python.git cubrid-python
(cd cubrid-python/cci-src && mkdir -p build_x86_64_release && cd build_x86_64_release \
  && cmake ../ && make -j3)
printf '#!/bin/bash\nexit 0\n' > cubrid-python/build_cci.sh
uv venv -p 3.12 venv-cubriddb && uv pip install -p venv-cubriddb/bin/python setuptools ./cubrid-python

# 1. Driver baseline: 5 trials per driver, driver order rotated every trial
PATH=$PWD/venv-1135/bin:$PATH CUBRID_PORT=33650 \
PY_MAIN=$PWD/venv-1135/bin/python PY_REL=$PWD/venv-1100/bin/python \
PY_CUBRIDDB=$PWD/venv-cubriddb/bin/python \
MAIN_SHA="pypi:1.13.5 (tag v1.13.5 = 35ea9198094787893e7cbd967c1abca4577810dd)" \
CUBRIDDB_SHA="c63ab9c51353e5c80e02dd2c1a19d4640acb29f5 (cci-src 7d1eb8f40f04089b8218d08e36e2c24a2de11b24)" \
experiments/pycubrid-release-baseline/run.sh <run-dir> 5

# 2. Tier 1: 3 back-to-back trials
uv venv -p 3.12 venv-tier1 && uv pip install -p venv-tier1/bin/python \
  -r python/requirements.txt pycubrid==1.13.5
cd python && for t in 1 2 3; do
  CUBRID_PORT=33650 CUBRID_DB=testdb PYTHONPATH=../experiments/tier1-python-workload \
    ../venv-tier1/bin/python -m pytest --noconftest -p cubrid_only_plugin bench_pycubrid.py \
    --benchmark-json=<run-dir>/raw/cubrid114_t$t.json -v
done
```

`run.sh` hard-codes its label for the current driver as `pycubrid-main`. In this run that
label is **pycubrid 1.13.5 from PyPI**, not a `main` checkout; the raw JSON records the
installed version (`metadata.driver.version`) and the commit string above. Wherever
`derived/summary.md` says "main", read "1.13.5".

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

## Results: pycubrid 1.13.5 against CUBRIDdb, same server

Pooled medians, milliseconds per operation (lower is faster).

| Operation | pycubrid 1.13.5 | CUBRIDdb (C, CCI) | pycubrid ÷ CUBRIDdb | 95% CI |
|---|---:|---:|---:|---|
| connect + close | 2.107 | 1.509 | 1.40× | 1.37–1.42 |
| SELECT by primary key (execute + fetchone) | 0.836 | 0.748 | 1.12× | 1.11–1.13 |
| `fetchall`, 10,000 rows | 51.3 | 41.1 | 1.25× | 1.22–1.30 |
| `fetchmany(100)` loop, 10,000 rows | 50.4 | 43.4 | 1.16× | 1.14–1.20 |
| `executemany` 10,000 rows + commit | 3,899 | 3,258 | 1.20× | 1.12–1.36 |
| `executemany` 1,000 rows + commit | 527 | 458 | 1.15× | 1.05–1.29 |
| INSERT 1 row, execute only | 1.51 | 1.20 | 1.26× | 1.25–1.28 |

Single-row writes with `commit()` measured 120–184 ms at the median for every driver, far
above the 33–41 ms recorded for the same harness on 2026-10-11. On this loaded host the
server commit dominates them, and they are not used as a driver comparison here; see
`derived/summary.md` for the full table.

**Concurrency** (SELECT by PK, one connection per worker): with 8 workers pycubrid sync
threads reached 2,906 queries/s and `pycubrid.aio` tasks 2,005 queries/s, against 995 for
CUBRIDdb threads; with 32 workers 3,201, 2,705 and 1,016.

**pycubrid 1.13.5 against 1.10.0**: the harness's regression rule (median more than 5%
slower *and* non-overlapping IQRs) found **no regression** in any case. On this loaded
host the rule can only detect slowdowns of roughly 15–35% for reads and connects and far
more for single-row commits (the `min detectable` column).

## Results: Tier 1 workload, pycubrid 1.13.5

| Scenario | Rows per round | Per-trial median round (s) | Median (s) | Rows/s at median |
|---|---:|---|---:|---:|
| insert_sequential | 10,000 | 8.662 / 8.745 / 8.308 | 8.662 | 1,154 |
| select_by_pk | 10,000 | 7.762 / 7.451 / 7.421 | 7.451 | 1,342 |
| select_full_scan | 10,000 | 0.0447 / 0.0393 / 0.0429 | 0.0429 | 233,000 |
| update_indexed | 1,000 | 0.941 / 0.786 / 0.976 | 0.941 | 1,062 |
| delete_sequential | 1,000 | 1.573 / 1.100 / 0.862 | 1.100 | 909 |

This uses the corrected `tier1-explicit-keys-v2` workload. The historical table in
APPENDIX.md section B came from the earlier workload, whose SELECT/UPDATE/DELETE rounds
addressed keys that no longer existed and whose rounds also timed the re-seed (see the
experiment's README), so the two tables measure different quantities and must not be
compared. There is no CUBRIDdb counterpart in this harness, and no PyMySQL/MySQL run was
made: a comparison across database engines mixes server differences with driver overhead.

## Known limitations

- One shared, heavily loaded machine. Medians and ratios between drivers measured in the
  same rotated trials are the robust part; absolute times are not.
- One server container, one host, localhost networking. No other CUBRID version was run.
- The deck's historical optimization rows (native ping, `pool_pre_ping`, bulk insert,
  select-all, fetch) were not rerun: their source harness and run are not recorded.
