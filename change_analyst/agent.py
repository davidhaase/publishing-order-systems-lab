from dataclasses import asdict
from pathlib import Path
from typing import Any

from change_analyst.schema import ChangeRequest
from change_analyst.response import AgentResponse

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
            "unresolved_required_fields": self.get_unresolved_required_fields(),
        }

    def apply_response(self, response: AgentResponse) -> None:
        for update in response.field_updates:
            if hasattr(self.change_request, update.field_name):
                requirement = getattr(
                    self.change_request,
                    update.field_name,
                )

                requirement.state = update.state
                requirement.value = update.value

        self.change_request.business_rules.extend(
            response.business_rules
        )

        self.change_request.exceptions.extend(
            response.exceptions
        )

        self.change_request.affected_systems.extend(
            response.affected_systems
        )

        self.change_request.acceptance_criteria.extend(
            response.acceptance_criteria
        )

        self.change_request.assumptions.extend(
            response.assumptions
        )

        self.change_request.open_questions.extend(
            response.open_questions
        )

        self.add_message(
            "analyst",
            response.message,
        )

    def analyze(self) -> str:
        context = self.build_context()

        response = self.client.responses.create(
            model="gpt-5.6-terra",
            instructions=self.system_prompt,
            input=str(context),
        )

        return response.output_text


if __name__ == "__main__":
    agent = ChangeAnalystAgent()

    agent.add_message(
        "requester",
        "We need to stop sending order acknowledgements immediately "
        "because sometimes pricing hasn't finished yet.",
    )

    print(agent.analyze())