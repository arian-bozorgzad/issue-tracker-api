from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


IssueStatus = Literal["open", "in_progress", "closed"]
IssuePriority = Literal["low", "medium", "high"]


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None


class UserRead(UserCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=1000)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=1000)


class ProjectRead(ProjectCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class IssueCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    description: str | None = Field(default=None, max_length=2000)
    status: IssueStatus = "open"
    priority: IssuePriority = "medium"
    project_id: int


class IssueUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=160)
    description: str | None = Field(default=None, max_length=2000)
    status: IssueStatus | None = None
    priority: IssuePriority | None = None


class IssueRead(IssueCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AssignmentCreate(BaseModel):
    issue_id: int
    user_id: int


class AssignmentUpdate(BaseModel):
    user_id: int


class AssignmentRead(AssignmentCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=2000)
    issue_id: int
    author_id: int


class CommentUpdate(BaseModel):
    body: str = Field(min_length=1, max_length=2000)


class CommentRead(CommentCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
