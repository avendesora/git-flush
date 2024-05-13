# git-flush

`git-flush` is a CLI (command line interface) tool to clean up a local git repository after finishing work on a feature branch.

## Installation

Using [pipx](https://pipx.pypa.io/stable/) to install `git-flush` is recommended.

```shell
pipx install git-flush
```

However, you can install `git-flush` using `pip` as well.

```shell
python3 -m pip install git-flush
```

## Usage

```shell
git-flush [OPTIONS]
```

### Options

 | Option                  | Short Name | Opposite Option            | Opposite Short Name | Environment Variable            | Default Value | Description                                                          |
 |-------------------------|------------|----------------------------|---------------------|---------------------------------|---------------|----------------------------------------------------------------------|
 | --default-branch        | -b         |                            |                     | GIT_FLUSH_DEFAULT_BRANCH        | main          | The default branch of the repository.                                |
 | --untracked-files       | -uf        | --no-untracked-files       | -UF                 | GIT_FLUSH_UNTRACKED_FILES       | True          | Check for untracked files in the local repository before "flushing". |
 | --delete-feature-branch | -dfb       | --no-delete-feature-branch | -DFB                | GIT_FLUSH_DELETE_FEATURE_BRANCH | False         | If true, delete the current feature branch after "flushing".         |
 | --help                  | -h         |                            |                     |                                 |               | Show the help message and exit.                                      |

The environment variables are optional, but they will override the defaults listed above if the exist. If the `git-flush` command is used without an option, the value of the environment variable will be used if it exists; otherwise, the default value listed above will be used.

### Examples

Run `git-flush` with the default options:

```shell
git-flush
```

Run `git-flush` for a repo where the default branch is "dev" instead of "main":

```shell
git-flush -b dev
```

Run `git-flush` and delete the current feature branch after "flushing":

```shell
git-flush -dfb
```

Run `git-flush` with the default options, but do not check for untracked files:

```shell
git-flush -UF
```
