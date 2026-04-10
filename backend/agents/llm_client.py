"""
LLM Client: Wraps Google Gemini API for all agent calls.
"""
import os
import json
import re
from typing import Any, Dict, List

import google.generativeai as genai

_model_instance = None
DEFAULT_MODEL = "gemini-2.0-flash"  # fast + cheap; swap to gemini-1.5-pro for higher quality


def get_model(model: str = DEFAULT_MODEL):
    global _model_instance
    if _model_instance is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        _model_instance = genai.GenerativeModel(model)
    return _model_instance


def call_llm(
    system_prompt: str,
    messages: List[Dict[str, str]],
    max_tokens: int = 1024,
    model: str = DEFAULT_MODEL,
) -> str:
    """Call Gemini and return raw text response."""
    gemini_model = get_model(model)
    user_content = "\n".join(m["content"] for m in messages if m["role"] == "user")
    full_prompt = f"{system_prompt}\n\n{user_content}"
    response = gemini_model.generate_content(
        full_prompt,
        generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens),
    )
    return response.text


def call_llm_json(
    system_prompt: str,
    messages: List[Dict[str, str]],
    max_tokens: int = 1024,
    model: str = DEFAULT_MODEL,
) -> Dict[str, Any]:
    """Call Gemini expecting a JSON response. Returns parsed dict."""
    raw = call_llm(system_prompt, messages, max_tokens, model)
    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw: {raw}")
