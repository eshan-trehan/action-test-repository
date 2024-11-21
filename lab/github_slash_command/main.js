const { program } = require('commander');
const { parse } = require('shell-quote');
const { dismiss } = require('./alfred/commands');

// In order to prevent treating the argument as comments we have to escape the # character
const commandString = process.env.ISSUE_COMMENT_BODY.replaceAll("#", "\\#");

const parsedCommand = parse(commandString, null, {comments: false});
console.log("Parsed Slash Command: ", parsedCommand);

program.addCommand(dismiss)

program.parse(parsedCommand, { from: "user" });

program.configureOutput({
  writeOut: (str) => {
    // Handle standard output (stdout)
    console.log('Captured STDOUT:', str);
    // You can also write to a file or buffer if needed
  },
  writeErr: (str) => {
    // Handle standard error output (stderr)
    console.error('Captured STDERR:', str);
  },
  outputError: (str, write) => {
    // Customize error output
    console.error('Captured ERROR:', str);
    // Decide whether to write the error using the provided write function
    // write(str);
  }
});
