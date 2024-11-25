"""Main module for the Slash Command Handler."""

import shlex
from typing import Tuple

from app import cli
from click.testing import CliRunner
from common import (
    get_issue_comment_body,
    get_issue_comment_id,
    get_owner,
    get_repo,
)
from github_client import (
    GithubReaction,
    add_reaction_to_issue_comment,
    append_issue_comment_with_footer,
)
import structlog

log = structlog.get_logger()


def process_command(command_str: str) -> Tuple[str, Exception]:
    """Process the command string"""

    # Split the command string into a list of arguments
    args = shlex.split(command_str)
    log.info("Processing command.", args=args)
    runner = CliRunner()
    result = runner.invoke(cli, args=args)
    return result.output, result.exception


if __name__ == "__main__":
    issue_comment_body = get_issue_comment_body()
    issue_comment_id = get_issue_comment_id()
    github_repo = get_repo()
    github_owner = get_owner()

    exception = None
    output = ""
    try:
        if not issue_comment_body:
            raise Exception("Issue comment body not found.")

        log.info(
            "Handling Slash Command for Issue Comment.",
            issue_comment_id=issue_comment_id,
            issue_comment_body=issue_comment_body,
        )
        output, exception = process_command(issue_comment_body)
        log.info("Command output.", output=output, exception=str(exception))
    except Exception as e:
        exception = e
        output += (
            f"An error occurred while processing the command: {str(exception)}"
        )
        log.error(
            "An error occurred while processing the command.",
            exception=str(exception),
        )

    if exception:
        # Add reaction to the issue comment about the error
        add_reaction_to_issue_comment(
            comment_id=issue_comment_id,
            reaction=GithubReaction.CONFUSED.value,
            repo=github_repo,
            owner=github_owner,
        )

        # Append the error message as a footer to the issue comment
        append_issue_comment_with_footer(
            comment_id=issue_comment_id,
            body=issue_comment_body,
            footer=output,
            repo=github_repo,
            owner=github_owner,
        )
    else:
        # Add reaction to the issue comment about the success
        add_reaction_to_issue_comment(
            comment_id=issue_comment_id,
            reaction=GithubReaction.ROCKET.value,
            repo=github_repo,
            owner=github_owner,
        )

        # Append the command output as a footer to the issue comment
        append_issue_comment_with_footer(
            comment_id=issue_comment_id,
            body=issue_comment_body,
            footer=output,
            repo=github_repo,
            owner=github_owner,
        )
