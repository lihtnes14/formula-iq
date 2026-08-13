from src.schema.discover import SchemaDiscovery

discovery = SchemaDiscovery()

schema = discovery.get_gold_schema()

for table, columns in schema.items():
    print(f"\n### {table}")

    for column in columns:
        print(column)