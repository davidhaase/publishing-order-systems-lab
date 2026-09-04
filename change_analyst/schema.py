from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class KnowledgeState(str, Enum):
    KNOWN = "known"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN_REQUIRED = "unknown_required"


@dataclass
class RequirementField:
    state: KnowledgeState = KnowledgeState.UNKNOWN_REQUIRED
    value: Optional[str] = None


@dataclass
class ChangeRequest:
    business_objective: RequirementField = field(default_factory=RequirementField)
    current_behavior: RequirementField = field(default_factory=RequirementField)
    desired_behavior: RequirementField = field(default_factory=RequirementField)
    actor: RequirementField = field(default_factory=RequirementField)
    trigger: RequirementField = field(default_factory=RequirementField)

    business_rules: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    affected_systems: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)

    assumptions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    blocking_questions: list[str] = field(default_factory=list)

    def unresolved_required_fields(self) -> list[str]:
        unresolved = []

        for name in [
            "business_objective",
            "current_behavior",
            "desired_behavior",
            "actor",
            "trigger",
        ]:
            requirement = getattr(self, name)

            if requirement.state == KnowledgeState.UNKNOWN_REQUIRED:
                unresolved.append(name)

        return unresolved

    def is_ready_for_draft(self) -> bool:
        required_fields = [
            self.business_objective,
            self.current_behavior,
            self.desired_behavior,
            self.trigger,
        ]
    
        core_fields_known = all(
            requirement.state == KnowledgeState.KNOWN
            for requirement in required_fields
        )
    
        return (
            core_fields_known
            and not self.blocking_questions
        )
