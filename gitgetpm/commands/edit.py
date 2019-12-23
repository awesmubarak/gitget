from ._base import Base
from loguru import logger
from os import path
import subprocess, os, platform


class Edit(Base):
    """Edit.

    Opens the default editor (run `echo $EDITOR`) to edit the package file.

    Usage: gitget edit [global options]

    Examples:
        gitget edit
    """

    def run(self):
        filepath = self.get_package_list_filepath()

        # https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
        logger.debug("Attempting to open the text editor")
        try:
            if platform.system() == "Darwin":
                logger.debug("macOS found")
                subprocess.call(("open", filepath))
            elif platform.system() == "Windows":
                logger.debug("Windows found")
                os.startfile(filepath)
            else:
                logger.debug("Assuming linux")
                subprocess.call(("xdg-open", filepath))
        except FileNotFoundError:
            logger.error(
                f"Could not open text editor, please edit manually: {filepath}"
            )
