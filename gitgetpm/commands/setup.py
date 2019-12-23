from ._base import Base
from loguru import logger
from os import path


class Setup(Base):
    """Setup.

    Creates the files gitget needs to function. Only `.gitget.yaml` is needed in
    the home directory.

    Usage: gitget setup [global options]

    Examples:
        gitget setup
    """

    def run(self):
        package_list_path = self.get_package_list_filepath()
        package_file_status = self.check_package_list_file(
            package_list_path=package_list_path
        )

        logger.debug("Verifying package file status")
        if package_file_status == 1:
            logger.debug("Package file `.gitget.yaml` missing in home directory")
        elif package_file_status == 2:
            logger.error(
                "Package file `.gitget.yaml` is a directory, please manually remove"
            )
            exit(1)
        elif package_file_status == 3:
            logger.error("Package file found")
            exit(1)

        # create the file
        logger.debug("Creating file")
        with open(package_list_path, "w") as file:
            file.write("")
        logger.info("Created package file `gitget.yaml` in home directory")
