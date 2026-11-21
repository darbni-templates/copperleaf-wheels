import pytest

from wheels import create_app


@pytest.fixture
def app(tmp_path):
    # NOW fixes Wheels' clock (clock.now()): Tuesday 17 November 2026, 10:00 in Bahrain.
    return create_app(
        {"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite"), "NOW": "2026-11-17T10:00"}
    )


@pytest.fixture
def client(app):
    return app.test_client()


def booking(car=4, start="2026-11-20", end="2026-11-22", **more):
    """The JSON of a booking for the demo driver (id 1)."""
    return {"car": car, "driver": 1, "start": start, "end": end, "insurance": "basic", **more}
