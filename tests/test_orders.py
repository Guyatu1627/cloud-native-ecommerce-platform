from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order_unauthorized():
    response = client.post("/api/v1/orders/", json={
        "items": [{"product_id": 1, "quantity": 2}]
    })
    assert response.status_code == 401

def test_list_orders_unauthorized():
    response = client.get("/api/v1/orders/")
    assert response.status_code == 401