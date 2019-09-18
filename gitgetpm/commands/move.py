from .base import Base
from loguru import logger
from os import path
from shutil import move as mmove # can't be called move, causes issues


class Move(Base):
    """Moves a package from one location to another."""

    def run(self):
        package_list = self.get_package_list()
        package_name = self.options["<package_name>"]
        location = self.options["<location>"]

        # verify location to move to
        location = path.abspath(location)
        path_exists = path.exists(location)
        path_is_dir = path.isdir(location)
        if path_exists and path_is_dir:
            logger.debug("Location to move package to is valid")
        else:
            logger.error("Location to move package to is not valid")

        # verify that the package exists in the package list
        try:
            _ = package_list[package_name]
        except KeyError as e:
            logger.error(f"Package name is not valid: {package_name}")
            exit(1)

        # move the package to the location
        try:
            mmove(package_list[package_name], location)
            logger.info("Moved package")
        except:
            logger.error("Could not move the package")
            exit(1)

        # update package list
        package_list[package_name] = location
        self.write_package_list(package_list)
        logger.info("Saved package information")
