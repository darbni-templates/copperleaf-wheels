def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Rent a car in Bahrain" in response.text


def test_about_page(client):
    assert "About Wheels" in client.get("/about").text


def test_the_cars_page_lists_the_fleet(client):
    text = client.get("/cars").text
    assert "Chevrolet Spark" in text
    assert "7.500 BHD per day" in text


def test_a_car_page_has_the_booking_form(client):
    text = client.get("/cars/4").text
    assert "Toyota Yaris" in text
    assert "Book this car" in text


def test_an_unknown_car_is_404(client):
    assert client.get("/cars/999").status_code == 404


def test_the_pick_page(client):
    assert "Pick a car" in client.get("/pick").text
