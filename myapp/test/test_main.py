import sys, os
sys.path.append('../myapp')
from src.api import main
from fastapi.testclient import TestClient
import pytest

app = main.app

client = TestClient(app)

def test_signup():
    #Test signing up user correctly
    response = client.post("/accounts/signup", json={
        "email": "test@email.com",
        "username": "username",
        "first_name": "Test",
        "last_name": "User",
        "password": "password"
    })
    assert response.status_code == 200
    responseJSON = response.json()
    assert responseJSON.get("username") == "username"
    assert responseJSON.get("last_name") == "User"
    assert responseJSON.get("is_active") == True
    assert responseJSON.get("first_name") == "Test"
    assert responseJSON.get("id") == 1
    assert responseJSON.get("email") == "test@email.com"

    #Test trying to sign up user with same email
    response = client.post("/accounts/signup", json={
        "email": "test@email.com",
        "username": "username",
        "first_name": "Test",
        "last_name": "User",
        "password": "password"
    })
    assert response.status_code == 400

def test_login():
    #Test logging in correct user
    formdatadict = {"username": "username", "password": "password"}
    response = client.post("/accounts/login",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "35"},
        data=formdatadict)
    assert response.status_code == 200
    responseJSON = response.json()
    assert responseJSON.get("token_type") == "bearer"
    global token 
    token = responseJSON.get("access_token")

    #Test logging in incorrect username
    formdataincorrectusername = {"username": "incorrect", "password": "password"}
    response = client.post("/accounts/login",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "35"},
        data=formdataincorrectusername)
    assert response.status_code == 401

    #Test loggin in incorrect password
    formdataincorrectpassword = {"username": "username", "password": "incorrect"}
    response = client.post("/accounts/login",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "35"},
        data=formdataincorrectpassword)
    assert response.status_code == 401

def test_currentuser():
    response = client.get("/accounts/currentuser", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    responseJSON = response.json()
    assert responseJSON.get("email") == "test@email.com"
    assert responseJSON.get("username") == "username"
    assert responseJSON.get("first_name") == "Test"
    assert responseJSON.get("last_name") == "User"
    assert responseJSON.get("id") == 1
    assert responseJSON.get("is_active") == True

@pytest.fixture(scope='session', autouse=True)
def teardown():
    yield None
    # Will be executed after the last test
    os.remove('test.db')