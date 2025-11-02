#!/usr/bin/python3
"""
2-lazy_paginate.py

Provides:
- paginate_users(page_size, offset): fetches a page (list of dicts) from user_data
- lazy_paginate(page_size): generator that yields pages lazily (uses paginate_users)
- lazy_pagination alias for compatibility with test/main
"""

from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """
    Fetch a single page from the user_data table.

    Args:
        page_size (int): number of rows to fetch
        offset (int): offset for LIMIT/OFFSET

    Returns:
        list[dict]: list of rows as dicts, empty list if none
    """
    conn = connect_to_prodev()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    try:
        conn.close()
    except Exception:
        pass
    return rows


def lazy_paginate(page_size):
    """
    Generator that yields pages (lists of dicts) of size `page_size`.
    Only fetches the next page when requested.

    Uses a single loop (while True).
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# compatibility alias used by some mains/tests
lazy_pagination = lazy_paginate
