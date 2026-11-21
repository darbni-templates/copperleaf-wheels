"""Wheels' clock. Use clock.now() or clock.today(), never datetime.now() or date.today(): tests
(yours and Darbni's) set the time with the app's NOW setting."""

from datetime import date, datetime, timedelta, timezone

from flask import current_app

# Asia/Bahrain: UTC+3 all year (Bahrain has no summer time).
BAHRAIN = timezone(timedelta(hours=3), "Asia/Bahrain")


def now() -> datetime:
    """The time in Bahrain now, or app.config["NOW"] if it is set (Bahrain time, written like
    "2026-11-17T10:00")."""
    fixed = current_app.config.get("NOW")
    if fixed:
        return datetime.fromisoformat(fixed).replace(tzinfo=BAHRAIN)
    return datetime.now(BAHRAIN)


def today() -> date:
    return now().date()
