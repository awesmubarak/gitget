from ._base import Base
from loguru import logger
from os import path
from shutil import move as mmove  # can't be called move, causes issues


class Move(Base):
    """Move.

    Moves a package from location to another and updates the information about
    it.

    Usage: gitget move <package_name> <location> [global options]

    Examples:
        gitget move 'awesmubarak/gitget' ..
    """

    def run(self):
        package_list = self.get_package_list()
        package_name = self.options["<package_name>"]
        location = self.options["<location>"]

        # verify location to move to
        logger.debug("Verifying the location to move to ")
        location = path.abspath(location)
        path_exists = path.exists(location)
        path_is_dir = path.isdir(location)
        if path_exists and path_is_dir:
            logger.debug("Location to move package to is valid")
        else:
            logger.error("Location to move package to is not valid")

        # verify that the package exists in the package list
        logger.debug("Checking if package in package list")
        try:
            _ = package_list[package_name]
        except KeyError as e:
            logger.error(f"Package name is not valid: {package_name}")
            exit(1)

        # move the package to the location
        logger.debug("Attempting to move package")
        try:
            mmove(package_list[package_name], location)
            logger.info("Moved package")
        except:
            logger.error("Could not move the package")
            exit(1)

        # update package list
        logger.debug("Updating package list")
        package_list[package_name] = location
        self.write_package_list(package_list)
        logger.info("Saved package information")
