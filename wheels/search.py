"""Search: the cars that are free between a pickup day and a return day."""

from datetime import date

from flask import Blueprint, render_template, request

from wheels import db

bp = Blueprint("search", __name__)
SHOWN = 20  # the page shows the 20 cheapest matches


@bp.get("/search")
def search():
    start_text = request.args.get("start", "")
    end_text = request.args.get("end", "")
    seats = request.args.get("seats", 0, type=int)
    transmission = request.args.get("transmission", "")
    form = {"start": start_text, "end": end_text, "seats": seats, "transmission": transmission}
    if not start_text and not end_text:
        return render_template("search.html", form=form, searched=False)
    try:
        start, end = date.fromisoformat(start_text), date.fromisoformat(end_text)
    except ValueError:
        return render_template("search.html", form=form, searched=False, error=True)

    conn = db.connect()
    try:
        cars = conn.execute("SELECT * FROM cars ORDER BY daily_fils, id").fetchall()
    finally:
        conn.close()
    found = [
        car
        for car in cars
        if car["seats"] >= seats and (not transmission or car["transmission"] == transmission)
    ]
    return render_template(
        "search.html",
        form=form,
        searched=True,
        start=start,
        end=end,
        count=len(found),
        cars=found[:SHOWN],
    )
