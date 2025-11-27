import sqlite3
import functools


def with_db_connection(func):
    """decorator to handle opening and closing sqlite3 connection"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect("users.db") as conn:
            return func(conn=conn, *args, **kwargs)

    return wrapper


def transactional(func):
    """If the function raises an error, rollback; otherwise commit the transaction."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:

            result = func(*args, **kwargs)
            kwargs.get("conn").commit()
            return result

        except sqlite3.Error as e:
            print(f"Error occured: {e}")
            kwargs.get("conn").rollback()
            return e

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email= ? WHERE id= ?", (new_email, user_id)
    )


update_user_email(user_id=1, new_email="caroline1@example.com")
