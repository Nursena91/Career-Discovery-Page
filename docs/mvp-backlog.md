# MVP Backlog (Phase 1)

## Milestone 1 — Repository & Engineering Baseline

- [x] Repo connected to GitHub
- [x] `main` and `develop` branches created
- [x] CI workflow added (`pytest`)
- [x] Python environment and base dependencies installed
- [x] Playwright browser install completed

## Milestone 2 — Source Adapter Foundation

- [x] Base `SourceAdapter` interface
- [x] Demo adapter
- [x] Public live source adapter skeleton (Remotive API)
- [x] Multi-source manager with dedupe
- [ ] Add adapter health metadata (success/error count)

## Milestone 3 — Normalization & Filtering

- [x] Internship / part-time focused filtering logic
- [x] Work mode and employment type filters in API
- [ ] Standardized date parsing (UTC)
- [ ] Text cleaning pipeline for descriptions

## Milestone 4 — Data Layer

- [ ] PostgreSQL models (SQLAlchemy)
- [ ] Migrations (Alembic)
- [ ] Save pipeline (`raw -> normalized -> deduped`)

## Milestone 5 — Product API

- [x] `/jobs/search` endpoint
- [ ] Pagination + cursor support
- [ ] Sorting (`posted_at`, `match_score`)
- [ ] User profile input endpoint

## Milestone 6 — Quality

- [ ] Unit tests for adapters
- [ ] Contract tests for schema validation
- [ ] Integration test for `/jobs/search` live-source-off mode
- [ ] Pre-commit hooks (format + lint)

## Suggested first issues

1. Adapter error telemetry (`source`, `latency`, `error_type`)
2. Job dedupe hash helper module
3. SQLAlchemy `Job` model and repository
4. Add `GET /jobs/sources/health` endpoint
