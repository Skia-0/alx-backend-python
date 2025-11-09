
#!/usr/bin/env python3
import time
import sqlite3
import functools

# with_db_connection: creates a fresh connection and passes it as the first arg
def with_db_connection(func):
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


# retry_on_failure decorator factory
def retry_on_failure(retries=3, delay=2, exceptions=(Exception,)):
    """
    retries: number of attempts total
    delay: seconds between retries
    exceptions: tuple of exception classes that should trigger a retry
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
                    # log attempt
                    print(f"[retry_on_failure] attempt {attempt}/{retries} failed: {e}")
                    if attempt < retries:
                        print(f"[retry_on_failure] sleeping {delay}s before retry...")
                        time.sleep(delay)
                    else:
                        print("[retry_on_failure] all retry attempts exhausted; re-raising exception.")
                        raise
            # if loop exits unexpectedly, re-raise last exception
            if last_exc:
                raise last_exc
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1, exceptions=(sqlite3.OperationalError, sqlite3.DatabaseError, Exception))
def fetch_users_with_retry(conn):
    """
    This function receives a sqlite3 connection from with_db_connection.
    The retry decorator will re-call the wrapped function (which will
    reopen a new connection each top-level call due to with_db_connection).
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
        print("Final failure:", type(exc).__name__, exc)
