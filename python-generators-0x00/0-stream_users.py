#!usr/bin/env python3

import os, sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def stream_users():
    """
    Generator that yields rows one by one from the user_data table.
    """

    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("DATABASE")
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    for user in stream_users():
        print(user)
class CallableModule:
    """
    A callable module that allows the generator function to be called
    directly when the module is imported.
    This helps in solving `for user in islice(stream_users(), 6)` 
    `TypeError: 'module' object is not callable` error. when 1-main.py is run.
    """
    def __call__(self):
        return stream_users()

    def __getattr__(self, name):
        return globals()[name]

sys.modules[__name__] = CallableModule()


