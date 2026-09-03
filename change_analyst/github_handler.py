import json
import os
import urllib.request

from change_analyst.agent import ChangeAnalystAgent
from change_analyst.spec import render_change_spec


def load_event() -> dict:
    event_path = os.environ["GITHUB_EVENT_PATH"]

    with open(event_path, encoding="utf-8") as event_file:
        return json.load(event_file)


def get_issue_number(event: dict) -> int:
    return event["issue"]["number"]


def get_issue_comments(
    repository: str,
    issue_number: int,
) -> list[dict]:
    token = os.environ["GITHUB_TOKEN"]

    url = (
        f"https://api.github.com/repos/"
        f"{repository}/issues/{issue_number}/comments"
    )

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )

    with urllib.request.urlopen(request) as response:
        return json.load(response)


def build_conversation(
    event: dict,
    comments: list[dict],
) -> list[dict[str, str]]:
    conversation = []

    issue_body = event["issue"]["body"] or ""

    if issue_body:
        conversation.append(
            {
                "role": "requester",
                "content": issue_body,
            }
        )

    for comment in comments:
        if comment["user"]["type"] == "Bot":
            role = "analyst"
        else:
            role = "requester"

        conversation.append(
            {
                "role": role,
                "content": comment["body"],
            }
        )

    return conversation


def post_issue_comment(
    repository: str,
    issue_number: int,
    body: str,
) -> None:
    token = os.environ["GITHUB_TOKEN"]

    url = (
        f"https://api.github.com/repos/"
        f"{repository}/issues/{issue_number}/comments"
    )

    payload = json.dumps(
        {"body": body}
    ).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(request) as response:
        response.read()


def main() -> None:
    event = load_event()

    repository = os.environ["GITHUB_REPOSITORY"]
    issue_number = get_issue_number(event)

    comments = get_issue_comments(
        repository,
        issue_number,
    )

    conversation = build_conversation(
        event,
        comments,
    )

    agent = ChangeAnalystAgent()

    for message in conversation:
        agent.add_message(
            message["role"],
            message["content"],
        )

    response = agent.analyze()
    agent.apply_response(response)

    print("\nAGENT RESPONSE")
    print(response.model_dump_json(indent=2))

    print("\nCHANGE REQUEST STATE")
    print(
        json.dumps(
            agent.get_change_request_state(),
            indent=2,
        )
    )
    
    print("\nREADY FOR DRAFT")
    print(agent.is_ready_for_draft())

    if agent.is_ready_for_draft():
        spec = render_change_spec(
            agent.change_request,
            title=event["issue"]["title"],
        )

        message = (
            "I have enough information to prepare a useful draft change "
            "specification.\n\n"
            "Here is the generated draft:\n\n"
            f"{spec}"
        )
    else:
        message = response.message

    post_issue_comment(
        repository=repository,
        issue_number=issue_number,
        body=message,
    )

if __name__ == "__main__":
    main()