from db.db import get_db

def get_all(month=None):
    conn = get_db()
    cur = conn.cursor()
    if month:
        cur.execute("SELECT * FROM expenses WHERE strftime('%Y-%m', date)=? ORDER BY date DESC", (month,))
    else:
        cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    return [dict(row) for row in cur.fetchall()]

def add(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (date, amount, category, merchant, notes) VALUES (?,?,?,?,?)",
        (data["date"], data["amount"], data["category"], data.get("merchant"), data.get("notes"))
    )
    conn.commit()
    return cur.lastrowid

def update(id, data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE expenses SET date=?, amount=?, category=?, merchant=?, notes=? WHERE id=?",
        (data["date"], data["amount"], data["category"], data.get("merchant"), data.get("notes"), id)
    )
    conn.commit()

def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
