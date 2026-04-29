"""LLM provider abstract base class — uniform interface across backends."""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Uniform LLM response — providers normalize to this."""
    content: str                                # raw text response
    parsed: dict | None = None                  # JSON-parsed if applicable
    model: str = ""
    usage: dict = field(default_factory=dict)   # {input_tokens, output_tokens}
    cost_usd: float = 0.0
    provider: str = ""
    raw_response: Any = None                    # provider-specific raw obj

    def parse_json(self, strict: bool = True) -> dict:
        """Parse self.content as JSON, handling markdown code fences."""
        if self.parsed is not None:
            return self.parsed
        text = self.content.strip()
        # Strip common markdown JSON fences
        if text.startswith("```"):
            text = text.split("```", 2)[1] if text.count("```") >= 2 else text[3:]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip("` \n")
        try:
            self.parsed = json.loads(text)
            return self.parsed
        except json.JSONDecodeError as exc:
            if strict:
                logger.error("JSON parse failed: %s\nResponse: %s", exc, text[:300])
                raise
            logger.warning("JSON parse failed, returning {}: %s", exc)
            return {}


class LLMProvider(ABC):
    """Abstract base for LLM backends."""

    name: str = "abstract"

    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.3,
        max_tokens: int = 1500,
        timeout: int = 60,
    ) -> None:
        self.model = model or self.default_model()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    @abstractmethod
    def default_model(self) -> str:
        """Return provider-default model name."""
        ...

    @abstractmethod
    def complete(
        self,
        system: str,
        user: str,
        json_schema: dict | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Single completion call. JSON mode enabled if json_schema provided."""
        ...

    def supports_json_mode(self) -> bool:
        """Whether this provider supports structured JSON output."""
        return False
