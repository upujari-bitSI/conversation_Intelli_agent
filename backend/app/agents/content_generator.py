"""Content Generator Agent – creates engagement strategies, humor, and reactions."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from app.services.llm import get_llm


SYSTEM_PROMPT = """\
You are a Content Generator Agent. You create engagement strategies, reactions,
and fun elements for conversations.

Return ONLY valid JSON with these keys:
- engagement_strategies: list of 5-7 strategies (storytelling hooks, analogies, participation cues)
- fun_elements: list of 3-5 humorous or light-hearted elements (jokes, anecdotes, wordplay)
- reactions:
    - agreement: list of 3-4 responses when the audience agrees
    - disagreement: list of 3-4 responses when the audience disagrees
    - silence: list of 3-4 responses when the audience is silent
    - confusion: list of 3-4 responses when the audience seems confused

Tailor humor and engagement to the tone and audience.
Do NOT include any text outside the JSON object.
"""


async def run_content_generator(params: dict, plan: dict, research: dict) -> dict:
    """Generate engagement content based on the plan and research."""
    llm = get_llm(temperature=0.9)

    user_msg = (
        f"Tone: {params.get('tone', 'casual')}\n"
        f"Audience: {params.get('audience_type', 'unknown')}\n"
        f"Context: {params.get('context', 'meeting')}\n"
        f"Role: {params.get('user_role', 'attendee')}\n\n"
        f"Conversation topics: {', '.join(plan.get('topic_flow', [])[:5])}\n"
        f"Key facts: {', '.join(research.get('facts', [])[:3])}\n"
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
        return {
            "engagement_strategies": [],
            "fun_elements": [],
            "reactions": {
                "agreement": [], "disagreement": [],
                "silence": [], "confusion": [],
            },
        }
