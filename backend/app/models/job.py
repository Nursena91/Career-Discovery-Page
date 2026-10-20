from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JobORM(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    source_job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(String(1200), nullable=False, index=True)
    dedupe_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    employment_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    work_mode: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills_csv: Mapped[str] = mapped_column(Text, default="", nullable=False)
    posted_at_raw: Mapped[str | None] = mapped_column(String(64), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(120), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
