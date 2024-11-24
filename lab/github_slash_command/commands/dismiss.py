import click
import structlog
from click import ClickException
from alfred_client import dismiss_reviewers 
from common import get_repo, get_owner, get_pull_request_number

log = structlog.get_logger()


@click.command("/dismiss")
@click.option("-r", "--reviewers", help="Comma separated list of reviewers to dismiss", required=True)
def dismiss(reviewers: str):
    """Dismiss the reviewers"""


    reviewers = [reviewer.strip() for reviewer in reviewers.split(",")]

    # Validate the passed reviewers
    for reviewer in reviewers:
        if len(reviewer) < 2:
            raise ClickException("Not a valid reviewer name: {reviewer}")
        elif reviewer[0] != "@" and reviewer[0] != "#":
            raise ClickException(f"Reviewer name should start with @ or #: {reviewer}")


    click.echo(f"Dismissing the reviewers: {reviewers}")
    try:
        dismiss_reviewers(
            pr_number=get_pull_request_number(),
            pr_repo=get_repo(),
            pr_owner=get_owner(),
            reviewers=reviewers
        )
    except Exception as e:
        click.echo(f"Failed to dismiss reviewers: {str(e)}")
        raise ClickException(str(e))
