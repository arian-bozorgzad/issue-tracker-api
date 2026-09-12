from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)

    assignments: Mapped[list["Assignment"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    issues: Mapped[list["Issue"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    priority: Mapped[str] = mapped_column(String(20), default="medium", index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    project: Mapped["Project"] = relationship(back_populates="issues")
    assignment: Mapped["Assignment | None"] = relationship(back_populates="issue", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="issue", cascade="all, delete-orphan")


class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = (UniqueConstraint("issue_id", name="one_assignee_per_issue"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issues.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    issue: Mapped["Issue"] = relationship(back_populates="assignment")
    user: Mapped["User"] = relationship(back_populates="assignments")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issues.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    issue: Mapped["Issue"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
