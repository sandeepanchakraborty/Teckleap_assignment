"""
Route handlers for /candidates.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app import database as db
from app.models import (
    CandidateCreate,
    CandidateListResponse,
    CandidateResponse,
    CandidateStatus,
    CandidateStatusUpdate,
    ErrorResponse,
)

router = APIRouter(prefix="/candidates", tags=["Candidates"])


# ---------------------------------------------------------------------------
# POST /candidates
# ---------------------------------------------------------------------------


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new candidate",
    responses={
        409: {"model": ErrorResponse, "description": "Email already registered"},
    },
)
def create_candidate(payload: CandidateCreate) -> CandidateResponse:
    """
    Register a new candidate in the recruitment pipeline.

    - **name**: Full name (1–128 chars)
    - **email**: Must be a valid, *unique* e-mail address
    - **skill**: Primary skill / technology (e.g. *Python*, *React*)
    - **status**: One of `applied` | `interview` | `selected` | `rejected`
    """
    if db.email_exists(payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A candidate with email '{payload.email}' already exists.",
        )
    return db.create_candidate(payload)


# ---------------------------------------------------------------------------
# GET /candidates
# ---------------------------------------------------------------------------


@router.get(
    "",
    response_model=CandidateListResponse,
    summary="List all candidates",
)
def list_candidates(
    status: Optional[CandidateStatus] = Query(
        default=None,
        description="Filter by pipeline status.",
        examples=["interview"],
    ),
) -> CandidateListResponse:
    """
    Retrieve all candidates, sorted newest-first.

    Pass an optional **status** query parameter to filter results:

    ```
    GET /candidates?status=interview
    ```
    """
    candidates = db.get_all_candidates(status=status)
    return CandidateListResponse(total=len(candidates), candidates=candidates)


# ---------------------------------------------------------------------------
# PUT /candidates/{id}/status
# ---------------------------------------------------------------------------


@router.put(
    "/{candidate_id}/status",
    response_model=CandidateResponse,
    summary="Update a candidate's status",
    responses={
        404: {"model": ErrorResponse, "description": "Candidate not found"},
    },
)
def update_status(
    candidate_id: UUID,
    payload: CandidateStatusUpdate,
) -> CandidateResponse:
    """
    Move a candidate to a new pipeline stage.

    Allowed values: `applied` | `interview` | `selected` | `rejected`
    """
    updated = db.update_candidate_status(candidate_id, payload.status)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id '{candidate_id}' not found.",
        )
    return updated
