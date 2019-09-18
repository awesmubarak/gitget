from .base import Base
from loguru import logger
from git import Repo
from shutil import rmtree


class Remove(Base):
    """Removes a repository from the package list and may delete the files locally."""

    def run(self):
        package_list = self.get_package_list()
        package_name = self.options["<package_name>"]
        soft_remove = self.options["--soft"]

        # check if package exists
        if not package_name in package_list:
            logger.error("Package name not in package list")
            exit(1)
        else:
            logger.debug("Package in package list")

        # remove package from package list
        package_location = package_list[package_name]
        package_list.pop(package_name, None)
        self.write_package_list(package_list)
        logger.info("Saved package information")

        # delete the package
        if soft_remove:
            logger.debug("Soft remove - not deleting files")
            return

        if (
            input(
                f"Are you sure you want to delete every file in {package_location}? [yes/NO]"
            )
            != "yes"
        ):
            logging.info("Exiting")
            exit(0)

        logger.info("Deleting files")
        try:
            rmtree(package_location)
        except:
            exception("Could not delete the files")
