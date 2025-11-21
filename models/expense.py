from db.db import get_db

def get_all(user_id, month=None):
    conn = get_db()
    cur = conn.cursor()

    if month:
        cur.execute("""
            SELECT * FROM expenses 
            WHERE user_id=? AND strftime('%Y-%m', date)=?
            ORDER BY date DESC
        """, (user_id, month))
    else:
        cur.execute("SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC", (user_id,))

    return [dict(row) for row in cur.fetchall()]


def add(data, user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO expenses (date, amount, category, merchant, notes, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["date"],
        data["amount"],
        data["category"],
        data.get("merchant"),
        data.get("notes"),
        user_id
    ))
    conn.commit()
    return cur.lastrowid


def update(id, data, user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE expenses
        SET date=?, amount=?, category=?, merchant=?, notes=?
        WHERE id=? AND user_id=?
    """, (
        data["date"],
        data["amount"],
        data["category"],
        data.get("merchant"),
        data.get("notes"),
        id,
        user_id
    ))
    conn.commit()
    return True


def delete(id, user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (id, user_id))
    conn.commit()
    return True
