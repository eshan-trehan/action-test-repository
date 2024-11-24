import click
from commands.dismiss import dismiss

@click.group()
def cli():
    """Root of CLI."""
    pass

@cli.command()
@click.pass_context
def help(ctx):
    """Show help information for commands."""

    click.echo(cli.get_help(ctx))

cli.add_command(dismiss)
