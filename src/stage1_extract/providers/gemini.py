"""Google Gemini provider — free tier (1000 RPD, 1M ctx, JSON support).

Setup (Heedo 5분):
    1. https://aistudio.google.com/apikey 접속
    2. Google 계정 로그인 → "Create API Key"
    3. Key 복사
    4. PowerShell:
       [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIza...", "User")

비용: $0 free tier, paid Tier 1은 0.10/1M tokens (Gemini 2.5 Flash-Lite).
CINA Stage 1 추산 (5 시드 × 6 issue × 5 sample = 150 calls): 무료 tier 안에 충족.

Install:
    pip install google-generativeai
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from .base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini API backend (free tier-friendly)."""

    name = "gemini"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise RuntimeError(
                "Install google-generativeai: pip install google-generativeai"
            ) from exc

        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get(
            "GOOGLE_API_KEY"
        )
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not set. Get free key: "
                "https://aistudio.google.com/apikey"
            )
        genai.configure(api_key=api_key)
        self.genai = genai

    def default_model(self) -> str:
        # 가장 generous free tier (1000 RPD)
        return "gemini-2.5-flash-lite"

    def supports_json_mode(self) -> bool:
        return True

    def complete(
        self,
        system: str,
        user: str,
        json_schema: dict | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        # Gemini API: system + user를 contents에 합침
        prompt = f"{system}\n\n---\n\n{user}"
        generation_config: dict = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_tokens,
        }
        if json_schema:
            generation_config["response_mime_type"] = "application/json"
            # Gemini는 schema도 지원하지만 단순 JSON 강제로 시작
            generation_config["response_schema"] = json_schema

        model = self.genai.GenerativeModel(
            model_name=self.model,
            generation_config=generation_config,
        )
        response = model.generate_content(prompt)
        text = response.text or ""
        usage = {}
        try:
            um = response.usage_metadata
            usage = {
                "input_tokens": um.prompt_token_count,
                "output_tokens": um.candidates_token_count,
                "total_tokens": um.total_token_count,
            }
        except Exception:
            pass
        return LLMResponse(
            content=text,
            model=self.model,
            usage=usage,
            cost_usd=0.0,  # free tier
            provider=self.name,
            raw_response=response,
        )
