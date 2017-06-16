#!/usr/bin/env python3

import logging
import os
import subprocess
import sys
import yaml


def set_logger():
    """Initialises logger"""
    global logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def get_config():
    """Load configuration file"""
    try:
        with open(os.path.expanduser("~/.git-get/config.yml")) as file:
            config = yaml.safe_load(file)
            logger.debug("Loaded config file")
    except FileNotFoundError:
        logger.error("Configuration file not found")
        sys.exit(1)
    return config


def get_package_list():
    """Loads package list from file"""
    try:
        with open(os.path.expanduser("~/.git-get/packages.yml"), "r") as file:
            package_list = yaml.safe_load(file)
            logger.debug("Loaded package list")
    except FileNotFoundError:
        logger.error("Package list not found")
        sys.exit(1)
    return package_list


def run_command(command, die_on_err=False, quiet=0):
    """Runs and handlles commands
    Quiet values:
    -   0 - logs all commands and errors
    -   1 - logs only errors
    -   2 - logs nothing
    """
    if quiet < 1:
        logger.debug("Running: " + command)
    # Run command and store output
    proc = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()[0]
    exit_code = proc.returncode
    if die_on_err and exit_code != 0:
        logger.error("Could not complete process")
        logger.debug("Process exited with " + str(exit_code))
        sys.exit(1)
    return output, exit_code


def install(package):
    """Installs packages"""
    package_list = get_package_list()
    # Install package or inform user already installed
    if package not in package_list:
        run_command("git clone https://github.com/" + package, die_on_err=True)
        # Add to packages list
        package_location = os.getcwd() + "/" + package.split("/")[-1]
        package_list[package] = [package_location, False]
        with open(os.path.expanduser("~/.git-get/packages.yml"), "w") as file:
            file.write(yaml.dump(package_list, default_flow_style=False))
        logger.info("Succefully installed package.")
        sys.exit(0)
    else:
        logger.error("Package already installed")
        sys.exit(1)


def remove(package):
    """Removes packages"""
    package_list = get_package_list()
    # Remove package or inform user not installed
    if package in package_list:
        if input("Uninstall " + package + "? (y/N)") == "y":
            run_command("rm " + package_list[package][0] + " -rf", die_on_err=True)
            # Write new package list
            del package_list[package]
            with open(os.path.expanduser("~/.git-get/packages.yml"), "w") as file:
                file.write(yaml.dump(package_list, default_flow_style=False))
            logger.info("Succefully removed package.")
            sys.exit(0)
        else:
            logger.info("Quitting")
            sys.exit(0)
    else:
        logger.error("Package not installed")
        sys.exit(1)


def upgrade():
    """Git pull all repositories"""
    package_list = get_package_list()
    for package_name in package_list:
        # if not package[1]: # Checks if HEAD is not modified
        package_location = package_list[package_name][0]
        command = "git -C " + package_location + " pull"
        tmp, return_value = run_command(command, quiet=2)
        if return_value == 0:
            logger.info("Package " + package_name + " succesfully upgraded")
        elif return_value == 1:
            logger.warning("Package " + package_name +
                           " may not have a working remote")
    logger.info("Upgraded all possible packages.")
    sys.exit(0)


def list_packages():
    """List all packages and isntall locations"""
    package_list = get_package_list()
    print("")
    for package_name in package_list:
        package_location = package_list[package_name][0]
        print((package_name).ljust(25) + package_location)
    print("")
    logger.info("Succefully Listed packages.")
    sys.exit(0)


def main(arguments):
    set_logger()
    logger.info("Starting")
    # get command and execute appropriate function
    if arguments[0] == "install":
        install(arguments[1])
    elif arguments[0] == "remove":
        remove(arguments[1])
    elif arguments[0] == "upgrade":
        upgrade()
    elif arguments[0] == "list":
        list_packages()
    else:
        logger.error("Invalid command: " + " ".join(arguments))
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
