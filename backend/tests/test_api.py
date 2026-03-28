"""Tests for the Conversation Intelligence Agent API."""

import pytest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import ConversationPlan, Reactions

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


MOCK_PLAN = ConversationPlan(
    opening_lines=["Hello everyone!", "Great to be here today."],
    topic_flow=["Introduction", "Main topic", "Q&A"],
    questions=["What do you think about AI?"],
    reactions=Reactions(
        agreement=["That's a great point!"],
        disagreement=["I see your perspective."],
        silence=["Let me rephrase that."],
        confusion=["Let me explain differently."],
    ),
    engagement_strategies=["Use storytelling"],
    fun_elements=["Quick trivia question"],
    facts=["AI market worth $200B"],
    recent_topics=["Latest GPT developments"],
    transition_phrases=["Speaking of which..."],
    poll_ideas=["Show of hands: who uses AI daily?"],
)


@patch("app.api.routes.generate_conversation_plan")
def test_generate(mock_gen):
    mock_gen.return_value = {
        "session_id": "test-123",
        "plan": MOCK_PLAN,
        "metadata": {"topic": "technology"},
    }
    resp = client.post("/api/v1/generate", json={
        "topic_category": "technology",
        "audience_type": "technical",
        "tone": "informative",
        "context": "conference",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "test-123"
    assert len(data["plan"]["opening_lines"]) > 0


# ── Sample scenario tests ────────────────────────────────────────────────────

SCENARIOS = [
    {
        "name": "Technical conference – AI topic, serious tone",
        "input": {
            "topic_category": "technology",
            "custom_topic": "Artificial Intelligence in Healthcare",
            "audience_type": "technical",
            "tone": "serious",
            "context": "conference",
            "user_role": "speaker",
            "audience_size": 200,
        },
    },
    {
        "name": "Family gathering – casual, funny",
        "input": {
            "topic_category": "personal_social",
            "audience_type": "family",
            "tone": "funny",
            "context": "party",
            "duration_minutes": 60,
        },
    },
    {
        "name": "Networking event – unknown audience",
        "input": {
            "topic_category": "business",
            "audience_type": "unknown",
            "tone": "networking",
            "context": "meeting",
            "user_role": "attendee",
            "location": "New York",
        },
    },
]


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s["name"] for s in SCENARIOS])
@patch("app.api.routes.generate_conversation_plan")
def test_scenario(mock_gen, scenario):
    mock_gen.return_value = {
        "session_id": f"scenario-{scenario['name'][:8]}",
        "plan": MOCK_PLAN,
        "metadata": {},
    }
    resp = client.post("/api/v1/generate", json=scenario["input"])
    assert resp.status_code == 200
    data = resp.json()
    assert "plan" in data
    assert "opening_lines" in data["plan"]
