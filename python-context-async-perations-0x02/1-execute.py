#!/usr/bin/python3
import sqlite3


class ExecuteQuery:
    """
    Custom context manager that handles both the connection
    and execution of a SQL query with parameters.
    """

    def __init__(self, query, params=None, db_name="users.db"):
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open the connection and execute the query."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the cursor and connection are closed properly."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Propagate exceptions if any occur
        return False


# --- Usage Example ---
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(query, params) as results:
        print(results)
