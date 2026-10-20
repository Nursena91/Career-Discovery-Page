from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import JobORM
from app.schemas.job import JobRecord
from app.services.dedupe import build_job_dedupe_key


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_many(self, jobs: list[JobRecord]) -> int:
        inserted = 0
        seen_in_batch: set[str] = set()

        for job in jobs:
            dedupe_key = build_job_dedupe_key(job)
            if dedupe_key in seen_in_batch:
                continue

            exists = self.db.scalar(select(JobORM.id).where(JobORM.dedupe_key == dedupe_key))
            if exists:
                continue

            self.db.add(
                JobORM(
                    source=job.source,
                    source_job_id=job.id,
                    source_url=job.source_url,
                    dedupe_key=dedupe_key,
                    title=job.title,
                    company_name=job.company_name,
                    location=job.location,
                    employment_type=job.employment_type.value,
                    work_mode=job.work_mode.value,
                    description=job.description,
                    skills_csv=",".join(job.skills),
                    posted_at_raw=job.posted_at,
                    salary_range=job.salary_range,
                )
            )
            inserted += 1
            seen_in_batch.add(dedupe_key)

        self.db.commit()
        return inserted

    def list_recent(self, limit: int = 20) -> list[JobORM]:
        stmt = select(JobORM).order_by(JobORM.id.desc()).limit(limit)
        return list(self.db.scalars(stmt).all())
