from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.job import JobRecord


class SourceAdapter(ABC):
    @abstractmethod
    def fetch_jobs(self, query: str | None = None, location: str | None = None, limit: int = 10) -> list[JobRecord]:
        """Return jobs from a specific source."""


class DemoSourceAdapter(SourceAdapter):
    def fetch_jobs(self, query: str | None = None, location: str | None = None, limit: int = 10) -> list[JobRecord]:
        jobs = [
            JobRecord(
                id="demo-001",
                source="demo-source",
                source_url="https://example.com/jobs/001",
                title="Data Science Intern",
                company_name="Northstar Labs",
                location="Istanbul, Turkey",
                employment_type="internship",
                work_mode="hybrid",
                description="Summer internship focused on machine learning and experimentation.",
                skills=["python", "sql", "machine learning"],
                posted_at="2026-10-15",
                salary_range="3500-5000 TRY",
            ),
            JobRecord(
                id="demo-002",
                source="demo-source",
                source_url="https://example.com/jobs/002",
                title="Part-Time Frontend Developer",
                company_name="Pixel Harbor",
                location="Remote",
                employment_type="part_time",
                work_mode="remote",
                description="Support product team with UI implementation and bug fixes.",
                skills=["javascript", "react", "css"],
                posted_at="2026-10-18",
                salary_range="1800-2500 TRY",
            ),
        ]

        if query:
            jobs = [job for job in jobs if query.lower() in job.title.lower() or query.lower() in " ".join(job.skills).lower()]

        if location:
            jobs = [job for job in jobs if location.lower() in job.location.lower()]

        return jobs[:limit]
