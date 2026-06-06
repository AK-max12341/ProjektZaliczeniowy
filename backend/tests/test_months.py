from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_months():

    response = client.get("/months/2025")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0