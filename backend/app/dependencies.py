"""Dependency injection for routes."""

from app.config import get_settings


async def get_settings_dependency():
    """Provide settings as a dependency."""
    return get_settings()
