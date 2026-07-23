import pytest

from app import create_app
from app.models import db


@pytest.fixture()
def client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with app.app_context():
        db.create_all()
    return app.test_client()


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_read_post(client):
    payload = {
        "title": "My First Post",
        "excerpt": "A useful summary",
        "content": "Longer article body",
        "author": "William",
    }
    created = client.post("/api/posts", json=payload)
    assert created.status_code == 201
    assert created.get_json()["slug"] == "my-first-post"

    fetched = client.get("/api/posts/my-first-post")
    assert fetched.status_code == 200
    assert fetched.get_json()["title"] == "My First Post"


def test_validation(client):
    response = client.post("/api/posts", json={"title": ""})
    assert response.status_code == 400
    assert "Missing required" in response.get_json()["error"]


def test_update_and_delete_post(client):
    client.post(
        "/api/posts",
        json={
            "title": "Draft",
            "excerpt": "Draft excerpt",
            "content": "Draft content",
            "author": "Editor",
        },
    )

    updated = client.put("/api/posts/draft", json={"title": "Published"})
    assert updated.status_code == 200
    assert updated.get_json()["title"] == "Published"

    deleted = client.delete("/api/posts/draft")
    assert deleted.status_code == 204
    assert client.get("/api/posts/draft").status_code == 404
