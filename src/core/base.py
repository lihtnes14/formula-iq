from src.core.databr import get_connection


class BaseService:

    def execute_query(self, query: str):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

                return [
                    dict(zip(columns, row))
                    for row in rows
                ]