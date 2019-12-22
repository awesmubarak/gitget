from .base import Base
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
        if not package_name in package_list:
            logger.error("Package name not in package list")
            exit(1)
        else:
            logger.debug("Package in package list")
        package_location = package_list[package_name]

        # conifrm deleting files if asked to do so
        if not soft_remove:
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
            # respnse
            if delete_file:
                logger.debug("Going ahead with deletion")
            else:
                logger.info("Exiting")
                exit(0)

        # remove package from package list
        package_list.pop(package_name, None)
        self.write_package_list(package_list)
        logger.info("Saved package information")

        # delete the files
        if soft_remove:
            logger.debug("Soft remove - not deleting files")
            return 0

        logger.info("Deleting files")
        try:
            rmtree(package_location)
        except:
            exception("Could not delete the files")
