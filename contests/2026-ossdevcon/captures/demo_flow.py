"""Contest demo flow — timed rehearsal of the DEMO_RUNBOOK terminal segments.

Layer 1 (Driver, 60s budget): connect, version, async query
Layer 2 (MCP, 90s budget): tables → describe → top-5 → DROP rejection → SET query
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

# ---------- Layer 1: Driver ----------
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
        await cur.execute("SELECT COUNT(*) FROM orders")
        return (await cur.fetchone())[0]


n = asyncio.run(async_query())
print(f"Async query: {n} orders")
mark("L1 asyncio query", t0)
conn.close()

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
    tables = r.get("result", {}).get("content", [{}])[0].get("text", "")
    print(f"Tables: {tables[:100]}")
    mark("L2 'what tables exist?'", t0)

    t0 = time.perf_counter()
    r = call(
        "SELECT * FROM db_attribute WHERE class_name = 'products' ORDER BY attr_name"
    )
    cols = r.get("result", {}).get("content", [{}])[0].get("text", "")
    print(f"products columns: {cols[:120]}")
    mark("L2 describe products", t0)

    t0 = time.perf_counter()
    r = call(
        "SELECT p.name, SUM(o.total_price) AS revenue "
        "FROM orders o JOIN products p ON o.product_id = p.id "
        "WHERE o.order_date >= SYS_DATE - 90 "
        "GROUP BY p.name ORDER BY revenue DESC LIMIT 5"
    )
    top5 = r.get("result", {}).get("content", [{}])[0].get("text", "")
    print(f"Top-5 revenue (90d):\n{top5}")
    mark("L2 top-5 revenue", t0)

    t0 = time.perf_counter()
    r = call("DROP TABLE products")
    rejected = r.get("result", {}).get("isError", False)
    msg = r.get("result", {}).get("content", [{}])[0].get("text", "")[:120]
    print(f"DROP TABLE products → {'REJECTED ✓' if rejected else 'ALLOWED (!!!)'}")
    print(f"  server message: {msg}")
    mark("L2 DROP rejection (the money shot)", t0)

    t0 = time.perf_counter()
    r = call("SELECT name, price FROM products WHERE 'sale' IN tags")
    sale = r.get("result", {}).get("content", [{}])[0].get("text", "")
    print(f"Products with 'sale' tag (SET semantics):\n{sale}")
    mark("L2 SET-type query", t0)
finally:
    proc.terminate()

# ---------- Summary ----------
print("\n" + "=" * 60)
print("TIMING SUMMARY")
print("=" * 60)
total = 0.0
for label, dt in T:
    print(f"  {dt:6.2f}s  {label}")
    total += dt
print(f"  ------")
print(f"  {total:6.2f}s  TOTAL (runbook terminal budget: 150s for L1+L2)")
