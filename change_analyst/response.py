from enum import Enum

from pydantic import BaseModel, Field

from change_analyst.schema import KnowledgeState


class AgentDecision(str, Enum):
    ASK = "ask"
    DRAFT = "draft"


class RequirementFieldName(str, Enum):
    BUSINESS_OBJECTIVE = "business_objective"
    CURRENT_BEHAVIOR = "current_behavior"
    DESIRED_BEHAVIOR = "desired_behavior"
    ACTOR = "actor"
    TRIGGER = "trigger"

class FieldUpdate(BaseModel):
    field_name: RequirementFieldName
    state: KnowledgeState
    value: str | None = None


class AgentResponse(BaseModel):
    message: str

    decision: AgentDecision

    field_updates: list[FieldUpdate] = Field(default_factory=list)

    business_rules: list[str] = Field(default_factory=list)
    exceptions: list[str] = Field(default_factory=list)
    affected_systems: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)

    assumptions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)