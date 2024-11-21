const { program } = require('commander');
const { parse } = require('shell-quote');
const { dismiss } = require('./alfred/commands');
const { githubExitHandler } = require('./common');

// In order to prevent treating the argument as comments we have to escape the # character
const commandString = process.env.ISSUE_COMMENT_BODY.replaceAll("#", "\\#");

const parsedCommand = parse(commandString, null, {comments: false});
console.log("Parsed Slash Command: ", parsedCommand);

program.addCommand(dismiss)

program.exitOverride(githubExitHandler);

program.parse(parsedCommand, { from: "user" });

