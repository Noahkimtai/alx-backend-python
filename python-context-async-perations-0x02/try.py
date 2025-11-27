import asyncio
import sqlite3


async def fetch_users(query):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


async def fetch_older_users(query, param=()):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, param)
        return cursor.fetchall()


async def fetch_concurrently():
    users_task = fetch_users("SELECT * FROM users")
    old_users_task = fetch_older_users(
        "SELECT * FROM users WHERE AGE > ?", (40,)
    )

    users, old_users = await asyncio.gather(users_task, old_users_task)

    # Return results instead of printing
    return users, old_users


if __name__ == "__main__":
    all_users, old_users = asyncio.run(fetch_concurrently())
    print("All users:", all_users)
    print("Old users:", old_users)
