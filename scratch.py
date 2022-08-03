# Standard Library Imports
import logging

# Third Party Library Imports

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')

change_types = [
    "ALTER",
    "DROP",
    "ADD"
]



def alter_field(database_object: database, table_object: table, field_object: field, change_type: str):
    '''Takes in the db objects and associated table and field as well as the type of change to be made'''

    sql = F"ALTER TABLE {table_object.name}"

    if change_type == "DROP":
        sql = f"{sql} DROP {field_object.name}"
    else:
        if change_type == "ADD":
            sql = f"{sql} ADD COLUMN {field_object.name} {field_object.type}"
        else:
            sql = f"{sql} MODIFY COLUMN {field_object.name} {field_object.type}"

        if field_object.length is not None:
            sql = f"{sql}({field_object.length})"
        if field_object.increment is True:
            sql = f"{sql} AUTO_INCREMENT"
        if field_object.null is False and field_object.primary is False:
            sql = f"{sql} NOT NULL"
        if field_object.primary is True:
            sql = f"{sql} PRIMARY KEY"

    log.info(f"MODIFIED FIELD {field_object.name}")

    return