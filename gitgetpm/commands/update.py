from ._base import Base
from loguru import logger
from os import getcwd
import git
from ._updateprogress import UpdateProgress


class Update(Base):
    """Update.

    Runs `git-pull` on all packages in the package list to update them.

    Usage: gitget update [global options]

    Examples:
        gitget update
    """

    def run(self):
        package_list = self.get_package_list()
        number_of_packages = len(package_list)

        logger.debug("Making sure there are some packages to update")
        if number_of_packages == 0:
            logger.info("No packages to update")
            exit(0)

        logger.debug("Going through each package")
        for package_number, package_name in enumerate(package_list):
            package_path = package_list[package_name]

            logger.debug(f"Attempting to update {package_name}")
            try:
                repo = git.Repo(package_path)
                origins = repo.remotes.origin
                progress = f"[{package_number+1}/{number_of_packages}]"
                logger.info(f"Updating {package_name}  {progress}")
                origins.pull(progress=UpdateProgress())
                logger.debug("Package updated successfully")
            except Exception:
                logger.exception(f"Package {package_name} could not be updated")
