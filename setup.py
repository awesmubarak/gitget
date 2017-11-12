#!/usr/bin/env python3

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='git-get',
    version='1.0.1',
    description='A package manager for git repositories.',
    long_description=long_description,
    url='https://github.com/awesmubarak/git-get',
    author='Awes Mubarak',
    author_email='awes.mubarak@awesmubarak.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Version Control :: Git',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    keywords='git github package manager',
    packages=['gitget'],
    entry_points={
        "console_scripts": [
            "git-get=gitget:main",
        ],
    },
    install_requires=['PyYAML', 'termcolor']
)
