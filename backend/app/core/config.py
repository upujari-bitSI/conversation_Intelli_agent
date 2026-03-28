"""Application configuration."""

from __future__ import annotations

import json
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ai_provider: str = "openai"
    ai_model: str = "gpt-4o"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    redis_url: str = ""
    news_api_key: str = ""
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: str = '["http://localhost:3000"]'

    @property
    def cors_origin_list(self) -> List[str]:
        return json.loads(self.cors_origins)

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
