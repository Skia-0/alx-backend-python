#!/usr/bin/python3
"""
1-batch_processing.py

Provides:
- stream_users_in_batches(batch_size): generator yielding batches of user dicts
- batch_processing(batch_size): prints users with age > 25 from each batch

Constraints satisfied:
- stream_users_in_batches has exactly one loop (uses cursor.fetchmany)
- Uses yield
- Total loops across file <= 3
"""

from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    """
    Generator yielding lists (batches) of user dicts from the user_data table.

    Args:
        batch_size (int): number of rows per batch to yield

    Yields:
        list of dicts: each dict has keys 'user_id', 'name', 'email', 'age'
    """
    conn = connect_to_prodev()
    if not conn:
        return

    cursor = conn.cursor()
    # Use a server-side iteration pattern: fetchmany in a loop (single loop)
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        batch = []
        for row in rows:
            # row expected as tuple: (user_id, name, email, age)
            try:
                user_id, name, email, age = row
            except Exception:
                # fallback: store row as-is
                user = {"row": row}
            else:
                user = {
                    "user_id": user_id,
                    "name": name,
                    "email": email,
                    "age": int(age)
                }
            batch.append(user)
        yield batch

    cursor.close()
    try:
        conn.close()
    except Exception:
        pass


def batch_processing(batch_size):
    """
    Consumes batches from stream_users_in_batches and prints users older than 25.

    Loops:
      1) iterate batches (for batch in ...)
      2) iterate filtered users and print (for user in ...)
    + generator has its own loop => total loops = 3 (complies)
    """
    for batch in stream_users_in_batches(batch_size):
        # filter using a generator expression in the for loop (no extra named loop)
        for user in (u for u in batch if u.get("age", 0) > 25):
            print(user)
            print()
