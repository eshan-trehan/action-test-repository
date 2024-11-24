import os

def get_issue_comment_body() -> str:
    """Get the issue comment body from the environment."""

    return os.environ["ISSUE_COMMENT_BODY"]

def get_issue_comment_id() -> int:
    """Get the issue comment ID from the environment."""

    return int(os.environ["ISSUE_COMMENT_ID"])

def get_github_token() -> str:
    """Get the Github token from the environment."""

    return os.environ["GITHUB_TOKEN"]

def get_repo() -> str:
    """Get the Github repository from the environment."""

    return os.environ["REPO"]

def get_owner() -> str:
    """Get the Github owner from the environment."""

    return os.environ["OWNER"]

def get_pull_request_number() -> int:
    """Get the pull request number from the environment."""

    return int(os.environ["PULL_REQUEST_NUMBER"])
