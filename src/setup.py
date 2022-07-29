# Standard Library Imports
import configparser
import getpass
import logging
import os
import shutil

# Third Party Library Imports

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')

# Configure config
config_file = configparser.ConfigParser()
config_file.read('config.ini')


def confirm_config() -> None:
    '''Searches for the config.ini file in the root dir. If it cant find the
    config file it will earch for a config_template.ini file and copy it; it
    will then prompt to complete the values in the new config.ini file'''

    # Check if the file exists
    if os.path.isfile('./config.ini') is False:
        log.warning('./config.ini does not exist')
        if os.path.isfile('./config_template.ini') is False:
            log.critical("No config_template.ini file to copy | -1")
            raise FileNotFoundError('No config_template.ini file to copy')
        else:
            log.info('Creating new config.ini')
            shutil.copy('./config_template.ini', './config.ini')

    # Import the file
    config_file = configparser.ConfigParser()
    config_file.read('config.ini')

    # Parse though the sections to complete the missing values
    for section in config_file.keys():
        for key, value in config_file[section].items():
            if len(value) == 0:
                log.info(f"key [{key}] is missing; attempting to capture")
                if key != 'password':
                    input_value = input(f"{key}: ")
                    log.info(f"Input: {input_value}")
                else:
                    input_value = getpass.getpass('password: ')
                    log.info(f"Password Length: {len(input_value)}")

                config_file.set(section, key, input_value)

        # Save the changes to the config file
        with open('./config.ini', 'w') as configfile:
            config_file.write(configfile)
