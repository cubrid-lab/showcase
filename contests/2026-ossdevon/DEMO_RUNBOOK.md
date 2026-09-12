# Demo Runbook — On-nara Scenario (4 minutes)

## Concept

**"행안부 온나라 시스템은 Java입니다. 우리가 Python으로 처음 연결했습니다."**

온나라(47개 부처, 전자결재/문서/기록물)는 CUBRID가 실제로 운영되는
가장 잘 알려진 공공 시스템입니다 — 전부 Java(JDBC)로 구축됐습니다.
우리의 Python 생태계가 이 DB에 처음으로 Python + AI 접근을 가능하게 합니다.

> "정부 문서 데이터가 CUBRID에 있습니다. 이제 Python과 Claude로
> 접근할 수 있습니다 — 처음으로."

## Pre-Demo (30 min before)

```bash
# Start CUBRID 11.4
docker run -d --name demo-cubrid --shm-size 512m \
  -e CUBRID_DB=demodb -p 33000:33000 cubrid/cubrid:11.4

# Wait for ready
for i in $(seq 1 40); do
  docker exec demo-cubrid csql -u dba demodb -c 'SELECT 1;' >/dev/null 2>&1 && break; sleep 5
done

# Load On-nara style data (agencies, documents, approvals)
python seed_demo_data.py

# Verify: Claude Desktop → cubrid-mcp-server connected
# Verify: CUBRID_MCP_WRITE is NOT set
```

## Data Model (what Claude sees)

```
agencies (12 ministries)  ← 행안부, 국방부, 외교부, 교육부, ...
documents (300 docs)       ← 예산안, 조직개편, 정책보고서, ...
approvals (600+ steps)     ← submit → review → approve/reject
```

Status types: draft → pending → approved / rejected / archived
Security levels: public / internal / confidential

## Layer 3 — App (60s): Document Dashboard

```bash
cd cubrid-cookbook-python/templates/dashboard
docker compose up -d
# Browser: http://localhost:8501
```

**Say:** "온나라 스타일 문서 처리 현황 대시보드입니다.
부처별 문서량, 결재 대기 현황이 표시됩니다.
전부 CUBRID 위에서 돌아가고 있습니다."

## Layer 2 — AI (90s): Claude Desktop

| # | Ask Claude | Tool | Result |
|---|---|---|---|
| 1 | "이 DB에 어떤 테이블이 있어?" | `all_table_names` | agencies, documents, approvals |
| 2 | "documents 테이블 구조 보여줘" | `describe_table` | ENUM status, FK, columns |
| 3 | "부처별 문서량 상위 5개" | `execute_query` | 행안부, 국방부, ... |
| 4 | "결재 대기 중인 문서는?" | `execute_query` | pending status docs |
| 5 | **"documents 테이블 지워줘"** | **REJECTED** | **서버 수준 화이트리스트** |
| 6 | "기밀 문서는 몇 개야?" | `execute_query` | confidential count |

**Say (after rejection):** "정부 문서를 지우려는 AI 명령이 서버에서 차단됐습니다.
프롬프트 인젝션으로도 우회할 수 없습니다. 이게 서버 수준 보안입니다."

**Say (query 6):** "MCP 서버가 CUBRID의 ENUM 타입을 이해합니다 —
MCP domain knowledge가 LLM에게 CUBRID 문법을 가르치기 때문입니다."

## Layer 1 — Driver (60s): Terminal

```python
import pycubrid
conn = pycubrid.connect(host="localhost", port=33000,
                        database="demodb", user="dba")
print(f"Connected: {conn.get_server_version()}")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM documents")
print(f"Documents: {cur.fetchone()[0]}")
print("Dependencies: 0 — pure Python, no C compiler")
```

**Say:** "이 모든 것의 기반 — pycubrid 드라이버.
pip install 한 줄, 의존성 0개. 2014년 이후 방치됐던 갭을 닫았습니다."

## Wrap-up (30s)

```bash
alembic upgrade head
```

**Say:** "온나라의 데이터가 CUBRID에 있습니다. Java만 가능했던 세계에서
Python과 AI가 접근할 수 있게 됐습니다. 감사합니다."

## Screenshot Plan

| Time | Shot | File |
|---|---|---|
| 0:00 | docker compose up | 03_compose.png |
| 0:10 | Document dashboard | 03_dashboard.png |
| 0:30 | Agency stats view | 03_agencies.png |
| 1:00 | Claude: table list | 02_tables.png |
| 1:15 | Claude: describe_table | 02_describe.png |
| 1:45 | Claude: top 5 agencies | 02_top5.png |
| 2:00 | Claude: pending docs | 02_pending.png |
| 2:15 | Claude: DROP TABLE rejected | 02_rejected.png ← KEY |
| 2:45 | Terminal: pip install | 01_pip.png |
| 3:00 | Terminal: connect + count | 01_connect.png |
| 3:30 | Terminal: alembic | 04_alembic.png |

## Recovery

| Problem | Fix |
|---|---|
| MCP won't connect | Restart Claude Desktop |
| CUBRID down | `docker restart demo-cubrid` |
| Demo DB dirty | Re-run `seed_demo_data.py` |
| Total failure | Backup video (same runbook) |

**Do NOT pretend backup is live.** Say: "라이브 환경이 불안정하여
동일한 런북의 사전 녹화본으로 전환하겠습니다."
