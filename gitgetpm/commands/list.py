from .base import Base
from loguru import logger


class List(Base):
    """List the packages installed."""

    def run(self):

        package_list = self.get_package_list()

        for package_name in package_list:
            package_path = package_list[package_name]
            print(f"{package_name}: {package_path}")
