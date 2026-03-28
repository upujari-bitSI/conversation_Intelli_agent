"""Planner Agent – breaks down the conversation strategy into a structured plan."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from app.services.llm import get_llm


SYSTEM_PROMPT = """\
You are a Conversation Planner Agent. Given details about an upcoming conversation
scenario, you produce a structured conversation strategy.

Return ONLY valid JSON with these keys:
- opening_lines: list of 3-5 ice-breaker / opening lines
- topic_flow: ordered list of 5-8 talking points with brief descriptions
- transition_phrases: list of 4-6 smooth transition phrases between topics
- questions: list of 5-7 engaging questions to ask the audience
- poll_ideas: list of 2-3 quick poll or show-of-hands ideas

Tailor everything to the audience type, tone, context, and role provided.
Do NOT include any text outside the JSON object.
"""


async def run_planner(params: dict) -> dict:
    """Generate the conversation plan skeleton."""
    llm = get_llm(temperature=0.8)
    user_msg = _build_prompt(params)
    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_msg),
    ])
    return _parse(response.content)


def _build_prompt(p: dict) -> str:
    parts = [
        f"Topic: {p.get('topic_category', 'general')}",
        f"Custom topic detail: {p.get('custom_topic', 'N/A')}",
        f"Audience: {p.get('audience_type', 'unknown')}",
        f"Tone/Mode: {p.get('tone', 'casual')}",
        f"Context: {p.get('context', 'meeting')}",
        f"User role: {p.get('user_role', 'attendee')}",
        f"Location: {p.get('location', 'not specified')}",
        f"Duration: {p.get('duration_minutes', 'not specified')} minutes",
        f"Audience size: {p.get('audience_size', 'not specified')}",
    ]
    return "\n".join(parts)


def _parse(text: str) -> dict:
    import json
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "opening_lines": [],
            "topic_flow": [],
            "transition_phrases": [],
            "questions": [],
            "poll_ideas": [],
        }
