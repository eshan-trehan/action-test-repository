from typing import List
import requests
import structlog

ALFRED_URL = "http://alfred.com"

log = structlog.get_logger()

def dismiss_reviewers(pr_number: int, pr_repo: str, pr_owner:str, reviewers: List[str]):
    """Dismiss the reviewers on a pull request."""

    url = f"{ALFRED_URL}/github/dismiss-reviewers"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "pull_request_id": f"{pr_owner}/{pr_repo}/{pr_number}",
        "reviewers": reviewers
    }

    # Make the PUT request, sending the payload as JSON
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        log.info("Successfully dismissed reviewers.")
    else:
        log.error("Failed to dismiss reviewers", url=url, status_code=response.status_code, response=response.json())
        raise Exception("Failed to dismiss reviewers")
