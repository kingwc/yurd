import sys
sys.path.append('../myapp')
from src import main
from fastapi.testclient import TestClient

app = main.app

client = TestClient(app)

def test_items():
    response = client.get("/items", headers={"Authorization": "Bearer token"})
    assert response.status_code == 200
    assert response.json() == {"token": "token"}
   