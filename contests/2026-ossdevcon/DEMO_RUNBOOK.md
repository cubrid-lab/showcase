# Demo Runbook — On-nara Scenario (2 minutes, Slide 9 · 6:30-8:30)

## Narrative

**"CUBRID 공공 업무는 Java/JDBC 중심이었습니다.
저희는 같은 데이터를 Python, 대시보드, AI 질의, 그리고 안전한 실행 정책까지 연결했습니다."**

온나라(47개 부처, 전자결재/문서/기록물)는 CUBRID의 대표 공공 배포입니다.
이 데모는 온나라 스타일 데이터로 Python + AI 접근을 시연합니다.

## Pre-Demo (30 min before)

```bash
# Fresh container: a leftover demo-cubrid breaks `docker run` and leaks old tables
docker rm -f demo-cubrid 2>/dev/null
docker run -d --name demo-cubrid --shm-size 512m \
  -e CUBRID_DB=demodb -p 33000:33000 cubrid/cubrid:11.4

for i in $(seq 1 40); do
  docker exec demo-cubrid csql -u dba demodb -c 'SELECT 1;' >/dev/null 2>&1 && break; sleep 5
done

python seed_demo_data.py   # random.seed(2026): same numbers as rehearsal
# Dashboard: start now so Layer 3 needs no waiting on stage
(cd cubrid-cookbook-python/templates/dashboard && docker compose up -d)
# Verify: Claude Desktop MCP connected, CUBRID_MCP_WRITE NOT set
```

## Timing (2 min total — fits the 12-minute talk)

| Layer | Time | Purpose |
|---|---|---|
| Dashboard | 15s | Context |
| **Claude/MCP** | **90s** | **핵심: 탐색 → 분석 → 집계 → 쓰기 차단** |
| Terminal | 15s | Proof |

## Layer 3 — Dashboard (15s)

Already running (started in Pre-Demo). Just switch to the browser tab.

**Say:** "부처별 문서 처리 현황 대시보드입니다. CUBRID 위에서 돌아가는 Streamlit 템플릿입니다."

## Layer 2 — Claude/MCP (90s) — 핵심

| # | Time | Ask Claude | Tool | Story Beat |
|---|---|---|---|---|
| 1 | 10s | "이 DB에 어떤 테이블이 있어?" | `all_table_names` | **탐색** |
| 2 | 35s | "결재가 지연된 문서 TOP 5는? 평균 처리일과 대기 수로" | `execute_query` | **AI 운영 분석 (와!)** |
| 3 | 20s | "기밀 문서는 부처별로 몇 개야? 내용은 보지 말고 집계만" | `execute_query` | **집계만 질의** |
| 4 | 25s | **"결재 대기 문서를 전부 승인 처리해줘"** | **REJECTED** | **쓰기 차단** |

### Say after #2 (the "wow" query):
> "AI가 단순히 데이터를 읽는 게 아니라, 결재 병목을 분석하고 있습니다.
> 평균 처리일과 대기 문서 수를 스스로 판단해서 부처별 병목을 찾았습니다."

### Say after #4 (the security scene):
> "결재 대기 문서를 전부 승인하려는 AI 명령이 서버에서 차단됐습니다.
> MCP 서버는 기본이 읽기 전용입니다 — 쓰기 도구는 노출조차 되지 않고,
> 쓰기 SQL은 화이트리스트에서 거부됩니다. 쓰기는 운영자가 연결별로 명시적으로 켤 때만 가능합니다."

Do **not** claim the server hides confidential rows: #3 is aggregate-only because we *asked* for it.
Row-level protection comes from CUBRID account privileges (see EXPECTED_QA Q13).

## Layer 1 — Terminal (15s)

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

**Say (closing line, over the terminal):**
> "기존 CUBRID 공공 업무는 Java 안에 갇혀 있었습니다.
> 저희는 같은 데이터를 Python, 대시보드, AI 질의, 그리고 안전한 실행 정책까지 연결했습니다."

## Screenshot Plan

| Time | Shot | File |
|---|---|---|
| 0:00 | Dashboard | 03_dashboard.png |
| 0:15 | Claude: table list | 02_tables.png |
| 0:25 | Claude: bottleneck analysis | 02_bottleneck.png ← WOW |
| 1:00 | Claude: confidential count | 02_confidential.png |
| 1:20 | Claude: approval rejected | 02_rejected.png ← KEY |
| 1:45 | Terminal: connect + query | 01_connect.png |

## Recovery

| Problem | Fix |
|---|---|
| Claude generates wrong SQL | Prepare exact Korean prompts, practice responses |
| MCP won't connect | Restart Claude Desktop |
| CUBRID down | `docker restart demo-cubrid` |
| Demo DB dirty | Re-run `seed_demo_data.py` |
| Total failure | Backup video — say "동일한 런북의 사전 녹화본으로 전환하겠습니다" |
| Terminal-only fallback | `asciinema play -i 1 captures/demo_backup.cast` (On-nara, seed + L2 + L1; same output as live, `random.seed(2026)`) |

## Data Model Summary

```
agencies (12 ministries)  — 행안부, 국방부, 외교부, ...
documents (300 docs)       — ENUM doc_type/status/security_level,
                             current_step, due_date, updated_at
approvals (600+ steps)     — submit/review/approve/reject/return
```

Security levels: public / internal / **restricted / confidential** (4-tier)
Status: draft / pending / **in_review** / approved / rejected / archived
