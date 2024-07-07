import psycopg2
from psycopg2 import OperationalError, Error
from psycopg2.extras import RealDictCursor
import os
import pandas as pd

class DatabaseHelper:
    def __init__(self):
        self.connection = self._get_db_connection()

    def _get_db_connection(self):
        try:
            conn = psycopg2.connect(
                dbname=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                host=os.environ.get("DB_HOST"),
                port=os.environ.get("DB_PORT")
            )
            print("Connection successful")
            return conn
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            return None

    def _execute_query(self, query, data=None):
        if self.connection is None:
            return None, 'Failed to connect to the database'

        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, data)
                self.connection.commit()
                rows = cur.fetchall()
                df = pd.DataFrame(rows)
                return df, None
        except Error as e:
            self.connection.rollback()
            return None, str(e)

    def _execute_update(self, query, data=None):
        if self.connection is None:
            return 'Failed to connect to the database'

        try:
            with self.connection.cursor() as cur:
                cur.execute(query, data)
                self.connection.commit()
                return None
        except Error as e:
            self.connection.rollback()
            return str(e)

    def _close_connection(self):
        if self.connection:
            self.connection.close()
db_helper = DatabaseHelper()
