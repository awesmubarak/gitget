from os import path
from loguru import logger
import yaml


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        pass

    def get_package_list_filepath(*args, **kwargs):
        """Returns the filepath of the file containing the package info."""
        logger.debug("Getting the package file filepath")
        user = path.expanduser("~")
        filepath = f"{user}/.gitget.yaml"
        logger.debug("Filepath found")
        return filepath

    @staticmethod
    def check_package_list_file(package_list_path, *args, **kwargs):
        """Verifies the package list file exists.

        Returns (int):
            0: valid
            1: not found
            2: a folder instead of a file
        """
        logger.debug("Checking file status")
        path_exists = path.exists(package_list_path)
        path_is_dir = path.isdir(package_list_path)

        logger.debug("File status found, returning vlaue")
        if not path_exists:
            return 1
        elif path_exists and path_is_dir:
            return 2
        else:
            return 3

    def get_package_list(*args):
        """Returns the extracted yaml data from the package file."""
        logger.debug("Loading package list")
        package_list_filepath = Base.get_package_list_filepath()

        # check package list file is valid
        logger.debug("Checking filepath")
        package_list_file_valid = Base.check_package_list_file(package_list_filepath)
        if package_list_file_valid == 1:
            logger.error("Package file missing, please run `gitget setup`")
            exit(1)
        elif package_list_file_valid == 2:
            logger.error(
                "Package file is a directory, please remove `.gitget.yaml` and run `gitget setup`"
            )
            exit(1)
        elif package_list_file_valid == 0:
            logger.debug("Package file found")

        # try loading the file
        logger.debug("Attempting to load file")
        try:
            with open(package_list_filepath) as file:
                package_list = yaml.safe_load(file)
        except:
            logger.error("Could not load package list")
            exit(1)
        logger.debug("Package list loaded")

        # if the list is NONE, set to an empty dictionary to prevent iteration errors
        logger.debug("Checking if package list is None")
        if package_list is None:
            package_list = {}
            logger.debug("Package list has no content, set to empty dict")
        return package_list

    def write_package_list(_, package_list, *args):
        """Writes the package information to the package file."""
        logger.debug("Attempting to write package list")
        try:
            with open(Base.get_package_list_filepath(), "w") as file:
                yaml.dump(package_list, file, sort_keys=True)
        except:
            logger.excpetion("Could not write package list")
            exit(1)
        logger.debug("Packages written to file")
