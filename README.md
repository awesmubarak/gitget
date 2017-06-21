# Git-get

Package manager for git repositories. Nothing is ready yet.

## Usage

The basic script is invoked using `python3 git-get.py`. An alias should be
added to your bashrc or zshrc toaccess the program from anywhere. The following
is a non-comprehensive list of commands are available:

### Install

`git-get install octocat/Hello-World`

Github repositories can be installed. The username of the owner and the
repository name should be passed as command line arguments, seperated by a
forward slash. The repository will be download to the directory where called.

`git-get install https://gitlab.com/octocat/Hello-World`

Installs a package from a non-github site.

`git-get install --local Hello-World`

Add local file to package list.

### Remove

`git-get remove octocat/Hello-World`

Remove a repository from disk and package list

`git-get remove --soft octocat/Hello-World`

Remove a repository from the package list but keep on drive.

### Upgrade

`git-get upgrade`

Run `git-pull` on all packagesin the package list.

### List

`git-get list`

List all packages and install location.

### move_repo

`git-get mv octocat/Hello-World ~/important`

Move a repository to another location.
