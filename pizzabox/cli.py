"""This module provides the CLI."""

from typing import Optional

import typer

from pizzabox import __app_name__, __version__

# Makes an instance of the Typer application, as variable "app"
app = typer.Typer()

# Defines the Boolean function _version_callback(). 
# When the value is True, the function prints the application's name and version, 
# then raises a typer.Exit exception to cleanly exit the application.
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

# Defines the function main() as a Typer callback function
@app.callback()

def main(
    version: Optional[bool] = typer.Option(
        # The first positional argument to the initializer of Option is None, 
        # which is required and supplies the option's default value.
        None,
        # Sets the command-line names for the version option: -v and --version
        "--version",
        "-v",
        # Attaches a callback function, _version_callback(), 
        # which means that running the option automatically calls the function.
        help="Show the application's version and exit.",
        # is_eager argument tells Typer that the version command-line option 
        # has precedence over other commands in the current application.
        callback=_version_callback,
        # is_eager argument tells Typer that the version command-line option 
        # has precedence over other commands in the current application.
        is_eager=True,
    )
) -> None:
    return