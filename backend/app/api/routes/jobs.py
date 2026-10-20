from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import get_db
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobSearchRequest
from app.services.job_source import DemoSourceAdapter, JobSourceManager, RemotiveSourceAdapter

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/search")
def search_jobs(payload: JobSearchRequest, db: Session = Depends(get_db)):
    adapters = [DemoSourceAdapter()]
    if settings.enable_live_sources:
        adapters.append(
            RemotiveSourceAdapter(
                api_url=settings.remotive_api_url,
                timeout_seconds=settings.source_request_timeout_seconds,
            )
        )

    manager = JobSourceManager(adapters=adapters)
    jobs = manager.search(
        query=payload.role,
        location=payload.location,
        employment_type=payload.employment_type,
        work_mode=payload.work_mode,
        limit=payload.limit,
    )
    repository = JobRepository(db)
    inserted_count = repository.save_many(jobs)

    return {
        "jobs": [job.model_dump() for job in jobs],
        "inserted_count": inserted_count,
    }


@router.get("/sources/health")
def source_health():
    return {"sources": JobSourceManager.get_source_health()}
