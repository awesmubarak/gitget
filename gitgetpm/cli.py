#!/usr/bin/env python3

"""Gitget.

Package manager for git repositories.

Usage:
    gitget install <package_url> [<package_name>] [options]
    gitget remove <package_name> [--soft] [options]
    gitget update [options]
    gitget move <package_name> <location> [options]
    gitget list [options]
    gitget edit [options]
    gitget doctor [options]
    gitget help <command>
    gitget -h | --help
    gitget --version

Global options:
    --debug    Increases verbosity of the output
    --nocolor  Logs will not have colors in them

Examples:
    gitget install awesmubarak/git-get
    gitget update
    gitget remove awesmubarak/git-get

Help:
    For help using this tool, please open an issue on the Github repository:
    https://github.com/awesmubarak/gitget

"""

from .version import __version__
from docopt import docopt
from gitgetpm import commands
from inspect import getmembers, isclass
from loguru import logger
from sys import stderr


def setup_logging(debug_level, colorize):
    """Sets up the format for logging, based on the debug level (info/dbug)."""
    logger.remove()

    if debug_level == "info":
        logger_format = "<green>{time:HH:mm:ss}</green> <level>{message}</level>"
        logger.add(
            stderr,
            colorize=colorize,
            format=logger_format,
            level="INFO",
            backtrace=False,
            diagnose=False,
        )
    else:
        logger_format = "<green>{time:HH:mm:ss}</green> {file: <12} <level>{level: <8} {message}</level>"
        logger.add(
            stderr,
            colorize=colorize,
            format=logger_format,
            level="DEBUG",
            backtrace=True,
            diagnose=True,
        )


def main():
    # setup the argument parser with the docstring and imported version number
    arguments = docopt(__doc__, version=f"Gitget {__version__}")

    # set up the logger
    debug_level = "debug" if arguments["--debug"] else "info"
    colorize = False if arguments["--nocolor"] else True
    setup_logging(debug_level, colorize)

    # dynamically call the correct submodule or print help menu
    for called_command in arguments:
        if arguments[called_command] and hasattr(commands, called_command):
            module = getattr(commands, called_command)
            module_commands = getmembers(module, isclass)
            command = [
                command[1] for command in module_commands if command[0] != "Base"
            ][0]
            command = command(arguments)
            command.run()


if __name__ == "__main__":
    main()
