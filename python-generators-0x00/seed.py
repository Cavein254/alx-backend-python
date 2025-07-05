import os
import mysql.connector
import uuid
import requests
import csv
from dotenv import load_dotenv
from mysql.connector import errorcode

load_dotenv()


def get_data_from_url():
    """
    fetches data from the url in the .env file
    """
    url = os.getenv("DATA_URL")
    filename = 'data.csv'
    if not os.path.exists(filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open('data.csv', 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    else:
        print(f"File {filename} already exists. Skipping download.")

def connect_db():
    """
    connects to the mysql database server
    """
    try:
        connection = mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD")
        )
        print(
            f"Database connection successful",
            f"Host:{os.getenv('HOST')}"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error {err}")
        return None


def create_database(connection):
    """
    creates the database `ALX_prodev` if it does not exist
    """
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")


def connect_to_prodev():
    """
    connects the the `ALX_prodev` database in MYSQL
    """
    try:
        connection = mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = os.getenv("DATABASE")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """
    creates a table user_data if it does not exists with the required fields
    """
    cursor = connection.cursor()
    create_table_sql = """CREATE TABLE IF NOT EXISTS user_data (
        user_id  CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )"""
    try:
        cursor.execute(create_table_sql)
        print("Table `user_data` created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    cursor.close()

def insert_data(connection, data):
    """
      inserts data in the database if it does not exist
    """

connection = connect_to_prodev()