from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_jobs():
    response = client.get("/api/jobs", params={"query": "developer", "location": "remote"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_jobs_no_results():
    response = client.get("/api/jobs", params={"query": "nonexistentjob", "location": "nowhere"})
    assert response.status_code == 200
    assert response.json() == []