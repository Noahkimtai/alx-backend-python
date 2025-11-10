import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE AGE > ?", (40,)) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    # Run both queries concurrently
    users_task = async_fetch_users()
    old_users_task = async_fetch_older_users()

    users, old_users = await asyncio.gather(users_task, old_users_task)

    # Return results instead of printing
    return users, old_users


if __name__ == "__main__":
    all_users, old_users = asyncio.run(fetch_concurrently())
    print("All users:", all_users)
    print("Old users:", old_users)
