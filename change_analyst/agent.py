from dataclasses import asdict
from pathlib import Path
from typing import Any

from change_analyst.schema import ChangeRequest
from change_analyst.response import AgentDecision, AgentResponse
from change_analyst.spec import render_change_spec

from openai import OpenAI

PROMPT_PATH = Path(__file__).parent / "prompts" / "system.md"


class ChangeAnalystAgent:
    def __init__(self) -> None:
        self.system_prompt = self._load_system_prompt()
        self.change_request = ChangeRequest()
        self.conversation: list[dict[str, str]] = []
        self.client = OpenAI()

    def _load_system_prompt(self) -> str:
        return PROMPT_PATH.read_text(encoding="utf-8")

    def add_message(self, role: str, content: str) -> None:
        self.conversation.append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_change_request_state(self) -> dict[str, Any]:
        return asdict(self.change_request)

    def get_conversation(self) -> list[dict[str, str]]:
        return self.conversation.copy()

    def get_unresolved_required_fields(self) -> list[str]:
        return self.change_request.unresolved_required_fields()

    def build_context(self) -> dict[str, Any]:
        return {
            "system_prompt": self.system_prompt,
            "conversation": self.get_conversation(),
            "change_request": self.get_change_request_state(),
        }

    def apply_response(self, response: AgentResponse) -> None:
        for update in response.field_updates:
            if hasattr(self.change_request, update.field_name):
                requirement = getattr(
                    self.change_request,
                    update.field_name.value,
                )

                requirement.state = update.state
                requirement.value = update.value

        self.change_request.business_rules = (
            response.business_rules.copy()
        )

        self.change_request.exceptions = (
            response.exceptions.copy()
        )

        self.change_request.affected_systems = (
            response.affected_systems.copy()
        )

        self.change_request.acceptance_criteria = (
            response.acceptance_criteria.copy()
        )

        self.change_request.assumptions = (
            response.assumptions.copy()
        )

        self.change_request.open_questions.extend(
            response.open_questions
        )

        self.change_request.open_questions = (
            response.open_questions.copy()
        )

        self.add_message(
            "analyst",
            response.message,
        )

    def analyze(self) -> AgentResponse:
        context = self.build_context()

        response = self.client.responses.parse(
            model="gpt-5.6-terra",
            instructions=self.system_prompt,
            input=str(context),
            text_format=AgentResponse,
        )

        return response.output_parsed

    def is_ready_for_draft(self) -> bool:
        return self.change_request.is_ready_for_draft()


if __name__ == "__main__":
    agent = ChangeAnalystAgent()

    agent.add_message(
        "requester",
        "We need to stop sending order acknowledgements immediately "
        "because sometimes pricing hasn't finished yet.",
    )

    first_response = agent.analyze()
    agent.apply_response(first_response)

    print("FIRST RESPONSE")
    print(first_response.model_dump_json(indent=2))

    agent.add_message(
        "requester",
        "It happens with EDI orders. We send the 855 too early. "
        "I think it gets created right after the 850 is accepted. "
        "It should wait until we've actually priced the order.",
    )

    second_response = agent.analyze()

    agent.apply_response(second_response)

    print("\nSECOND RESPONSE")
    print(second_response.model_dump_json(indent=2))

    agent.add_message(
        "requester",
        "That's a good question. I don't know. Operations needs to decide that. "
        "But if pricing succeeds, yes, send the 855 once we have the final price.",
    )

    third_response = agent.analyze()
    agent.apply_response(third_response)

    print("\nTHIRD RESPONSE")
    print(third_response.model_dump_json(indent=2))

    if agent.is_ready_for_draft():
        spec = render_change_spec(
            agent.change_request,
            title="Delay EDI 855 Until Pricing Completes",
        )

        print("\nGENERATED CHANGE SPEC")
        print(spec)

    