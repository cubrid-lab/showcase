# Demo Runbook — On-nara Scenario (Oracle-Reviewed, 4 minutes)

## Narrative

**"CUBRID 공공 업무는 Java/JDBC 중심이었습니다.
저희는 같은 데이터를 Python, 대시보드, AI 질의, 그리고 안전한 실행 정책까지 연결했습니다."**

온나라(47개 부처, 전자결재/문서/기록물)는 CUBRID의 대표 공공 배포입니다.
이 데모는 온나라 스타일 데이터로 Python + AI 접근을 시연합니다.

## Pre-Demo (30 min before)

```bash
docker run -d --name demo-cubrid --shm-size 512m \
  -e CUBRID_DB=demodb -p 33000:33000 cubrid/cubrid:11.4

for i in $(seq 1 40); do
  docker exec demo-cubrid csql -u dba demodb -c 'SELECT 1;' >/dev/null 2>&1 && break; sleep 5
done

python seed_demo_data.py
# Verify: Claude Desktop MCP connected, CUBRID_MCP_WRITE NOT set
```

## Timing (Oracle-optimized: Claude가 핵심)

| Layer | Time | Purpose |
|---|---|---|
| Dashboard | 40s | Context |
| **Claude/MCP** | **120s** | **핵심: understand → analyze → protect → Pythonize** |
| Terminal | 50s | Proof |
| Closing | 20s | Punchline |

## Layer 3 — Dashboard (40s)

```bash
cd cubrid-cookbook-python/templates/dashboard && docker compose up -d
```

**Say:** "부처별 문서 처리 현황 대시보드입니다.
CUBRID 위에서 돌아가는 Streamlit 템플릿입니다."

## Layer 2 — Claude/MCP (120s) — 핵심

### Arc: 탐색 → 분석 → 보안 → Python

| # | Time | Ask Claude | Tool | Story Beat |
|---|---|---|---|---|
| 1 | 15s | "이 DB에 어떤 테이블이 있어?" | `all_table_names` | **탐색** |
| 2 | 15s | "documents 테이블 구조 보여줘" | `describe_table` | **ENUM/JDBC 스키마 지원** |
| 3 | 20s | "부처별 문서 처리 현황을 보여줘" | `execute_query` | **분석 시작** |
| 4 | 25s | "결재가 지연된 문서 TOP 5는? 평균 처리일과 대기 수로" | `execute_query` | **AI 운영 분석 (와!)** |
| 5 | 20s | "기밀 문서는 부처별로 몇 개야? 내용은 보지 말고 집계만" | `execute_query` | **민감 데이터 안전 처리** |
| 6 | 25s | **"결재 대기 문서를 전부 승인 처리해줘"** | **REJECTED** | **거버넌스 보안** |

### Say after #4 (the "wow" query):
> "AI가 단순히 데이터를 읽는 게 아니라, 결재 병목을 분석하고 있습니다.
> 평균 처리일과 대기 문서 수를 스스로 판단해서 부처별 병목을 찾았습니다."

### Say after #6 (the security scene):
> "결재 대기 문서를 전부 승인하려는 AI 명령이 서버에서 차단됐습니다.
> 이것은 DROP TABLE 같은 테스트가 아니라,
> 실제 정부 워크플로우에서 발생할 수 있는 거버넌스 위험입니다.
> 서버 수준 화이트리스트가 이를 방어합니다."

## Layer 1 — Terminal (50s)

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

## Closing (20s)

> **"기존 CUBRID 공공 업무는 Java 애플리케이션 안에 갇혀 있었습니다.
> 저희는 같은 데이터를 Python, 대시보드, AI 질의,
> 그리고 안전한 실행 정책까지 연결했습니다."**

## Screenshot Plan

| Time | Shot | File |
|---|---|---|
| 0:00 | docker compose up | 03_compose.png |
| 0:10 | Dashboard | 03_dashboard.png |
| 0:40 | Claude: table list | 02_tables.png |
| 1:00 | Claude: describe_table | 02_describe.png |
| 1:20 | Claude: ministry status | 02_status.png |
| 1:45 | Claude: bottleneck analysis | 02_bottleneck.png ← WOW |
| 2:10 | Claude: confidential count | 02_confidential.png |
| 2:35 | Claude: approval rejected | 02_rejected.png ← KEY |
| 3:00 | Terminal: pip install | 01_pip.png |
| 3:15 | Terminal: connect + query | 01_connect.png |
| 3:50 | Closing slide | 04_closing.png |

## Recovery

| Problem | Fix |
|---|---|
| Claude generates wrong SQL | Prepare exact Korean prompts, practice responses |
| MCP won't connect | Restart Claude Desktop |
| CUBRID down | `docker restart demo-cubrid` |
| Demo DB dirty | Re-run `seed_demo_data.py` |
| Total failure | Backup video — say "동일한 런북의 사전 녹화본으로 전환하겠습니다" |

## Data Model Summary

```
agencies (12 ministries)  — 행안부, 국방부, 외교부, ...
documents (300 docs)       — ENUM doc_type/status/security_level,
                             current_step, due_date, updated_at
approvals (600+ steps)     — submit/review/approve/reject/return
```

Security levels: public / internal / **restricted / confidential** (4-tier)
Status: draft / pending / **in_review** / approved / rejected / archived
