import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def check_database_health(db: AsyncSession) -> tuple[bool, str]:
    """Execute a lightweight query to verify active database connectivity.

    Returns:
        tuple[bool, str]: (is_healthy, detail_message)
    """
    try:
        result = await db.execute(text("SELECT 1"))
        scalar_val = result.scalar()
        if scalar_val == 1:
            return True, "connected"
        return False, f"unexpected query result: {scalar_val}"
    except Exception as exc:
        logger.error("Database health check failed: %s", exc, exc_info=True)
        return False, f"unreachable: {type(exc).__name__}"

