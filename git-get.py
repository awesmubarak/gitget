#!/usr/bin/env python3

import logging
import os
import subprocess
import yaml
import sys

def get_config():
    with open(os.path.expanduser("~/.git_get.yml")) as file:
        config = yaml.safe_load(file)
    return config


def git(command):
    """Runs command"""
    command = "git " + command
    logger.debug("Running: " + command)
    try:
        subprocess.run(command.split(" "), stdout=subprocess.PIPE)
    except Exception as error_message:
        print("Failed to run command: " + command)
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


def install(package):
    target = os.path.abspath(os.path.expanduser("~/pro/git-get/files"))
    if not os.path.exists(target):
        os.makedirs(target)
    git("clone https://github.com/" + package)


def main(arguments):
    set_logger()
    if arguments[0] == "install":
        config = get_config()
        package = arguments[1]
        logger.debug("Package to install: " + package)
        install(package)
    else:
        print("Invalid command")


if __name__ == '__main__':
    main(sys.argv[1:])
