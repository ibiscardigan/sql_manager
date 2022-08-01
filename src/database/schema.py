# Standard Library Imports
import logging
from dataclasses import dataclass

# Third Party Library Imports
import git

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


@dataclass
class field():
    name: str
    type: str
    length: int = None
    default: str = None
    null: bool = True
    primary: bool = False
    increment: bool = None


@dataclass
class table():
    name: str
    fields: list = None


@dataclass
class database():
    name: str
    env: str = None
    tables: list = None


class schema():
    def __init__(self) -> None:
        self.databases = []
        self.env = str(git.Repo('.').active_branch)
        pass

    def process_dict(self, schema_dict) -> None:
        for db, content in schema_dict['schema'].items():
            schema_database = database(name=db, env=self.env)
            log.debug(schema_database)

            schema_database.tables = process_tables(content)
            log.info(schema_database)

            self.databases.append(schema_database)
        pass


def process_tables(database_dict: dict) -> list:
    '''Takes in the parsed json as a dict and attempts to generate table obj'''
    response = []

    for dict_table, content in database_dict.items():
        schema_table = table(name=dict_table)
        log.debug(schema_table)

        schema_table.fields = process_fields(content)
        log.info(schema_table)

        response.append(schema_table)

    return response


def process_fields(table_dict: dict) -> list:
    '''Takes in the parsed json as a dict and attempts to generate field obj'''
    response = []

    for dict_field, content in table_dict.items():
        log.info(content)

        if check_valid_fields(content) is False:
            raise ValueError("Submitted field is not valid")

        else:
            schema_field = field(
                name=dict_field,
                type=content['type'],
                length=content['length'],
                default=content['default'],
                null=content['null'],
                primary=content['primary'],
                increment=content['increment']
                )

        response.append(schema_field)

    return response


def check_valid_fields(field_dict: dict) -> bool:
    '''Takes in a dict of an expected field and returns true if it has all
    the right attributes'''
    # Get the attributes from the dataclass
    expected_keys = list(field.__annotations__.keys())
    expected_keys.remove('name')

    log.info(field_dict)

    actual_keys = list(field_dict.keys())

    # Sort both keys so they should be in the same order
    ek = sorted(expected_keys)
    ak = sorted(actual_keys)

    if ak == ek:
        return True
    else:
        log.error(f"Field Missmatch: Expected: {ek}")
        log.error(f"Field Missmatch: Actual:   {ak}")
        return False
