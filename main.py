# Standard Library Imports
import logging
import sys
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
    json_schema = git.confirm_schema(config)


    schema = db_schema.schema().process_dict(json_schema)

    # Now we need to go and get the db schema itself
    print(query.get_databases())

    pass


if __name__ == '__main__':
    main()
