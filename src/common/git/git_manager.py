# NOTE I THINK WE CAN MAKE THIS MORE GENERAL AND THUS GIVING THIS MODULE MORE FLEXIBILITY

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
    schema_dir = config['schema']['dir']

    if os.path.isdir(schema_dir) is False:
        log.info("GIT: DIR DOESNT EXIST")
        clone_schema_git(config)
    else:
        log.info("GIT: FOUND")
        update_schema(config)
        pass

    with open(f"{schema_dir}/{schema_file_name}") as schemaFile:
        json_schema = json.load(schemaFile)

    return json_schema


def clone_schema_git(config: configparser.ConfigParser) -> None:
    '''Clones the repo of the schema'''
    log.info("GIT: ATTEMPTING CLONE")

    path_list = (os.path.dirname(__file__)).split()[0].split('/')
    del path_list[-4:]
    path = ''

    for level in path_list:
        path = f"{path}/{level}"

    git_dir = config['schema']['dir'].split("/")[-1]
    path = f"{path}/{git_dir}"

    try:
        git.Repo.clone_from(config['schema']['url'], path, branch=config['instance']['env'])
        log.info("GIT: CLONED")
    except Exception as error:
        log.critical(f"GIT: {error}")
        sys.exit()

    pass


def update_schema(config: configparser.ConfigParser) -> None:
    '''Git pulls an update to the schema'''
    log.info("GIT: UPDATING")

    path_list = (os.path.dirname(__file__)).split()[0].split('/')
    del path_list[-4:]
    path = ''

    for level in path_list:
        path = f"{path}/{level}"

    git_dir = config['schema']['dir'].split("/")[-1]

    repo_path = f"{path}/{git_dir}/.git"
    log.debug(f"GIT: REPO PATH: {repo_path}")
    repo = git.Repo(repo_path)
    origin = repo.remotes[0]
    try:
        origin.pull()
        log.info("GIT: UPDATED")
    except Exception as error:
        log.error(f"GIT: PULL: {error}")

    pass
