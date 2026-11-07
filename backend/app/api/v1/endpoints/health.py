from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.schemas.health import HealthResponse, LivenessResponse
from app.services.health import check_database_health

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Comprehensive Health Check",
    description="Verifies the operational status of the API server and its PostgreSQL database connection.",
    responses={
        status.HTTP_200_OK: {"description": "All systems operational."},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Database or dependent service is unhealthy."},
    },
)
async def health_check(
    db: AsyncSession = Depends(get_db),
) -> JSONResponse | HealthResponse:
    """Check application and database health status."""
    is_healthy, db_detail = await check_database_health(db)
    overall_status = "ok" if is_healthy else "unhealthy"

    payload = {
        "status": overall_status,
        "database": db_detail,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }

    if not is_healthy:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=payload,
        )

    return HealthResponse(**payload)


@router.get(
    "/health/live",
    response_model=LivenessResponse,
    summary="Liveness Probe",
    description="Fast check indicating if the HTTP process is responsive.",
)
async def liveness_check() -> LivenessResponse:
    """Basic process ping for container orchestrators."""
    return LivenessResponse(status="ok")

