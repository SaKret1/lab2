import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("DELETE FROM users")

    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES
        ('admin', 'admin123'),
        ('user', 'user123'),
        ('student', 'student123')
    """)

    conn.commit()
    conn.close()
