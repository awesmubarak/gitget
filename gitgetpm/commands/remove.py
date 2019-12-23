from ._base import Base
from distutils.util import strtobool
from git import Repo
from loguru import logger
from shutil import rmtree


class Remove(Base):
    """Remove

    Removes a repository from the package list and also deletes the files
    locally.

    Usage: gitget remove <package_name> [options] [global options]

    Options:
        --soft  Local files will not be deleted

    Examples:
        gitget remove awesmubarak/gitget
        gitget remove awesmubarak/gitget --soft
    """

    def run(self):
        package_list = self.get_package_list()
        package_name = self.options["<package_name>"]
        soft_remove = self.options["--soft"]

        # check if package exists
        logger.debug("Checking if package in package list")
        if not package_name in package_list:
            logger.error("Package name not in package list")
            exit(1)
        else:
            logger.debug("Package in package list")
        package_location = package_list[package_name]

        # conifrm deleting files if asked to do so
        if not soft_remove:
            logger.debug("Making sure user wants to delete the files")
            # prompt user wether to delete or not
            delete_prompt_input = input(
                f"Are you sure you want to delete {package_location}? [y/N]"
            )
            # try to convert to a true/false value, except invalid responses
            try:
                delete_file = strtobool(delete_prompt_input)
            except ValueError:
                logger.error("Not a valid response")
                exit(1)
            # handling response
            if delete_file:
                logger.debug("Going ahead with deletion")
            else:
                logger.info("Exiting")
                exit(0)

        # remove package from package list
        logger.debug("Updating package list")
        package_list.pop(package_name, None)
        self.write_package_list(package_list)
        logger.info("Saved package information")

        # delete the files
        if soft_remove:
            logger.debug("Soft remove so not deleting files")
            exit(0)

        logger.info("Deleting files")
        try:
            rmtree(package_location)
        except:
            logger.exception("Could not delete the files")
