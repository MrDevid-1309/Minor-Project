import sqlite3
from werkzeug.security import generate_password_hash

DB = "placement.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, name TEXT NOT NULL,
        cgpa REAL DEFAULT 7, projects INTEGER DEFAULT 0, internships INTEGER DEFAULT 0,
        communication INTEGER DEFAULT 5, role TEXT DEFAULT 'student');
    CREATE TABLE IF NOT EXISTS attempts(
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        aptitude REAL, technical REAL, coding REAL, logic REAL,
        probability REAL, label TEXT, details TEXT);
    """)
    if not conn.execute("SELECT 1 FROM users WHERE username='admin'").fetchone():
        conn.execute("INSERT INTO users(username,password,name,role) VALUES(?,?,?,?)",
                     ("admin", generate_password_hash("admin123"), "Administrator", "admin"))
    conn.commit()
    conn.close()
