from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from html import unescape
from time import perf_counter
import re

import httpx

from app.schemas.job import EmploymentType, JobRecord, WorkMode
from app.services.dedupe import build_job_dedupe_key


class SourceAdapter(ABC):
    source_name: str = "unknown"

    @abstractmethod
    def fetch_jobs(self, query: str | None = None, location: str | None = None, limit: int = 10) -> list[JobRecord]:
        """Return jobs from a specific source."""


@dataclass(slots=True)
class SourceFetchResult:
    source_name: str
    jobs: list[JobRecord]


@dataclass(slots=True)
class AdapterHealth:
    source: str
    success_count: int = 0
    error_count: int = 0
    last_latency_ms: float | None = None
    last_error: str | None = None


class AdapterTelemetryStore:
    def __init__(self):
        self._store: dict[str, AdapterHealth] = {}

    def ensure(self, source: str) -> None:
        if source not in self._store:
            self._store[source] = AdapterHealth(source=source)

    def record_success(self, source: str, latency_ms: float) -> None:
        self.ensure(source)
        item = self._store[source]
        item.success_count += 1
        item.last_latency_ms = round(latency_ms, 2)
        item.last_error = None

    def record_error(self, source: str, latency_ms: float, error: Exception) -> None:
        self.ensure(source)
        item = self._store[source]
        item.error_count += 1
        item.last_latency_ms = round(latency_ms, 2)
        item.last_error = f"{error.__class__.__name__}: {str(error)}"

    def snapshot(self) -> list[dict[str, str | int | float | None]]:
        return [
            {
                "source": item.source,
                "success_count": item.success_count,
                "error_count": item.error_count,
                "last_latency_ms": item.last_latency_ms,
                "last_error": item.last_error,
            }
            for item in sorted(self._store.values(), key=lambda row: row.source)
        ]


telemetry_store = AdapterTelemetryStore()


def normalize_posted_at(value: str | None) -> str | None:
    if not value:
        return None

    normalized = value.strip()
    if not normalized:
        return None

    try:
        dt = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        dt = None

    if dt is None:
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                dt = datetime.strptime(normalized, fmt)
                break
            except ValueError:
                continue

    if dt is None:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    else:
        dt = dt.astimezone(UTC)

    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_description(value: str | None) -> str | None:
    if not value:
        return None

    no_html = re.sub(r"<[^>]+>", " ", value)
    normalized = re.sub(r"\s+", " ", unescape(no_html)).strip()
    return normalized or None


class DemoSourceAdapter(SourceAdapter):
    source_name = "demo-source"

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
                description=clean_description("Summer internship focused on machine learning and experimentation."),
                skills=["python", "sql", "machine learning"],
                posted_at=normalize_posted_at("2026-10-15"),
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
                description=clean_description("Support product team with UI implementation and bug fixes."),
                skills=["javascript", "react", "css"],
                posted_at=normalize_posted_at("2026-10-18"),
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
    source_name = "remotive"

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
                    description=clean_description(row.get("description")),
                    skills=self._extract_skills(row.get("tags", [])),
                    posted_at=normalize_posted_at(row.get("publication_date")),
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
        for adapter in adapters:
            telemetry_store.ensure(adapter.source_name)

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
            started_at = perf_counter()
            try:
                jobs = adapter.fetch_jobs(query=query, location=location, limit=limit)
                elapsed_ms = (perf_counter() - started_at) * 1000
                telemetry_store.record_success(adapter.source_name, elapsed_ms)
            except Exception as exc:
                elapsed_ms = (perf_counter() - started_at) * 1000
                telemetry_store.record_error(adapter.source_name, elapsed_ms, exc)
                # Non-blocking strategy: one source outage should not break the API response.
                continue

            for job in jobs:
                dedupe_key = build_job_dedupe_key(job)
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                merged.append(job)

        if employment_type:
            merged = [job for job in merged if job.employment_type == employment_type]

        if work_mode:
            merged = [job for job in merged if job.work_mode == work_mode]

        return merged[:limit]

    @staticmethod
    def get_source_health() -> list[dict[str, str | int | float | None]]:
        return telemetry_store.snapshot()
