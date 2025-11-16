#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime

# -----------------------------------
# log_queries decorator
# -----------------------------------
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", None)
        if query:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Execute if run directly
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)

