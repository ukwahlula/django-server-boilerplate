import os

from fabric import task
from patchwork.transfers import rsync

TESTING_SSH_HOST = os.environ["TESTING_SSH_HOST"]
TESTING_SSH_FOLDER_PATH = os.environ["TESTING_SSH_FOLDER_PATH"]

SERVER_RSYNC_OPTS = dict(
    rsync_opts='--filter=":- .gitignore"',
    exclude=[
        ".git",
        ".github",
        ".vscode",
        ".gitignore",
        "CODEOWNERS",
        "LICENSE",
        "README.md",
        ".pre-commit-config.yaml",
        ".secrets.baseline",
        "pyproject.toml",
        "setup.cfg",
        ".isort.cfg",
    ],
)


@task(hosts=(TESTING_SSH_HOST,))
def deploytesting(connection):
    rsync(connection, ".", TESTING_SSH_FOLDER_PATH, **SERVER_RSYNC_OPTS)

    compose = "docker-compose -f docker-compose-testing.yml"

    with connection.cd(TESTING_SSH_FOLDER_PATH):
        connection.run(f"{compose} build")
        connection.run(f"{compose} stop")
        connection.run(f"{compose} up -d")


@task
def deploystaging(connection):
    pass


@task
def deployprod(connection):
    pass
