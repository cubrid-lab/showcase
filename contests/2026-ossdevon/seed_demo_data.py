"""Seed demo data — On-nara style document/approval system (행안부 전자결재).

Simulates the type of data found in CUBRID government deployments
(47 ministries, e-approval workflow, records management). All Java(JDBC)
in production — our ecosystem makes it accessible from Python for the first time.
"""

import pycubrid

conn = pycubrid.connect(host="localhost", port=33000, database="demodb", user="dba")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS approvals")
cur.execute("DROP TABLE IF EXISTS documents")
cur.execute("DROP TABLE IF EXISTS agencies")

# ── 기관 (47개 부처 중 대표 12개) ──
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

# ── 문서 (전자결재) ──
cur.execute("""
    CREATE TABLE documents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        doc_type ENUM('policy','budget','personnel','report','approval','directive'),
        agency_id INT NOT NULL,
        status ENUM('draft','pending','approved','rejected','archived'),
        security_level ENUM('public','internal','confidential') DEFAULT 'internal',
        created_at DATETIME DEFAULT SYS_DATETIME,
        FOREIGN KEY (agency_id) REFERENCES agencies(id)
    )
""")

import random

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

statuses = ["approved"] * 4 + ["pending"] * 3 + ["draft", "rejected", "archived"]

for i in range(300):
    template, doc_type = random.choice(doc_templates)
    dept = random.choice(agencies)[0]
    title = template.format(dept=dept)
    agency_id = random.randint(1, 12)
    status = random.choice(statuses)
    days_ago = random.randint(0, 180)
    security = random.choices(
        ["public", "internal", "confidential"], weights=[5, 3, 2]
    )[0]
    cur.execute(
        "INSERT INTO documents (title, doc_type, agency_id, status, security_level, created_at) VALUES (?, ?, ?, ?, ?, SYS_DATETIME - INTERVAL ? DAY)",
        [title, doc_type, agency_id, status, security, days_ago],
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

actions = ["submit", "review", "approve", "approve", "reject", "return"]
for doc_id in range(1, 301):
    steps = random.randint(1, 4)
    for step in range(1, steps + 1):
        action = random.choice(actions)
        actor = random.choice(["과장", "부장", "실장", "국장", "차관", "장관"])
        comment = random.choice(
            [
                "검토 완료. 승인합니다.",
                "예산 반영 필요. 보완 후 재상신 바랍니다.",
                "협조 부처 의견 확인 요청.",
                "규정 위배 사항 없음.",
                "법제처 협의 완료.",
                None,
            ]
        )
        cur.execute(
            "INSERT INTO approvals (document_id, step, action, actor, comment, acted_at) VALUES (?, ?, ?, ?, ?, SYS_DATETIME - INTERVAL ? HOUR)",
            [doc_id, step, action, actor, comment, random.randint(1, 720)],
        )

conn.commit()

cur.execute("SELECT COUNT(*) FROM agencies")
print(f"Agencies: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM documents")
print(f"Documents: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM approvals")
print(f"Approvals: {cur.fetchone()[0]}")

# Demo queries that will be asked via Claude
cur.execute("""
    SELECT a.name, COUNT(*) as cnt, SUM(CASE WHEN d.status='pending' THEN 1 ELSE 0 END) as pending
    FROM documents d JOIN agencies a ON d.agency_id = a.id
    GROUP BY a.name ORDER BY cnt DESC LIMIT 5
""")
print("\nTop 5 agencies by document count:")
for row in cur:
    print(f"  {row[0]}: {row[1]} docs ({row[2]} pending)")

cur.execute("SELECT status, COUNT(*) FROM documents GROUP BY status")
print("\nDocument status:")
for row in cur:
    print(f"  {row[0]}: {row[1]}")

cur.close()
conn.close()
print("\n✓ On-nara demo data ready")
