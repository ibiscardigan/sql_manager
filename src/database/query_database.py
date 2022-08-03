# Standard Library Imports
import logging
import sys

# Third Party Library Imports

# Local Library Imports
import src.database.connection as connection
import src.common.db_interaction.classes as classes

# Configure Logging
log = logging.getLogger('log')


class sql_database():
    def __init__(self) -> None:
        log.info("DATABASE: CAPTURING SCHEMA")
        self.schema = self.build_schema()
        pass

    def build_schema(self) -> list:
        '''Queries a MySQL instance and returns a list of the database with their structure as dict'''

        db = connection.connect()
        self.cursor = db.cursor()

        try:
            self.databases = self.get_databases()
        except Exception as error:
            log.critical(f"DATABASE: {error}")

        connection.disconnect(db)

        return self.databases

    def lookup(self, database_name: str) -> classes.database:
        '''Looks for a database in the schema, and if found returns it'''
        for db in self.databases:
            if db.name == database_name:
                return db

        return

    def get_databases(self) -> list:
        '''Queries a MySQL instance and returns a list of the databases'''

        sql = "SHOW DATABASES"
        log.info(f"DATABASE: QUERY: {sql}")

        try:
            self.cursor.execute(sql)
        except Exception as error:
            log.critical(f"DATABASE: {error}")

        results = self.cursor.fetchall()
        log.info(f"DATABASE: RESPONSE: {results}")

        response = []
        default_databases = ["information_schema", "mysql", "performance_schema"]

        for record in results:
            if record[0] not in default_databases:
                database = classes.database(name=record[0])
                log.info(f"DATABASE: PROCESSING {database.name}")

                self.use_database(database_name=database.name)

                database.tables = self.get_tables()
                response.append(database)
                log.info(f"DATABASE: PROCESSED: {database}")

        return response

    def use_database(self, database_name: str) -> None:
        '''Changes the database being queried'''

        sql = f"USE {database_name}"
        log.info(f"DATABASE: QUERY: {sql}")
        try:
            self.cursor.execute(sql)
        except Exception as error:
            log.critical(f"DATABASE: {error}")
            sys.exit()

        return

    def get_tables(self) -> list:
        '''Takes in a database name and queries for the tables'''
        sql = "SHOW TABLES"

        log.info(f"DATABASE: QUERY: {sql}")
        self.cursor.execute(sql)

        results = self.cursor.fetchall()
        log.debug(f"DATABASE: RESPONSE: {results}")

        response = []
        for record in results:
            table_record = classes.table(name=record[0])
            log.info(f"DATABASE: PROCESSING TABLE: {table_record.name}")
            table_record.fields = self.get_fields(table_name=table_record.name)
            response.append(table_record)

        log.info(f"DATABASE; PROCESSED {len(response)} TABLES")

        return response

    def get_fields(self, table_name: str) -> list:
        '''Queries for the fields in a table'''
        sql = f"SHOW COLUMNS FROM {table_name}"

        log.info(f"DATABASE: QUERY: {sql}")
        self.cursor.execute(sql)

        results = self.cursor.fetchall()
        log.debug(f"DATABASE: RESPONSE: {results}")

        response = []
        for record in results:
            log.debug(f"DATABASE: PROCESSING FIELD: {record[0]}")
            field_type = record[1].replace("(", ",").replace(")", "").split(",")

            field_data = classes.field(
                name=record[0],
                type=field_type[0].upper()
            )
            if len(field_type) > 1:
                if field_type[1].isnumeric() is True:
                    field_data.length = int(field_type[1])
                else:
                    field_data.length = int(field_type[1][:-9])

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

        log.info(f"DATABASE: PROCESSED {len(response)} FIELDS")

        return response
