"""Pick a car: a chat that suggests cars from our fleet. Only the page exists so far."""

from flask import Blueprint, render_template

bp = Blueprint("assistant", __name__)


@bp.get("/pick")
def pick_page():
    return render_template("pick.html")
