import json
import os
import urllib.request

from change_analyst.agent import ChangeAnalystAgent


def load_event() -> dict:
    event_path = os.environ["GITHUB_EVENT_PATH"]

    with open(event_path, encoding="utf-8") as event_file:
        return json.load(event_file)


def get_issue_number(event: dict) -> int:
    return event["issue"]["number"]


def get_user_message(event: dict) -> str:
    if "comment" in event:
        return event["comment"]["body"]

    return event["issue"]["body"] or ""


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

    issue_number = get_issue_number(event)
    user_message = get_user_message(event)

    agent = ChangeAnalystAgent()
    agent.add_message("requester", user_message)

    response = agent.analyze()

    post_issue_comment(
        repository=os.environ["GITHUB_REPOSITORY"],
        issue_number=issue_number,
        body=response.message,
    )


if __name__ == "__main__":
    main()