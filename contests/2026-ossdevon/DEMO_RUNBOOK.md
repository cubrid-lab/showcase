# Demo Runbook — 2026 OSS Developer Contest Finals (4 minutes)

## Pre-Demo (30 min before)

```bash
# Start CUBRID 11.4
docker run -d --name demo-cubrid --shm-size 512m \
  -e CUBRID_DB=demodb -p 33000:33000 cubrid/cubrid:11.4

# Wait for ready
for i in $(seq 1 40); do
  docker exec demo-cubrid csql -u dba demodb -c 'SELECT 1;' >/dev/null 2>&1 && break; sleep 5
done

# Load seed data
python seed_demo_data.py

# Verify MCP connection (Claude Desktop)
# Check: cubrid-mcp-server appears in Claude's MCP list
# Call: health_check → "OK"
# Verify: CUBRID_MCP_WRITE is NOT set (DROP TABLE must be rejected)
```

## Layer 3 — App (60s)

```bash
cd cubrid-cookbook-python/templates/dashboard
docker compose up -d
# Browser: http://localhost:8501
```

**Say:** "This is the cookbook dashboard template. One docker compose command
spins up CUBRID 11.4 and Streamlit. Everything you see runs on the stack
we're presenting today."

## Layer 2 — AI (90s) — Claude Desktop

1. "Show tables" → `all_table_names`
2. "Show products structure" → `describe_table`
3. "Top 5 products by price" → `execute_query` (SELECT)
4. **"DROP TABLE products"** → **REJECTED** ← server-level whitelist
5. "Products with 'sale' tag" → SET type query

**Say (after rejection):** "The whitelist is server-enforced, not prompt-based.
No prompt injection can bypass it. Write access requires explicit opt-in."

## Layer 1 — Driver (60s)

```python
import pycubrid
conn = pycubrid.connect(host="localhost", port=33000, database="demodb", user="dba")
print(f"Connected: {conn.get_server_version()}")
cur = conn.cursor()
cur.execute("SELECT 1 + 1")
print(cur.fetchone())  # (2,)
print("Dependencies: 0 — pure Python, no C compiler")
```

## Wrap-up (30s)

```bash
alembic upgrade head  # schema migration with standard tools
```

## Capture Files

| Time | Screenshot | File |
|---|---|---|
| 0:00 | docker compose up | 03_compose.png |
| 0:05 | Dashboard first view | 03_dashboard.png |
| 1:00 | Claude: table list | 02_tables.png |
| 1:15 | Claude: describe_table | 02_describe.png |
| 1:30 | Claude: top 5 query | 02_top5.png |
| 1:45 | Claude: DROP TABLE rejected | 02_rejected.png |
| 2:30 | Terminal: pip install | 01_pip.png |
| 2:40 | Terminal: connect + query | 01_connect.png |
| 3:30 | Terminal: alembic | 04_alembic.png |

## Recovery

| Problem | Fix |
|---|---|
| MCP won't connect | Restart Claude Desktop → reconnect |
| CUBRID down | `docker restart demo-cubrid` |
| Demo DB dirty | Re-run `seed_demo_data.py` |
| Total failure | Play backup video (pre-recorded, same runbook) |

**Do NOT pretend backup video is live. Say: "We'll use the pre-recorded
backup of the exact same runbook." Judges reward preparedness.**
