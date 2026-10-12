def test_post_car_returns_201_and_json(client):
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"

def test_invalid_year_is_not_saved(client):
    bad_payload = {
        "make": "Honda",
        "model": "Civic",
        "year": 1800,
        "color": "Grey"
    }
    resp = client.post("/api/cars", json=bad_payload)
    assert resp.status_code == 422

    get_resp = client.get("/api/cars")
    car_list = get_resp.json()
    assert len(car_list) == 0
