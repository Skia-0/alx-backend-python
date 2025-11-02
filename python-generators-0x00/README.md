# python-generators-0x00 — seed.py

## Purpose
`seed.py` creates the `ALX_prodev` MySQL database, creates the `user_data` table and inserts rows from `user_data.csv`.
It also exposes a simple generator `stream_rows()` that yields rows from a table one-by-one.

## Required files
- `user_data.csv` — CSV with columns: `user_id,name,email,age` (header optional). Example UUIDs expected.

## Functions exported (used by tests)
- `connect_db()` -> connect to MySQL server (no database)
- `create_database(connection)` -> create `ALX_prodev` if missing
- `connect_to_prodev()` -> connect to `ALX_prodev`
- `create_table(connection)` -> create `user_data` table
- `insert_data(connection, csv_path)` -> insert rows from CSV (skips invalid rows)
- `stream_rows(connection, table='user_data', chunk_size=100)` -> generator yielding rows

## Usage (example)
Provided `0-main.py` in tests uses:
```python
connection = seed.connect_db()
seed.create_database(connection)
connection.close()

connection = seed.connect_to_prodev()
seed.create_table(connection)
seed.insert_data(connection, 'user_data.csv')
