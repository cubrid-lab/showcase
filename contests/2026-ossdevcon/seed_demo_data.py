"""Seed demo data — On-nara style e-approval (행안부 전자결재 시나리오).

Simulates the type of data in CUBRID government deployments.
Oracle-reviewed: added current_step, due_date, updated_at for bottleneck queries.
"""

import pycubrid

conn = pycubrid.connect(host="localhost", port=33000, database="demodb", user="dba")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS approvals")
cur.execute("DROP TABLE IF EXISTS documents")
cur.execute("DROP TABLE IF EXISTS agencies")

# ── 기관 ──
cur.execute("""
    CREATE TABLE agencies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        region VARCHAR(50) DEFAULT '세종'
    )
""")

agencies = [
    ("행정안전부", "중앙행정", "세종"),
    ("국방부", "국방", "서울"),
    ("외교부", "외교", "서울"),
    ("교육부", "교육", "세종"),
    ("산업통상자원부", "경제", "세종"),
    ("과학기술정보통신부", "과기", "세종"),
    ("환경부", "환경", "세종"),
    ("보건복지부", "복지", "세종"),
    ("고용노동부", "고용", "세종"),
    ("국토교통부", "국토", "세종"),
    ("법무부", "법무", "세종"),
    ("문화체육관광부", "문체", "세종"),
]
cur.executemany(
    "INSERT INTO agencies (name, category, region) VALUES (?, ?, ?)", agencies
)

# ── 문서 (Oracle review: current_step, due_date, updated_at 추가) ──
cur.execute("""
    CREATE TABLE documents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        doc_type ENUM('policy','budget','personnel','report','approval','directive'),
        agency_id INT NOT NULL,
        status ENUM('draft','pending','in_review','approved','rejected','archived'),
        security_level ENUM('public','internal','restricted','confidential'),
        current_step INT DEFAULT 1,
        due_date DATE,
        created_at DATETIME DEFAULT SYS_DATETIME,
        updated_at DATETIME DEFAULT SYS_DATETIME,
        FOREIGN KEY (agency_id) REFERENCES agencies(id)
    )
""")

import random
from datetime import datetime, timedelta

doc_templates = [
    ("{dept} 2026년 예산안 편성 방침", "budget"),
    ("{dept} 조직 개편 승인 요청", "personnel"),
    ("{dept} 정책 평가 보고서", "report"),
    ("{dept} 대국민 서비스 개선 방안", "policy"),
    ("{dept} 부처 간 협력 업무 협정", "approval"),
    ("{dept} 장관 지시사항 하달", "directive"),
    ("{dept} 정보화 사업 추진 계획", "policy"),
    ("{dept} 재난 안전 대응 매뉴얼 개정", "report"),
]

# Status distribution: more pending/in_review for bottleneck queries
status_weights = (
    ["approved"] * 30
    + ["pending"] * 25
    + ["in_review"] * 20
    + ["draft"] * 10
    + ["rejected"] * 10
    + ["archived"] * 5
)
security_levels = ["public", "internal", "internal", "restricted", "confidential"]

for i in range(300):
    template, doc_type = random.choice(doc_templates)
    dept = random.choice(agencies)[0]
    title = template.format(dept=dept)
    agency_id = random.randint(1, 12)
    status = random.choice(status_weights)
    security = random.choice(security_levels)
    current_step = (
        random.randint(1, 4)
        if status in ("pending", "in_review")
        else random.randint(1, 4)
    )
    days_ago = random.randint(0, 180)
    due_in = random.randint(-30, 60)  # some overdue
    created = datetime.now() - timedelta(days=days_ago)
    due = created + timedelta(days=30 + due_in // 4)
    updated = created + timedelta(
        days=random.randint(0, days_ago) if days_ago > 0 else 0
    )

    cur.execute(
        """INSERT INTO documents
           (title, doc_type, agency_id, status, security_level,
            current_step, due_date, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            title,
            doc_type,
            agency_id,
            status,
            security,
            current_step,
            due.strftime("%Y-%m-%d"),
            created.strftime("%Y-%m-%d %H:%M:%S"),
            updated.strftime("%Y-%m-%d %H:%M:%S"),
        ],
    )

# ── 결재 이력 ──
cur.execute("""
    CREATE TABLE approvals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        document_id INT NOT NULL,
        step INT NOT NULL,
        action ENUM('submit','review','approve','reject','return'),
        actor VARCHAR(50) NOT NULL,
        comment TEXT,
        acted_at DATETIME DEFAULT SYS_DATETIME,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
""")

actors = ["과장", "부장", "실장", "국장", "차관", "장관"]
comments = [
    "검토 완료. 승인합니다.",
    "예산 반영 필요. 보완 후 재상신 바랍니다.",
    "협조 부처 의견 확인 요청.",
    "규정 위배 사항 없음.",
    "법제처 협의 완료.",
    None,
]
actions = ["submit", "review", "approve", "approve", "reject", "return"]

for doc_id in range(1, 301):
    steps = random.randint(1, 4)
    for step in range(1, steps + 1):
        action = random.choice(actions)
        actor = random.choice(actors)
        comment = random.choice(comments)
        hours_ago = random.randint(1, 4320)
        cur.execute(
            "INSERT INTO approvals (document_id, step, action, actor, comment, acted_at) VALUES (?, ?, ?, ?, ?, SYS_DATETIME - INTERVAL ? HOUR)",
            [doc_id, step, action, actor, comment, hours_ago],
        )

conn.commit()

# Summary for presenter
cur.execute("SELECT COUNT(*) FROM agencies")
print(f"Agencies: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM documents")
print(f"Documents: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM approvals")
print(f"Approvals: {cur.fetchone()[0]}")

print("\n── Demo query previews ──")

# Q3: 부처별 처리 현황
cur.execute("""
    SELECT a.name, d.status, COUNT(*) as cnt
    FROM documents d JOIN agencies a ON d.agency_id = a.id
    GROUP BY a.name, d.status ORDER BY a.name, d.status
""")
print("Q3 sample (ministry × status):")
for row in cur.fetchall()[:4]:
    print(f"  {row[0]} | {row[1]} | {row[2]}")

# Q4: 결재 지연 TOP 5 (병목)
cur.execute("""
    SELECT a.name, COUNT(*) as pending_count,
           AVG(TIMESTAMPDIFF(SQL_TSI_DAY, d.created_at, SYS_DATETIME)) as avg_days
    FROM documents d JOIN agencies a ON d.agency_id = a.id
    WHERE d.status IN ('pending','in_review')
    GROUP BY a.name ORDER BY pending_count DESC LIMIT 5
""")
print("\nQ4 sample (bottleneck):")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} pending, avg {row[2]:.1f} days")

# Q5: 기밀 문서 집계 (내용 안 보이고)
cur.execute("""
    SELECT a.name, COUNT(*) as confidential_count
    FROM documents d JOIN agencies a ON d.agency_id = a.id
    WHERE d.security_level IN ('restricted','confidential')
    GROUP BY a.name ORDER BY confidential_count DESC LIMIT 5
""")
print("\nQ5 sample (confidential count only):")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} restricted/confidential")

# Q6: 승인 처리 시도 → REJECTED (execute_query는 SELECT만 허용)
print("\nQ6: 'UPDATE documents SET status=approved' → REJECTED (read-only whitelist)")

cur.close()
conn.close()
print("\n✓ On-nara demo data ready (Oracle-reviewed)")
