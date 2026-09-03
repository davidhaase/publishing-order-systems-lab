from change_analyst.agent import ChangeAnalystAgent
from change_analyst.response import AgentDecision, AgentResponse, FieldUpdate
from change_analyst.schema import KnowledgeState


def test_apply_response_updates_change_request():
    agent = ChangeAnalystAgent()

    response = AgentResponse(
        message=(
            "It sounds like acknowledgements are being sent before pricing "
            "completes. What currently triggers the acknowledgement?"
        ),
        decision=AgentDecision.ASK,
        field_updates=[
            FieldUpdate(
                field_name="business_objective",
                state=KnowledgeState.KNOWN,
                value=(
                    "Prevent order acknowledgements from being sent before "
                    "pricing has completed."
                ),
            ),
        ],
        assumptions=[
            "The current acknowledgement timing may be related to incomplete pricing."
        ],
        open_questions=[
            "What currently triggers the acknowledgement?"
        ],
    )

    agent.apply_response(response)

    assert (
        agent.change_request.business_objective.state
        == KnowledgeState.KNOWN
    )

    assert (
        agent.change_request.business_objective.value
        == "Prevent order acknowledgements from being sent before pricing has completed."
    )

    assert (
        "The current acknowledgement timing may be related to incomplete pricing."
        in agent.change_request.assumptions
    )

    assert (
        "What currently triggers the acknowledgement?"
        in agent.change_request.open_questions
    )

    assert agent.get_conversation()[-1]["role"] == "analyst"
    assert agent.get_conversation()[-1]["content"] == response.message