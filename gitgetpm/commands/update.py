from .base import Base
from loguru import logger
from os import getcwd
import git


class Update(Base):
    """Update.

    Runs `git-pull` on all packages in the package list to update them.

    Usage: gitget update [global options]

    Examples:
        gitget update
    """

    def run(self):
        package_list = self.get_package_list()

        for package_name in package_list:
            package_path = package_list[package_name]

            try:
                repo = git.Repo(package_path)
                origins = repo.remotes.origin
                logger.info(f"Updating {package_name}")
                origins.pull()
                logger.debug("Package updated successfully")
            except Exception:
                logger.exception(f"Package {package_name} could not be updated")
