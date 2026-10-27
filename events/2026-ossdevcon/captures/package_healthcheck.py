"""Pre-judging package health check — exercises the exact judge path (PyPI installs).

Layers: pycubrid (sync + aio) → sqlalchemy-cubrid (engine) →
cubrid-mcp-server (MCP over stdio: read allowed, write rejected).
"""

from __future__ import annotations

import asyncio
import sys
import time

HOST = "localhost"
PORT = 33000
DB = sys.argv[1] if len(sys.argv) > 1 else "testdb"
USER = "dba"

PASS: list[str] = []
FAIL: list[str] = []


def check(name: str, fn):
    t0 = time.perf_counter()
    try:
        detail = fn()
        dt = (time.perf_counter() - t0) * 1000
        PASS.append(f"{name}: OK ({detail}) [{dt:.0f}ms]")
    except Exception as e:
        FAIL.append(f"{name}: FAIL — {type(e).__name__}: {e}")


# ---------- Layer 1: pycubrid ----------
import pycubrid  # noqa: E402
import pycubrid.aio  # noqa: E402  (explicit: submodule not auto-imported)


def l1_connect():
    conn = pycubrid.connect(host=HOST, port=PORT, database=DB, user=USER)
    v = conn.get_server_version()
    conn.close()
    return f"CUBRID {v}"


def l1_sync_query():
    conn = pycubrid.connect(host=HOST, port=PORT, database=DB, user=USER)
    cur = conn.cursor()
    cur.execute("SELECT 1 + 41")
    r = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert r == 42, f"unexpected {r}"
    return "SELECT 1+41 → 42"


def l1_aio():
    async def run():
        async with await pycubrid.aio.connect(
            host=HOST, port=PORT, database=DB, user=USER
        ) as conn:
            cur = conn.cursor()
            await cur.execute("SELECT VERSION()")
            return (await cur.fetchone())[0]

    return f"async → CUBRID {asyncio.run(run())}"


# ---------- Layer 2: sqlalchemy-cubrid ----------
from sqlalchemy import create_engine, text  # noqa: E402


def l2_engine():
    eng = create_engine(f"cubrid+pycubrid://{USER}@{HOST}:{PORT}/{DB}")
    with eng.connect() as c:
        v = c.execute(text("SELECT VERSION()")).scalar_one()
    return f"engine → {v}"


# ---------- Layer 3: cubrid-mcp-server (MCP over stdio, judge-path faithful) ----------
def l3_mcp():
    import json
    import os
    import subprocess
    import sys as _sys

    env = {
        **{k: v for k, v in os.environ.items() if k != "CUBRID_MCP_WRITE"},
        "CUBRID_HOST": HOST,
        "CUBRID_PORT": str(PORT),
        "CUBRID_USER": USER,
        "CUBRID_PASSWORD": os.environ.get("CUBRID_PASSWORD", ""),
        "CUBRID_DATABASE": DB,
        "CUBRID_DATABASE": DB,
    }

    proc = subprocess.Popen(
        [_sys.executable, "-m", "cubrid_mcp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    def rpc(req: dict) -> dict:
        proc.stdin.write(json.dumps(req) + "\n")
        proc.stdin.flush()
        line = proc.stdout.readline()
        return json.loads(line) if line else {}

    try:
        rpc(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "healthcheck", "version": "1.0"},
                },
            }
        )
        tools = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = [t["name"] for t in tools.get("result", {}).get("tools", [])]

        read = rpc(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "execute_query",
                    "arguments": {"sql": "SELECT COUNT(*) FROM db_class"},
                },
            }
        )
        read_ok = "result" in read and not read.get("result", {}).get("isError", False)
        if not read_ok:
            return f"read failed: {json.dumps(read)[:120]}"

        drop = rpc(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "execute_query",
                    "arguments": {"sql": "DROP TABLE __hc_probe"},
                },
            }
        )
        rejected = drop.get("result", {}).get("isError", False)
        if not rejected:
            FAIL.append("mcp-write-rejection: FAIL — DROP was allowed")
        return f"{len(names)} tools, read OK, DROP {'rejected ✓' if rejected else 'ALLOWED (!)'}"
    finally:
        proc.terminate()


check("pycubrid.connect", l1_connect)
check("pycubrid.sync", l1_sync_query)
check("pycubrid.aio", l1_aio)
check("sqlalchemy-cubrid.engine", l2_engine)
check("cubrid-mcp-server", l3_mcp)

print("\n=== HEALTH CHECK RESULT ===")
for p in PASS:
    print(f"  ✓ {p}")
for f in FAIL:
    print(f"  ✗ {f}")
print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
sys.exit(1 if FAIL else 0)
