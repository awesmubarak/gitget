#!/usr/bin/env python3

import logging
import os
import subprocess
import sys
import yaml


def get_config():
    """Load configuration file"""
    try:
        with open(os.path.expanduser("~/.git_get/config.yml")) as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error("Configuration file not found")
        sys.exit(1)
    return config


def run_command(command):
    """Runs and handlles commands"""
    logger.debug("Running: " + command)
    try:
        subprocess.run(command.split(" "), stdout=subprocess.PIPE)
    except Exception as error_message:
        logger.error("Failed to run command: " + command)
        logger.debug("Error message: " + str(error_message))
        sys.exit(1)


def set_logger():
    """Initialises logger"""
    global logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def install(package):
    """Installs packages"""
    # Load package list
    try:
        # Try/execept not below as taken care of here
        with open(os.path.expanduser("~/.git_get/packages.yml"), "r") as file:
            package_list = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error("Package list not found")
    # Install package or inform user already installed
    if package not in package_list:
        run_command("git clone https://github.com/" + package)
        # Add to packages list
        current_location = os.path.dirname(os.path.realpath(__file__))
        package_location = current_location + "/" + package.split("/")[-1]
        package_list[package] = [package_location, False]
        with open(os.path.expanduser("~/.git_get/packages.yml"), "w") as file:
            file.write(yaml.dump(package_list, default_flow_style=False))
        logger.debug("That went better than expected")
        sys.exit(0)
    else:
        logger.error("Package already installed")
        sys.exit(1)


def remove(package):
    """Removes packages"""
    try:
        # Try/execept not below as taken care of here
        with open(os.path.expanduser("~/.git_get/packages.yml"), "r") as file:
            package_list = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error("Package list not found")
    # Remove package or inform user not installed
    if package in package_list:
        if input("Uninstall " + package + "? (y/N)") == "y":
            run_command("rm " + package_list[package][0] + " -rf")
            # Write new package list
            del package_list[package]
            with open(os.path.expanduser("~/.git_get/packages.yml"), "w") as file:
                file.write(yaml.dump(package_list, default_flow_style=False))
            logger.debug("That went better than expected")
            sys.exit(0)
        else:
            logger.info("Quitting")
            sys.exit(0)
    else:
        logger.error("Package not installed")
        sys.exit(1)


def main(arguments):
    set_logger()
    logger.debug("Starting")
    # get command and execute appropriate function
    if arguments[0] == "install":
        install(arguments[1])
    elif arguments[0] == "remove":
        remove(arguments[1])
    else:
        logger.error("Invalid command: " + " ".join(arguments))
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
