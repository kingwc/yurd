import sys, os
sys.path.append('../myapp')
from src import main
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
    #Test getting the current user
    response = client.get("/accounts/currentuser", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    responseJSON = response.json()
    assert responseJSON.get("email") == "test@email.com"
    assert responseJSON.get("username") == "username"
    assert responseJSON.get("first_name") == "Test"
    assert responseJSON.get("last_name") == "User"
    assert responseJSON.get("id") == 1
    assert responseJSON.get("is_active") == True

def test_createEvent():
    #Test creating an event
    response = client.post("/events/create", headers={"Authorization": "Bearer " + token}, 
        json={
            "title": "Test Event",
            "description": "This is a test event",
            "is_public": True
        })
    assert response.status_code == 200
    responseJSON = response.json()
    assert responseJSON.get("title") == "Test Event"
    assert responseJSON.get("description") == "This is a test event"
    assert responseJSON.get("is_public") == True
    assert responseJSON.get("hub_id") == None
    assert responseJSON.get("id") == 1

    #Test creating an event, unathorized
    response = client.post("/events/create", 
        json={
            "title": "Test Event",
            "description": "This is a test event",
            "is_public": True
        })
    assert response.status_code == 401

def test_getMyEvents():
    #Test getting all events for user
    response = client.get("/events/myevents", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    responseJSONList = response.json()
    assert responseJSONList[0].get("title") == "Test Event"
    assert responseJSONList[0].get("description") == "This is a test event"
    assert responseJSONList[0].get("is_public") == True
    assert responseJSONList[0].get("hub_id") == None
    assert responseJSONList[0].get("id") == 1

    #Test getting all events for invalid user
    response = client.get("/events/myevents")
    assert response.status_code == 401

def test_getEvent():
    #Test getting an event by id
    response = client.get("/events/1")
    assert response.status_code == 200
    responseJSON = response.json()
    assert responseJSON.get("title") == "Test Event"
    assert responseJSON.get("description") == "This is a test event"
    assert responseJSON.get("is_public") == True
    assert responseJSON.get("hub_id") == None
    assert responseJSON.get("id") == 1

@pytest.fixture(scope='session', autouse=True)
def teardown():
    yield None
    # Will be executed after the last test
    os.remove('test.db')