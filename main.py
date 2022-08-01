# Standard Library Imports
import logging
import sys
import json
import os
from datetime import date

# Third Party Library Imports

# Local Library Imports
import src.common.config_manager as config_manager
import src.database.schema as db_schema
import src.database.query as query
import src.common.git_manager as git

# Configure Logging
log = logging.getLogger('log')
logFilename = (f"logs/{str(date.today())}_sqlmanager.log")
logFileHandler = logging.FileHandler(logFilename)

log.setLevel(logging.INFO)
logFileHandler.setLevel(logging.INFO)

logFormat = logging.Formatter(' %(asctime)s | %(filename)s | %(funcName)s | %(lineno)d | %(levelname)s | %(message)s')
logFileHandler.setFormatter(logFormat)
log.removeHandler(logFileHandler)
log.addHandler(logFileHandler)


def main():
    log.info("STARTING ------------------------------------------------")
    if '-debug' in sys.argv:
        log.setLevel(logging.DEBUG)
        logFileHandler.setLevel(logging.DEBUG)
        log.debug("DEBUG MODE")

    # Get user generated config
    config = config_manager.confirm_config()

    # Get system generated config
    # Apply to logging

    schema_json_path = (config['schema']['filename'])
    schema_git_repo_path = f"{os.path.split(os.path.dirname(__file__))[0]}/sql_schema/.git"

    git.get_git_atts(schema_git_repo_path)
    sys.exit()

    with open(os.path.split(os.path.dirname(__file__))[0] + config['schema']['filename']) as schemaFile:
        json_schema = json.load(schemaFile)

    schema = db_schema.schema().process_dict(json_schema)

    # Now we need to go and get the db schema itself
    print(query.get_databases())

    pass


if __name__ == '__main__':
    main()
