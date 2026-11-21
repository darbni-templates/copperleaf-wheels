"""Drivers: who drives the car. Every booking has one."""

from datetime import date

from flask import Blueprint, request

from wheels import db

bp = Blueprint("drivers", __name__)


def find_driver(conn, driver_id):
    """The driver with this id, or None."""
    return conn.execute("SELECT * FROM drivers WHERE id = ?", (driver_id,)).fetchone()


def add_driver(conn, name, birth_date, licence):
    """Saves a driver and returns the new id. Raises ValueError with a message for the customer."""
    name = name.strip() if isinstance(name, str) else ""
    licence = licence.strip() if isinstance(licence, str) else ""
    if not name:
        raise ValueError("missing name")
    if not licence:
        raise ValueError("missing licence")
    try:
        born = date.fromisoformat(birth_date)
    except (TypeError, ValueError):
        raise ValueError("bad birth date") from None
    cursor = conn.execute(
        "INSERT INTO drivers (name, birth_date, licence) VALUES (?, ?, ?)",
        (name, born.isoformat(), licence),
    )
    conn.commit()
    return cursor.lastrowid


@bp.post("/api/drivers")
def create():
    data = request.get_json(silent=True) or {}
    conn = db.connect()
    try:
        driver_id = add_driver(conn, data.get("name"), data.get("birth_date"), data.get("licence"))
    except ValueError as exc:
        return {"error": str(exc)}, 400
    finally:
        conn.close()
    return {"id": driver_id}, 201


@bp.get("/api/drivers/<int:driver_id>")
def show(driver_id):
    conn = db.connect()
    try:
        driver = find_driver(conn, driver_id)
    finally:
        conn.close()
    if driver is None:
        return {"error": "driver not found"}, 404
    return {"id": driver["id"], "name": driver["name"], "birth_date": driver["birth_date"]}
