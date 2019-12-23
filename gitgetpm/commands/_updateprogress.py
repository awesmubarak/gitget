import git
from sys import stdout


class UpdateProgress(git.remote.RemoteProgress):
    """Shows the progress of a git command."""

    def update(self, op_code, cur_count, max_count=None, message=""):
        stdout.write(f"{self._cur_line} \r")
        stdout.flush()

    def clear_line():
        stdout.write(" " * 80 + "\r")
        stdout.flush()
