"""LLM provider abstraction for Stage 1 stance extraction.

CINA Stage 1 LLM 추출은 Anthropic Claude API 외에도 다음 무료/저비용
backend로 전환 가능:

    - gemini       : Google Gemini API (free tier 1000 RPD, 1M ctx)
    - groq         : Groq Llama 3.3 70B (free 30 RPM)
    - ollama       : Local Ollama (Qwen 2.5 / Llama 3.3, zero cost)
    - openrouter   : OpenRouter free pool (DeepSeek, Llama 등 free models)
    - anthropic    : Claude (paid, 기본 v1.2 호환성)

기본 provider는 환경변수 `CINA_LLM_PROVIDER`로 설정. 미설정 시 'gemini'.

Heedo가 무료로 사용하려면:
    export CINA_LLM_PROVIDER=gemini       # 가장 generous
    export GEMINI_API_KEY=...

또는 완전 로컬 (zero cost):
    ollama pull qwen2.5:7b-instruct
    export CINA_LLM_PROVIDER=ollama
"""
from __future__ import annotations

import os
from typing import Any

from .base import LLMProvider, LLMResponse


def get_provider(name: str | None = None, **kwargs: Any) -> LLMProvider:
    """Factory — return provider instance by name.

    Args:
        name: 'gemini' | 'groq' | 'ollama' | 'openrouter' | 'anthropic'.
              If None, reads CINA_LLM_PROVIDER env var (default 'gemini').
    """
    name = (name or os.environ.get("CINA_LLM_PROVIDER", "gemini")).lower()

    if name == "gemini":
        from .gemini import GeminiProvider
        return GeminiProvider(**kwargs)
    if name == "groq":
        from .groq_provider import GroqProvider
        return GroqProvider(**kwargs)
    if name == "ollama":
        from .ollama_provider import OllamaProvider
        return OllamaProvider(**kwargs)
    if name == "openrouter":
        from .openrouter import OpenRouterProvider
        return OpenRouterProvider(**kwargs)
    if name == "anthropic":
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider(**kwargs)
    raise ValueError(f"Unknown LLM provider: {name}. Choose from "
                     "gemini, groq, ollama, openrouter, anthropic.")


__all__ = ["LLMProvider", "LLMResponse", "get_provider"]
