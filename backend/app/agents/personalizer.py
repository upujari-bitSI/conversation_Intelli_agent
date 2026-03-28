"""Personalization Agent – adjusts the final output based on audience and tone."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from app.services.llm import get_llm


SYSTEM_PROMPT = """\
You are a Personalization Agent. You receive a draft conversation plan and
refine it to perfectly match the audience, tone, and context.

Your job:
1. Adjust language complexity for the audience
2. Ensure tone consistency throughout
3. Add/remove humor based on the mode
4. Adapt formality level
5. Add cultural sensitivity notes if location is specified

Return ONLY valid JSON with the SAME structure as the input, but refined.
Do NOT include any text outside the JSON object.
"""


async def run_personalizer(params: dict, merged_plan: dict) -> dict:
    """Refine the merged plan to match audience and tone preferences."""
    llm = get_llm(temperature=0.6)

    user_msg = (
        f"Audience: {params.get('audience_type', 'unknown')}\n"
        f"Tone: {params.get('tone', 'casual')}\n"
        f"Context: {params.get('context', 'meeting')}\n"
        f"Location: {params.get('location', 'not specified')}\n"
        f"Duration: {params.get('duration_minutes', 'not specified')} minutes\n"
        f"Audience size: {params.get('audience_size', 'not specified')}\n\n"
        f"Draft plan:\n```json\n{_to_json(merged_plan)}\n```\n\n"
        "Refine and return the improved plan."
    )

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_msg),
    ])
    return _parse(response.content, merged_plan)


def _to_json(data: dict) -> str:
    import json
    return json.dumps(data, indent=2)


def _parse(text: str, fallback: dict) -> dict:
    import json
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return fallback
