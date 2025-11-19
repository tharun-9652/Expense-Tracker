from db.db import get_db

def get_all():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories ORDER BY name")
    return [dict(row) for row in cur.fetchall()]

def add(name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    return cur.lastrowid
