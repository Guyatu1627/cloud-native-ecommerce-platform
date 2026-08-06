from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_products_empty():
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product_unauthorized():
    response = client.post("/api/v1/products/", json={
        "title": "Test Laptop",
        "price": 999.99,
        "stock": 10
    })
    assert response.status_code == 401