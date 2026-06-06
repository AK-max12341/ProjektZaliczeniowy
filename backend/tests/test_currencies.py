from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_currencies_by_date():

    response = client.get("/currencies/2025-01-02")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

    first_currency = data[0]

    assert "currency" in first_currency
    assert "code" in first_currency
    assert "rate" in first_currency
    assert "date" in first_currency