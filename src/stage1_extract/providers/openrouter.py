"""OpenRouter provider — unified API for many free models.

OpenRouter aggregates 100+ LLM providers + has free model pool:
    - deepseek/deepseek-chat-v3.1:free
    - meta-llama/llama-3.3-70b-instruct:free
    - google/gemini-2.0-flash-exp:free
    - qwen/qwen-2.5-72b-instruct:free
    등 수십 개

Setup:
    1. https://openrouter.ai/keys 접속 → 회원가입
    2. Create Key (free pool 사용 시 결제 정보 불필요)
    3. PowerShell:
       [Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-...", "User")

비용: free pool은 $0 (단, 가용성 변동). paid는 매우 저렴.

Install:
    pip install openai     # OpenRouter는 OpenAI-compatible API
"""
from __future__ import annotations

import logging
import os
from typing import Any

from .base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class OpenRouterProvider(LLMProvider):
    name = "openrouter"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai: pip install openai") from exc

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY not set. Get free: https://openrouter.ai/keys"
            )
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/cina-research/cina",
                "X-Title": "CINA Climate Issue-Network Analysis",
            },
        )

    def default_model(self) -> str:
        # Free pool 우선
        return os.environ.get(
            "OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free"
        )

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
        if resp.usage:
            usage = {
                "input_tokens": resp.usage.prompt_tokens,
                "output_tokens": resp.usage.completion_tokens,
                "total_tokens": resp.usage.total_tokens,
            }
        return LLMResponse(
            content=text,
            model=self.model,
            usage=usage,
            cost_usd=0.0 if ":free" in self.model else None,
            provider=self.name,
            raw_response=resp,
        )
