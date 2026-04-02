# Candidate Management API

A clean, production-ready REST API built with **FastAPI** for managing recruitment candidates.

## Features

| Feature | Endpoint |
|---|---|
| Create a candidate | `POST /candidates` |
| List all candidates | `GET /candidates` |
| Filter by status | `GET /candidates?status=interview` |
| Update candidate status | `PUT /candidates/{id}/status` |
| Health check | `GET /health` |

## Candidate Status Pipeline

```
applied → interview → selected
                   ↘ rejected
```

## Project Structure

```
teckleap/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, middleware, startup
│   ├── models.py        # Pydantic schemas & enums
│   ├── database.py      # In-memory data store / repository
│   └── routes/
│       ├── __init__.py
│       └── candidates.py # Route handlers
├── requirements.txt
└── README.md
```

## Setup & Run

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn app.main:app --reload
```

The server will be available at **http://localhost:8000**

## Interactive Docs

| URL | Description |
|---|---|
| http://localhost:8000/docs | Swagger UI (try it live) |
| http://localhost:8000/redoc | ReDoc (clean reference docs) |

## API Reference

### `POST /candidates` — Create a candidate

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "skill": "Python",
  "status": "applied"
}
```

**Validation rules:**
- `email` must be a valid, unique email address
- `status` must be one of: `applied`, `interview`, `selected`, `rejected`
- `name` and `skill` are required (1–128 characters)

**Responses:**
- `201 Created` — Candidate created successfully
- `409 Conflict` — Email already registered
- `422 Unprocessable Entity` — Validation error

---

### `GET /candidates` — List all candidates

```bash
# All candidates
GET /candidates

# Filter by status
GET /candidates?status=interview
```

**Response:**
```json
{
  "total": 1,
  "candidates": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "John Doe",
      "email": "john@example.com",
      "skill": "Python",
      "status": "applied",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

---

### `PUT /candidates/{id}/status` — Update candidate status

```json
{
  "status": "interview"
}
```

**Responses:**
- `200 OK` — Updated candidate record
- `404 Not Found` — Candidate not found
- `422 Unprocessable Entity` — Invalid status value

## Tech Stack

- **Python 3.10+**
- **FastAPI** — High-performance async web framework
- **Pydantic v2** — Data validation and serialization
- **Uvicorn** — ASGI server

## Notes

- Data is stored in-memory — it resets when the server restarts
- The repository layer (`database.py`) is designed for easy database replacement (SQLAlchemy, MongoDB, etc.)
- CORS is enabled for all origins (restrict in production)
