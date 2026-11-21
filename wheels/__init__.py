"""Wheels: rent a car in Bahrain. Customers search for a free car, book it and get an invoice."""

from flask import Flask

from wheels import (
    admin,
    assistant,
    bookings,
    cars,
    clock,
    db,
    drivers,
    invoice,
    money,
    pages,
    paylater,
    returns,
    search,
    settings,
)


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        DATABASE="wheels.sqlite",
        SECRET_KEY=settings.SECRET_KEY,
        ADMIN_TOKEN=settings.ADMIN_TOKEN,
    )
    app.config.update(config or {})
    db.migrate(app.config["DATABASE"])  # runs the new files in wheels/migrations/, once each
    # One blueprint per area of the app.
    areas = (pages, cars, search, bookings, invoice, drivers, returns, paylater, assistant, admin)
    for area in areas:
        app.register_blueprint(area.bp)
    app.jinja_env.filters["bhd"] = money.bhd  # {{ 12000 | bhd }} shows 12.000 BHD
    app.jinja_env.globals["now"] = clock.now  # {{ now() }}: Bahrain time, in templates too
    return app
