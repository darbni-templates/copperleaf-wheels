"""The fleet: the list of cars and a page per car."""

from flask import Blueprint, abort, render_template

from wheels import db, pricing

bp = Blueprint("cars", __name__)


def find_car(conn, car_id):
    """The car with this id, or None."""
    return conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()


@bp.get("/cars")
def car_list():
    conn = db.connect()
    try:
        cars = conn.execute("SELECT * FROM cars ORDER BY daily_fils, id").fetchall()
    finally:
        conn.close()
    return render_template("cars.html", cars=cars)


@bp.get("/cars/<int:car_id>")
def car_page(car_id):
    conn = db.connect()
    try:
        car = find_car(conn, car_id)
    finally:
        conn.close()
    if car is None:
        abort(404)
    return render_template("car.html", car=car, plans=pricing.INSURANCE)
