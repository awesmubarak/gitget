#!/usr/bin/env python3

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

# Get the Version
exec(open('gitgetpm/version.py').read())

setup(
    name="gitget-pm",
    version=__version__,
    description="A package manager for git repositories.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/awesmubarak/gitget",
    author="Awes Mubarak",
    author_email="contact@awesmubarak.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Version Control :: Git",
        "Operating System :: POSIX",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    keywords="git github package manager",
    packages=["gitgetpm"],
    entry_points={"console_scripts": ["gitget=gitgetpm:main"]},
    install_requires=["docopt", "loguru", "gitpython", "pyyaml"],
)
