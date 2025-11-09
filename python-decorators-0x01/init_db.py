import sqlite3


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT CHECK(role IN ('guest', 'host', 'admin')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
    """
    )

    # Optionally insert some sample data
    cursor.executemany(
        """
    INSERT INTO users (first_name, last_name, email, role)
    VALUES (?, ?, ?, ?)
    """,
        [
            ("Alice", "Mwangi", "alice1@example.com", "guest"),
            ("Brian", "Otieno", "brian1@example.com", "host"),
            ("Caroline", "Kariuki", "caroline1@example.com", "admin"),
        ],
    )

    conn.commit()
    conn.close()

    print("✅ Database and users table created successfully!")


if __name__ == "__main__":
    init_db()
