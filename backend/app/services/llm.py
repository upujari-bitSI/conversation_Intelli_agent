"""LLM client abstraction – supports OpenAI and Anthropic."""

from __future__ import annotations

from app.core.config import settings


def get_llm(temperature: float = 0.7):
    """Return a LangChain chat model based on configuration."""
    provider = settings.ai_provider.lower()

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=settings.ai_model or "claude-sonnet-4-20250514",
            anthropic_api_key=settings.anthropic_api_key,
            temperature=temperature,
            max_tokens=4096,
        )

    # Default: OpenAI
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=settings.ai_model or "gpt-4o",
        openai_api_key=settings.openai_api_key,
        temperature=temperature,
        max_tokens=4096,
    )
