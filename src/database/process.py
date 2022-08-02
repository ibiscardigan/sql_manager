# Standard Library Imports
import logging

# Third Party Library Imports

# Local Library Imports
import src.database.schema as schema
import src.database.query_database as query

# Configure Logging
log = logging.getLogger('log')


class difference_processor():
    def __init__(self, db_schema: schema.schema, instance_schema: query.sql_database) -> None:
        self.json_schema = db_schema
        self.instance_schema = instance_schema
        self.process_database_differences()
        pass

    def process_database_differences(self) -> None:
        '''Takes in the schema and current state; identifies te changes to be made and executes those changes'''

        create_databases = []
        drop_databases = []
        update_databases = []

        # If there is a db in current state that is not in schema, add to drop list
        for db in self.instance_schema.databases:
            if self.json_schema.lookup(db.name) is None:
                log.warning(f"PROCESS: DB {db.name} TO BE DROPPED")
                drop_databases.append(db)
            elif db.name not in update_databases:
                log.debug(f"PROCESS: ADDING DB {db.name} TO UPDATE")
            else:
                log.debug(f"PROCESS: DB {db.name} ALREADY IN UPDATE LIST")

        # If there is a db in schema that is not in current state, add to create list
        for db in self.json_schema.databases:
            if self.instance_schema.lookup(db.name) is None:
                log.info(f"PROCESS: DB {db.name} TO BE CREATED")
                create_databases.append(db)
            elif db.name not in update_databases:
                log.debug(f"PROCESS: ADDING DB {db.name} TO UPDATE")
            else:
                log.debug(f"PROCESS: DB {db.name} ALREADY IN UPDATE LIST")

        for db in update_databases:
            self.process_table_differences(db)

        pass

    def process_table_differences(self, database_name: str) -> None:
        ''''Get the changes in tables'''

        schema_structure = self.json_schema.lookup(database_name)
        instance_structure = self.instance_schema.lookup(database_name)

        drop_tables = []
        create_tables = []
        update_tables = []

        for table in instance_structure.tables:
            if schema_structure.lookup(table.name) is None:
                log.warning(f"PROCESS: TABLE {table.name} TO BE DROPPED")
                drop_tables.append(table.name)
            elif table.name not in update_tables:
                log.debug(f"PROCESS: ADDING TABLE {table.name} TO UPDATE")
            else:
                log.debug(f"PROCESS: TABLE {table.name} ALREADY IN UPDATE LIST")

        for table in schema_structure.tables:
            if instance_structure.lookup(table.name) is None:
                log.warning(f"PROCESS: TABLE {table.name} TO BE CREATED")
                create_tables.append(table.name)
            elif table.name not in update_tables:
                log.debug(f"PROCESS: ADDING TABLE {table.name} TO UPDATE")
            else:
                log.debug(f"PROCESS: TABLE {table.name} ALREADY IN UPDATE LIST")

        pass
