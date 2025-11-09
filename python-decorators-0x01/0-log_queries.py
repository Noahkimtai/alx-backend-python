import sqlite3
import functools
import logging
from datetime import datetime


# decorator to lof sql queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
        )
        logging.info(kwargs["querry"])
        func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(querry):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(querry)
    results = cursor.fetchall()
    conn.close()
    return results


### fetch users while logging the query
users = fetch_all_users(querry="SELECT * FROM users")
