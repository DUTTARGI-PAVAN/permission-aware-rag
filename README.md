# Permission-Aware RAG System

A production-oriented, multi-tenant Retrieval-Augmented Generation (RAG) platform built with **Python 3.12**, **FastAPI**, **PostgreSQL with pgvector**, **SQLAlchemy 2.x (async)**, and **Alembic**.

---

## Current Status: Phase 0 (Foundation)

Phase 0 establishes the clean architecture foundation:
- **FastAPI** application with lifecycle management (lifespan).
- **PostgreSQL + pgvector** via Docker Compose (`pgvector/pgvector:pg16`).
- **SQLAlchemy 2.x** with async engine (`asyncpg`) and connection pooling.
- **Alembic** asynchronous migrations configured.
- **Pydantic v2 Settings** for type-safe environment configuration.
- **Health Check endpoints** (`GET /health` with active DB connectivity check, `GET /health/live`).
- **Pytest** async test suite with mocked and live database tests.

---

## Project Structure

```
permission-aware-rag/
    backend/
        app/
            __init__.py
            main.py              # FastAPI application initialization & lifespans
            core/                # Config, database engine, dependencies
            api/                 # API routers and endpoints
            models/              # SQLAlchemy 2.x declarative models
            schemas/             # Pydantic v2 request/response schemas
            services/            # Business logic (health checks, etc.)
            rag/                 # Future RAG retrieval, reranking, generation
            ingestion/           # Future document ingestion and chunking
        tests/                   # Pytest test suite
        alembic/                 # Migration environment and versions
        alembic.ini              # Alembic migration configuration
        requirements.txt         # Backend Python dependencies
        Dockerfile               # Production Docker container image
        pytest.ini               # Pytest configuration
    docker-compose.yml           # Multi-container orchestration (DB + Backend)
    .env.example                 # Template for environment variables
    .env                         # Active environment configuration
    .gitignore                   # Git ignore rules
    README.md                    # Documentation
```

---

## Quickstart Guide

### 1. Prerequisites
- **Python 3.12+**
- **Docker & Docker Compose**

### 2. Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```

### 3. Start Database Service
Start the PostgreSQL container with pgvector:
```bash
docker compose up -d db
```
*(Or `docker-compose up -d db` depending on your Docker version)*

Verify the container is healthy:
```bash
docker ps
```

### 4. Install Dependencies
Create and activate a virtual environment, then install dependencies:

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### 5. Run Database Migrations
Run Alembic migrations to enable the `pgvector` extension:
```bash
cd backend
alembic upgrade head
cd ..
```

### 6. Start FastAPI Application
From the `backend` folder:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at:
- **API Root**: [http://localhost:8000/](http://localhost:8000/)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Running with Docker Compose (Full Stack)

To build and start both the PostgreSQL database and FastAPI backend:
```bash
docker compose up -d --build
```

Check the logs:
```bash
docker compose logs -f backend
```

---

## Health Check API

### `GET /health`
Performs an active database ping (`SELECT 1`) using the async database session.

**Sample 200 OK Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "version": "0.1.0",
  "environment": "development"
}
```

**Sample 503 Service Unavailable Response (if DB is down):**
```json
{
  "status": "unhealthy",
  "database": "unreachable: CannotConnectNowError",
  "version": "0.1.0",
  "environment": "development"
}
```

### `GET /health/live`
Fast liveness probe for container orchestrators.

**Response:**
```json
{
  "status": "ok"
}
```

---

## Running Tests

Run the test suite using `pytest`:
```bash
cd backend
pytest -v
```

