import structlog
from typing import Tuple
import shlex
from app import cli
from common import get_issue_comment_body, get_issue_comment_id, get_repo, get_owner
from github_client import add_reaction_to_issue_comment, append_issue_comment_with_footer, GithubReaction
from click.testing import CliRunner

log = structlog.get_logger()


def process_command(command_str) -> Tuple[str, str]:
    # Split the command string into a list of arguments
    args = shlex.split(command_str)

    log.info("Processing command", args=args)
    runner = CliRunner()
    result = runner.invoke(cli, args=args)
    return result.output, str(result.exception)

if __name__ == "__main__":

    issue_comment_body = get_issue_comment_body()
    issue_comment_id = get_issue_comment_id()
    github_repo = get_repo()
    github_owner = get_owner()

    output, error = None, None
    if issue_comment_body:
        try:
            log.info(
                "Handling Slash Command for Issue Comment", 
                issue_comment_id=issue_comment_id, 
                issue_comment_body=issue_comment_body
            )
            output, error = process_command(issue_comment_body)
            log.info("Command output.", output=output, error=error)
        except Exception as e:
            error = str(e)

    else:
        log.error("Issue comment body not found.")

    if error:
        # Add reaction to the issue comment about the error
        add_reaction_to_issue_comment(
            comment_id=issue_comment_id, 
            reaction=GithubReaction.CONFUSED.value, 
            repo=github_repo, 
            owner=github_owner
        )

        # Append the error message as a footer to the issue comment
        append_issue_comment_with_footer(
            comment_id=issue_comment_id,
            body=issue_comment_body,
            footer=error,
            repo=github_repo,
            owner=github_owner
        )
    elif output:
        # Add reaction to the issue comment about the success
        add_reaction_to_issue_comment(
            comment_id=issue_comment_id,
            reaction=GithubReaction.ROCKET.value,
            repo=github_repo,
            owner=github_owner
        )
    else:
        pass
