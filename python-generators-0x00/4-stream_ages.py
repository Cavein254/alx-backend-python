import os
import mysql.connector
from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields one user age at a time from the database.
    """
    try:
        connection = connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # loop over rows, each row is a tuple like (age,)
            yield age

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()


def compute_average_age():
    """
    Consumes stream_user_ages() to calculate the average age.
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
