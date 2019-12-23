from ._base import Base
from git import Repo
from loguru import logger
from os import getcwd, path
import http.client as httplib
from ._updateprogress import UpdateProgress


class Install(Base):
    """Install.

    Downloads a repository from github and saves information about it.
    Optionally, a name for the package can be specified. This name will also
    be used as the directory name. Otherwise, the package name is set to
    `username/repository`.

    Usage: gitget install <package_url> [<package_name>] [global options]

    Examples:
        gitget install 'https://github.com/awesmubarak/gitget'
        gitget install 'https://github.com/awesmubarak/gitget' 'gitget-download'
    """

    def run(self):
        package_list = self.get_package_list()
        package_url = self.options["<package_url>"]
        directory_name = ""

        # sort out package name
        logger.debug("Deciding on package name")
        if self.options["<package_name>"] is not None:
            # use argument
            logger.debug("Using the name provided as argument")
            package_name = self.options["<package_name>"]
            directory_name = package_name
        else:
            # use the last part of the url
            logger.debug("Using the URL to generate a name")
            package_name = "_".join(package_url.split("/")[-2:])

        # check if the package is in the package list already
        logger.debug("Checking if the package name already exists")
        if package_name in package_list:
            logger.error(f"Package name {package_name} already exists")
            exit(1)
        logger.info(f"Using package name {package_name}")

        # figure out the package location
        logger.debug("Deciding package location")
        if directory_name == "":
            package_location = f"{getcwd()}/{package_url.split('/')[-1]}"
            logger.debug("Using the name of the package for directory name")
        else:
            package_location = f"{getcwd()}/{directory_name}"
            logger.debug("Using the argument's specified name for directory name")

        # check if directory already exists
        logger.debug("Checking if the directory name already exists")
        if path.isdir(package_location):
            logger.error(f"Directory already exists: {package_location}")
            exit(1)

        # check if the repository can be reached
        logger.debug("Checking if repository can be reached")
        trimmed_package_url = package_url.replace("https://", "").replace("http://", "")
        trimmed_package_url = trimmed_package_url.split("/")[0]
        connection = httplib.HTTPConnection(trimmed_package_url, timeout=5)
        try:
            connection.request("HEAD", "/")
            connection.close()
            logger.debug("Connection made succesfully")
        except:
            connection.close()
            logger.exception(
                "Could not connect to the URL, check the URL and your internet"
            )
            exit(1)

        # clone repository
        logger.info(f"Cloning repository {package_name}")
        try:
            Repo.clone_from(package_url, package_location, progress=UpdateProgress())
        except:
            logger.exception("Could not clone the repository")
            exit(1)
        UpdateProgress.clear_line()
        logger.debug("Clone successfull")

        # add package to package list
        logger.debug("Adding package to package list")
        package_list[package_name] = package_location
        self.write_package_list(package_list)
        logger.info("Saved package information")
