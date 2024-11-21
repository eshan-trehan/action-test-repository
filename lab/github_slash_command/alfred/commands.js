const { Command } = new require("commander")
const { githubExitHandler } = new require("../common")

function commaSeparatedList(value) {
    return value.split(',');
}

const dismiss = new Command("/dismiss")
    .description("Dismiss specified reviewers from the pull request")
    .requiredOption("-r, --reviewers <reviewers>", "Comma separated list of reviewers", commaSeparatedList)
    .action((options) => {
        if (options.reviewers.length === 0) {
            console.log("No reviewers specified. Use the -r flag to specify reviewers to dismiss.")
            return
        }

        console.log("Dismissing Reviewers ", options.reviewers)
    })

dismiss.exitOverride(githubExitHandler);

module.exports = {
    dismiss
}