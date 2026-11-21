def test_the_search_form(client):
    assert "Find a free car" in client.get("/search").text


def test_a_search_lists_cars(client):
    text = client.get("/search?start=2026-11-20&end=2026-11-22").text
    assert "cars free from 2026-11-20 to 2026-11-22" in text
    assert "Chevrolet Spark" in text


def test_a_search_with_filters(client):
    text = client.get("/search?start=2026-11-20&end=2026-11-22&seats=9").text
    assert "Toyota Hiace" in text
    assert "Toyota Yaris" not in text
