=======
Gitget
=======

Package manager for git repositories.

Installation
============

To install from pypi run:

``sudo pip3 install gitget``

Then create the file ``.gitget.yaml`` in your home directory.

Usage
=====

This program is useful for people that tend to download a lot of repositories
from github to simply use as software and want to manage these repositories.
Github repositories are treated like software 'packages', and basic tasks such
as downloading and saving information about repositories, updating repository,
and removing them once they aren't needed anymore. The contents of the git
repositories is not changed; installation scripts are not run and dependencies
are not installed (yet).

Help
----

``gitget -h``

``gitget --help``

Displays a help menu.

Install
-------

``gitget install <package>``

``gitget install <package>' '<package_name>'``

Downloads a repository from github and saves information about it. Optionally,
a name for the package can be specified. This name will also be used as the
directory name. Otherwise, the package name is set to ``username/repository``.

Remove
------

``gitget remove <repository_name>``
``gitget remove <repository_name> --soft``

Removes a repository from the package list and also deletes the files locally.
If the ``--soft`` flag is passed, the local files will not be deleted.

Upgrade
-------

``gitget update``

Runs ``git-pull`` on all packages in the package list.

Doctor
-----

``gitget doctor``

Verifies integrity of files and packages. Any errors are then reported and need
to be fixed.

List
----

``gitget list``

Lists all packages and install locations.

Edit
----

``gitget edit packages``

``gitget edit config``

Opens the default editor (run ``echo $EDITOR``) to edit the package file.
