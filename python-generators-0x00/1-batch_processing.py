import mysql.connector
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Generator function to yield users in batches.
    """

    try:
        connection = connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []  # Reset batch for next iteration
        
        if batch:  # Yield any remaining users that didn't fill a complete batch
            yield batch
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    batch_size = 10  # Define the size of each batch
    for batch in stream_users_in_batches(batch_size):
        print(f"Processing batch of {len(batch)} users:")
        for user in batch:
            print(user)
        print("Batch processed.\n")
    print("All batches processed.")