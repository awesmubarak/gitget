=======
Git-get
=======

Package manager for git repositories.

Installation
============

To install from pypi run:

``sudo pip3 install git-get``

It should run on both linux and maybe other unix-like oses (bsd, osx), but
shouldn't run on windows (unless you're a cybermancer).

Usage
=====

The following is a list of commands available:

Help
----

``git-get -h``

``git-get --help``

Displays a help menu.

Setup
-----

``git-get setup``

Sets up the core configuration files. This should be the first command run.

Install
-------

``git-get install <username/repository>``

``git-get install abactel/git-get``

Github repositories can be installed without typing the whole URL; the username
of the owner and the repository name should be passed as command line
arguments, separated by a forward slash. The repository will be download to the
directory where called.

``git-get install <URL>``

``git-get install https://gitlab.com/abactel/git-get``

Installs a package from a non-github site. The name of the repository is saved

``git-get install <directory> --local``

``git-get install git-get-patch --local``

Add local file to package list. The file will not be saved by appending the
folder name to "local_", e.g the above example would result in "local_git-get".
More than one package with the same name can be added, subsequent packages will
have a number appended ("local_git-get_1")

Remove
------

``git-get remove <username/repository>``

``git-get remove abactel/git-get``

Removes a repository from the package list and removes the files locally.

``git-get remove <username/repository> --soft``

``git-get remove abactel/git-get --soft``

Removes a repository from the package list but does not remove the files
locally.

Upgrade
-------

``git-get upgrade``

Runs ``git-pull`` on all packages in the package list, to upgrade them.

Check
-----

``git-get check``

Verifies integrity of files and packages. First, the core files are checked
for. Both the configuration and the package list are looked for. If both are
found the packages list is parsed and the location of every package is
verified.

List
----

``git-get list``

Lists all packages and install locations.

``git-get list --local``

``git-get list --remote``

Filters to output to only local or remote repositories.

Move
----

``git-get move <username/repository> <location>``

``git-get move abactel/git-get ~/stuff``

Move a repository to another location.

Edit
----

``git-get edit packages``

``git-get edit config``

The default system editor (run ``echo $EDITOR``) is used to open the packages
list or configuration file. This allows manual fixing of errors.
