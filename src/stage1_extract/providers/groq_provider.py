"""Groq provider — Llama 3.3 70B free tier (30 RPM, 6K TPM, 1000 RPD).

Setup:
    1. https://console.groq.com/keys 접속
    2. 회원가입 (이메일 또는 Google)
    3. Create API Key → 복사
    4. PowerShell:
       [Environment]::SetEnvironmentVariable("GROQ_API_KEY", "gsk_...", "User")

비용: $0 free tier (개인 dev 충분).
초고속 inference (Llama 3.3 70B at 280+ tok/sec).

Install:
    pip install groq
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from .base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class GroqProvider(LLMProvider):
    name = "groq"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            from groq import Groq
        except ImportError as exc:
            raise RuntimeError("Install groq: pip install groq") from exc

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not set. Get free: https://console.groq.com/keys"
            )
        self.client = Groq(api_key=api_key)

    def default_model(self) -> str:
        return "llama-3.3-70b-versatile"

    def supports_json_mode(self) -> bool:
        return True

    def complete(
        self,
        system: str,
        user: str,
        json_schema: dict | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        params: dict = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if json_schema:
            params["response_format"] = {"type": "json_object"}

        resp = self.client.chat.completions.create(**params)
        text = resp.choices[0].message.content or ""
        usage = {}
        if hasattr(resp, "usage") and resp.usage:
            usage = {
                "input_tokens": resp.usage.prompt_tokens,
                "output_tokens": resp.usage.completion_tokens,
                "total_tokens": resp.usage.total_tokens,
            }
        return LLMResponse(
            content=text,
            model=self.model,
            usage=usage,
            cost_usd=0.0,
            provider=self.name,
            raw_response=resp,
        )
