"""Typed prompt registry placeholder module."""

from app.prompts.templates import PROMPT_TEMPLATES


def get_prompt(name: str) -> str:
    return PROMPT_TEMPLATES.get(name, PROMPT_TEMPLATES["default"])
