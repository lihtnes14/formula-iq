from databricks import sql

from .config import (
    DATABRICKS_HOST,
    DATABRICKS_HTTP_PATH,
    DATABRICKS_TOKEN,
)


def get_connection():

    return sql.connect(
        server_hostname=DATABRICKS_HOST,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
    )


class DatabricksService:

    def execute_query(self, query: str) -> list[dict]:

        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(query)

                columns = [
                    column[0]
                    for column in cursor.description
                ]

                rows = cursor.fetchall()

                return [
                    dict(zip(columns, row))
                    for row in rows
                ]