# 데모 런북 — 2026 오픈소스 개발자대회 2차 발표 (4분)

> 발표 시 배점: 데모 10점 + 기능테스트 10점 직결
> 실패 대비: 전 구간 백업 영상 필수, 원커맨드 복구 스크립트 포함

## Pre-Demo Setup (30 min before presentation)

```bash
# -- Checklist --
[ ] All Docker images cached locally
    docker images | grep cubrid
[ ] Start CUBRID 11.4 container 10 min early
    docker run -d --name demo-cubrid --shm-size 512m -e CUBRID_DB=demodb -p 33000:33000 cubrid/cubrid:11.4
[ ] Verify container health
    docker exec demo-cubrid csql -u dba demodb -c 'SELECT 1;'
[ ] Load seed data (script below)
    python seed_demo_data.py
[ ] Verify Claude Desktop MCP connection
    → cubrid-mcp-server가 목록에 있는지
    → health_check 도구 호출해서 "OK" 확인
[ ] Verify CUBRID_MCP_WRITE is NOT set (rejection demo required)
    → claude_desktop_config.json에 CUBRID_MCP_WRITE 없는지
[ ] Terminal font 18pt+, light theme (for projector)
[ ] Browser tab ready: http://localhost:8501 (dashboard)
[ ] Backup video ready to play (full 4 min + layer clips)
```

## Seed Data Script

```python
# seed_demo_data.py — 발표 전 실행
import pycubrid

conn = pycubrid.connect(host="localhost", port=33000, database="demodb", user="dba")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        price NUMERIC(10,2),
        stock INT DEFAULT 0,
        tags SET(VARCHAR(30)),
        created_at DATETIME DEFAULT SYS_DATETIME
    )
""")

products = [
    ("노트북 Pro 16", "전자제품", 2450000, 15, {"bestseller", "new"}),
    ("스마트폰 X", "전자제품", 1350000, 42, {"bestseller"}),
    ("무선 이어폰", "전자제품", 189000, 128, {"new", "sale"}),
    ("태블릿 Air", "전자제품", 890000, 35, set()),
    ("스마트워치", "전자제품", 450000, 67, {"sale"}),
    ("게이밍 마우스", "주변기기", 89000, 210, {"bestseller"}),
    ("기계식 키보드", "주변기기", 159000, 89, {"new"}),
    ("모니터 27인치", "주변기기", 389000, 23, set()),
    ("USB-C 허브", "주변기기", 45000, 350, {"sale", "bestseller"}),
    ("웹캠 4K", "주변기기", 129000, 56, set()),
]

cur.executemany(
    "INSERT INTO products (name, category, price, stock, tags) VALUES (?, ?, ?, ?, ?)",
    [(n, c, p, s, "{" + ", ".join(f"'{t}'" for t in t2) + "}") for n, c, p, s, t2 in products]
)

cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        total_price NUMERIC(12,2),
        order_date DATETIME DEFAULT SYS_DATETIME,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

import random, datetime
for i in range(200):
    pid = random.randint(1, 10)
    qty = random.randint(1, 5)
    cur.execute("SELECT price FROM products WHERE id = ?", [pid])
    price = cur.fetchone()[0]
    days_ago = random.randint(0, 90)
    dt = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    cur.execute(
        "INSERT INTO orders (product_id, quantity, total_price, order_date) VALUES (?, ?, ?, ?)",
        [pid, qty, price * qty, dt]
    )

conn.commit()
cur.execute("SELECT COUNT(*) FROM products")
print(f"Products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM orders")
print(f"Orders: {cur.fetchone()[0]}")
cur.close()
conn.close()
print("✓ Seed data ready")
```

---

## Layer 3 — App (60s) — "This actually runs"

### 화면: 브라우저 → http://localhost:8501

**캡처**: Streamlit 대시보드 전체 화면 — 제품 테이블이 그려진 상태

**대사**:
> "cubrid-cookbook-python의 대시보드 템플릿입니다. docker compose up 한 줄로
> CUBRID 11.4와 Streamlit이 함께 뜹니다. 지금 보시는 데이터가 전부
> 오늘 발표하는 스택 위에서 돌아가고 있습니다."

### 캡처 목록
| 시점 | 캡처 내용 | 파일명 |
|---|---|---|
| 00:00 | 터미널에서 `docker compose up -d` 실행 | `03_compose_up.png` |
| 00:05 | 브라우저에서 대시보드 첫 화면 | `03_dashboard_main.png` |
| 00:15 | 테이블 뷰어에서 제품 데이터 | `03_table_viewer.png` |
| 00:30 | KPI 카드 (총 매출, 주문 수) | `03_kpi_cards.png` |
| 00:45 | 필터 기능 시연 (카테고리 선택) | `03_filter.png` |

---

## Layer 2 — LLM (90s) — "AI queries safely"

### 화면: Claude Desktop

**대사**:
> "이제 같은 데이터베이스를 Claude에게 물어보겠습니다."

### 질문 1 (15초): "이 DB에 어떤 테이블이 있어?"
- Claude가 `all_table_names` 호출
- **캡처**: Claude 응답에 테이블 목록 표시 | `02_tables.png`

### 질문 2 (15초): "products 테이블 구조 보여줘"
- Claude가 `describe_table` 호출
- **캡처**: 컬럼 목록 + SET 타입 tags 컬럼 확인 | `02_describe.png`

### 질문 3 (20초): "지난 3개월 매출 상위 5개 상품은?"
- Claude가 `execute_query`로 SELECT 실행
- **캡처**: 결과 테이블 + SQL 표시 | `02_top5.png`

### 질문 4 (20초) — 핵심 장면: "products 테이블 지워줘"
- Claude가 `execute_query`로 DROP TABLE 시도
- **서버가 거부** ← 이 장면이 가장 중요
- **캡처**: 거부 메시지 | `02_rejected.png`

**대사 (거부 후)**:
> "화이트리스트가 서버 수준에서 작동합니다. 프롬프트 인젝션이나
> 실수로도 데이터를 지울 수 없습니다. 쓰기는 별도 옵트인이 필요합니다."

### 질문 5 (20초): "tags에 'sale'이 있는 상품은?"
- Claude가 컬렉션 타입을 이해하고 쿼리
- **캡처**: SET 타입 조회 결과 | `02_collection.png`
- "CUBRID의 SET 타입을 MCP 스킬이 알려주기 때문에
>   Claude가 처음 보는 타입도 올바르게 다룹니다."

---

## Layer 1 — Driver (60s) — "Underneath, this is what powers it"

### 화면: 터미널 → Python REPL 또는 스크립트

**캡처**: 터미널 전체 — 코드 + 실행 결과

```python
import pycubrid

# 1. 연결 — pip install pycubrid 한 줄, C 컴파일러 없음
conn = pycubrid.connect(host="localhost", port=33000, database="demodb", user="dba")
print(f"Connected to CUBRID {conn.get_server_version()}")

# 2. 순수 Python — asyncio 네이티브
import pycubrid.aio, asyncio

async def async_query():
    async with await pycubrid.aio.connect(host="localhost", database="demodb", user="dba") as conn:
        cur = conn.cursor()
        await cur.execute("SELECT COUNT(*) FROM orders")
        return await cur.fetchone()

result = asyncio.run(async_query())
print(f"Async query result: {result[0]} orders")

# 3. TLS 지원
print("TLS: 지원 (SSLContext 전달)")
print("Python: 3.10–3.14 전부 지원")
print("의존성: 0개 (pip install pycubrid 끝)")

conn.close()
```

**대사**:
> "이 모든 것의 기반이 되는 순수 Python 드라이버입니다.
> pip install 한 줄이면 끝나고, C 컴파일러가 필요 없고,
> asyncio와 TLS를 네이티브로 지원합니다.
> 2014년 이후 방치됐던 공식 드라이버의 모든 문제를 해결했습니다."

### 캡처 목록
| 시점 | 캡처 내용 | 파일명 |
|---|---|---|
| 00:00 | `pip install pycubrid` 실행 | `01_pip_install.png` |
| 00:05 | 연결 + 버전 확인 | `01_connect.png` |
| 00:20 | asyncio 쿼리 실행 | `01_async.png` |
| 00:40 | 출력: "의존성: 0개" | `01_zero_deps.png` |

---

## Wrap-up (30s) — "Schema changes with standard tools too"

### 화면: 터미널

```bash
alembic upgrade head
# → 새 컬럼 추가 마이그레이션 실행
```

**대사**:
> "스키마 변경도 Alembic으로 표준적으로 처리합니다.
> 방금 보신 4개 계층 — 드라이버, ORM, 예제, AI — 이 전부
> pip install로 설치됩니다. 감사합니다."

---

## Capture Files

```
showcase/contests/2026-ossdevcon/captures/
├── 01_pip_install.png      # 층 1: pip install
├── 01_connect.png           # 층 1: 연결 + 버전
├── 01_async.png             # 층 1: asyncio 쿼리
├── 01_zero_deps.png         # 층 1: 의존성 0
├── 02_tables.png            # 층 2: 테이블 목록
├── 02_describe.png          # 층 2: 테이블 구조
├── 02_top5.png              # 층 2: 매출 상위 5개
├── 02_rejected.png          # 층 2: DROP TABLE 거부 ← 핵심
├── 02_collection.png        # 층 2: SET 타입 조회
├── 03_compose_up.png        # 층 3: docker compose up
├── 03_dashboard_main.png    # 층 3: 대시보드 전체
├── 03_table_viewer.png      # 층 3: 테이블 뷰어
├── 03_kpi_cards.png         # 층 3: KPI 카드
├── 03_filter.png            # 층 3: 필터 시연
├── 04_alembic.png           # 마무리: alembic upgrade
├── backup_video_full.mp4    # 백업 영상 (전체 4분)
├── backup_layer1.mp4        # 백업: 층 1 클립
├── backup_layer2.mp4        # 백업: 층 2 클립
└── backup_layer3.mp4        # 백업: 층 3 클립
```

## Capture Tools

```bash
# 스크린샷 (전체 화면)
# macOS: Cmd+Shift+3 (전체) / Cmd+Shift+4 (영역)
# Linux: gnome-screenshot -f filename.png
#      또는 import filename.png (ImageMagick)

# 화면 녹화 (백업 영상)
# macOS: QuickTime Player → New Screen Recording
# Linux: OBS Studio 또는 SimpleScreenRecorder
# 해상도: 1920×1080 (1080p) 권장

# 터미널 캡처 팁
# 1. 라이트 테마 (프로젝터에서 어두운 테마는 안 보임)
# 2. 폰트 크기 18pt 이상
# 3. 불필요한 프롬프트/경로 숨기기 (PS1 단순화)
```

## Recovery Procedures

| 증상 | 복구 |
|---|---|
| MCP 서버 연결 안 됨 | Claude Desktop 재시작 → MCP 재연결 |
| CUBRID 컨테이너 다운 | `docker restart demo-cubrid` |
| 데모 DB 오염 | `seed_demo_data.py` 재실행 |
| 전체 실패 | **백업 영상 재생** (층별 클립 → 순서대로) |

## Presentation Time Allocation

| 구간 | 시간 | 누적 |
|---|---|---|
| 층 3 — 앱 (대시보드) | 60초 | 0:00–1:00 |
| 층 2 — LLM (MCP) | 90초 | 1:00–2:30 |
| 층 1 — 드라이버 | 60초 | 2:30–3:30 |
| 마무리 (Alembic) | 30초 | 3:30–4:00 |
| **전체** | **4분** | |
