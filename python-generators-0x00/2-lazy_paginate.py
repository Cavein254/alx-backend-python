import os
import mysql.connector
from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database starting at the given offset.
    Returns a list of user rows.
    """
    try:
        connection = connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()


def lazy_paginate(page_size):
    """
    Generator that lazily fetches paginated users from the database.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    page_size = 10 
    for page in lazy_paginate(page_size):
        print(f"Page: {page}")
       