from conftest import booking


def test_booking_a_car(client):
    response = client.post("/api/bookings", json=booking())
    assert response.status_code == 201
    assert response.json["code"] == "WH-1001"
    assert response.json["status"] == "booked"


def test_a_booked_car_cannot_be_booked_again(client):
    client.post("/api/bookings", json=booking())
    response = client.post("/api/bookings", json=booking(start="2026-11-21", end="2026-11-23"))
    assert response.status_code == 409
    assert response.json == {"error": "car not available"}


def test_a_cancelled_booking_frees_the_car(client):
    client.post("/api/bookings", json=booking())
    assert client.post("/api/bookings/WH-1001/cancel").json["status"] == "cancelled"
    assert client.post("/api/bookings", json=booking()).status_code == 201


def test_the_invoice_page(client):
    client.post("/api/bookings", json=booking())
    text = client.get("/bookings/WH-1001").text
    assert "Invoice WH-1001" in text
    assert "Toyota Yaris" in text


def test_returning_a_car(client):
    client.post("/api/bookings", json=booking())
    response = client.post("/api/bookings/WH-1001/return")
    assert response.json == {"code": "WH-1001", "status": "returned"}


def test_a_pickup_in_the_past_is_refused(client):
    response = client.post("/api/bookings", json=booking(start="2026-11-01", end="2026-11-02"))
    assert response.status_code == 400


def test_the_promo_code_takes_ten_percent_off_the_car(client):
    # The Yaris costs 10.000 BHD per day: 10% of a one-day rental is 1.000 BHD.
    response = client.get("/api/quote?car=4&start=2026-11-20&end=2026-11-20&promo=WELCOME10")
    assert response.json["discount_fils"] == 1000


def test_the_form_on_the_car_page_books_and_shows_the_invoice(client):
    form = {
        "name": "Sara Ali", "birth_date": "1995-03-02", "licence": "BH-2015-1234",
        "start": "2026-11-20", "end": "2026-11-22", "insurance": "full", "promo": "",
    }
    response = client.post("/cars/9/book", data=form, follow_redirects=True)
    assert "Invoice WH-1001" in response.text
