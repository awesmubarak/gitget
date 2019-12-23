from ._base import Base
from loguru import logger
from gitgetpm import commands
from docopt import docopt
from inspect import getmembers, isclass


class Help(Base):
    """Help.

    Displays a help menu for a specific command.

    Usage: gitget help [global options]

    Examples:
        gitget help
    """

    def run(self):

        called_command = self.options["<command>"]

        # check if command is valid
        logger.debug("Checking if the command is valid")
        if hasattr(commands, called_command) and called_command != "base":
            logger.debug("Command is valid")
        else:
            logger.error("Command is not valid")
            exit(1)

        # display the docstring
        logger.debug("Displaying the docstring for the command")
        module = getattr(commands, called_command)
        module_commands = getmembers(module, isclass)
        command = [command[1] for command in module_commands if command[0] != "Base"][0]
        print(command.__doc__)
