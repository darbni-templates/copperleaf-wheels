"""Bookings: a price quote, booking a car (JSON for the app, a form on the car page), a booking's
details and cancelling it."""

import re
from datetime import date

from flask import Blueprint, abort, redirect, render_template, request

from wheels import availability, cars, clock, db, drivers, pricing, promo

bp = Blueprint("bookings", __name__)
MAX_DAYS = 90
CODE = re.compile(r"WH-(\d{4,})")


class BookingError(Exception):
    """A booking we refuse: the HTTP status and the message for the customer."""

    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def code_of(booking):
    """The code customers see: WH- and 1000 + the booking's id (WH-1001, WH-1002, ...)."""
    return f"WH-{1000 + booking['id']}"


def find_booking(conn, code):
    """The booking with this code, or None."""
    match = CODE.fullmatch(code or "")
    if match is None:
        return None
    return conn.execute(
        "SELECT * FROM bookings WHERE id = ?", (int(match[1]) - 1000,)
    ).fetchone()


def whole(value):
    """An id from JSON (4) or a form or query string ("4"), or None."""
    text = str(value) if isinstance(value, int | str) and not isinstance(value, bool) else ""
    return int(text) if text.isdigit() else None


def read_dates(start_text, end_text):
    """The pickup and return days of a request, as two datetime.date."""
    try:
        start, end = date.fromisoformat(start_text), date.fromisoformat(end_text)
    except (TypeError, ValueError):
        raise BookingError(400, "bad dates") from None
    if end < start:
        raise BookingError(400, "return before pickup")
    if start < clock.today():
        raise BookingError(400, "pickup in the past")
    if pricing.rental_days(start, end) > MAX_DAYS:
        raise BookingError(400, f"at most {MAX_DAYS} days")
    return start, end


def read_request(conn, data, need_driver=True):
    """Checks what a customer asked for. Returns a dict with the car and driver rows, the dates,
    the insurance key and the promo row (or None). Raises BookingError."""
    car = cars.find_car(conn, whole(data.get("car")))
    if car is None:
        raise BookingError(404, "car not found")
    driver = None
    if need_driver or data.get("driver") is not None:
        driver = drivers.find_driver(conn, whole(data.get("driver")))
        if driver is None:
            raise BookingError(404, "driver not found")
    start, end = read_dates(data.get("start"), data.get("end"))
    insurance = data.get("insurance") or "basic"
    if insurance not in pricing.INSURANCE:
        raise BookingError(400, "unknown insurance")
    code = (data.get("promo") or "").strip()
    try:
        promo_row = promo.check(conn, code) if code else None
    except promo.PromoError as exc:
        raise BookingError(400, str(exc)) from None
    return {
        "car": car,
        "driver": driver,
        "start": start,
        "end": end,
        "insurance": insurance,
        "promo": promo_row,
    }


def price(car, start, end, insurance, promo_row):
    """What a rental costs, in fils."""
    days = pricing.rental_days(start, end)
    car_fils = pricing.car_total(car["daily_fils"], days)
    insurance_fils = pricing.INSURANCE[insurance]["daily_fils"] * days
    discount_fils = 0
    if promo_row is not None:
        # A percentage off the car's price, rounded half up to the fils.
        discount_fils = (car_fils * promo_row["percent"] + 50) // 100
    return {
        "days": days,
        "car_fils": car_fils,
        "insurance_fils": insurance_fils,
        "discount_fils": discount_fils,
        "total_fils": car_fils + insurance_fils - discount_fils,
    }


def create_booking(conn, data):
    """Books the car. Returns the new booking row. Raises BookingError."""
    asked = read_request(conn, data)
    if not availability.is_free(conn, asked["car"]["id"], asked["start"], asked["end"]):
        raise BookingError(409, "car not available")
    cost = price(asked["car"], asked["start"], asked["end"], asked["insurance"], asked["promo"])
    cursor = conn.execute(
        "INSERT INTO bookings (car_id, driver_id, start_date, end_date, insurance, promo_code,"
        " total_fils, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, 'booked', ?)",
        (
            asked["car"]["id"],
            asked["driver"]["id"],
            asked["start"].isoformat(),
            asked["end"].isoformat(),
            asked["insurance"],
            asked["promo"]["code"] if asked["promo"] else None,
            cost["total_fils"],
            clock.now().isoformat(timespec="minutes"),
        ),
    )
    conn.commit()
    return conn.execute("SELECT * FROM bookings WHERE id = ?", (cursor.lastrowid,)).fetchone()


def as_json(booking):
    start, end = date.fromisoformat(booking["start_date"]), date.fromisoformat(booking["end_date"])
    return {
        "code": code_of(booking),
        "car": booking["car_id"],
        "driver": booking["driver_id"],
        "start": booking["start_date"],
        "end": booking["end_date"],
        "days": pricing.rental_days(start, end),
        "insurance": booking["insurance"],
        "promo": booking["promo_code"],
        "total_fils": booking["total_fils"],
        "status": booking["status"],
    }


@bp.get("/api/quote")
def quote():
    """GET /api/quote?car=4&start=2026-11-20&end=2026-11-22&insurance=basic&promo=...&driver=..."""
    conn = db.connect()
    try:
        asked = read_request(conn, request.args, need_driver=False)
    except BookingError as exc:
        return {"error": exc.message}, exc.status
    finally:
        conn.close()
    cost = price(asked["car"], asked["start"], asked["end"], asked["insurance"], asked["promo"])
    return {"car": asked["car"]["id"], **cost}


@bp.post("/api/bookings")
def create():
    data = request.get_json(silent=True) or {}
    conn = db.connect()
    try:
        booking = create_booking(conn, data)
    except BookingError as exc:
        return {"error": exc.message}, exc.status
    finally:
        conn.close()
    cost = as_json(booking)
    return {"code": cost["code"], "days": cost["days"], "total_fils": cost["total_fils"],
            "status": "booked"}, 201


@bp.post("/cars/<int:car_id>/book")
def book_form(car_id):
    """The booking form on the car page: the driver's details and the rental."""
    form = request.form
    conn = db.connect()
    try:
        try:
            driver_id = drivers.add_driver(
                conn, form.get("name"), form.get("birth_date"), form.get("licence")
            )
            booking = create_booking(conn, {**form.to_dict(), "car": car_id, "driver": driver_id})
        except ValueError as exc:
            error, status = str(exc), 400
        except BookingError as exc:
            error, status = exc.message, exc.status
        else:
            return redirect(f"/bookings/{code_of(booking)}")
        car = cars.find_car(conn, car_id)
    finally:
        conn.close()
    if car is None:
        abort(404)
    return render_template("car.html", car=car, plans=pricing.INSURANCE, error=error), status


@bp.get("/api/bookings/<code>")
def show(code):
    conn = db.connect()
    try:
        booking = find_booking(conn, code)
    finally:
        conn.close()
    if booking is None:
        return {"error": "booking not found"}, 404
    return as_json(booking)


@bp.post("/api/bookings/<code>/cancel")
def cancel(code):
    conn = db.connect()
    try:
        booking = find_booking(conn, code)
        if booking is None:
            return {"error": "booking not found"}, 404
        if booking["status"] != "booked":
            return {"error": "booking is closed"}, 409
        conn.execute("UPDATE bookings SET status = 'cancelled' WHERE id = ?", (booking["id"],))
        conn.commit()
    finally:
        conn.close()
    return {"code": code_of(booking), "status": "cancelled"}
