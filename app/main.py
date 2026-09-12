from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Issue Tracker API",
    description="A small REST API for projects, issues, assignments and comments.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Issue Tracker API is running"}


# Users
@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(**data.model_dump())
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(user)
    return user


@app.get("/users", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.scalars(select(models.User).order_by(models.User.id)).all()


@app.get("/users/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(user)
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()


# Projects
@app.post("/projects", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = models.Project(**data.model_dump())
    db.add(project)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Project name already exists")
    db.refresh(project)
    return project


@app.get("/projects", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    return db.scalars(select(models.Project).order_by(models.Project.id)).all()


@app.get("/projects/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.patch("/projects/{project_id}", response_model=schemas.ProjectRead)
def update_project(project_id: int, data: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Project name already exists")
    db.refresh(project)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()


# Issues
@app.post("/issues", response_model=schemas.IssueRead, status_code=status.HTTP_201_CREATED)
def create_issue(data: schemas.IssueCreate, db: Session = Depends(get_db)):
    if not db.get(models.Project, data.project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    issue = models.Issue(**data.model_dump())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


@app.get("/issues", response_model=list[schemas.IssueRead])
def list_issues(
    issue_status: schemas.IssueStatus | None = Query(default=None, alias="status"),
    priority: schemas.IssuePriority | None = None,
    project_id: int | None = None,
    assignee_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = select(models.Issue)

    if issue_status:
        query = query.where(models.Issue.status == issue_status)
    if priority:
        query = query.where(models.Issue.priority == priority)
    if project_id:
        query = query.where(models.Issue.project_id == project_id)
    if assignee_id:
        query = query.join(models.Assignment).where(models.Assignment.user_id == assignee_id)

    return db.scalars(query.order_by(models.Issue.id)).all()


@app.get("/issues/{issue_id}", response_model=schemas.IssueRead)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(models.Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@app.patch("/issues/{issue_id}", response_model=schemas.IssueRead)
def update_issue(issue_id: int, data: schemas.IssueUpdate, db: Session = Depends(get_db)):
    issue = db.get(models.Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Only change fields that were actually sent by the client.
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(issue, field, value)

    db.commit()
    db.refresh(issue)
    return issue


@app.delete("/issues/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(models.Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    db.delete(issue)
    db.commit()


# Assignments
@app.post("/assignments", response_model=schemas.AssignmentRead, status_code=status.HTTP_201_CREATED)
def create_assignment(data: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    if not db.get(models.Issue, data.issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")
    if not db.get(models.User, data.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    assignment = models.Assignment(**data.model_dump())
    db.add(assignment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Issue is already assigned")
    db.refresh(assignment)
    return assignment


@app.get("/assignments", response_model=list[schemas.AssignmentRead])
def list_assignments(db: Session = Depends(get_db)):
    return db.scalars(select(models.Assignment).order_by(models.Assignment.id)).all()


@app.get("/assignments/{assignment_id}", response_model=schemas.AssignmentRead)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.get(models.Assignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@app.patch("/assignments/{assignment_id}", response_model=schemas.AssignmentRead)
def update_assignment(assignment_id: int, data: schemas.AssignmentUpdate, db: Session = Depends(get_db)):
    assignment = db.get(models.Assignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if not db.get(models.User, data.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    assignment.user_id = data.user_id
    db.commit()
    db.refresh(assignment)
    return assignment


@app.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.get(models.Assignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()


# Comments
@app.post("/comments", response_model=schemas.CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(data: schemas.CommentCreate, db: Session = Depends(get_db)):
    if not db.get(models.Issue, data.issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")
    if not db.get(models.User, data.author_id):
        raise HTTPException(status_code=404, detail="User not found")

    comment = models.Comment(**data.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@app.get("/issues/{issue_id}/comments", response_model=list[schemas.CommentRead])
def list_issue_comments(issue_id: int, db: Session = Depends(get_db)):
    if not db.get(models.Issue, issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")

    query = select(models.Comment).where(models.Comment.issue_id == issue_id).order_by(models.Comment.id)
    return db.scalars(query).all()


@app.get("/comments/{comment_id}", response_model=schemas.CommentRead)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(models.Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@app.patch("/comments/{comment_id}", response_model=schemas.CommentRead)
def update_comment(comment_id: int, data: schemas.CommentUpdate, db: Session = Depends(get_db)):
    comment = db.get(models.Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.body = data.body
    db.commit()
    db.refresh(comment)
    return comment


@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(models.Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
