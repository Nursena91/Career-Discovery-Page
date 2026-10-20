from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Career Discovery Agent",
    version="0.1.0",
    description="Intern and part-time career opportunity discovery agent.",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(jobs_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Career Discovery Agent is running."}
