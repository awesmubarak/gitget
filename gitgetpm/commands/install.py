from .base import Base
from git import Repo
from loguru import logger
from os import getcwd, path
import http.client as httplib


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
        if self.options["<package_name>"] is not None:
            logger.debug("Using the name provided as argument")
            package_name = self.options["<package_name>"]
            directory_name = package_name
        else:
            logger.debug("Using the URL to generate a name")
            package_name = "/".join(package_url.split("/")[-2:])

        # check if the package is in the package list already
        if package_name in package_list:
            logger.error(f"Package name {package_name} already exists")
            exit(1)
        logger.info(f"Using package name {package_name}")

        # figure out the package location
        if directory_name == "":
            package_location = f"{getcwd()}/{package_url.split('/')[-1]}"
        else:
            package_location = f"{getcwd()}/{directory_name}"

        # check if directory already exists
        if path.isdir(package_location):
            logger.error(f"Directory already exists: {package_location}")
            exit(1)

        # check if the repository can be reached
        trimmed_package_url = package_url.replace("https://", "").replace("http://", "")
        trimmed_package_url = trimmed_package_url.split("/")[0]
        logger.debug("Checking internet connection")
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
            Repo.clone_from(package_url, package_location)
        except:
            logger.exception("Could not clone the repository")
            exit(1)
        logger.debug("Clone successfull")

        # add package to package list
        package_list[package_name] = package_location
        self.write_package_list(package_list)
        logger.info("Saved package information")
