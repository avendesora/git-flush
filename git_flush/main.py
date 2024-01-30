import os

import typer
from click import BadParameter

from git import InvalidGitRepositoryError, Repo

app = typer.Typer()


@app.command()
def main():
    current_directory = os.getcwd()

    try:
        repo = Repo(current_directory)

        # If there are any uncommitted changes, exit.
        if repo.is_dirty():
            raise BadParameter(f"{current_directory} has uncommitted changes")

        # Get current branch name
        branch = repo.active_branch.name

        print(f"Current branch: {branch}")

        if branch != "main":
            print("Checking out main branch")
            repo.git.checkout("main")

        # Pull latest changes from remote
        print("Pulling latest changes from remote")
        repo.git.pull()

        # Fetch all branches from remote
        print("Fetching all branches from remote")
        repo.git.fetch("--all")

        if branch != "main":
            # Delete the original branch
            print(f"Deleting {branch}")
            repo.git.branch("-D", branch)

    except InvalidGitRepositoryError as e:
        raise BadParameter(f"{current_directory} is not a git repository") from e


if __name__ == "__main__":
    app()
