from app.schemas.job import EmploymentType, JobRecord, WorkMode
from app.services.dedupe import build_content_hash, build_job_dedupe_key, normalize_url


def _job(source_url: str) -> JobRecord:
    return JobRecord(
        id="j-1",
        source="demo",
        source_url=source_url,
        title="Data Intern",
        company_name="Acme",
        location="Istanbul",
        employment_type=EmploymentType.INTERNSHIP,
        work_mode=WorkMode.HYBRID,
        description="Work with data",
        skills=["python"],
    )


def test_normalize_url_removes_query_and_trailing_slash():
    assert normalize_url("HTTPS://Example.com/jobs/1/?ref=abc") == "https://example.com/jobs/1"


def test_dedupe_key_prefers_url_when_available():
    key_a = build_job_dedupe_key(_job("https://example.com/jobs/1?x=1"))
    key_b = build_job_dedupe_key(_job("https://example.com/jobs/1"))
    assert key_a == key_b


def test_content_hash_is_stable_for_whitespace_differences():
    h1 = build_content_hash("Data Intern", "Acme", "Istanbul", "Hello   world")
    h2 = build_content_hash("data intern", "acme", "istanbul", "hello world")
    assert h1 == h2
