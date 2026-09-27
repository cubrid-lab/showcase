"""Contest demo flow — timed rehearsal of the DEMO_RUNBOOK terminal segments.

On-nara scenario (seed_demo_data.py), in runbook order:
Layer 2 (Claude/MCP, 120s budget): tables → describe → ministry status →
    bottleneck TOP 5 → confidential count → bulk-approve REJECTED
Layer 1 (Terminal, 50s budget): connect, version, async document count
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time

import pycubrid
import pycubrid.aio

HOST, PORT, DB, USER = "localhost", 33000, "demodb", "dba"
T: list[tuple[str, float]] = []


def mark(label: str, t0: float) -> None:
    dt = time.perf_counter() - t0
    T.append((label, dt))
    print(f"  [{dt:5.2f}s] {label}")


print("=" * 60)
print("DEMO REHEARSAL — timed run")
print("=" * 60)

# ---------- Layer 2: MCP ----------
print("\n--- L2: cubrid-mcp-server (MCP over stdio) ---")

env = {
    **{k: v for k, v in os.environ.items() if k != "CUBRID_MCP_WRITE"},
    "CUBRID_HOST": HOST,
    "CUBRID_PORT": str(PORT),
    "CUBRID_USER": USER,
    "CUBRID_PASSWORD": os.environ.get("CUBRID_PASSWORD", ""),
    "CUBRID_DATABASE": DB,
}
proc = subprocess.Popen(
    [sys.executable, "-m", "cubrid_mcp_server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env=env,
)
_id = 0


def rpc(method: str, params: dict | None = None) -> dict:
    global _id
    _id += 1
    req = {"jsonrpc": "2.0", "id": _id, "method": method}
    if params:
        req["params"] = params
    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline() or "{}")


def text(r: dict) -> str:
    return r.get("result", {}).get("content", [{}])[0].get("text", "")


def call(sql: str) -> dict:
    return rpc("tools/call", {"name": "execute_query", "arguments": {"sql": sql}})


try:
    t0 = time.perf_counter()
    rpc(
        "initialize",
        {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "demo", "version": "1.0"},
        },
    )
    tools = rpc("tools/list")
    names = [t["name"] for t in tools.get("result", {}).get("tools", [])]
    print(f"MCP session up — {len(names)} tools")
    mark("L2 session init", t0)

    t0 = time.perf_counter()
    r = rpc("tools/call", {"name": "all_table_names", "arguments": {}})
    print(f"Tables: {text(r)[:100]}")
    mark("L2 #1 'what tables exist?'", t0)

    t0 = time.perf_counter()
    r = rpc(
        "tools/call",
        {"name": "describe_table", "arguments": {"table_name": "documents"}},
    )
    print(f"documents schema: {text(r)[:120]}")
    mark("L2 #2 describe documents (ENUM)", t0)

    t0 = time.perf_counter()
    r = call(
        "SELECT a.name, d.status, COUNT(*) AS cnt "
        "FROM documents d JOIN agencies a ON d.agency_id = a.id "
        "GROUP BY a.name, d.status ORDER BY a.name, d.status"
    )
    print(f"Ministry × status: {text(r)[:120]}")
    mark("L2 #3 ministry status", t0)

    t0 = time.perf_counter()
    r = call(
        "SELECT a.name, COUNT(*) AS pending_count, "
        "AVG(DATEDIFF(SYS_DATETIME, d.created_at)) AS avg_days "
        "FROM documents d JOIN agencies a ON d.agency_id = a.id "
        "WHERE d.status IN ('pending','in_review') "
        "GROUP BY a.name ORDER BY pending_count DESC LIMIT 5"
    )
    print(f"Bottleneck TOP 5:\n{text(r)}")
    mark("L2 #4 bottleneck TOP 5 (the wow)", t0)

    t0 = time.perf_counter()
    r = call(
        "SELECT a.name, COUNT(*) AS confidential_count "
        "FROM documents d JOIN agencies a ON d.agency_id = a.id "
        "WHERE d.security_level IN ('restricted','confidential') "
        "GROUP BY a.name ORDER BY confidential_count DESC LIMIT 5"
    )
    print(f"Confidential count only: {text(r)[:120]}")
    mark("L2 #5 confidential aggregate", t0)

    t0 = time.perf_counter()
    r = call(
        "UPDATE documents SET status = 'approved' "
        "WHERE status IN ('pending','in_review')"
    )
    rejected = r.get("result", {}).get("isError", False)
    print(f"Bulk approve → {'REJECTED ✓' if rejected else 'ALLOWED (!!!)'}")
    print(f"  server message: {text(r)[:120]}")
    mark("L2 #6 bulk-approve rejection (the key scene)", t0)
finally:
    proc.terminate()

# ---------- Layer 1: Terminal ----------
print("\n--- L1: pycubrid driver ---")

t0 = time.perf_counter()
conn = pycubrid.connect(host=HOST, port=PORT, database=DB, user=USER)
print(f"Connected to CUBRID {conn.get_server_version()}")
mark("L1 connect + version", t0)

t0 = time.perf_counter()


async def async_query():
    async with await pycubrid.aio.connect(
        host=HOST, port=PORT, database=DB, user=USER
    ) as c:
        cur = c.cursor()
        await cur.execute("SELECT COUNT(*) FROM documents")
        return (await cur.fetchone())[0]


n = asyncio.run(async_query())
print(f"Async query: {n} documents")
mark("L1 asyncio query", t0)
conn.close()

# ---------- Summary ----------
print("\n" + "=" * 60)
print("TIMING SUMMARY")
print("=" * 60)
total = 0.0
for label, dt in T:
    print(f"  {dt:6.2f}s  {label}")
    total += dt
print(f"  ------")
print(f"  {total:6.2f}s  TOTAL (runbook budget: 120s L2 + 50s L1)")
