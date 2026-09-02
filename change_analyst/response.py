from dataclasses import dataclass, field
from enum import Enum

from change_analyst.schema import KnowledgeState


class AgentDecision(str, Enum):
    ASK = "ask"
    DRAFT = "draft"


@dataclass
class FieldUpdate:
    field_name: str
    state: KnowledgeState
    value: str | None = None


@dataclass
class AgentResponse:
    message: str

    decision: AgentDecision

    field_updates: list[FieldUpdate] = field(default_factory=list)

    business_rules: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    affected_systems: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)

    assumptions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)