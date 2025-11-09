import sqlite3
import functools


def with_db_connection(func):
    """decorator to handle opening and closing sqlite3 connection"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # conn = sqlite3.connect("users.db")
        # results = func(conn=conn, *args, **kwargs)
        # conn.close()
        # return results

        with sqlite3.connect("users.db") as conn:
            return func(conn=conn, *args, **kwargs)

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))

    return cursor.fetchone()


#### Fetch user by ID with automatic connection handling

user = get_user_by_id(user_id=1)
print(user)
