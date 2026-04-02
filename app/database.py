"""
In-memory data store for candidates.

Provides a simple repository layer so route handlers stay thin.
If you later want to swap this for a real database (SQLAlchemy, Motor, etc.)
you only need to touch this file.
"""

from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional

from app.models import CandidateCreate, CandidateResponse, CandidateStatus


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# In-memory "database"
# ---------------------------------------------------------------------------

_candidates: dict[UUID, CandidateResponse] = {}


# ---------------------------------------------------------------------------
# Repository helpers
# ---------------------------------------------------------------------------


def create_candidate(payload: CandidateCreate) -> CandidateResponse:
    """Persist a new candidate and return the full record."""
    now = _utcnow()
    record = CandidateResponse(
        id=uuid4(),
        name=payload.name,
        email=payload.email,
        skill=payload.skill,
        status=payload.status,
        created_at=now,
        updated_at=now,
    )
    _candidates[record.id] = record
    return record


def email_exists(email: str) -> bool:
    """Return True if the e-mail is already registered."""
    return any(c.email.lower() == email.lower() for c in _candidates.values())


def get_all_candidates(
    status: Optional[CandidateStatus] = None,
) -> list[CandidateResponse]:
    """Return all candidates, optionally filtered by status."""
    records = list(_candidates.values())
    if status is not None:
        records = [r for r in records if r.status == status]
    # Sort newest-first for a nicer UX
    records.sort(key=lambda r: r.created_at, reverse=True)
    return records


def get_candidate(candidate_id: UUID) -> Optional[CandidateResponse]:
    """Fetch a single candidate by ID, or None if not found."""
    return _candidates.get(candidate_id)


def update_candidate_status(
    candidate_id: UUID, new_status: CandidateStatus
) -> Optional[CandidateResponse]:
    """
    Update a candidate's status.
    Returns the updated record, or None if the candidate doesn't exist.
    """
    record = _candidates.get(candidate_id)
    if record is None:
        return None

    updated = record.model_copy(
        update={"status": new_status, "updated_at": _utcnow()}
    )
    _candidates[candidate_id] = updated
    return updated
