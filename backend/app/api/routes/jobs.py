from fastapi import APIRouter

from app.schemas.job import JobSearchRequest
from app.services.job_source import DemoSourceAdapter

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/search")
def search_jobs(payload: JobSearchRequest):
    adapter = DemoSourceAdapter()
    jobs = adapter.fetch_jobs(
        query=payload.role,
        location=payload.location,
        limit=payload.limit,
    )
    return {"jobs": [job.model_dump() for job in jobs]}
