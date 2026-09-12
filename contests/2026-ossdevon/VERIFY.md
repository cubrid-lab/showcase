# Judge Verification Guide

This guide lets anyone verify the CUBRID Python ecosystem works — with or without PyPI.

## Option A: PyPI (preferred, when published)

```bash
# 1. Driver — one command, pure Python
pip install pycubrid
python -c "import pycubrid; print(pycubrid.__version__)"
# Expected: 1.7.0 (or later)

# 2. ORM
pip install sqlalchemy-cubrid
python -c "import sqlalchemy_cubrid; print('OK')"

# 3. MCP Server
uvx cubrid-mcp-server --help
# Expected: server starts (requires CUBRID_* env vars)
```

## Option B: GitHub Release (fallback, works today)

```bash
# 1. Start CUBRID database
git clone https://github.com/cubrid-lab/cubrid-cookbook-python.git
cd cubrid-cookbook-python
docker compose up -d
# Wait ~30 seconds for database to be ready

# 2. Install from release artifacts
# Download from: https://github.com/cubrid-lab/pycubrid/releases/latest
pip install pycubrid-*.whl

# 3. Run first query
export CUBRID_HOST=localhost CUBRID_PORT=33000 CUBRID_DATABASE=testdb CUBRID_USER=dba
python fundamentals/pycubrid/01_connect.py
# Expected: Connected to CUBRID 11.x

# 4. Run the golden-verified test suite
pip install pycubrid sqlalchemy sqlalchemy-cubrid
make verify
# Expected: all examples pass against live CUBRID

# 5. MCP Server (from source)
pip install -e .
export CUBRID_MCP_READONLY=1
python -m cubrid_mcp_server &
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"verify","version":"1.0"}}}' | python -m cubrid_mcp_server
```

## What to Look For

| Component | Check | Expected |
|---|---|---|
| pycubrid | `pip install pycubrid` | Installs without C compiler |
| pycubrid | `connect()` | Returns Connection object |
| pycubrid | `execute("SELECT 1")` | Returns `(1,)` |
| sqlalchemy-cubrid | `create_engine("cubrid+pycubrid://...")` | Engine creates successfully |
| sqlalchemy-cubrid | ORM query | Results returned |
| cookbook | `make verify` | All examples pass |
| mcp-server | Initialize JSON-RPC | serverInfo returned |
| mcp-server | DROP TABLE via execute_query | **Rejected** (read-only whitelist) |

## Troubleshooting

| Problem | Solution |
|---|---|
| `Connection refused` | Wait 30s for CUBRID container, check `docker compose logs` |
| `Authentication failed` | Default user is `dba` with empty password |
| `uvx: command not found` | Install [uv](https://docs.astral.sh/uv/): `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| MCP server won't start | Set `CUBRID_HOST`, `CUBRID_DATABASE`, `CUBRID_USER` env vars |

## Verify SBOM and Licensing

```bash
# SPDX SBOM attached to every GitHub Release
gh release download v0.4.0 -R cubrid-lab/cubrid-mcp-server -p sbom.spdx.json
cat sbom.spdx.json | python -m json.tool | head -20

# THIRD_PARTY_LICENSES.md in every repo
cat https://raw.githubusercontent.com/cubrid-lab/pycubrid/main/THIRD_PARTY_LICENSES.md | head -10
```

## CI Status (live)

All 4 repositories have green main branches:
- https://github.com/cubrid-lab/pycubrid/actions
- https://github.com/cubrid-lab/sqlalchemy-cubrid/actions
- https://github.com/cubrid-lab/cubrid-mcp-server/actions
- https://github.com/cubrid-lab/cubrid-cookbook-python/actions
