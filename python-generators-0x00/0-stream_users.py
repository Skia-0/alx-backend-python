#!/usr/bin/python3
import MySQLdb

def stream_users():
    """
    Generator that yields user rows one by one from user_data table.
    """
    # Connect to database (adjust credentials as needed)
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="your_password",
        db="your_database"
    )

    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user_data;")

    # Single loop with yield
    for row in cursor:
        yield row

    cursor.close()
    db.close()
