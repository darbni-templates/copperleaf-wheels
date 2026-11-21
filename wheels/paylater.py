"""PayLater: "book now, pay in 3". The invoice page links here; the customer starts a plan and
PayLater's site takes over. The sandbox never charges anyone."""

from flask import Blueprint, abort, render_template

from wheels import bookings, db, settings

bp = Blueprint("paylater", __name__)


def instalment(total_fils):
    """One of the PAYLATER_INSTALMENTS payments, rounded up to the fils."""
    return -(-total_fils // settings.PAYLATER_INSTALMENTS)


@bp.get("/paylater/<code>")
def offer(code):
    conn = db.connect()
    try:
        booking = bookings.find_booking(conn, code)
    finally:
        conn.close()
    if booking is None:
        abort(404)
    return render_template(
        "paylater.html",
        code=bookings.code_of(booking),
        count=settings.PAYLATER_INSTALMENTS,
        each=instalment(booking["total_fils"]),
    )


@bp.post("/paylater/<code>")
def start_plan(code):
    conn = db.connect()
    try:
        booking = bookings.find_booking(conn, code)
    finally:
        conn.close()
    if booking is None:
        return {"error": "booking not found"}, 404
    # The real provider gets a POST to PAYLATER_URL; the sandbox only answers "pending".
    return {
        "provider": "PayLater",
        "merchant": settings.PAYLATER_MERCHANT_ID,
        "url": settings.PAYLATER_URL,
        "instalments": settings.PAYLATER_INSTALMENTS,
        "status": "pending",
    }
