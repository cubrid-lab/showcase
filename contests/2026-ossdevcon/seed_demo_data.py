"""Seed demo data for the contest presentation — run before the demo.

Idempotent: drops and recreates the demo tables (resets AUTO_INCREMENT
serials) and reloads deterministic content on every run.
"""

from __future__ import annotations

import datetime
import random

import pycubrid

conn = pycubrid.connect(host="localhost", port=33000, database="demodb", user="dba")
cur = conn.cursor()

# Idempotent reset — DROP (not DELETE) so AUTO_INCREMENT serials restart at 1;
# a partially-failed earlier run leaves serials advanced otherwise.
for t in ("orders", "products"):
    cur.execute(f"DROP TABLE IF EXISTS {t}")

cur.execute("""
    CREATE TABLE products (
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
    ("Laptop Pro 16", "Electronics", 2450000, 15, {"bestseller", "new"}),
    ("Smartphone X", "Electronics", 1350000, 42, {"bestseller"}),
    ("Wireless Earbuds", "Electronics", 189000, 128, {"new", "sale"}),
    ("Tablet Air", "Electronics", 890000, 35, set()),
    ("Smart Watch", "Electronics", 450000, 67, {"sale"}),
    ("Gaming Mouse", "Accessories", 89000, 210, {"bestseller"}),
    ("Mechanical Keyboard", "Accessories", 159000, 89, {"new"}),
    ("27-inch Monitor", "Accessories", 389000, 23, set()),
    ("USB-C Hub", "Accessories", 45000, 350, {"sale", "bestseller"}),
    ("4K Webcam", "Accessories", 129000, 56, set()),
]

# SET columns take SQL collection literals (cookbook fundamentals pattern:
# fundamentals/pycubrid/10_collection_columns.py) — binding a string for a
# SET column raises "Casting ... to type set is not supported".
for n, c, p, s, t2 in products:
    tags_sql = "SET{" + ", ".join(f"'{t}'" for t in sorted(t2)) + "}"
    cur.execute(
        f"INSERT INTO products (name, category, price, stock, tags) "
        f"VALUES (?, ?, ?, ?, {tags_sql})",
        (n, c, p, s),
    )

cur.execute("""
    CREATE TABLE orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        total_price NUMERIC(12,2),
        order_date DATETIME DEFAULT SYS_DATETIME,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")

# Fetch id/price pairs by query — immune to any serial drift.
cur.execute("SELECT id, price FROM products")
catalog = [(r[0], r[1]) for r in cur.fetchall()]

for _ in range(200):
    pid, price = random.choice(catalog)
    qty = random.randint(1, 5)
    days_ago = random.randint(0, 90)
    dt = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    cur.execute(
        "INSERT INTO orders (product_id, quantity, total_price, order_date) VALUES (?, ?, ?, ?)",
        (pid, qty, price * qty, dt),
    )

conn.commit()
cur.execute("SELECT COUNT(*) FROM products")
print(f"Products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM orders")
print(f"Orders: {cur.fetchone()[0]}")
cur.close()
conn.close()
print("Seed data ready")
