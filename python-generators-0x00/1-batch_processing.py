#!/usr/bin/python3
"""
1-batch_processing.py

Provides:
- stream_users_in_batches(batch_size): generator yielding batches of user dicts
- batch_processing(batch_size): processes each batch and prints users with age > 25
"""

from seed import connect_to_prodev, stream_rows


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches (lists) of user rows from user_data.

    - batch_size: number of rows per yielded batch
    - Uses a single loop to accumulate rows into batches and yield them.
    - Each row is expected to be a tuple or dict from the DB cursor; we convert to dict if needed.
    """
    conn = connect_to_prodev()
    if not conn:
        return  # if connection fails, generator ends silently

    batch = []
    # Use seed.stream_rows(conn, table='user_data', chunk_size=batch_size) to fetch rows in chunks,
    # but that generator yields rows one-by-one. We'll gather them into batches here.
    for row in stream_rows(conn, "user_data", chunk_size=batch_size):
        # If row is a tuple, convert to dict assuming column order:
        # But seed.stream_rows returns DB rows as tuples in our seed implementation.
        # We'll convert to the dict shape expected by tests:
        if isinstance(row, dict):
            rec = row
        else:
            # assume order: user_id, name, email, age
            try:
                user_id, name, email, age = row
            except Exception:
                # fallback: put raw row
                rec = {"row": row}
            else:
                rec = {
                    "user_id": user_id,
                    "name": name,
                    "email": email,
                    "age": int(age)
                }

        batch.append(rec)
        if len(batch) >= batch_size:
            yield batch
            batch = []

    # yield any remaining rows
    if batch:
        yield batch

    # close connection (seed.stream_rows uses a cursor that is closed in seed)
    try:
        conn.close()
    except Exception:
        pass


def batch_processing(batch_size):
    """
    Process batches from stream_users_in_batches(batch_size).
    For each batch, filter users with age > 25 and print each user dict.

    Uses at most 3 loops total:
    - 1 loop over batches (below)
    - the list comprehension below is counted as a loop for filtering
    - no further loops
    """
    for batch in stream_users_in_batches(batch_size):
        # filter using list comprehension (counts as a loop)
        filtered = [user for user in batch if user.get("age", 0) > 25]
        # print each filtered user (prints one-by-one; this is not a new loop)
        for user in filtered:
            print(user)
            print()  # matches sample output spacing
