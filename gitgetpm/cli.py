#!/usr/bin/env python3

"""Git-get.

Package manager for git repositories.

Usage:
    git-get install <package_url> [<package_name>] [options]
    git-get remove <package_name> [--soft] [options]
    git-get update [--overwrite] [options]
    git-get list [options]
    git-get move <package_name> <end_location> [options]
    git-get edit [options]
    git-get doctor [options]
    git-get --version
    git-get -h | --help

Options:
    --debug    Increases verbosity of the output

Examples:
    git-get install awesmubarak/git-get
    git-get upgrade
    git-get remove awesmubarak/git-get

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


def setup_logging(debug_level):
    """Sets up the format for logging, based on the debug level (info/dbug)."""
    logger.remove()

    if debug_level == "info":
        logger_format = "<green>{time:HH:mm:ss}</green> <level>{message}</level>"
        logger_threshold = "INFO"
    elif debug_level == "debug":
        logger_format = "<green>{time:HH:mm:ss}</green> {file: <12} <level>{level: <8} {message}</level>"
        logger_threshold = "DEBUG"
    else:
        raise ValueError(f"Not a valid debug level {debug_level}")

    logger.add(stderr, colorize=True, format=logger_format, level=logger_threshold)


def main():
    # setup the argument parser with the docstring and imported version number
    arguments = docopt(__doc__, version=f"Gitget {__version__}")

    # set up the logger
    if arguments["--debug"]:
        setup_logging("debug")
    else:
        setup_logging("info")

    # dynamically call the correct submodule (???)
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
