#!usr/bin/venv python3
import os
import mysql.connector
import uuid
import requests
import csv
from dotenv import load_dotenv


load_dotenv()
filename = 'user_data.csv'

def get_data_from_url():
    """
    fetches data from the url in the .env file
    """
    url = os.getenv("DATA_URL")
    if not os.path.exists(filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open('user_data.csv', 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    else:
        print(f"File {filename} already exists. Skipping download.")
   

def read_csv_file(filename):
    """ 
    reads the csv file and returns from disk
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = csv.DictReader(file)
            return list(content)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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

def insert_data(connection, filename):
    """
      inserts data in the database if it does not exist
    """
    data = rearid_csv_file(filename)
    if not data:
        print("No data to insert.")
        return
    cursor = connection.cursor()
    insert_data = """INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        email = VALUES(email),
                        age = VALUES(age)
                    """
    try:
        for row in data:
            user_id = str(uuid.uuid4())
            cursor.execute(insert_data, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to insert data: {err}")
    cursor.close()

if __name__ == "__main__":
    get_data_from_url()
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Database connection successful")
        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, filename)
            connection.close()
        else:
            print("Failed to connect to ALX_prodev database.")
    else:
        print("Failed to connect to MySQL server.")
else:
    print("This script is intended to be run as a standalone program.")
    print("Please run it directly..")    