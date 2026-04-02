"""
Pydantic models and enums for the Candidate Management API.
"""

from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CandidateStatus(str, Enum):
    """Allowed pipeline stages for a candidate."""

    applied = "applied"
    interview = "interview"
    selected = "selected"
    rejected = "rejected"


# ---------------------------------------------------------------------------
# Request / Response Schemas
# ---------------------------------------------------------------------------


class CandidateCreate(BaseModel):
    """Payload expected when creating a new candidate."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        examples=["John Doe"],
        description="Full name of the candidate.",
    )
    email: EmailStr = Field(
        ...,
        examples=["john@example.com"],
        description="A valid email address (must be unique).",
    )
    skill: str = Field(
        ...,
        min_length=1,
        max_length=128,
        examples=["Python"],
        description="Primary skill or technology the candidate is applying for.",
    )
    status: CandidateStatus = Field(
        CandidateStatus.applied,
        description="Initial pipeline status. Defaults to **applied**.",
    )


class CandidateStatusUpdate(BaseModel):
    """Payload expected when updating a candidate's status."""

    status: CandidateStatus = Field(
        ...,
        description="New pipeline status for the candidate.",
    )


class CandidateResponse(BaseModel):
    """Full candidate record returned by the API."""

    model_config = ConfigDict(use_enum_values=True)

    id: UUID = Field(..., description="Unique identifier (UUID v4).")
    name: str = Field(..., description="Full name of the candidate.")
    email: EmailStr = Field(..., description="Email address.")
    skill: str = Field(..., description="Primary skill.")
    status: CandidateStatus = Field(..., description="Current pipeline status.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")


class CandidateListResponse(BaseModel):
    """Paginated / filtered list of candidates."""

    total: int = Field(..., description="Total number of records returned.")
    candidates: list[CandidateResponse]


class MessageResponse(BaseModel):
    """Generic success / informational message."""

    message: str


class ErrorResponse(BaseModel):
    """Standard error envelope."""

    detail: str
