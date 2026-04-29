"""Ollama provider — local LLM (Qwen 2.5 / Llama 3.3, zero cost, offline).

Setup (Heedo 10분, completely free):
    1. https://ollama.com/download 에서 Ollama Windows installer 다운로드
    2. 설치 후 자동 실행 (background service)
    3. PowerShell:
       ollama pull qwen2.5:7b-instruct      # ~4.4 GB, 추천 (한국어/포어 OK, JSON ok)
       # 또는 더 작게:
       ollama pull qwen2.5:3b               # ~2 GB, 빠름
       # 또는 더 큰 (16GB RAM 권장):
       ollama pull qwen2.5:14b-instruct      # ~9 GB, 최고 품질
    4. CINA에서:
       export CINA_LLM_PROVIDER=ollama

비용: $0 (영구). RAM 8GB+ 노트북에서 7B 모델 가능. RAM 16GB+에서 14B 권장.
속도: M1/M2/M3 Mac은 빠름. CPU only도 작동 (느림).

Install:
    pip install ollama
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from .base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, host: str | None = None, **kwargs):
        super().__init__(**kwargs)
        try:
            import ollama
        except ImportError as exc:
            raise RuntimeError("Install ollama: pip install ollama") from exc
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.Client(host=self.host)

    def default_model(self) -> str:
        return os.environ.get("OLLAMA_MODEL", "qwen2.5:7b-instruct")

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
        options = {
            "temperature": self.temperature,
            "num_predict": self.max_tokens,
        }
        chat_kwargs: dict = {
            "model": self.model,
            "messages": messages,
            "options": options,
        }
        if json_schema:
            # Ollama supports `format=json` (basic) or schema dict (>=0.3.0)
            chat_kwargs["format"] = json_schema if isinstance(json_schema, dict) else "json"

        resp = self.client.chat(**chat_kwargs)
        text = resp.get("message", {}).get("content", "")
        usage = {}
        if "prompt_eval_count" in resp:
            usage = {
                "input_tokens": resp.get("prompt_eval_count", 0),
                "output_tokens": resp.get("eval_count", 0),
                "total_tokens": resp.get("prompt_eval_count", 0) + resp.get("eval_count", 0),
            }
        return LLMResponse(
            content=text,
            model=self.model,
            usage=usage,
            cost_usd=0.0,
            provider=self.name,
            raw_response=resp,
        )
