from flask import Blueprint, request, jsonify
from db.db import get_db

reports_bp = Blueprint("reports", __name__)

@reports_bp.get("/monthly")
def monthly_report():
    month = request.args.get("month")
    if not month:
        return jsonify({"error":"month param required"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) AS total FROM expenses WHERE strftime('%Y-%m', date)=?", (month,))
    total = cur.fetchone()["total"] or 0

    cur.execute("SELECT category, SUM(amount) AS total FROM expenses WHERE strftime('%Y-%m', date)=? GROUP BY category ORDER BY total DESC", (month,))
    breakdown = [dict(row) for row in cur.fetchall()]

    cur.execute("SELECT date, SUM(amount) AS total FROM expenses WHERE strftime('%Y-%m', date)=? GROUP BY date ORDER BY date", (month,))
    daily = [dict(row) for row in cur.fetchall()]

    return jsonify({"total": total, "breakdown": breakdown, "daily": daily})
