#! /bin/env python
"""CLI program to Control PoE on supported routers."""
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

from typing import Optional

import typer

from .cliapp import CLIApp

app = typer.Typer(add_completion=False, no_args_is_help=True)
cliapp = CLIApp()


@app.callback(invoke_without_command=True)
def ver(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        is_eager=True,
        help="Show version number and exit.",
    )
):
    """Control PoE on supported routers."""
    if version:
        ver = metadata.version("poectrl")
        typer.echo(f"Version number : {ver}")
        raise typer.Exit()


@app.command()
def apply(
    profile_name: str = typer.Argument(
        ..., help="Profile to apply", show_default=False
    )
):
    """Call the apply function on the specified profile."""
    cliapp.apply(profile_name)


@app.command()
def show(
    profile_name: str = typer.Argument(
        ..., help="Profile to view", show_default=False
    )
):
    """Show information for the specified profile."""
    cliapp.show(profile_name)


@app.command()
def list():
    """List all profiles."""
    cliapp.list()


@app.command()
def serve(
    reload: bool = typer.Option(
        False,
        "--reload",
        help="Reload the server on code changes",
        show_default=False,
    ),
    port: int = typer.Option(8000, help="Port to listen on"),
    host: bool = typer.Option(
        False, "--host", help="Listen on all hosts", show_default=False
    ),
):
    """Run a server to provide API access."""
    cliapp.serve(reload, port, host)


if __name__ == "__main__":
    app()
