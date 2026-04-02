"""
FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes.candidates import router as candidates_router

# ---------------------------------------------------------------------------
# App metadata — powers the /docs & /redoc pages
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Candidate Management API",
    description=(
        "A recruitment pipeline API built with **FastAPI**.\n\n"
        "Manage candidates through their hiring journey:\n\n"
        "`applied` → `interview` → `selected` | `rejected`"
    ),
    version="1.0.0",
    contact={
        "name": "TeckLeap Recruitment Platform",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "Candidates",
            "description": "Create, list, and update candidates in the hiring pipeline.",
        },
        {
            "name": "Health",
            "description": "Service health checks.",
        },
    ],
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global exception handlers
# ---------------------------------------------------------------------------


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(candidates_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health", tags=["Health"], summary="Health check")
def health_check():
    """Returns `200 OK` if the service is running."""
    return {"status": "ok", "service": "Candidate Management API"}


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Welcome to the Candidate Management API!",
        "docs": "/docs",
        "redoc": "/redoc",
    }
