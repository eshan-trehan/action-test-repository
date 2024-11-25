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


def process_command(command_str: str) -> Tuple[str, str]:
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

    error = None
    output = ""
    if issue_comment_body:
        try:
            log.info(
                "Handling Slash Command for Issue Comment.",
                issue_comment_id=issue_comment_id,
                issue_comment_body=issue_comment_body,
            )
            output, error = process_command(issue_comment_body)
            log.info("Command output.", output=output, error=error)
        except Exception as e:
            output += (
                f"An error occurred while processing the command: {str(e)}"
            )
            log.error(
                "An error occurred while processing the command.", error=str(e)
            )

    else:
        error = "Issue comment body not found."
        log.error("Issue comment body not found.")

    if error:
        # Add reaction to the issue comment about the error
        add_reaction_to_issue_comment(
            comment_id=issue_comment_id,
            reaction=GithubReaction.CONFUSED.value,
            repo=github_repo,
            owner=github_owner,
        )

        footer_text = output + f"\nError: {error}"

        # Append the error message as a footer to the issue comment
        append_issue_comment_with_footer(
            comment_id=issue_comment_id,
            body=issue_comment_body,
            footer=footer_text,
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
