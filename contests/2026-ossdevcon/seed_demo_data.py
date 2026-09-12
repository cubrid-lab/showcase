"""Seed demo data for the contest presentation — run before the demo."""
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
