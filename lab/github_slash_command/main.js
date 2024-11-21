const { program } = require('commander');
const { parse } = require('shell-quote');
const { dismiss } = require('./alfred/commands');

const commandString = process.env.ISSUE_COMMENT_BODY.replaceAll("#", "\\#");

const parsedCommand = parse(commandString, null, {comments: false});
console.log("Parsed Command: ", parsedCommand);

program.addCommand(dismiss)

program.parse(parsedCommand, { from: 'user' });
