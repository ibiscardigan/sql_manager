# Standard Library Imports
import configparser
import json
import logging
import os
import pathlib
import sys

# Third Party Library Imports
import git

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


def get_git_atts(repo_path: str) -> None:
    repo = git.Repo(repo_path)

    branch = repo.active_branch
    print(branch.name)
    origin = repo.remotes[0]
    print(type(origin))


def confirm_schema(config: configparser.ConfigParser) -> dict:
    '''takes in an expected file name and return the dict extraction of the json'''

    schema_file_name = config['schema']['filename']

    if os.path.isdir('../sql_schema') is False:
        log.info("SCHEMA: DIR DOESNT EXIST")
        # Create the file here
    else:
        log.info("SCHEMA: UPDATING")
        update_schema()
        pass

    with open(f"../sql_schema/{schema_file_name}") as schemaFile:
        json_schema = json.load(schemaFile)

    return json_schema


def clone_schema_git():
    '''Clones the repo of the schema'''

    pass


def update_schema():
    '''Git pulls an update to the schema'''
    path_list = (os.path.dirname(__file__)).split()[0].split('/')
    del path_list[-3:]
    path = ''

    for level in path_list:
        path = f"{path}/{level}"

    repo_path = f"{path}/sql_schema/.git"
    log.info(f"GIT REPO PATH: {repo_path}")
    repo = git.Repo(repo_path)
    origin = repo.remotes[0]
    try:
        origin.pull()
        log.info("SCHEMA: UPDATED")
    except Exception as error:
        log.error(f"GIT PULL: {error}")

    pass
