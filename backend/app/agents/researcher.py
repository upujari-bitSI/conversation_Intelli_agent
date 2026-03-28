"""Research Agent – fetches current affairs, trends, and facts."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from app.services.llm import get_llm
from app.services.news import fetch_recent_news


SYSTEM_PROMPT = """\
You are a Research Agent. Given a topic and recent news headlines,
produce factual, relevant supporting material for a conversation.

Return ONLY valid JSON with these keys:
- facts: list of 5-7 interesting, verified facts relevant to the topic
- recent_topics: list of 4-6 recent trends or news items to reference
- historical_context: list of 2-3 historical anecdotes or milestones

Do NOT include any text outside the JSON object.
"""


async def run_researcher(params: dict) -> dict:
    """Gather research material for the conversation."""
    topic = params.get("custom_topic") or params.get("topic_category", "general")
    headlines = await fetch_recent_news(topic)

    llm = get_llm(temperature=0.5)
    user_msg = (
        f"Topic: {topic}\n"
        f"Context: {params.get('context', 'meeting')}\n"
        f"Audience: {params.get('audience_type', 'unknown')}\n"
        f"Location: {params.get('location', 'not specified')}\n\n"
        f"Recent headlines:\n" + ("\n".join(f"- {h}" for h in headlines) if headlines else "No headlines available — use your knowledge of recent trends.")
    )

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_msg),
    ])
    return _parse(response.content)


def _parse(text: str) -> dict:
    import json
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"facts": [], "recent_topics": [], "historical_context": []}
