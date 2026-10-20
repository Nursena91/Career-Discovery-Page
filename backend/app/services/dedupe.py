from __future__ import annotations

import hashlib
import re
from urllib.parse import urlsplit, urlunsplit

from app.schemas.job import JobRecord


def _normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip().lower()


def normalize_url(url: str | None) -> str:
    if not url:
        return ""

    parsed = urlsplit(url.strip())
    path = parsed.path.rstrip("/")
    normalized = urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", ""))
    return normalized


def build_content_hash(
    title: str | None,
    company_name: str | None,
    location: str | None,
    description: str | None,
) -> str:
    blob = "|".join(
        [
            _normalize_text(title),
            _normalize_text(company_name),
            _normalize_text(location),
            _normalize_text(description),
        ]
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def build_job_dedupe_key(job: JobRecord) -> str:
    source_url = normalize_url(job.source_url)
    if source_url:
        return f"url:{source_url}"

    content_hash = build_content_hash(
        title=job.title,
        company_name=job.company_name,
        location=job.location,
        description=job.description,
    )
    return f"hash:{content_hash}"
