from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.board import create_random_board


def test_create_board(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/boards/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_board(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    board = create_random_board(db)
    response = client.get(
        f"{settings.API_V1_STR}/boards/{board.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == board.title
    assert content["description"] == board.description
    assert content["id"] == board.id
    assert content["owner_id"] == board.owner_id
