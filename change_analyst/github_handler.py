import base64
import json
import os
import re
import urllib.request

from change_analyst.agent import ChangeAnalystAgent
from change_analyst.spec import render_change_spec


def load_event() -> dict:
    event_path = os.environ["GITHUB_EVENT_PATH"]

    with open(event_path, encoding="utf-8") as event_file:
        return json.load(event_file)


def get_issue_number(event: dict) -> int:
    return event["issue"]["number"]


def github_request(
    url: str,
    method: str = "GET",
    payload: dict | None = None,
) -> dict:
    token = os.environ["GITHUB_TOKEN"]

    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    with urllib.request.urlopen(request) as response:
        return json.load(response)


def get_issue_comments(
    repository: str,
    issue_number: int,
) -> list[dict]:
    url = (
        f"https://api.github.com/repos/"
        f"{repository}/issues/{issue_number}/comments"
    )

    return github_request(url)


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
    url = (
        f"https://api.github.com/repos/"
        f"{repository}/issues/{issue_number}/comments"
    )

    github_request(
        url=url,
        method="POST",
        payload={"body": body},
    )


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def get_branch_sha(
    repository: str,
    branch: str,
) -> str:
    url = (
        f"https://api.github.com/repos/"
        f"{repository}/git/ref/heads/{branch}"
    )

    response = github_request(url)

    return response["object"]["sha"]


def create_branch(
    repository: str,
    branch_name: str,
    source_sha: str,
) -> None:
    url = (
        f"https://api.github.com/repos/"
        f"{repository}/git/refs"
    )

    github_request(
        url=url,
        method="POST",
        payload={
            "ref": f"refs/heads/{branch_name}",
            "sha": source_sha,
        },
    )


def create_file(
    repository: str,
    path: str,
    branch: str,
    content: str,
    commit_message: str,
) -> None:
    url = (
        f"https://api.github.com/repos/"
        f"{repository}/contents/{path}"
    )

    encoded_content = base64.b64encode(
        content.encode("utf-8")
    ).decode("utf-8")

    github_request(
        url=url,
        method="PUT",
        payload={
            "message": commit_message,
            "content": encoded_content,
            "branch": branch,
        },
    )


def create_pull_request(
    repository: str,
    title: str,
    head: str,
    base: str,
    body: str,
) -> dict:
    url = (
        f"https://api.github.com/repos/"
        f"{repository}/pulls"
    )

    return github_request(
        url=url,
        method="POST",
        payload={
            "title": title,
            "head": head,
            "base": base,
            "body": body,
            "draft": True,
        },
    )


def create_spec_pull_request(
    event: dict,
    repository: str,
    issue_number: int,
    spec: str,
) -> dict:
    issue_title = event["issue"]["title"]
    default_branch = event["repository"]["default_branch"]

    slug = slugify(issue_title)

    branch_name = (
        f"change-analyst/issue-{issue_number}-{slug}"
    )

    file_path = (
        f"docs/change-requests/"
        f"{issue_number}-{slug}.md"
    )

    source_sha = get_branch_sha(
        repository,
        default_branch,
    )

    create_branch(
        repository,
        branch_name,
        source_sha,
    )

    create_file(
        repository=repository,
        path=file_path,
        branch=branch_name,
        content=spec,
        commit_message=(
            f"Add draft change specification for issue #{issue_number}"
        ),
    )

    pull_request = create_pull_request(
        repository=repository,
        title=f"Draft change specification: {issue_title}",
        head=branch_name,
        base=default_branch,
        body=(
            "## Change Analyst Draft\n\n"
            f"Generated from the requirements elicitation in #{issue_number}.\n\n"
            "This specification is a draft for human review. "
            "Assumptions and unresolved questions remain explicitly "
            "identified in the document.\n\n"
            f"Closes #{issue_number}"
        ),
    )

    return pull_request


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

        pull_request = create_spec_pull_request(
            event=event,
            repository=repository,
            issue_number=issue_number,
            spec=spec,
        )

        message = (
            "I have enough information to prepare a useful draft "
            "change specification.\n\n"
            f"Draft specification created for human review: "
            f"{pull_request['html_url']}\n\n"
            "Unresolved assumptions and open questions have been "
            "preserved in the specification."
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