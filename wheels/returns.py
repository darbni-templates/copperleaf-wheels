"""Returns: the desk marks a car as returned, and it is free again."""

from flask import Blueprint

from wheels import bookings, db

bp = Blueprint("returns", __name__)


@bp.post("/api/bookings/<code>/return")
def return_car(code):
    conn = db.connect()
    try:
        booking = bookings.find_booking(conn, code)
        if booking is None:
            return {"error": "booking not found"}, 404
        if booking["status"] != "booked":
            return {"error": "booking is closed"}, 409
        conn.execute("UPDATE bookings SET status = 'returned' WHERE id = ?", (booking["id"],))
        conn.commit()
    finally:
        conn.close()
    return {"code": bookings.code_of(booking), "status": "returned"}
