# Standard Library Imports
import configparser
import getpass
import logging
import os
import shutil

# Third Party Library Imports
import pygit2

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


def confirm_config() -> None:
    '''Searches for the config.ini file in the root dir. If it cant find the
    config file it will earch for a config_template.ini file and copy it; it
    will then prompt to complete the values in the new config.ini file'''

    # Check if the file exists
    if os.path.isfile('./config.ini') is False:
        log.warning('./config.ini does not exist')
        create_config()

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

    return config_file


def create_config() -> None:
    '''Creates the config from a template ini file'''
    if os.path.isfile('./config_template.ini') is False:
        log.critical("No config_template.ini file to copy | -1")
        raise FileNotFoundError('No config_template.ini file to copy')
    else:
        log.info('Creating new config.ini')
        shutil.copy('./config_template.ini', './config.ini')
    return


def update_config(config_file: configparser.ConfigParser,
                  template_file: configparser.ConfigParser) -> None:
    '''Compares the config to the temaplte and creates missing keys'''

    # Get the config details
    config_sections = list(config_file.keys())
    config_sections.remove("DEFAULT")
    config_dict = {}

    for key in config_sections:
        config_dict[key] = []
        for item in config_file[key].keys():
            config_dict[key].append(item)

    # Get the template details
    template_sections = list(template_file.keys())
    template_sections.remove("DEFAULT")
    template_dict = {}

    for key in template_sections:
        template_dict[key] = []
        for item in template_file[key].keys():
            template_dict[key].append(item)

    for template_key, template_value in template_dict.items():
        if template_key not in config_dict.keys():
            # Create the new key and attributes
            pass
        else:
            for template_attribute in template_value:
                if template_attribute not in config_dict[key]:
                    # Create the ne attribute
                    pass

    return


def get_environment() -> str:
    '''Returns the branch from git'''
    response = pygit2.Repository('.').head.shorthand

    return response
