# Git-get

Package manager for git repositories. Nothing is ready yet.

## Usage

The basic script is invoked using `python3 git-get.py`. An alias should be
added to your bashrc or zshrc to access the program from anywhere. The
following is a list of commands available:

### Install

`git-get install octocat/Hello-World`

Github repositories can be installed. The username of the owner and the
repository name should be passed as command line arguments, separated by a
forward slash. The repository will be download to the directory where called.

`git-get install https://gitlab.com/octocat/Hello-World`

Installs a package from a non-github site.

`git-get install --local Hello-World`

Add local file to package list.

### Remove

`git-get remove octocat/Hello-World`

Remove a repository from disk and package list

`git-get remove soft octocat/Hello-World`

Remove a repository from the package list but keep on drive.

### Upgrade

`git-get upgrade`

Run `git-pull` on all packages in the package list.

### List

`git-get list`

List all packages and install location.

### Move

`git-get move octocat/Hello-World ~/important`

Move a repository to another location.

### Edit

`git-get edit packages`

Edit the package list using the default system text editor.

`git-get edit config`

Edit the config file using the default system text editor.
