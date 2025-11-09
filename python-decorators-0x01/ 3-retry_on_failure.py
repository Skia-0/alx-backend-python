#!/usr/bin/python3
import time
import sqlite3
import functools

def with_db_connection(func):
    """
    Creates a fresh sqlite3 connection for each call, passes it as first arg,
    and closes it after the call returns.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=2, exceptions=(sqlite3.OperationalError,)):
    """
    Decorator factory that retries the wrapped function up to `retries` times,
    waiting `delay` seconds between attempts when one of `exceptions` is raised.

    Important: Use this decorator OUTSIDE (above) the connection decorator so
    each retry invokes the inner function that creates a fresh DB connection.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"[retry_on_failure] attempt {attempt}/{retries} failed: {e}")
                    if attempt < retries:
                        print(f"[retry_on_failure] retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print("[retry_on_failure] all retry attempts exhausted, raising last exception.")
                        raise
        return wrapper
    return decorator


# --- IMPORTANT: retry_on_failure MUST be applied OUTSIDE (on top of) with_db_connection ---
@retry_on_failure(retries=3, delay=1, exceptions=(sqlite3.OperationalError, sqlite3.DatabaseError, Exception))
@with_db_connection
def fetch_users_with_retry(conn):
    """
    Performs a simple SELECT. Each retry will get a fresh connection because
    retry_on_failure wraps with_db_connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    return rows


if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as exc:
        print("Final error:", type(exc).__name__, exc)
