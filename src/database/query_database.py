# Standard Library Imports
import logging

# Third Party Library Imports

# Local Library Imports
import src.database.connection as connection
import src.database.classes as classes

# Configure Logging
log = logging.getLogger('log')


class sql_database():
    def __init__(self) -> None:
        self.schema = self.build_schema()
        pass

    def build_schema(self) -> list:
        '''Queries a MySQL instance and returns a list of the database with their structure as dict'''

        db = connection.connect()
        self.cursor = db.cursor()

        try:
            self.databases = self.get_databases()
        except Exception as error:
            log.critical(f"SQL: {error}")

        connection.disconnect(db)

        return self.databases

    def get_databases(self) -> list:
        '''Queries a MySQL instance and returns a list of the databases'''

        sql = "SHOW DATABASES"
        log.debug(f"SQL QUERY: {sql}")

        try:
            self.cursor.execute(sql)
        except Exception as error:
            log.critical(f"SQL: {error}")

        results = self.cursor.fetchall()

        response = []
        default_databases = ["information_schema", "mysql", "performance_schema"]

        for record in results:
            if record[0] not in default_databases:
                database = classes.database(name=record[0])
                self.use_database(database_name=database.name)
                database.tables = self.get_tables()
                response.append(database)
                log.info(database)

        return response

    def use_database(self, database_name: str) -> None:
        '''Changes the database being queried'''

        sql = f"USE {database_name}"
        log.debug(f"SQL QUERY: {sql}")
        self.cursor.execute(sql)

        return

    def get_tables(self) -> list:
        '''Takes in a database name and queries for the tables'''
        sql = "SHOW TABLES"

        log.debug(f"SQL QUERY: {sql}")
        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        response = []
        for record in results:
            log.debug(f"TABLE FOUND: {record[0]}")
            table_record = classes.table(name=record[0])
            table_record.fields = self.get_fields(table_name=table_record.name)
            response.append(table_record)

        log.info(f"SQL RESPONSE QTY: {len(response)}")

        return response

    def get_fields(self, table_name: str) -> list:
        '''Queries for the fields in a table'''
        sql = f"SHOW COLUMNS FROM {table_name}"

        log.debug(f"SQL: {sql}")
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        response = []
        for record in results:
            log.debug(f"FIELD FOUND: {record[0]}")
            field_type = record[1].replace("(", ",").replace(")", "").split(",")

            field_data = classes.field(
                name=record[0],
                type=field_type[0].upper()
            )
            if len(field_type) > 1:
                field_data.length = int(field_type[1])

            if record[2] == "NO":
                field_data.null = False
            else:
                field_data.null = True

            if "PRI" in record[3]:
                field_data.primary = True
            else:
                field_data.primary = False

            if "auto_increment" in record[5]:
                field_data.increment = True
            else:
                field_data.increment = False

            response.append(field_data)

        log.info(f"{table_name} FIELD QTY: {len(response)}")

        return response