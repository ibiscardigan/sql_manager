# Standard Library Imports
import logging
from inspect import getmembers

# Third Party Library Imports
import git
import commonsql.classes as classes

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


class schema():
    def __init__(self, schema_dict: dict) -> None:
        log.info("SCHEMA: GENERATING SCHEMA OBJECT")
        self.databases = []
        self.env = str(git.Repo('.').active_branch)
        self.process_dict(schema_dict)
        pass

    def process_dict(self, schema_dict: dict) -> None:
        for db, content in schema_dict['schema'].items():
            if self.env != "master":
                schema_database = classes.database(name=f"{self.env}_{db}")
            else:
                schema_database = classes.database(name=db)
            log.info(f"SCHEMA: PROCESSING DB: {schema_database}")

            schema_database.tables = self.process_tables(content)
            log.info(f"SCHEMA: PROCESSED: {schema_database}")

            self.databases.append(schema_database)
        pass

    def lookup(self, database_name: str) -> classes.database:
        '''Looks for a database in the schema, and if found returns it'''
        for db in self.databases:
            if db.name == database_name:
                return db

        return

    def process_tables(self, database_dict: dict) -> list:
        '''Takes in the parsed json as a dict and attempts to generate table obj'''
        response = []

        for dict_table, content in database_dict.items():
            schema_table = classes.table(name=dict_table)
            log.info(f"SCHEMA: PROCESSING TABLE: {schema_table}")

            schema_table.fields = self.process_fields(content)
            log.debug(f"SCHEMA: TABLE PROCESSED: {schema_table}")

            response.append(schema_table)

        log.info(f"SCHEMA: PROCESSED {len(response)} TABLES")
        return response

    def process_fields(self, table_dict: dict) -> list:
        '''Takes in the parsed json as a dict and attempts to generate field obj'''
        response = []

        for dict_field, content in table_dict.items():
            log.debug(f"SCHEMA: PROCESSING FIELD: {content}")

            if self.check_valid_fields(content) is False:
                log.warning("SCHEMA: FIELD IS NOT VALID")
                raise ValueError("Submitted field is not valid")

            else:
                schema_field = classes.field(
                    name=dict_field,
                    field_type=content['field_type'],
                    length=content['length'],
                    default=content['default']
                    )
                if content['null'] == "True":
                    schema_field.null = True
                else:
                    schema_field.null = False

                if content['primary'] == "True":
                    schema_field.primary = True
                else:
                    schema_field.primary = False

                if content['increment'] == "True":
                    schema_field.increment = True
                else:
                    schema_field.increment = False

            response.append(schema_field)

        log.info(f"SCHEMA: PROCESSED {len(response)} FIELDS")
        return response

    def check_valid_fields(self, field_dict: dict) -> bool:
        '''Takes in a dict of an expected field and returns true if it has all
        the right attributes'''
        # Get the attributes from the dataclass
        expected_keys = list(getmembers(classes.field.__init__)[0][1])
        log.debug(f"SCHEMA: KEYS: {expected_keys}")
        expected_keys.remove('name')
        expected_keys.remove('return')

        log.debug(f"SCHEMA: VERIFYING FIELD: {field_dict}")

        actual_keys = list(field_dict.keys())

        # Sort both keys so they should be in the same order
        ek = sorted(expected_keys)
        ak = sorted(actual_keys)

        if ak == ek:
            return True
        else:
            log.error(f"SCHEMA: FIELD EXPECTED: {ek}")
            log.error(f"SCHEMA: FIELD ACTUAL:   {ak}")
            return False
