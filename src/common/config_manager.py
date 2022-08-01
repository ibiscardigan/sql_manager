# Standard Library Imports
import configparser
import getpass
import logging
import os
import shutil

# Third Party Library Imports
import git

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


def confirm_config() -> configparser.ConfigParser:
    '''Searches for the config.ini file in the root dir. If it cant find the
    config file it will earch for a config_template.ini file and copy it; it
    will then prompt to complete the values in the new config.ini file'''

    # Check if the file exists
    if os.path.isfile('./config.ini') is False:
        log.warning('./config.ini does not exist')
        create_config()
        config_file = configparser.ConfigParser()
        config_file.read('config.ini')
    else:
        config_file = configparser.ConfigParser()
        config_file.read('config.ini')
        template_file = configparser.ConfigParser()
        template_file.read('config_template.ini')

        config_file = update_config(config_file=config_file,
                                    template_file=template_file)

        with open('./config.ini', 'w') as configfile:
            config_file.write(configfile)

    # Parse though the sections to complete the missing values
    config_file = verify_values(config_file)

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
                  template_file: configparser.ConfigParser) -> configparser.ConfigParser:
    '''Compares the config to the temaplte and creates missing keys'''

    log.debug("CONFIG CHECK")

    # Get the config details
    config_sections = list(config_file.keys())
    config_sections.remove("DEFAULT")
    config_dict = {}

    for key in config_sections:
        config_dict[key] = []
        for item in config_file[key].keys():
            config_dict[key].append(item)
    log.debug(config_dict)

    # Get the template details
    template_sections = list(template_file.keys())
    template_sections.remove("DEFAULT")
    template_dict = {}

    for key in template_sections:
        template_dict[key] = []
        for item in template_file[key].keys():
            template_dict[key].append(item)
    log.debug(template_dict)

    for template_key, template_value in template_dict.items():
        log.debug(f"CONFIG CHECKING {template_key}")
        if template_key not in config_dict.keys():
            log.info(f"CONFIG [{template_key}] NOT FOUND")
            config_file.add_section(template_key)
            for template_attribute in template_value:
                config_file.set(template_key, template_attribute, "")
        else:
            log.debug(f"CONFIG [{template_key}] FOUND")
            for template_attribute in template_value:
                if template_attribute not in config_dict[template_key]:
                    log.debug(f"{template_key} {config_dict[key]}")
                    log.info(f"CONFIG [{template_key}][{template_attribute}] NOT FOUND")
                    config_file.set(template_key, template_attribute, "")

    return config_file


def get_environment() -> str:
    '''Returns the branch from git'''
    response = str(git.Repo('.').active_branch)
    log.info(f"BRANCH: {response}")

    return response


def verify_values(config: configparser.ConfigParser) -> configparser.ConfigParser:
    ''''''
    for section in config.keys():
        for key, value in config[section].items():
            if len(value) == 0:
                log.info(f"key [{key}] is missing; attempting to capture")
                if key == 'password':
                    input_value = getpass.getpass('password: ')
                    log.info(f"Password Length: {len(input_value)}")
                elif key == 'env':
                    input_value = get_environment()
                else:
                    input_value = input(f"{key}: ")
                    log.info(f"Input: {input_value}")

                log.debug(section, key, input_value)
                config.set(section, key, input_value)

    return config
