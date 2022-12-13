#! /bin/env python
"""CLI program to Control PoE on supported routers."""

import typer

from .cliapp import CLIApp

app = typer.Typer(add_completion=False, no_args_is_help=True)
cliapp = CLIApp()


@app.command()
def apply(profile_name: str):
    """Call the apply function on the specified profile."""
    cliapp.apply(profile_name)


@app.command()
def show(profile_name: str):
    """Show information for the specified profile."""
    cliapp.show(profile_name)


@app.command()
def list():
    """List all profiles."""
    cliapp.list()


if __name__ == "__main__":
    app()
