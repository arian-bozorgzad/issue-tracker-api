import os

os.environ["DATABASE_URL"] = "sqlite:///./test_issues.db"

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module():
    if os.path.exists("test_issues.db"):
        os.remove("test_issues.db")


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Issue Tracker API is running"


def test_basic_issue_flow():
    user = client.post("/users", json={"name": "Arian", "email": "arian@example.com"})
    project = client.post("/projects", json={"name": "Backend Practice", "description": "Small API project"})

    assert user.status_code == 201
    assert project.status_code == 201

    issue = client.post(
        "/issues",
        json={
            "title": "Add login page",
            "description": "Create the first login endpoint later",
            "priority": "high",
            "project_id": project.json()["id"],
        },
    )
    assert issue.status_code == 201

    assignment = client.post(
        "/assignments",
        json={"issue_id": issue.json()["id"], "user_id": user.json()["id"]},
    )
    assert assignment.status_code == 201

    filtered = client.get("/issues?priority=high&status=open")
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1
