# Standard Library Imports
import logging

# Third Party Library Imports
import git

# Local Library Imports
import src.common.db_interaction.classes as classes

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
                    type=content['type'],
                    length=content['length'],
                    default=content['default'],
                    null=bool(content['null']),
                    primary=bool(content['primary']),
                    increment=bool(content['increment'])
                    )

            response.append(schema_field)

        log.info(f"SCHEMA: PROCESSED {len(response)} FIELDS")
        return response

    def check_valid_fields(self, field_dict: dict) -> bool:
        '''Takes in a dict of an expected field and returns true if it has all
        the right attributes'''
        # Get the attributes from the dataclass
        expected_keys = list(classes.field.__annotations__.keys())
        expected_keys.remove('name')

        log.debug(f"SCHEMA: VERIFYING FILED: {field_dict}")

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
