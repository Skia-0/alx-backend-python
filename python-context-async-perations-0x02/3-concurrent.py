#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_FILE = "users.db"

async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        # return rows as list of tuples
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def fetch_concurrently():
    """Run both queries concurrently and print the results."""
    # gather runs both coroutines in parallel
    all_users_coro = async_fetch_users()
    older_users_coro = async_fetch_older_users()

    all_users, older_users = await asyncio.gather(all_users_coro, older_users_coro)

    print("All users (first 10 shown):")
    for row in all_users[:10]:
        print(row)
    print("\nUsers older than 40 (first 10 shown):")
    for row in older_users[:10]:
        print(row)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
