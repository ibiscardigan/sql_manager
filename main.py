# Standard Library Imports
import logging
import json
from datetime import date

# Third Party Library Imports

# Local Library Imports
import src.setup as setup

# Configure Logging
log = logging.getLogger('log')
logFilename = (f"logs/{str(date.today())}_sqlmanager.log")
logFileHandler = logging.FileHandler(logFilename)

log.setLevel(logging.INFO)
logFileHandler.setLevel(logging.DEBUG)

logFormat = logging.Formatter(' %(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(message)s')
logFileHandler.setFormatter(logFormat)
log.removeHandler(logFileHandler)
log.addHandler(logFileHandler)

default_databases = ["information_schema", "mysql", "performance_schema"]


def main():
    log.info("STARTING ------------------------------------------------")
    setup.confirm_config()


if __name__ == '__main__':
    main()
