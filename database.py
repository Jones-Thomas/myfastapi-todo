import sqlite3

def initialize_database():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT
        )
        """
    )
    conn.commit()

    cursor.close()
    conn.close()
