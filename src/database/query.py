# Standard Library Imports
import logging

# Third Party Library Imports

# Local Library Imports
import src.database.connection as connection
# import src.database.classes as classes

# Configure Logging
log = logging.getLogger('log')


def get_databases() -> list:
    '''Queries a MySQL instance and returns a list of the databases'''

    sql = "SHOW DATABASES"

    db = connection.connect()
    cursor = db.cursor()
    cursor.execute(sql)
    log.debug(f"SQL: {sql}")

    results = cursor.fetchall()
    connection.disconnect(db)

    response = []
    default_databases = ["information_schema", "mysql", "performance_schema"]

    for record in results:
        if record[0] not in default_databases:
            response.append(record[0])

    return response

# Map out the subsequent functions to get tables and fields within each
# need to convert then to a dict the same as the schema
