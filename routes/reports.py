from flask import Blueprint, request, jsonify
from db.db import get_db
from utils.auth_middleware import require_auth

reports_bp = Blueprint("reports", __name__)

@reports_bp.get("/monthly")
@require_auth
def monthly_report():
    month = request.args.get("month")
    if not month:
        return jsonify({"error": "month param required"}), 400

    user_id = request.user_id
    conn = get_db()
    cur = conn.cursor()

    # Total
    cur.execute("""
        SELECT SUM(amount) AS total 
        FROM expenses 
        WHERE user_id=? AND strftime('%Y-%m', date)=?
    """, (user_id, month))
    total = cur.fetchone()["total"] or 0

    # Category breakdown
    cur.execute("""
        SELECT category, SUM(amount) AS total 
        FROM expenses 
        WHERE user_id=? AND strftime('%Y-%m', date)=?
        GROUP BY category
        ORDER BY total DESC
    """, (user_id, month))
    breakdown = [dict(row) for row in cur.fetchall()]

    # Daily trend
    cur.execute("""
        SELECT date, SUM(amount) AS total
        FROM expenses
        WHERE user_id=? AND strftime('%Y-%m', date)=?
        GROUP BY date
        ORDER BY date
    """, (user_id, month))
    daily = [dict(row) for row in cur.fetchall()]

    return jsonify({"total": total, "breakdown": breakdown, "daily": daily})
