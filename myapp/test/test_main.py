import sys
sys.path.append('../myapp')
from src import main
from fastapi.testclient import TestClient

app = main.app

client = TestClient(app)

#def test_items():
#    response = client.get("/login/items", headers={"Authorization": "Bearer token"})
#    assert response.status_code == 200
#    assert response.json() == {"token": "token"}

def test_signup():
    response = client.post("/accounts/signup", json={
        "email": "string",
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "string"
    })
    assert response.status_code == 200

def test_login():
    response = client.post("/accounts/login")
    assert response.status_code == 200

def test_get_user_me():
    response = client.get("/accounts/users/me")
    assert response.status_code == 200