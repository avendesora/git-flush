import os
import importlib.metadata
from typing import Annotated

import typer
from click import BadParameter

from git import InvalidGitRepositoryError, Repo

app = typer.Typer()


_TRUTHY = ("true", "t", "1", "yes", "y")

DEFAULT_BRANCH = os.getenv("GIT_FLUSH_DEFAULT_BRANCH", "main")
UNTRACKED_FILES = os.getenv("GIT_FLUSH_UNTRACKED_FILES", "true").lower() in _TRUTHY
DELETE_FEATURE_BRANCH = (
    os.getenv("GIT_FLUSH_DELETE_FEATURE_BRANCH", "false").lower() in _TRUTHY
)


def _get_repo() -> Repo:
    current_directory = os.getcwd()

    try:
        return Repo(current_directory)
    except InvalidGitRepositoryError as e:
        raise BadParameter(f"{current_directory} is not a git repository") from e


@app.command()
def main(
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Display version")
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-V", help="Display verbose output")
    ] = False,
    default_branch: Annotated[
        str, typer.Option("--default-branch", "-b")
    ] = DEFAULT_BRANCH,
    untracked_files: Annotated[
        bool, typer.Option("--untracked-files/--no-untracked-files", "-uf/-UF")
    ] = UNTRACKED_FILES,
    delete_feature_branch: Annotated[
        bool,
        typer.Option("--delete-feature-branch/--no-delete-feature-branch", "-dfb/-DBF"),
    ] = DELETE_FEATURE_BRANCH,
):
    if version:
        typer.echo(importlib.metadata.version("git-flush"))
        raise typer.Exit()

    if verbose:
        typer.echo(f"Default branch: {default_branch}")
        typer.echo(f"Untracked files: {untracked_files}")
        typer.echo(f"Delete feature branch: {delete_feature_branch}")

    current_directory = os.getcwd()
    repo = _get_repo()

    # Check default branch
    try:
        repo.refs[default_branch]
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

    if branch != "main" and delete_feature_branch:
        # Delete the original branch
        typer.echo(f"Deleting {branch}")
        repo.git.branch("-D", branch)


if __name__ == "__main__":
    app()
