"""Github client to interact with the Github API"""
import requests
from github import Github
from enum import Enum
from common import get_github_token
import structlog

DEFAULT_REPO = "sdmain"
DEFAULT_OWNER = "scaledata"

HEADERS = {
    'Accept': 'application/vnd.github.squirrel-girl-preview+json',
    'Authorization': f'token {get_github_token()}'
}

log = structlog.get_logger()
github_client = Github(get_github_token())


class GithubReaction(Enum):
    """Github Reaction constants."""

    THUMBS_UP = "+1"
    THUMBS_DOWN = "-1"
    CONFUSED = "confused"
    ROCKET = "rocket"
    EYES = "eyes"


def add_reaction_to_issue_comment(comment_id:int, reaction:str, repo: str = DEFAULT_REPO, owner: str = DEFAULT_OWNER):
    """Add a reaction to an issue comment."""
    # GitHub API endpoint for adding a reaction to an issue comment
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}/reactions"
    payload = { "content": reaction }

    response = requests.post(url, json=payload, headers=HEADERS)

    # Check the response
    if response.status_code == 200 or response.status_code == 201:
        log.info("Successfully added reaction to Issue Comment.")
    else:
        log.error("Failed to add reaction", response=response.json())

def append_issue_comment_with_footer(comment_id:int, body:str, footer:str, repo: str = DEFAULT_REPO, owner: str = DEFAULT_OWNER):
    """Append a footer to an issue comment."""

    footer_lines = footer.split("\n")
    footer = "\n".join([f"> {line}" for line in footer_lines])

    final_body = f"{body}\n\n{footer}"

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"
    payload = { "body": final_body }

    response = requests.patch(url, json=payload, headers=HEADERS)

    # Check the response
    if response.status_code == 200 or response.status_code == 201:
        log.info("Successfully added footer to Issue Comment.")
    else:
        log.error("Failed to add footer to Issue Comment.", response=response.json())
