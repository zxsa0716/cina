"""Anthropic Claude provider — paid (existing v1.2 compatibility).

Setup:
    1. https://console.anthropic.com/ → API Keys → Create Key
    2. Add credit ($5 minimum)
    3. PowerShell:
       [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")

비용 (Stage 1, 5 시드 × 6 issue × 5 sample = 150 calls):
    - claude-haiku-4: ~$0.50
    - claude-sonnet-4: ~$3-5
    - claude-opus-4: ~$25-40

Install: pip install anthropic
"""
from __future__ import annotations

import logging
import os
from typing import Any

from .base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise RuntimeError("Install anthropic: pip install anthropic") from exc

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. Get key: https://console.anthropic.com/"
            )
        self.client = Anthropic(api_key=api_key)

    def default_model(self) -> str:
        return os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4")

    def supports_json_mode(self) -> bool:
        return True

    def complete(
        self,
        system: str,
        user: str,
        json_schema: dict | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = msg.content[0].text if msg.content else ""
        usage = {
            "input_tokens": msg.usage.input_tokens,
            "output_tokens": msg.usage.output_tokens,
            "total_tokens": msg.usage.input_tokens + msg.usage.output_tokens,
        }
        # 비용 추산 (Haiku 4 기준)
        cost = (msg.usage.input_tokens * 1.0 + msg.usage.output_tokens * 5.0) / 1_000_000
        return LLMResponse(
            content=text,
            model=self.model,
            usage=usage,
            cost_usd=cost,
            provider=self.name,
            raw_response=msg,
        )
