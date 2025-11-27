import sqlite3


class ExecuteQuery:
    """context manager that takes a query as input and executes it, managing both connection and the query execution"""

    def __init__(self, db, query, param=None):
        self.db = db
        self.query = query
        self.param = param or ()
        self.connection_object = None
        self.results = None

    def __enter__(self):
        """open db session context"""
        print("establishing db connection")
        self.connection_object = sqlite3.connect(self.db)
        self.results = self.query_db(
            self.connection_object, self.query, self.param
        )
        return self.results

    def __exit__(self, exc_type, exc_value, exc_tb):
        """close db session context"""
        if exc_type:
            print(f"Exception has been handled {exc_value}")

        self.connection_object.close()
        return True

    def query_db(self, conn, query, param):
        cursor = conn.cursor()
        cursor.execute(query, param)
        results = cursor.fetchall()
        return results


with ExecuteQuery(
    "users.db", "SELECT * FROM users WHERE age > ?", (25,)
) as res:
    print(res)

with ExecuteQuery("users.db", "SELECT * FROM users WHERE id = 1") as res:
    print(res)

with ExecuteQuery("users.db", "SELECT * FROM users WHERE id = ?", (1,)) as res:
    print(res)
