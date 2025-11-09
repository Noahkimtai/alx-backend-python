import sqlite3


class DatabaseConnection:
    def __init__(self, db):
        self.connection_object = sqlite3.connect(db)

    def __enter__(self):
        """open db session context"""
        print("db connection established")
        return self.connection_object

    def __exit__(self, exc_type, exc_value, exc_tb):
        """close db session context"""
        if exc_type:
            print(f"Exception has been handled {exc_value}")

        self.connection_object.close()
        return True


with DatabaseConnection("users.db") as db_connection:
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)


# class File:

#     def __init__(self, file_name, method):
#         self.file_object = open(file_name, method)

#     def __enter__(self):
#         return self.file_object

#     def __exit__(self):
#         print("exception handled")
#         self.file_object.close()
#         return True
