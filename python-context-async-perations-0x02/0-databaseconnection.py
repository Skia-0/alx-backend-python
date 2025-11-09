#!/usr/bin/python3
import sqlite3

class DatabaseConnection:
    """
    Custom context manager that automatically opens and closes
    a connection to the 'users.db' SQLite database.
    """

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Establish and return the SQLite connection."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection gracefully, even if an exception occurs."""
        if self.conn:
            self.conn.close()
        # Return False to propagate exceptions if any occur
        return False


# --- Usage Example ---
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        print(rows)
