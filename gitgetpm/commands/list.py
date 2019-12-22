from .base import Base
from loguru import logger


class List(Base):
    """List.

    Lists all packages and install locations.

    Usage: gitget list [global options]

    Examples:
        gitget list
    """

    def run(self):

        package_list = self.get_package_list()

        # print message if no content in package List
        if not package_list:
            logger.info("Package list is empty")
            return 0

        for package_name in package_list:
            package_path = package_list[package_name]
            print(f"{package_name}\n{package_path}\n")
