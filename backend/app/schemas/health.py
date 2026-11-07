from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """Schema for system health check status."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "database": "connected",
                "version": "0.1.0",
                "environment": "development",
            }
        }
    )

    status: str = Field(..., description="Overall service status ('ok' or 'unhealthy')")
    database: str = Field(..., description="Database connection health status")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Current running environment")


class LivenessResponse(BaseModel):
    """Schema for basic service liveness check."""

    status: str = Field(default="ok", description="Basic liveness status")

