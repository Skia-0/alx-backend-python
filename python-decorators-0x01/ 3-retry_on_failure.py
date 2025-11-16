#!/usr/bin/env python3
import time
import sqlite3
import functools

# -----------------------------
# with_db_connection decorator
# -----------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("database.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# -----------------------------
# retry_on_failure decorator
# -----------------------------
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == retries:
                        raise
                    time.sleep(delay)
            # Not reachable, but keeps linter happy
        return wrapper
    return decorator


# -----------------------------
# Function using BOTH decorators
# -----------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# -----------------------------
# Run the function
# -----------------------------
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
