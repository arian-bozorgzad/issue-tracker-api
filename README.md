# Issue Tracker REST API

A simple backend project for managing projects and issues.

I made this project with FastAPI and SQLite to practice building REST APIs and working with related database records.

## Features

- Create and manage users and projects
- Create, update and delete issues
- Assign users to issues
- Add comments to issues
- Filter issues by status and priority
- Basic validation and error handling

## Built with

- Python
- FastAPI
- SQLite
- SQLAlchemy

## Run the project

Install the requirements:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn app.main:app --reload
```

Then open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Tests

```bash
pytest
```
