# Standard Library Imports
import logging

# Third Party Library Imports
import mysql.connector

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


def execute_sql(sql: str, db_connection: mysql.connector.connection) -> None:
    ''''''
    log.info(f"EXECUTING: {sql}")

    cursor = db_connection.cursor()
    try:
        cursor.execute(sql)
    except Exception as error:
        log.error(f"EXECUTING: {error}")

    return
