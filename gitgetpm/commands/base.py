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
        Base.check_package_list_file(filepath)
        return filepath

    def get_package_list(*args):
        """Returns the extracted yaml data from the package file."""
        logger.debug("Loading package list")
        package_list_filepath = Base.get_package_list_filepath()
        try:
            with open(package_list_filepath) as file:
                package_list = yaml.safe_load(file)
        except:
            logger.error("Could not load package list")
            exit(1)
        logger.debug("Package list loaded")
        return package_list

    def write_package_list(_, package_list, *args):
        """Writes the package information the package file."""
        logger.debug("Writing package list")
        try:
            with open(Base.get_package_list_filepath(), "w") as file:
                yaml.dump(package_list, file, sort_keys=True)
        except:
            logger.excpetion("Could not write package list")
            exit(1)
        logger.debug("Packages written to file")

    def check_package_list_file(package_list_path, *args):
        """Verifies the package list file exists."""
        path_exists = path.exists(package_list_path)
        path_is_dir = path.isdir(package_list_path)

        if not path_exists:
            logger.error(
                "The package file does not exist, create '.gitget.yaml' in your home directory'"
            )
            exit(1)
        elif path_exists and path_is_dir:
            logger.error(
                "The package file is a directory, remove '.gitget.yaml' and create it again as a file"
            )
            exit(1)
        else:
            logger.debug("Package file found")
