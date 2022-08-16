# Standard Library Imports
import logging
import sys
from datetime import date

# Third Party Library Imports
import commonsql.connection as connection

# Local Library Imports
import src.common.config.config_manager as config_manager
import src.common.git.git_manager as git
import src.process_schema as db_schema
import src.process_differences as process


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
    schema = db_schema.schema(json_schema)
    if "-test_schema" in sys.argv:
        sys.exit()

    # Get the current state from the mysql instance
    database = connection.connection(config=config)
    database.connect()
    sql_instance = database.build_schema()
    if "-test_database" in sys.argv:
        sys.exit()

    # Compare and update
    changes = process.difference_processor(db_schema=schema, instance_schema=sql_instance)
    if "-test_difference" in sys.argv:
        sys.exit()

    for change in changes.change_sql:
        log.debug(f"MAIN: {change}")
        database.schema_execute(change)

    database.disconnect()

    pass


if __name__ == '__main__':
    main()
