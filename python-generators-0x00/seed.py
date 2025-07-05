#!/usr/bin/python3

import os
import mysql.connector
import uuid
from dotenv import load_dotenv, dotenv_values
from mysql.connector import errorcode

load_dotenv()


def connect_db():
    """
    connects to a MySQL database
    """
    try:
        conn = mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD")
        )
        print(
            f"Database connection successful",
            f"Host:{os.getenv('HOST')}"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error {err}")
        return None


connect_db()
