"""Controlled state domains for Kinder Signs publication operations."""

from __future__ import annotations

from enum import Enum


class InvalidTransition(ValueError):
    """Raised when an operation attempts to bypass a governed state."""


class TechnicalState(str, Enum):
    NOT_RUN = "NOT_RUN"
    PASS = "PASS"
    REVIEW_NEEDED = "REVIEW_NEEDED"
    FAIL = "FAIL"


class ContentState(str, Enum):
    DRAFT = "DRAFT"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    APPROVED = "APPROVED"
    CHANGES_REQUIRED = "CHANGES_REQUIRED"


class VisualState(str, Enum):
    NEEDS_ARTWORK = "NEEDS_ARTWORK"
    NEEDS_HAND_REVIEW = "NEEDS_HAND_REVIEW"
    READY = "READY"
    CHANGES_REQUIRED = "CHANGES_REQUIRED"


class PublicationState(str, Enum):
    DRAFT = "DRAFT"
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"


ALLOWED_TRANSITIONS = {
    "technical": {
        "NOT_RUN": {"PASS", "REVIEW_NEEDED", "FAIL"},
        "PASS": {"REVIEW_NEEDED", "FAIL"},
        "REVIEW_NEEDED": {"PASS", "FAIL"},
        "FAIL": {"NOT_RUN"},
    },
    "content": {
        "DRAFT": {"READY_FOR_REVIEW"},
        "READY_FOR_REVIEW": {"APPROVED", "CHANGES_REQUIRED"},
        "APPROVED": {"CHANGES_REQUIRED"},
        "CHANGES_REQUIRED": {"DRAFT"},
    },
    "visual": {
        "NEEDS_ARTWORK": {"NEEDS_HAND_REVIEW", "CHANGES_REQUIRED"},
        "NEEDS_HAND_REVIEW": {"READY", "CHANGES_REQUIRED"},
        "READY": {"CHANGES_REQUIRED"},
        "CHANGES_REQUIRED": {"NEEDS_ARTWORK"},
    },
    "publication": {
        "DRAFT": {"READY_FOR_HUMAN_REVIEW"},
        "READY_FOR_HUMAN_REVIEW": {"APPROVED", "DRAFT"},
        "APPROVED": {"PUBLISHED", "DRAFT"},
        "PUBLISHED": set(),
    },
}


def transition_state(domain: str, current: str, target: str) -> str:
    """Return target only when the explicit domain transition is allowed."""
    if domain not in ALLOWED_TRANSITIONS:
        raise InvalidTransition(f"Unknown state domain: {domain}")
    allowed = ALLOWED_TRANSITIONS[domain].get(current)
    if allowed is None:
        raise InvalidTransition(f"Unknown {domain} state: {current}")
    if target not in allowed:
        raise InvalidTransition(f"Invalid {domain} transition: {current} → {target}")
    return target
