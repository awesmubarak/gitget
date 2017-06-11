#!/usr/bin/env python3

import logging
import os
import subprocess


def git(command):
    """Runs command"""
    command = "git " + command
    logger.debug("Running: " + command)
    try:
        subprocess.run(command.split(" "), stdout=subprocess.PIPE)
    except Exception as error_message:
        logger.error("Failed to run command: " + command)
        logger.debug("Error message: " + str(error_message))


def set_logger():
    """Initialises logger"""
    global logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(name)-8s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def install():
    target = os.path.abspath(os.path.expanduser("~/pro/git-get/files"))
    if not os.path.exists(target):
        os.makedirs(target)
    git("clone https://github.com/" + "abactel/smhwr")


def main():
    set_logger()
    install()


if __name__ == '__main__':
    main()
