from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.job import JobORM
from app.repositories.job_repository import JobRepository
from app.schemas.job import EmploymentType, JobRecord, WorkMode


def _job(source_job_id: str, source_url: str) -> JobRecord:
    return JobRecord(
        id=source_job_id,
        source="demo-source",
        source_url=source_url,
        title="Backend Intern",
        company_name="Northstar",
        location="Remote",
        employment_type=EmploymentType.INTERNSHIP,
        work_mode=WorkMode.REMOTE,
        description="desc",
        skills=["python", "fastapi"],
        posted_at="2026-10-20T00:00:00Z",
        salary_range=None,
    )


def test_repository_save_many_dedupes_by_key():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(bind=engine)

    with TestingSession() as db:
        repo = JobRepository(db)
        inserted_first = repo.save_many([
            _job("1", "https://example.com/jobs/1"),
            _job("2", "https://example.com/jobs/1?ref=dup"),
        ])
        assert inserted_first == 1

        rows = db.query(JobORM).all()
        assert len(rows) == 1
