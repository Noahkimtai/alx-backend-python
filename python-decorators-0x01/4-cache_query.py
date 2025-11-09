import time
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


query_cache = {}


def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if query in query_cache.keys():
            print("hitting cache")
            return query_cache[query]
        print("Not hitting cache")
        query_cache[query] = func(*args, **kwargs)
        return query_cache[query]

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# first call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)
# second call will use the cache result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
