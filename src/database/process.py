# Standard Library Imports
import logging

# Third Party Library Imports

# Local Library Imports
import src.database.schema as schema
import src.database.query_database as query
import src.common.db_interaction.schema_manipulation as sql

# Configure Logging
log = logging.getLogger('log')


class difference_processor():
    def __init__(self, db_schema: schema.schema, instance_schema: query.sql_database) -> None:
        log.info("PROCESS: STARTING DIF ASSESSMENT")
        self.json_schema = db_schema
        self.instance_schema = instance_schema
        self.change_sql = []

        self.process_database_differences()

        pass

    def process_database_differences(self) -> None:
        '''Takes in the schema and current state; identifies te changes to be made and executes those changes'''

        create_databases = []
        drop_databases = []
        update_databases = []
        log.info("PROCESS: ASSESSING DB OBJECTS")

        # If there is a db in current state that is not in schema, add to drop list
        for db in self.instance_schema.databases:
            if self.json_schema.lookup(db.name) is None:
                log.warning(f"PROCESS: DB {db.name} TO BE DROPPED")
                drop_databases.append(db)
            elif db.name not in update_databases:
                log.info(f"PROCESS: ADDING DB {db.name} TO UPDATE")
                update_databases.append(db.name)
            else:
                log.debug(f"PROCESS: DB {db.name} ALREADY IN UPDATE LIST")

        # If there is a db in schema that is not in current state, add to create list
        for db in self.json_schema.databases:
            if self.instance_schema.lookup(db.name) is None:
                log.info(f"PROCESS: DB {db.name} TO BE CREATED")
                create_databases.append(db)
            elif db.name not in update_databases:
                log.info(f"PROCESS: ADDING DB {db.name} TO UPDATE")
                update_databases.append(db.name)
            else:
                log.debug(f"PROCESS: DB {db.name} ALREADY IN UPDATE LIST")

        log.debug(f"PROCESS: CREATE LIST: {create_databases}")
        log.debug(f"PROCESS: DROP LIST:   {drop_databases}")
        log.debug(f"PROCESS: UPDATE LIST: {update_databases}")

        for db in create_databases:
            log.info(f"PROCESS: GENERATING SQL for NEW DB: {db.name}")
            log.debug(f"PROCESS: DB: {db}")
            create_commands = sql.create_database(db)
            self.change_sql.extend(create_commands)
            log.info(f"PROCESS: {len(create_commands)} SQL COMMANDS GENERATED")
            for command in create_commands:
                log.debug(f"PROCESS: SQL GENERATED: {command}")

        for db in update_databases:
            self.process_table_differences(db)

        pass

    def process_table_differences(self, database_name: str) -> None:
        ''''Get the changes in tables'''
        log.info(f"PROCESS: ASSESSING TABLE OBJECTS FOR {database_name}")

        log.info(f"PROCESS: COLLECTING {database_name} SCHEMA")
        schema_structure = self.json_schema.lookup(database_name)
        log.info(f"PROCESS: COLLECTING {database_name} INSTANCE")
        instance_structure = self.instance_schema.lookup(database_name)

        drop_tables = []
        create_tables = []
        update_tables = []

        for table in instance_structure.tables:
            if schema_structure.lookup(table.name) is None:
                log.warning(f"PROCESS: TABLE {table.name} TO BE DROPPED")
                drop_tables.append(table.name)
            elif table.name not in update_tables:
                log.info(f"PROCESS: ADDING TABLE {table.name} TO UPDATE")
                update_tables.append(table.name)
            else:
                log.debug(f"PROCESS: TABLE {table.name} ALREADY IN UPDATE LIST")

        for table in schema_structure.tables:
            if instance_structure.lookup(table.name) is None:
                log.info(f"PROCESS: TABLE {table.name} TO BE CREATED")
                create_tables.append(table)
            elif table.name not in update_tables:
                log.info(f"PROCESS: ADDING TABLE {table.name} TO UPDATE")
                update_tables.append(table.name)
            else:
                log.debug(f"PROCESS: TABLE {table.name} ALREADY IN UPDATE LIST")

        log.debug(f"PROCESS: CREATE LIST: {create_tables}")
        log.debug(f"PROCESS: DROP LIST:   {drop_tables}")
        log.debug(f"PROCESS: UPDATE LIST: {update_tables}")

        for table in create_tables:
            log.info(f"PROCESS: GENERATING SQL for NEW TABLE: {table.name}")
            log.debug(f"PROCESS: TABLE: {table}")
            create_commands = sql.create_table(table=table, db_name=database_name)
            self.change_sql.extend(create_commands)
            log.info(f"PROCESS: {len(create_commands)} SQL COMMANDS GENERATED")
            for command in create_commands:
                log.debug(f"PROCESS: SQL GENERATED: {command}")

        for table in update_tables:
            self.process_field_differences(table_name=table, db_name=database_name)

        pass

    def process_field_differences(self, table_name: str, db_name:  str) -> None:
        ''''Get the changes in fields'''
        log.info(f"PROCESS: ASSESSING FIELD OBJECTS FOR {table_name}")

        log.info(f"PROCESS: COLLECTING {table_name} SCHEMA")
        schema_structure = self.json_schema.lookup(db_name).lookup(table_name)
        log.info(f"PROCESS: COLLECTING {table_name} INSTANCE")
        instance_structure = self.instance_schema.lookup(db_name).lookup(table_name)

        drop_fields = []
        create_fields = []
        update_fields = []

        # If there is a field in the instance that is not in schema, add to drop list
        for field in instance_structure.fields:
            if schema_structure.lookup(field.name) is None:
                log.warning(f"PROCESS: FIELD {field.name} TO BE DROPPED")
                drop_fields.append(field.name)
            elif field.name not in update_fields:
                log.info(f"PROCESS: ADDING FIELD {field.name} TO UPDATE")
                update_fields.append(field.name)
            else:
                log.debug(f"PROCESS: FIELD {field.name} ALREADY IN UPDATE LIST")

        # If there is a field in schema that is not in the instance, add to create list
        for field in schema_structure.fields:
            if instance_structure.lookup(field.name) is None:
                log.info(f"PROCESS: FIELD {field.name} TO BE CREATED")
                create_fields.append(field)
            elif field.name not in update_fields:
                log.info(f"PROCESS: ADDING FIELD {field.name} TO UPDATE")
                update_fields.append(field.name)
            else:
                log.debug(f"PROCESS: FIELD {field.name} ALREADY IN UPDATE LIST")

        for field in create_fields:
            log.info(f"PROCESS: GENERATING SQL for NEW FIELD: {field.name}")
            log.debug(f"PROCESS: FIELD: {field}")
            create_commands = sql.create_field(field=field, table_name=table_name, db_name=db_name)
            log.info(f"PROCESS: {len(create_commands)} SQL COMMANDS GENERATED")
            for command in create_commands:
                log.debug(f"PROCESS: SQL GENERATED: {command}")
        self.change_sql.extend(create_commands)

        for field in update_fields:
            self.process_attribute_differences(field_name=field, table_name=table_name, db_name=db_name)
            pass

        pass

    def process_attribute_differences(self, field_name: str, table_name: str, db_name: str) -> None:
        ''''Get the changes in fields'''
        log.info(f"PROCESS: ASSESSING FIELD ATTRIBUTES FOR {field_name}")

        log.info(f"PROCESS: COLLECTING {field_name} SCHEMA")
        schema_structure = self.json_schema.lookup(db_name).lookup(table_name).lookup(field_name)
        log.info(f"PROCESS: COLLECTING {field_name} INSTANCE")
        instance_structure = self.instance_schema.lookup(db_name).lookup(table_name).lookup(field_name)

        # This time we actually need to compare the 'structure' of the differences and store down the updates
        # likley need to make the output sql

        attributes = list(schema_structure.__annotations__.keys())
        attributes.remove('name')

        for attribute in attributes:
            schema_value = getattr(schema_structure, attribute)
            instance_value = getattr(instance_structure, attribute)

            if schema_value != instance_value:
                log.warning(f"PROCESS: REQUIRED CHANGE: FIELD {field_name}.{attribute} {instance_value} -> {schema_value}")
                log.debug(f"PROCESS: TYPES: INSTANCE {type(instance_value)} -> SCHEMA {type(schema_value)}")

        pass
