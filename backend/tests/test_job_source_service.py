from app.schemas.job import JobRecord
from app.services.job_source import (
    JobSourceManager,
    SourceAdapter,
    clean_description,
    normalize_posted_at,
    telemetry_store,
)


class _FailingAdapter(SourceAdapter):
    source_name = "failing-source"

    def fetch_jobs(self, query=None, location=None, limit=10):
        raise RuntimeError("simulated adapter failure")


class _OkAdapter(SourceAdapter):
    source_name = "ok-source"

    def fetch_jobs(self, query=None, location=None, limit=10):
        return [
            JobRecord(
                id="ok-001",
                source="ok-source",
                source_url="https://example.com/jobs/ok-001",
                title="Intern QA",
                company_name="Acme",
                location="Remote",
                employment_type="internship",
                work_mode="remote",
                description="ok",
                skills=["qa"],
                posted_at="2026-10-20T00:00:00Z",
            )
        ]


def test_normalize_posted_at_to_utc_iso():
    assert normalize_posted_at("2026-10-20") == "2026-10-20T00:00:00Z"
    assert normalize_posted_at("2026-10-20T15:30:00+03:00") == "2026-10-20T12:30:00Z"


def test_clean_description_removes_html_and_normalizes_spaces():
    text = "<p>Hello&nbsp; <b>world</b>\n\n from   agent</p>"
    assert clean_description(text) == "Hello world from agent"


def test_source_health_records_success_and_error():
    manager = JobSourceManager(adapters=[_OkAdapter(), _FailingAdapter()])
    jobs = manager.search(limit=3)

    assert len(jobs) == 1

    health = telemetry_store.snapshot()
    by_source = {row["source"]: row for row in health}

    assert by_source["ok-source"]["success_count"] >= 1
    assert by_source["failing-source"]["error_count"] >= 1
