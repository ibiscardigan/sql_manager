# Standard Library Imports
import configparser
import json
import logging
import os
import sys

# Third Party Library Imports
import git

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


def confirm_schema(config: configparser.ConfigParser) -> dict:
    '''takes in an expected file name and return the dict extraction of the json'''

    schema_file_name = config['schema']['filename']

    if os.path.isdir('../sql_schema') is False:
        log.info("SCHEMA: DIR DOESNT EXIST")
        clone_schema_git(config)
    else:
        log.info("SCHEMA: UPDATING")
        update_schema()
        pass

    with open(f"../sql_schema/{schema_file_name}") as schemaFile:
        json_schema = json.load(schemaFile)

    return json_schema


def clone_schema_git(config: configparser.ConfigParser) -> None:
    '''Clones the repo of the schema'''
    log.info("SCHEMA: ATTEMPTING CLONE")

    path_list = (os.path.dirname(__file__)).split()[0].split('/')
    del path_list[-3:]
    path = ''

    for level in path_list:
        path = f"{path}/{level}"

    path = f"{path}/sql_schema"

    try:
        git.Repo.clone_from(config['schema']['url'], path, branch=config['instance']['env'])
        log.info("SCHEMA: CLONED")
    except Exception as error:
        log.critical(f"GIT: {error}")
        sys.exit()

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
