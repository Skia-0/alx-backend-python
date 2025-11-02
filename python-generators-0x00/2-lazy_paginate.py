#!/usr/bin/python3
from seed import connect_to_prodev


def paginate_users(page_size, offset):
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
