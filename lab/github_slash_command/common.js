const { Octokit } = require("@octokit/rest");

const octokit = new Octokit();

function githubExitHandler(err) {
    console.log("Exit Override: ", err.message);
    octokit.rest.reactions.createForIssueComment({
        owner: process.env.OWNER,
        repo: process.env.REPO,
        comment_id: process.env.ISSUE_COMMENT_ID,
        content: "confused"
    })
    console.log("Adding a comment to the PR with the error message.")
}

module.exports = {
    githubExitHandler
}