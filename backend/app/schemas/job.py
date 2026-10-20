from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EmploymentType(str, Enum):
    INTERNSHIP = "internship"
    PART_TIME = "part_time"
    FULL_TIME = "full_time"
    CONTRACT = "contract"


class WorkMode(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class JobRecord(BaseModel):
    id: str = Field(..., description="Unique job identifier")
    source: str = Field(..., description="Source website")
    source_url: str = Field(..., description="Original URL")
    title: str = Field(..., description="Normalized job title")
    company_name: str = Field(..., description="Company name")
    location: str = Field(..., description="Location string")
    employment_type: EmploymentType = Field(..., description="Internship, part time, or full time")
    work_mode: WorkMode = Field(..., description="Remote, hybrid, onsite")
    description: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    posted_at: Optional[str] = None
    salary_range: Optional[str] = None


class JobSearchRequest(BaseModel):
    role: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    work_mode: Optional[WorkMode] = None
    limit: int = 10
