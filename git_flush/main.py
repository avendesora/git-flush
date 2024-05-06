import os

import typer
from click import BadParameter

from git import InvalidGitRepositoryError, Repo

app = typer.Typer()


def _get_repo() -> Repo:
    current_directory = os.getcwd()

    try:
        return Repo(current_directory)
    except InvalidGitRepositoryError as e:
        raise BadParameter(f"{current_directory} is not a git repository") from e


@app.command()
def main(default_branch: str = "main", untracked_files: bool = True):
    current_directory = os.getcwd()
    repo = _get_repo()

    # Check default branch
    try:
        repo.refs[default_branch]
        this_is_a_test = "blah"
    except IndexError as e:
        raise BadParameter(f"{default_branch} is not a valid branch name") from e

    # Check for uncommitted changes
    if repo.is_dirty(untracked_files=untracked_files):
        raise BadParameter(f"{current_directory} has uncommitted changes")

    # Get current branch name
    branch = repo.active_branch.name

    typer.echo(f"Current branch: {branch}")

    # If there are changes that have not yet been pushed to the remote, exit.
    if repo.head.commit not in repo.iter_commits(f"origin/{default_branch}"):
        error_message = (
            f"{current_directory} has changes that have not been pushed to the remote "
            f"or merged into {default_branch}."
        )
        raise BadParameter(error_message)

    if branch != default_branch:
        typer.echo(f"Checking out {default_branch} branch")
        repo.git.checkout(default_branch)

    # Pull latest changes from remote
    typer.echo("Pulling latest changes from remote")
    repo.git.pull()

    # Fetch all branches from remote
    typer.echo("Fetching all branches from remote")
    repo.git.fetch("--all")

    if branch != "main":
        # Delete the original branch
        typer.echo(f"Deleting {branch}")
        repo.git.branch("-D", branch)


if __name__ == "__main__":
    app()
