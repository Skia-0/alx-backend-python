#!/usr/bin/python3
"""
4-stream_ages.py

- stream_user_ages(): generator that yields ages one by one (memory-efficient)
- compute_average_age(): consumes the generator and prints the average age

Constraints satisfied:
- stream_user_ages uses exactly one loop (while with fetchone)
- compute_average_age uses at most one loop to aggregate
- total loops in script = 2
- does not use SQL AVG
"""

from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields the 'age' field from every row in user_data one by one.
    Uses a single loop with cursor.fetchone() so batches aren't loaded in memory.
    """
    conn = connect_to_prodev()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data;")

    while True:
        row = cursor.fetchone()
        if row is None:
            break
        # row can be a tuple like (age,)
        try:
            yield int(row[0])
        except Exception:
            # skip rows that don't parse
            continue

    cursor.close()
    try:
        conn.close()
    except Exception:
        pass


def compute_average_age():
    """
    Consumes stream_user_ages() and computes average age without loading all rows.
    Prints: Average age of users: <average>
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    avg = float(total) / count if count else 0.0
    # Print result in required format
    print(f"Average age of users: {avg}")


if __name__ == "__main__":
    compute_average_age()
