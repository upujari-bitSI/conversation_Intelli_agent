"""News / web search service for the Research Agent."""

from __future__ import annotations

from typing import List

import httpx

from app.core.config import settings


async def fetch_recent_news(topic: str, count: int = 5) -> List[str]:
    """Fetch recent headlines related to *topic*.

    Uses NewsAPI if a key is configured; otherwise returns an empty list
    (the Research Agent will fall back to its training knowledge).
    """
    if not settings.news_api_key:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "sortBy": "publishedAt",
        "pageSize": count,
        "apiKey": settings.news_api_key,
        "language": "en",
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            articles = resp.json().get("articles", [])
            return [
                f"{a['title']} — {a.get('source', {}).get('name', 'Unknown')}"
                for a in articles[:count]
            ]
    except Exception:
        return []
