import os

os.environ[
    "DATABASE_URL"
] = "sqlite:///./test_pocketsmart.db"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_register_and_session():

    email = "testuser@example.com"


    response = client.post(

        "/api/register",

        json={
            "name": "Test User",
            "email": email,
            "password": "secret123"
        }
    )


    assert response.status_code in (
        200,
        409
    )


    token = response.json().get(
        "access_token"
    )


    if token:

        session_response = client.get(

                "/api/session-info",

                headers={
                    "Authorization":
                        f"Bearer {token}"
                }
            )

        assert (
            session_response.status_code
            == 200
        )