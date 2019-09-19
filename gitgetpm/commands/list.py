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

        for package_name in package_list:
            package_path = package_list[package_name]
            print(f"{package_name}\n{package_path}\n")
