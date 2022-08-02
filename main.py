# Standard Library Imports
import logging
import sys
from datetime import date

# Third Party Library Imports

# Local Library Imports
import src.common.config_manager as config_manager
import src.common.git_manager as git
import src.database.schema as db_schema
import src.database.query_database as query_database
import src.database.process as process


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

    # Get the schema
    json_schema = git.confirm_schema(config)
    schema = db_schema.schema().process_dict(json_schema)

    # Get the current state from the mysql instance
    sql_instance = query_database.sql_database()

    # Compare and update
    process.process_schema_changes(schema=schema, current_state=sql_instance)

    pass


if __name__ == '__main__':
    main()
