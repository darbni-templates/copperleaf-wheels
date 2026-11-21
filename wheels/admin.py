"""Pages for the desk staff. They need ?token=<ADMIN_TOKEN> (settings.py)."""

import csv
import io

from flask import Blueprint, abort, current_app, render_template, request

from wheels import bookings, db

bp = Blueprint("admin", __name__)


def all_bookings(conn):
    return conn.execute(
        "SELECT bookings.*, cars.name AS car_name, drivers.name AS driver_name,"
        " drivers.licence FROM bookings JOIN cars ON cars.id = bookings.car_id"
        " JOIN drivers ON drivers.id = bookings.driver_id ORDER BY bookings.id"
    ).fetchall()


@bp.get("/admin/bookings")
def booking_list():
    if request.args.get("token") != current_app.config["ADMIN_TOKEN"]:
        abort(404)  # strangers don't learn that the page exists
    conn = db.connect()
    try:
        rows = all_bookings(conn)
    finally:
        conn.close()
    return render_template("admin_bookings.html", rows=rows, code_of=bookings.code_of)


@bp.get("/admin/export.csv")
def export():
    """Every booking as CSV, for the accountant's spreadsheet."""
    conn = db.connect()
    try:
        rows = all_bookings(conn)
    finally:
        conn.close()
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["code", "car", "driver", "licence", "start", "end", "total_fils", "status"])
    for row in rows:
        writer.writerow([
            bookings.code_of(row), row["car_name"], row["driver_name"], row["licence"],
            row["start_date"], row["end_date"], row["total_fils"], row["status"],
        ])
    return out.getvalue(), 200, {"Content-Type": "text/csv; charset=utf-8"}
