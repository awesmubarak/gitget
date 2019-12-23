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
    gitget setup [options]
    gitget help <command>
    gitget -h | --help
    gitget --version

Global options:
    --debug    Increases verbosity of the output
    --nocolor  Logs will not have colors in them

Examples:
    gitget setup
    gitget install awesmubarak/git-get
    gitget update
    gitget remove awesmubarak/git-get

Help:
    For help using this tool, please open an issue on the Github repository:
    https://github.com/awesmubarak/gitget

"""

from . import commands
from .version import __version__
from docopt import docopt
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
    logger.debug("Set up logging")


def main():
    # setup the argument parser with the docstring and imported version number
    arguments = docopt(__doc__, version=f"Gitget {__version__}")

    # set up the logger
    debug_level = "debug" if arguments["--debug"] else "info"
    colorize = False if arguments["--nocolor"] else True
    setup_logging(debug_level, colorize)

    # call the right command, based on the argument
    logger.debug("Calling the function based on the command sent")
    if arguments["doctor"]:
        commands.doctor.Doctor(arguments).run()
    elif arguments["edit"]:
        commands.edit.Edit(arguments).run()
    elif arguments["help"]:
        commands.help.Help(arguments).run()
    elif arguments["install"]:
        commands.install.Install(arguments).run()
    elif arguments["list"]:
        commands.list.List(arguments).run()
    elif arguments["move"]:
        commands.move.Move(arguments).run()
    elif arguments["remove"]:
        commands.remove.Remove(arguments).run()
    elif arguments["setup"]:
        commands.setup.Setup(arguments).run()
    elif arguments["update"]:
        commands.update.Update(arguments).run()


if __name__ == "__main__":
    main()
