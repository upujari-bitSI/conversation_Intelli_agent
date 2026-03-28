"""Orchestrator – coordinates all agents using LangGraph-style workflow."""

from __future__ import annotations

import asyncio
import uuid
from typing import Any, Dict

from app.agents.planner import run_planner
from app.agents.researcher import run_researcher
from app.agents.content_generator import run_content_generator
from app.agents.personalizer import run_personalizer
from app.models.schemas import ConversationPlan, Reactions
from app.services.memory import store_session


async def generate_conversation_plan(params: dict) -> Dict[str, Any]:
    """Run the full agentic pipeline and return a ConversationPlan.

    Workflow (LangGraph-style node execution):
    ┌─────────────────────────────────────────────┐
    │  1. Planner + Researcher run in PARALLEL     │
    │  2. Content Generator uses both outputs      │
    │  3. Personalizer refines the merged result   │
    └─────────────────────────────────────────────┘
    """
    session_id = str(uuid.uuid4())

    # ── Step 1: Planner & Researcher in parallel ─────────────────────────────
    plan_result, research_result = await asyncio.gather(
        run_planner(params),
        run_researcher(params),
    )

    # ── Step 2: Content Generator ────────────────────────────────────────────
    content_result = await run_content_generator(params, plan_result, research_result)

    # ── Step 3: Merge outputs ────────────────────────────────────────────────
    merged = _merge_results(plan_result, research_result, content_result)

    # ── Step 4: Personalizer ─────────────────────────────────────────────────
    final = await run_personalizer(params, merged)

    # ── Build response ───────────────────────────────────────────────────────
    plan = _to_conversation_plan(final)

    # Persist session
    store_session(session_id, {
        "request": params,
        "plan": plan.model_dump(),
    })

    return {
        "session_id": session_id,
        "plan": plan,
        "metadata": {
            "topic": params.get("custom_topic") or params.get("topic_category", ""),
            "audience": params.get("audience_type", ""),
            "tone": params.get("tone", ""),
        },
    }


async def refine_plan(session_id: str, feedback: str, section: str | None, current_plan: dict, params: dict) -> Dict[str, Any]:
    """Re-run the personalizer with user feedback to refine a section."""
    from langchain_core.messages import HumanMessage, SystemMessage
    from app.services.llm import get_llm

    llm = get_llm(temperature=0.7)
    import json

    system = (
        "You are a Conversation Plan Refiner. The user wants to improve their "
        "conversation plan. Apply the feedback and return the updated plan as JSON "
        "with the same structure. Do NOT include any text outside the JSON object."
    )
    user_msg = (
        f"Current plan:\n```json\n{json.dumps(current_plan, indent=2)}\n```\n\n"
        f"Feedback: {feedback}\n"
        f"Section to focus on: {section or 'entire plan'}\n"
        f"Audience: {params.get('audience_type', 'unknown')}\n"
        f"Tone: {params.get('tone', 'casual')}\n"
    )

    response = await llm.ainvoke([
        SystemMessage(content=system),
        HumanMessage(content=user_msg),
    ])

    text = response.content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        refined = json.loads(text)
    except json.JSONDecodeError:
        refined = current_plan

    plan = _to_conversation_plan(refined)
    store_session(session_id, {"request": params, "plan": plan.model_dump()})

    return {
        "session_id": session_id,
        "plan": plan,
        "metadata": {
            "topic": params.get("custom_topic") or params.get("topic_category", ""),
            "audience": params.get("audience_type", ""),
            "tone": params.get("tone", ""),
            "refined": "true",
        },
    }


def _merge_results(plan: dict, research: dict, content: dict) -> dict:
    return {
        "opening_lines": plan.get("opening_lines", []),
        "topic_flow": plan.get("topic_flow", []),
        "transition_phrases": plan.get("transition_phrases", []),
        "questions": plan.get("questions", []),
        "poll_ideas": plan.get("poll_ideas", []),
        "facts": research.get("facts", []),
        "recent_topics": research.get("recent_topics", []),
        "engagement_strategies": content.get("engagement_strategies", []),
        "fun_elements": content.get("fun_elements", []),
        "reactions": content.get("reactions", {
            "agreement": [], "disagreement": [],
            "silence": [], "confusion": [],
        }),
    }


def _to_conversation_plan(data: dict) -> ConversationPlan:
    reactions_data = data.get("reactions", {})
    if isinstance(reactions_data, dict):
        reactions = Reactions(**reactions_data)
    else:
        reactions = Reactions()

    return ConversationPlan(
        opening_lines=data.get("opening_lines", []),
        topic_flow=data.get("topic_flow", []),
        questions=data.get("questions", []),
        reactions=reactions,
        engagement_strategies=data.get("engagement_strategies", []),
        fun_elements=data.get("fun_elements", []),
        facts=data.get("facts", []),
        recent_topics=data.get("recent_topics", []),
        transition_phrases=data.get("transition_phrases", []),
        poll_ideas=data.get("poll_ideas", []),
    )
