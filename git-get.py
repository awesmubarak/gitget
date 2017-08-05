#!/usr/bin/env python3

import logging
import os
import subprocess
import yaml

from termcolor import colored
from sys import exit, argv


def set_logger(detail_level=2):
    """Initialises logger
    Detail level values:
    -   0 - Only messages
    -   1 - Messages and time
    -   2 - Messages, time and debug level
    """
    global logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    # set logger format
    if detail_level == 0:
        formatter = logging.Formatter("%(message)s")
    elif detail_level == 1:
        formatter = logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S")
    elif detail_level == 2:
        formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s",
                                      "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)


def get_config():
    """Load configuration file"""
    try:
        with open(os.path.expanduser("~/.git-get/config.yml")) as file:
            config = yaml.safe_load(file)
            logger.debug("Loaded config file")
    except FileNotFoundError:
        logger.error("Configuration file not found")
        exit(1)
    return config


def get_package_list():
    """Loads package list from file"""
    try:
        with open(os.path.expanduser("~/.git-get/packages.yml"), "r") as file:
            package_list = yaml.safe_load(file)
            logger.debug("Loaded package list")
    except FileNotFoundError:
        logger.error("Package list not found")
        exit(1)
    return package_list


def write_package_list(package_list):
    with open(os.path.expanduser("~/.git-get/packages.yml"), "w") as file:
        file.write(yaml.dump(package_list, default_flow_style=False))


def run_command(command, die_on_err=True, quiet=0):
    """Runs and handlles commands
    Quiet values:
    -   0 - logs all commands and errors
    -   1 - logs only errors
    -   2 - logs nothing
    """
    if quiet < 1:
        logger.debug("Running: " + command)
    # run command and store output
    proc = subprocess.Popen(command.split(" "),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()[0].decode("utf-8")[:-1]
    exit_code = proc.returncode
    # die if required
    if die_on_err and exit_code != 0:
        logger.critical("Process died")
        logger.debug("Process exited with " + str(exit_code))
        exit(1)
    return output, exit_code


def install(remote_package):
    """Installs packages"""
    package_list = get_package_list()
    # parse if package refers to direct URL
    if remote_package.startswith("http") or remote_package.startswith("git"):
        package_name = "/".join(remote_package.split("/")[-2:])
        if package_name.endswith(".git"):
            package_name = package_name[:-4]
    else:
        package_name = remote_package
        remote_package = "https://github.com/" + remote_package
    # install package or inform user already installed
    if package_name not in package_list:
        run_command("git clone " + remote_package)
        # add to packages list
        package_location = os.path.join(
            os.getcwd(), remote_package.split("/")[-1])
        package_list[str(package_name)] = {"location": package_location}
        write_package_list(package_list)
        logger.info("Succefully installed package.")
        exit(0)
    else:
        logger.error("Package already installed")
        exit(1)


def install_local(location):
    """Install local package"""
    package_list = get_package_list()
    # expand location
    location = os.path.expanduser(location)
    package = "local_" + str(location.split("/")[-1])
    # modify package name
    if package in package_list:
        package = package + "_1"
    package_count = 0
    while package in package_list:
        package_count += 1
        package = package[:-1] + str(package_count)
    # install package
    package_location = os.path.join(os.getcwd(), location)
    package_list[package] = {"location": package_location}
    write_package_list(package_list)
    logger.info("Succefully installed package.")
    exit(0)


def remove(package, keep_package=False):
    """Removes packages"""
    package_list = get_package_list()
    # remove package or inform user not installed
    if package in package_list:
        if input("Uninstall " + package + "? (y/N)") == "y":
            if not keep_package:
                run_command("rm " + package_list[package]["location"] + " -rf")
            # write new package list
            del package_list[package]
            write_package_list(package_list)
            logger.info("Succefully removed package.")
            exit(0)
        else:
            logger.info("Quitting")
            exit(0)
    else:
        logger.error("Package not installed")
        exit(1)


def upgrade():
    """Git pull all packages"""
    package_list = get_package_list()
    num_packages = str(len(package_list))
    for package_num, package_name in enumerate(package_list):
        # basic variable initiation
        package_location = package_list[package_name]["location"]
        base_command = "git -C " + package_location + " "
        # check for remotes
        output, tmp = run_command(base_command + "remote -v", die_on_err=False)
        # Create progress bar
        progress = "(" + str(package_num + 1) + "/" + str(num_packages) + ")"
        # Pull, figure out correct message and display
        if len(output) != 0:
            command = base_command + "pull"
            output, return_value = run_command(command, die_on_err=False)
            if output == "Already up-to-date." and return_value == 0:
                msg = ("Package " + package_name + " already up to date. "
                       + colored(progress, "yellow"))
            elif return_value == 0:
                msg = ("Package " + package_name + " succesfully upgraded. "
                       + colored(progress, "green"))
            else:
                msg = ("Package " + package_name + " could not be upgraded. "
                       + colored(progress, "red"))
        else:
            msg = ("Package " + package_name + " does not have any remotes. "
                   + colored(progress, "red"))
        logger.info(msg)
    logger.info("Upgraded all possible packages.")
    exit(0)


def list_packages():
    """List all packages and install locations"""
    package_list = get_package_list()
    print("")
    for package_name in package_list:
        package_location = package_list[package_name]["location"]
        print((package_name).ljust(25) + package_location)
    print("")
    logger.info("Succefully Listed packages.")
    exit(0)


def move_package(package_name, end_location):
    """Move a package"""
    package_list = get_package_list()
    # check if package is installed
    if package_name not in package_list:
        logger.error("Package not found in package list")
        exit(1)
    # run command
    package_location = package_list[package_name]["location"]
    end_location = os.path.abspath(end_location)
    run_command("mv " + package_location + " " + end_location)
    # update packages list
    package_list[package_name]["location"] = end_location
    write_package_list(package_list)


def open_file(file_name):
    editor = os.getenv("EDITOR")
    if editor:
        # does not use `run_command` as output needs to be shown
        logger.debug("Running: " + editor + " " + file_name)
        try:
            subprocess.call([editor, file_name])
        except Exception as e:
            logger.critical("Could not open editor")
            logger.debug("Error message: " + str(e))
            exit(1)
        logger.info("File edited.")
        exit(0)
    else:
        logger.error("Editor not set, exiting")
        exit(1)


def check():
    package_list = get_package_list()
    # check core files
    config_file = os.path.join("~", ".git-get", "config.yml")
    if os.path.exists(os.path.expanduser(config_file)):
        logger.info("Config file exists")
    else:
        logger.error("Config file not found")
        exit(1)
    packages_file = os.path.join("~", ".git-get", "packages.yml")
    if os.path.exists(os.path.expanduser(packages_file)):
        logger.info("Packages list exists")
    else:
        logger.error("Packages list not found")
        exit(1)
    # check packages
    for package_name in package_list:
        all_found = True
        if os.path.isdir(package_list[package_name]["location"]):
            logger.debug("Pakage " + package_name + " found")
        else:
            logger.error("Package " + package_name + " not found")
            all_found = False
    if all_found:
        logger.info("All packages found")
    logger.info("All checks complete")


def main(arguments):
    def invalid_command():
        logger.error("Invalid command: " + " ".join(arguments))
        exit(1)
    set_logger(detail_level=1)
    logger.info("Starting")
    # confirm that a command has been selected
    if len(arguments) < 1:
        logger.error("Command not supplied")
        exit(1)
    # get command and execute appropriate function
    if arguments[0] == "install":
        if arguments[1] == "local":
            install_local(arguments[2])
        else:
            install(arguments[1])
    elif arguments[0] == "remove":
        if arguments[1] == "soft":
            remove(arguments[2], keep_package=True)
        else:
            remove(arguments[1])
    elif arguments[0] == "upgrade":
        upgrade()
    elif arguments[0] == "list":
        list_packages()
    elif arguments[0] == "move":
        move_package(arguments[1], arguments[2])
    elif arguments[0] == "edit":
        if arguments[1] == "packages":
            open_file(os.path.expanduser("~/.git-get/packages.yml"))
        elif arguments[1] == "config":
            open_file(os.path.expanduser("~/.git-get/config.yml"))
        else:
            invalid_command()
    elif arguments[0] == "check":
        check()
    else:
        invalid_command()


if __name__ == '__main__':
    main(argv[1:])
