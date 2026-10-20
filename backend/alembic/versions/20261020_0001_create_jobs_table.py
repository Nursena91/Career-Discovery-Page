"""create jobs table

Revision ID: 20261020_0001
Revises:
Create Date: 2026-10-20 00:00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20261020_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("jobs"):
        op.create_table(
            "jobs",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("source", sa.String(length=120), nullable=False),
            sa.Column("source_job_id", sa.String(length=255), nullable=False),
            sa.Column("source_url", sa.String(length=1200), nullable=False),
            sa.Column("dedupe_key", sa.String(length=255), nullable=False),
            sa.Column("title", sa.String(length=300), nullable=False),
            sa.Column("company_name", sa.String(length=255), nullable=False),
            sa.Column("location", sa.String(length=255), nullable=False),
            sa.Column("employment_type", sa.String(length=50), nullable=False),
            sa.Column("work_mode", sa.String(length=50), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("skills_csv", sa.Text(), nullable=False),
            sa.Column("posted_at_raw", sa.String(length=64), nullable=True),
            sa.Column("salary_range", sa.String(length=120), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("dedupe_key"),
        )

    existing_indexes = {idx["name"] for idx in inspector.get_indexes("jobs")}
    if "ix_jobs_company_name" not in existing_indexes:
        op.create_index("ix_jobs_company_name", "jobs", ["company_name"], unique=False)
    if "ix_jobs_dedupe_key" not in existing_indexes:
        op.create_index("ix_jobs_dedupe_key", "jobs", ["dedupe_key"], unique=True)
    if "ix_jobs_employment_type" not in existing_indexes:
        op.create_index("ix_jobs_employment_type", "jobs", ["employment_type"], unique=False)
    if "ix_jobs_location" not in existing_indexes:
        op.create_index("ix_jobs_location", "jobs", ["location"], unique=False)
    if "ix_jobs_source" not in existing_indexes:
        op.create_index("ix_jobs_source", "jobs", ["source"], unique=False)
    if "ix_jobs_source_url" not in existing_indexes:
        op.create_index("ix_jobs_source_url", "jobs", ["source_url"], unique=False)
    if "ix_jobs_title" not in existing_indexes:
        op.create_index("ix_jobs_title", "jobs", ["title"], unique=False)
    if "ix_jobs_work_mode" not in existing_indexes:
        op.create_index("ix_jobs_work_mode", "jobs", ["work_mode"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_jobs_work_mode", table_name="jobs")
    op.drop_index("ix_jobs_title", table_name="jobs")
    op.drop_index("ix_jobs_source_url", table_name="jobs")
    op.drop_index("ix_jobs_source", table_name="jobs")
    op.drop_index("ix_jobs_location", table_name="jobs")
    op.drop_index("ix_jobs_employment_type", table_name="jobs")
    op.drop_index("ix_jobs_dedupe_key", table_name="jobs")
    op.drop_index("ix_jobs_company_name", table_name="jobs")
    op.drop_table("jobs")
