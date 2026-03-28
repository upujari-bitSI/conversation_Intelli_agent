"""Pydantic schemas for request/response models."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────────────

class TopicCategory(str, Enum):
    TECHNOLOGY = "technology"
    CURRENT_AFFAIRS = "current_affairs"
    BUSINESS = "business"
    PERSONAL_SOCIAL = "personal_social"
    ENTERTAINMENT = "entertainment"
    CUSTOM = "custom"


class AudienceType(str, Enum):
    FRIENDS = "friends"
    UNKNOWN = "unknown"
    NEW_GROUP = "new_group"
    PUBLIC = "public"
    FORMAL = "formal"
    TECHNICAL = "technical"
    FAMILY = "family"


class ToneMode(str, Enum):
    SERIOUS = "serious"
    TECHNICAL = "technical"
    FUNNY = "funny"
    CASUAL = "casual"
    INFORMATIVE = "informative"
    ICE_BREAKER = "ice_breaker"
    NETWORKING = "networking"


class ContextType(str, Enum):
    MEETING = "meeting"
    CONFERENCE = "conference"
    PARTY = "party"
    INTERVIEW = "interview"
    PANEL = "panel"
    WORKSHOP = "workshop"


class UserRole(str, Enum):
    SPEAKER = "speaker"
    ATTENDEE = "attendee"
    HOST = "host"


# ── Request ────────────────────────────────────────────────────────────────────

class ConversationRequest(BaseModel):
    topic_category: TopicCategory
    custom_topic: Optional[str] = None
    audience_type: AudienceType
    tone: ToneMode
    context: ContextType
    location: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=5, le=480)
    user_role: Optional[UserRole] = None
    audience_size: Optional[int] = Field(None, ge=1)


# ── Response ───────────────────────────────────────────────────────────────────

class Reactions(BaseModel):
    agreement: List[str] = []
    disagreement: List[str] = []
    silence: List[str] = []
    confusion: List[str] = []


class ConversationPlan(BaseModel):
    opening_lines: List[str] = []
    topic_flow: List[str] = []
    questions: List[str] = []
    reactions: Reactions = Reactions()
    engagement_strategies: List[str] = []
    fun_elements: List[str] = []
    facts: List[str] = []
    recent_topics: List[str] = []
    transition_phrases: List[str] = []
    poll_ideas: List[str] = []


class ConversationResponse(BaseModel):
    session_id: str
    plan: ConversationPlan
    metadata: Dict[str, str] = {}


class RefineRequest(BaseModel):
    session_id: str
    feedback: str
    section: Optional[str] = None


class SessionInfo(BaseModel):
    session_id: str
    request: ConversationRequest
    plan: ConversationPlan
