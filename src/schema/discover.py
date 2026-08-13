from src.core.base import BaseService
import json

class SchemaDiscovery(BaseService):

    def get_tables(self):
        return self.execute_query("SHOW TABLES IN formula1.gold;")

    def get_table_schema(self, table_name: str):
        return self.execute_query(f"DESCRIBE TABLE formula1.gold.{table_name};")

    def get_gold_schema(self):
        tables = self.get_tables()
        gold_schema = {}
        for table in tables:
            table_name = table["tableName"]
            gold_schema[table_name] = self.get_table_schema(table_name)

        with open("/Users/senthilvelaapalani/OG Dev/f1-app/src/schema/gold_schema.txt", "w+") as schema_file:
            json.dump(
                gold_schema,
                schema_file,
                indent = 4
            )

    def schema_loader(self):
        with open("/Users/senthilvelaapalani/OG Dev/f1-app/src/schema/gold_schema.txt") as schema_file:
            return schema_file.read()
