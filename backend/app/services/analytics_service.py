"""In-process analytics for support interactions."""

from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Dict


class AnalyticsService:
    """Collect and summarize interaction metrics for the running service."""

    _events = []

    @classmethod
    def record_interaction(cls, intent: str, escalated: bool, resolved: bool) -> None:
        cls._events.append({
            "timestamp": datetime.utcnow(),
            "intent": intent,
            "escalated": escalated,
            "resolved": resolved,
        })

    @classmethod
    def summary(cls) -> Dict[str, Any]:
        total = len(cls._events)
        escalated = sum(event["escalated"] for event in cls._events)
        resolved = sum(event["resolved"] for event in cls._events)
        return {
            "total_conversations": total,
            "resolved_conversations": resolved,
            "escalated_conversations": escalated,
            "automation_rate": round((total - escalated) / total, 3) if total else 0,
            "resolution_rate": round(resolved / total, 3) if total else 0,
        }

    @classmethod
    def trends(cls, days: int = 7) -> list[Dict[str, Any]]:
        start = datetime.utcnow() - timedelta(days=days - 1)
        counts = Counter(event["timestamp"].date().isoformat() for event in cls._events if event["timestamp"] >= start)
        return [
            {"date": (start.date() + timedelta(days=offset)).isoformat(), "conversations": counts.get((start.date() + timedelta(days=offset)).isoformat(), 0)}
            for offset in range(days)
        ]

    @classmethod
    def categories(cls) -> list[Dict[str, Any]]:
        counts = Counter(event["intent"] for event in cls._events)
        return [{"intent": intent, "count": count} for intent, count in counts.most_common()]