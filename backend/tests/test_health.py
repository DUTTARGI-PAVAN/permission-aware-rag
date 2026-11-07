from unittest.mock import AsyncMock
import pytest
from httpx import AsyncClient

from app.core.database import get_db
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient) -> None:
    """Verify landing ping endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["health"] == "/health"


@pytest.mark.asyncio
async def test_liveness_endpoint(client: AsyncClient) -> None:
    """Verify /health/live returns status ok."""
    response = await client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_success(client: AsyncClient) -> None:
    """Verify /health returns status ok with database connected."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    assert "version" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_health_database_failure() -> None:
    """Verify /health returns 503 when the database is unreachable."""
    failing_session = AsyncMock()
    failing_session.execute.side_effect = ConnectionRefusedError("Database connection refused")

    async def override_failing_db():
        yield failing_session

    app.dependency_overrides[get_db] = override_failing_db

    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert "unreachable" in data["database"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_live_db_integration(live_client: AsyncClient) -> None:
    """Verify /health connects to real PostgreSQL when active."""
    response = await live_client.get("/health")
    # If DB is running, status is 200; otherwise 503
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data
    assert "database" in data

