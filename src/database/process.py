# Standard Library Imports
import logging

# Third Party Library Imports

# Local Library Imports
import src.database.schema as schema
import src.database.query_database as query

# Configure Logging
log = logging.getLogger('log')


def process_differences(db_schema: schema.schema, current_state: query.sql_database) -> None:
    '''Takes in the schema and current state; identifies te changes to be made and executes those changes'''

    create_databases = []
    drop_databases = []

    # If there is a db in current state that is not in schema, add to drop list
    for db in current_state.databases:
        if db_schema.lookup(db.name) is None:
            log.warning(f"PROCESS: DB {db.name} TO BE DROPPED")
            drop_databases.append(db)

    # If there is a db in schema that is not in current state, add to create list
    for db in db_schema.databases:
        if current_state.lookup(db.name) is None:
            log.info(f"PROCESS: DB {db.name} TO BE CREATED")
            create_databases.append(db)

    pass
