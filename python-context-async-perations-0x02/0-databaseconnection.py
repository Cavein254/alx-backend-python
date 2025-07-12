import sqlite3

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()

with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)