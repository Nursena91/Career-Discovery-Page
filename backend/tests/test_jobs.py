from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_jobs_returns_results():
    response = client.post("/jobs/search", json={"role": "intern", "limit": 5})
    assert response.status_code == 200

    payload = response.json()
    assert "jobs" in payload
    assert len(payload["jobs"]) >= 1
    assert payload["jobs"][0]["posted_at"].endswith("Z")


def test_search_jobs_filters_by_employment_type():
    response = client.post(
        "/jobs/search",
        json={"employment_type": "part_time", "limit": 10},
    )
    assert response.status_code == 200

    jobs = response.json()["jobs"]
    assert len(jobs) >= 1
    assert all(job["employment_type"] == "part_time" for job in jobs)


def test_sources_health_endpoint_after_search():
    _ = client.post("/jobs/search", json={"limit": 2})
    health_response = client.get("/jobs/sources/health")

    assert health_response.status_code == 200
    payload = health_response.json()
    assert "sources" in payload
    assert any(source["source"] == "demo-source" for source in payload["sources"])
