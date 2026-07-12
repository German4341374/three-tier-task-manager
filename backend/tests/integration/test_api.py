import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client() -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    def override_db():
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


@pytest.mark.integration
def test_task_lifecycle(client: TestClient) -> None:
    created = client.post(
        "/api/v1/tasks",
        json={"title": "Ship portfolio", "description": "Run the demo"},
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    listed = client.get("/api/v1/tasks")
    assert listed.status_code == 200
    assert [task["title"] for task in listed.json()] == ["Ship portfolio"]

    updated = client.patch(f"/api/v1/tasks/{task_id}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/api/v1/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get("/api/v1/tasks").json() == []


@pytest.mark.integration
def test_unknown_task_returns_not_found(client: TestClient) -> None:
    response = client.patch("/api/v1/tasks/999", json={"completed": True})
    assert response.status_code == 404

    delete_response = client.delete("/api/v1/tasks/999")
    assert delete_response.status_code == 404


def test_liveness(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
