"""Conservative content resolution for optional LLM assistance."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def resolve_content(existing: dict[str, Any], proposed: dict[str, Any] | None = None, llm_error: str | None = None) -> dict[str, Any]:
    """Preserve approved human copy and preserve all existing copy on LLM failure."""
    if existing.get("generation_method") == "human" and existing.get("state") == "APPROVED":
        return deepcopy(existing)
    if llm_error or proposed is None:
        return deepcopy(existing)
    candidate = deepcopy(proposed)
    candidate["generation_method"] = "llm_assisted"
    candidate["state"] = "READY_FOR_REVIEW"
    return candidate
