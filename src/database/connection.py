# Standard Library Imports
import configparser
import logging

# Third Party Library Imports
import mysql.connector

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')

# Setup config
config_file = configparser.ConfigParser()
config_file.read('config.ini')


def connect(database_name: str = None):

    if database_name is not None and isinstance(database_name, str) is False:
        raise TypeError(f"DATABASE: database_name != str; {type(database_name)}")

    if database_name is None:
        log.info(f"DATABASE: ATTEMPTING CONNECTION AS {config_file['db']['db_user']}")
        try:
            database = mysql.connector.connect(
                host=config_file['db']['host'],
                user=config_file['db']['db_user'],
                password=config_file['db']['password']
                )
        except Exception as error:
            print(error)
            log.error(f"DATABASE: COULD NOT CONNECT | {error}")

    else:
        log.info(f"DATABASE: CONNECTING TO {database_name} USING {config_file['db']['db_user']}")
        try:
            database = mysql.connector.connect(
                host=config_file['db']['host'],
                user=config_file['db']['db_user'],
                password=config_file['db']['password'],
                database=database_name
                )
        except Exception as error:
            log.error(f"DATABASE: COULD NOT CONNECT | {error}")
            return

    log.info(f"DATABASE: CONNECTED TO {database_name}")
    return database


def disconnect(database):
    log.debug("DATABASE: DISCONNECTING")
    database.disconnect()
    log.info("DATABASE: DISCONNECTED")
    pass
