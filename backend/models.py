from datetime import datetime

from typing import Literal

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class RoleRequest(BaseModel):
    role: str = Field(min_length=1)
    difficulty: Literal["Easy", "Medium", "Hard", "Mix"] = "Mix"
    exclude_questions: list[str] = Field(default_factory=list, max_length=10)


class AnswerRequest(BaseModel):
    role: str = Field(min_length=1)
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)


class InterviewAttempt(Base):
    __tablename__ = "interview_attempts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    overall_feedback: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    improvements: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sample_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    word_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
