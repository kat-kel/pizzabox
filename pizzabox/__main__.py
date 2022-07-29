"""ColdPizza entry point script."""

from pizzabox import cli, __app_name__

def main():
    # Call the Typer app and pass it the application's name
    # By providing a value to prog_name, the user will get the
    # correct app name when running the --help option
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
