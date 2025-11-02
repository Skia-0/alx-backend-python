#!/usr/bin/python3
"""
1-batch_processing.py

Implements:
- stream_users_in_batches(batch_size): generator yielding batches of user rows
- batch_processing(batch_size): processes and prints users with age > 25
"""

from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows from user_data.

    Args:
        batch_size (int): number of rows per batch

    Yields:
        list[dict]: each batch containing up to batch_size user dicts
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")

    batch = []
    for row in cursor:
        user = {
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "age": int(row[3]),
        }
        batch.append(user)

        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:  # yield leftover rows
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes batches and prints users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in (u for u in batch if u["age"] > 25):
            print(user)
            print()
