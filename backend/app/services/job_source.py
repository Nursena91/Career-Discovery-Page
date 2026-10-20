from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx

from app.schemas.job import EmploymentType, JobRecord, WorkMode


class SourceAdapter(ABC):
    @abstractmethod
    def fetch_jobs(self, query: str | None = None, location: str | None = None, limit: int = 10) -> list[JobRecord]:
        """Return jobs from a specific source."""


@dataclass(slots=True)
class SourceFetchResult:
    source_name: str
    jobs: list[JobRecord]


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


class RemotiveSourceAdapter(SourceAdapter):
    """Public API adapter for remotive.com remote jobs feed."""

    def __init__(self, api_url: str = "https://remotive.com/api/remote-jobs", timeout_seconds: float = 8.0):
        self.api_url = api_url
        self.timeout_seconds = timeout_seconds

    def fetch_jobs(self, query: str | None = None, location: str | None = None, limit: int = 10) -> list[JobRecord]:
        params: dict[str, str] = {}
        if query:
            params["search"] = query

        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.get(self.api_url, params=params)
            response.raise_for_status()
            payload = response.json()

        raw_jobs = payload.get("jobs", [])
        normalized: list[JobRecord] = []

        for row in raw_jobs:
            employment_type = self._infer_employment_type(
                title=row.get("title", ""),
                tags=row.get("tags", []),
                job_type=row.get("job_type", ""),
            )

            # We intentionally keep only internship and part-time jobs for MVP scope.
            if employment_type not in {EmploymentType.INTERNSHIP, EmploymentType.PART_TIME}:
                continue

            candidate_location = row.get("candidate_required_location") or "Remote"
            if location and location.lower() not in candidate_location.lower():
                continue

            normalized.append(
                JobRecord(
                    id=f"remotive-{row.get('id')}",
                    source="remotive",
                    source_url=row.get("url", ""),
                    title=row.get("title", ""),
                    company_name=row.get("company_name", ""),
                    location=candidate_location,
                    employment_type=employment_type,
                    work_mode=WorkMode.REMOTE,
                    description=row.get("description"),
                    skills=self._extract_skills(row.get("tags", [])),
                    posted_at=row.get("publication_date"),
                    salary_range=row.get("salary"),
                )
            )

            if len(normalized) >= limit:
                break

        return normalized

    @staticmethod
    def _extract_skills(tags: list[str] | None) -> list[str]:
        if not tags:
            return []
        return [str(tag).strip().lower() for tag in tags if str(tag).strip()]

    @staticmethod
    def _infer_employment_type(title: str, tags: list[str] | None, job_type: str) -> EmploymentType:
        blob = " ".join(
            [title or "", job_type or "", " ".join(tags or [])]
        ).lower()

        if any(token in blob for token in ["intern", "internship", "staj"]):
            return EmploymentType.INTERNSHIP
        if any(token in blob for token in ["part-time", "part time", "parttime"]):
            return EmploymentType.PART_TIME
        if any(token in blob for token in ["contract", "freelance"]):
            return EmploymentType.CONTRACT
        return EmploymentType.FULL_TIME


class JobSourceManager:
    def __init__(self, adapters: list[SourceAdapter]):
        self.adapters = adapters

    def search(
        self,
        query: str | None = None,
        location: str | None = None,
        employment_type: EmploymentType | None = None,
        work_mode: WorkMode | None = None,
        limit: int = 10,
    ) -> list[JobRecord]:
        merged: list[JobRecord] = []
        seen: set[str] = set()

        for adapter in self.adapters:
            try:
                jobs = adapter.fetch_jobs(query=query, location=location, limit=limit)
            except Exception:
                # Non-blocking strategy: one source outage should not break the API response.
                continue

            for job in jobs:
                dedupe_key = (job.source_url or f"{job.source}:{job.id}").strip().lower()
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                merged.append(job)

        if employment_type:
            merged = [job for job in merged if job.employment_type == employment_type]

        if work_mode:
            merged = [job for job in merged if job.work_mode == work_mode]

        return merged[:limit]
