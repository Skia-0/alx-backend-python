#!/usr/bin/env python3
import time
import sqlite3
import functools

# Global cache storage
query_cache = {}

# Decorator for managing DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Decorator for caching query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from args or kwargs
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]
        # Execute and cache
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Caching new result for query.")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
