"""Analytics endpoints for support operations."""

from fastapi import APIRouter, Query

from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/summary")
async def get_summary():
    """Return aggregate metrics for the current service process."""
    return AnalyticsService.summary()


@router.get("/trends")
async def get_trends(days: int = Query(default=7, ge=1, le=31)):
    """Return daily conversation counts for the requested period."""
    return {"days": days, "trends": AnalyticsService.trends(days)}


@router.get("/categories")
async def get_categories():
    """Return conversation counts grouped by classified intent."""
    return {"categories": AnalyticsService.categories()}