# Issue Tracker REST API

A small backend project built with **FastAPI**, **SQLAlchemy**, and **SQLite**. It can be used to manage projects, users, issues, assignments, and issue comments.

I built this project mainly to practice REST API design, relational database models, request validation, filtering, and common API error handling.

## Features

- CRUD endpoints for users, projects, issues, assignments, and comments
- Assign one user to an issue
- Add and edit comments on issues
- Filter issues by status, priority, project, or assignee
- Validation for issue status and priority
- Basic 404 and conflict responses
- Automatic Swagger documentation from FastAPI

## Project structure

```text
issue-tracker-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Run locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn app.main:app --reload
```

Open:

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

The SQLite database file is created automatically on first run.

## Example

Create a project:

```json
POST /projects
{
  "name": "Portfolio API",
  "description": "Tasks for my backend project"
}
```

Create an issue:

```json
POST /issues
{
  "title": "Add validation",
  "description": "Validate issue input fields",
  "status": "open",
  "priority": "high",
  "project_id": 1
}
```

Filter issues:

```text
GET /issues?status=open&priority=high
```

## Tests

```bash
pytest
```

The tests cover the root endpoint and a basic workflow for creating a user, project, issue, and assignment.
