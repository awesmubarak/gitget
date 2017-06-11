#!/usr/bin/env python3

import logging
import os
import subprocess
import yaml
import sys


def get_config():
    with open(os.path.expanduser("~/.git_get/config.yml")) as file:
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
    """Installs packages"""
    # Load package list
    with open(os.path.expanduser("~/.git_get/packages.yml"), "r") as file:
        package_list = yaml.safe_load(file)
    # Install package or inform user already installed
    if package not in package_list:
        git("clone https://github.com/" + package)
        # add to packages list
        current_location = os.path.dirname(os.path.realpath(__file__))
        package_list[package] = current_location + "/"+ package.split("/")[-1]
        with open(os.path.expanduser("~/.git_get/packages.yml"), "w") as file:
            file.write(yaml.dump(package_list, default_flow_style=False))
    else:
        print("Package already installed")


def remove(package):
    """Removes packages"""
    with open(os.path.expanduser("~/.git_get/packages.yml"), "r") as file:
        package_list = yaml.safe_load(file)
    if package in package_list:
        subprocess.run(["rm", package_list[package], "-r"], stdout=subprocess.PIPE)
        del package_list[package]
        with open(os.path.expanduser("~/.git_get/packages.yml"), "w") as file:
            file.write(yaml.dump(package_list, default_flow_style=False))
    else:
        print("Package no installeds")


def main(arguments):
    set_logger()
    # get command
    if arguments[0] == "install":
        install(arguments[1])
    elif arguments[0] == "remove":
        remove(arguments[1])
    else:
        print("Invalid command")


if __name__ == '__main__':
    main(sys.argv[1:])
