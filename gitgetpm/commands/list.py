from ._base import Base
from loguru import logger
from tabulate import tabulate


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
        logger.debug("Checking if package list is empty")
        if not package_list:
            logger.info("Package list is empty")
            return 0

        # create the table, trimming each section
        logger.debug("Creating table for printing")
        table = []
        for package_name, package_location in package_list.items():
            table.append([package_name, package_location])

        logger.debug("Printing table")
        number_str = f"{len(package_list)} packages:"
        table = tabulate(table, headers=["Package name", "Location"])
        logger.info(f"{number_str}\n\n{table}\n")
