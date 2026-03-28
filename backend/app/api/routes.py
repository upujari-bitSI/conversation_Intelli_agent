"""API routes for the Conversation Intelligence Agent."""

from __future__ import annotations

import json
from io import BytesIO

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.agents.orchestrator import generate_conversation_plan, refine_plan
from app.models.schemas import (
    ConversationRequest,
    ConversationResponse,
    RefineRequest,
)
from app.services.memory import get_session

router = APIRouter(prefix="/api/v1", tags=["conversation"])


@router.post("/generate", response_model=ConversationResponse)
async def generate(request: ConversationRequest):
    """Generate a full conversation strategy plan."""
    params = request.model_dump()
    result = await generate_conversation_plan(params)
    return ConversationResponse(**result)


@router.post("/refine", response_model=ConversationResponse)
async def refine(request: RefineRequest):
    """Refine an existing conversation plan with user feedback."""
    session = get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await refine_plan(
        session_id=request.session_id,
        feedback=request.feedback,
        section=request.section,
        current_plan=session["plan"],
        params=session["request"],
    )
    return ConversationResponse(**result)


@router.get("/session/{session_id}")
async def get_session_data(session_id: str):
    """Retrieve a stored session."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/export/{session_id}")
async def export_pdf(session_id: str):
    """Export the conversation plan as a PDF."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    pdf_bytes = _generate_pdf(session["plan"])
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=conversation-plan-{session_id[:8]}.pdf"},
    )


def _generate_pdf(plan: dict) -> bytes:
    """Generate a simple PDF from the conversation plan."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Conversation Intelligence Plan", ln=True, align="C")
    pdf.ln(10)

    sections = [
        ("Opening Lines", plan.get("opening_lines", [])),
        ("Topic Flow", plan.get("topic_flow", [])),
        ("Questions", plan.get("questions", [])),
        ("Engagement Strategies", plan.get("engagement_strategies", [])),
        ("Fun Elements", plan.get("fun_elements", [])),
        ("Facts", plan.get("facts", [])),
        ("Recent Topics", plan.get("recent_topics", [])),
        ("Transition Phrases", plan.get("transition_phrases", [])),
        ("Poll Ideas", plan.get("poll_ideas", [])),
    ]

    for title, items in sections:
        if items:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, title, ln=True)
            pdf.set_font("Helvetica", "", 10)
            for item in items:
                text = str(item)
                pdf.multi_cell(0, 6, f"  - {text}")
            pdf.ln(4)

    # Reactions section
    reactions = plan.get("reactions", {})
    if reactions:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Reactions", ln=True)
        for rtype, items in reactions.items():
            if items:
                pdf.set_font("Helvetica", "BI", 10)
                pdf.cell(0, 6, f"  {rtype.title()}:", ln=True)
                pdf.set_font("Helvetica", "", 10)
                for item in items:
                    pdf.multi_cell(0, 6, f"    - {item}")

    return pdf.output()
