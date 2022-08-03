# Standard Library Imports
import logging
import sys
from datetime import date

# Third Party Library Imports

# Local Library Imports
import src.common.config.config_manager as config_manager
import src.common.git.git_manager as git
import src.database.schema as db_schema
import src.database.query_database as query_database
import src.database.connection as connection
import src.database.process as process
import src.database.execute as execute


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

    if "-install" in sys.argv:
        sys.exit()

    # Get the current state from the mysql instance
    sql_instance = query_database.sql_database()

    # Compare and update
    changes = process.difference_processor(db_schema=schema, instance_schema=sql_instance)

    database = connection.connect()

    for change in changes.change_sql:
        execute.execute_sql(change, database)

    connection.disconnect(database)

    pass


if __name__ == '__main__':
    main()
