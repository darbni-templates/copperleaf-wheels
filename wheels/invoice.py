"""The invoice page of a booking: /bookings/<code>, one line per thing the customer pays for."""

from datetime import date

from flask import Blueprint, abort, render_template

from wheels import bookings, cars, db, pricing

bp = Blueprint("invoice", __name__)


def days_text(days):
    return f"{days} day" + ("" if days == 1 else "s")


def invoice_lines(conn, booking, car):
    """[(label, fils), ...]: what the customer pays for, then the total. A discount is negative."""
    start = date.fromisoformat(booking["start_date"])
    end = date.fromisoformat(booking["end_date"])
    days = pricing.rental_days(start, end)
    rental = days * car["daily_fils"]
    plan = pricing.INSURANCE[booking["insurance"]]
    lines = [
        (f"Rental ({days_text(days)})", rental),
        (f"Insurance ({plan['name']})", days * plan["daily_fils"]),
    ]
    if booking["promo_code"]:
        row = conn.execute(
            "SELECT percent FROM promos WHERE code = ?", (booking["promo_code"],)
        ).fetchone()
        discount = (rental * row["percent"] + 50) // 100
        lines.append((f"Promo {booking['promo_code']}", -discount))
    lines.append(("Total", sum(fils for _, fils in lines)))
    return lines


@bp.get("/bookings/<code>")
def invoice(code):
    conn = db.connect()
    try:
        booking = bookings.find_booking(conn, code)
        if booking is None:
            abort(404)
        car = cars.find_car(conn, booking["car_id"])
        lines = invoice_lines(conn, booking, car)
    finally:
        conn.close()
    return render_template(
        "invoice.html", code=bookings.code_of(booking), booking=booking, car=car, lines=lines
    )
