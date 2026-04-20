import pytest
from fastapi.testclient import TestClient
from backend.main import app
from datetime import date

client = TestClient(app)

@pytest.fixture
def user_token():
    # Register
    r = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User"
    })
    assert r.status_code == 200
    # Login
    r = client.post("/api/auth/login", data={"username": "test@example.com", "password": "testpassword"})
    assert r.status_code == 200
    return r.json()["access_token"]

def test_register_and_login():
    r = client.post("/api/auth/register", json={
        "email": "user2@example.com",
        "password": "password123",
        "full_name": "User Two"
    })
    assert r.status_code == 200
    r = client.post("/api/auth/login", data={"username": "user2@example.com", "password": "password123"})
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_crop_crud(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    crop = {
        "crop_type": "Wheat",
        "planting_date": str(date.today()),
        "expected_harvest_date": str(date.today()),
        "growth_stage": "Seedling"
    }
    r = client.post("/api/crops", json=crop, headers=headers)
    assert r.status_code == 200
    crop_id = r.json()["id"]
    r = client.get("/api/crops", headers=headers)
    assert r.status_code == 200
    assert any(c["id"] == crop_id for c in r.json())
    r = client.put(f"/api/crops/{crop_id}", json={"growth_stage": "Mature"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["growth_stage"] == "Mature"
    r = client.delete(f"/api/crops/{crop_id}", headers=headers)
    assert r.status_code == 200

def test_task_crud(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Create crop first
    crop = {
        "crop_type": "Corn",
        "planting_date": str(date.today()),
        "expected_harvest_date": str(date.today()),
    }
    r = client.post("/api/crops", json=crop, headers=headers)
    crop_id = r.json()["id"]
    task = {
        "crop_id": crop_id,
        "title": "Watering",
        "due_date": str(date.today()),
    }
    r = client.post("/api/tasks", json=task, headers=headers)
    assert r.status_code == 200
    task_id = r.json()["id"]
    r = client.get("/api/tasks", headers=headers)
    assert r.status_code == 200
    assert any(t["id"] == task_id for t in r.json())
    r = client.put(f"/api/tasks/{task_id}", json={"status": "in_progress"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"
    r = client.post(f"/api/tasks/{task_id}/complete", headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
    r = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert r.status_code == 200

def test_book_catalog():
    book = {
        "title": "Book 1",
        "author": "Author 1",
        "price": 10.5,
        "description": "A test book"
    }
    r = client.post("/api/books", json=book)
    assert r.status_code == 200
    book_id = r.json()["id"]
    r = client.get("/api/books")
    assert r.status_code == 200
    assert any(b["id"] == book_id for b in r.json())
    r = client.put(f"/api/books/{book_id}", json={"price": 12.0})
    assert r.status_code == 200
    assert r.json()["price"] == 12.0
    r = client.delete(f"/api/books/{book_id}")
    assert r.status_code == 200

def test_cart_and_order(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Add book
    book = {
        "title": "Book 2",
        "author": "Author 2",
        "price": 20.0
    }
    r = client.post("/api/books", json=book)
    book_id = r.json()["id"]
    # Add to cart
    r = client.post("/api/cart/add", json={"book_id": book_id, "quantity": 2}, headers=headers)
    assert r.status_code == 200
    assert any(i["book_id"] == book_id for i in r.json()["items"])
    # Remove from cart
    r = client.post("/api/cart/remove", params={"book_id": book_id}, headers=headers)
    assert r.status_code == 200
    # Add again and order
    r = client.post("/api/cart/add", json={"book_id": book_id, "quantity": 1}, headers=headers)
    r = client.post("/api/orders", json={
        "items": [{"book_id": book_id, "quantity": 1}],
        "shipping_address": "123 Main St",
        "payment_method": "card"
    }, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "confirmed"
    r = client.get("/api/orders", headers=headers)
    assert r.status_code == 200

def test_restaurant_crud():
    rest = {
        "name": "Testaurant",
        "address": "1 Food St",
        "contact": "1234567890",
        "hours": "9-9",
        "rating": 4.5,
        "menu": [{"item": "Pizza", "price": 12.0}]
    }
    r = client.post("/api/restaurants", json=rest)
    assert r.status_code == 200
    rest_id = r.json()["id"]
    r = client.get("/api/restaurants")
    assert r.status_code == 200
    assert any(rst["id"] == rest_id for rst in r.json())
    r = client.put(f"/api/restaurants/{rest_id}", json={"rating": 5.0})
    assert r.status_code == 200
    assert r.json()["rating"] == 5.0
    r = client.get(f"/api/restaurants/{rest_id}")
    assert r.status_code == 200
