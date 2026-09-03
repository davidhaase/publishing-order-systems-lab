from pathlib import Path

from change_analyst.schema import ChangeRequest, KnowledgeState


TEMPLATE_PATH = (
    Path(__file__).parent
    / "templates"
    / "change-spec.md"
)


def _requirement_value(requirement) -> str:
    if requirement.state == KnowledgeState.KNOWN:
        return requirement.value or "Not specified."

    if requirement.state == KnowledgeState.NOT_APPLICABLE:
        return "Not applicable."

    return "Unresolved."


def _render_list(items: list[str]) -> str:
    if not items:
        return "None identified."

    return "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(items, start=1)
    )


def render_change_spec(
    change_request: ChangeRequest,
    title: str = "Untitled Change",
) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    replacements = {
        "title": title,
        "business_objective": _requirement_value(
            change_request.business_objective
        ),
        "current_behavior": _requirement_value(
            change_request.current_behavior
        ),
        "desired_behavior": _requirement_value(
            change_request.desired_behavior
        ),
        "trigger": _requirement_value(
            change_request.trigger
        ),
        "business_rules": _render_list(
            change_request.business_rules
        ),
        "exceptions": _render_list(
            change_request.exceptions
        ),
        "affected_systems": _render_list(
            change_request.affected_systems
        ),
        "acceptance_criteria": _render_list(
            change_request.acceptance_criteria
        ),
        "assumptions": _render_list(
            change_request.assumptions
        ),
        "open_questions": _render_list(
            change_request.open_questions
        ),
    }

    for key, value in replacements.items():
        template = template.replace(
            "{{ " + key + " }}",
            value,
        )

    return template