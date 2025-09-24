
import sqlite3
import bcrypt

DB = "library.db"

schema = '''
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin','user')) DEFAULT 'user',
    membership_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    duration_months INTEGER,
    max_books INTEGER,
    fee REAL
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    isbn TEXT UNIQUE,
    category TEXT,
    copies_total INTEGER DEFAULT 1,
    copies_available INTEGER DEFAULT 1,
    shelf TEXT,
    year INTEGER,
    publisher TEXT
);

CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    director TEXT,
    category TEXT,
    year INTEGER,
    copies_total INTEGER DEFAULT 1,
    copies_available INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    user_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    return_date TEXT,
    status TEXT,
    fine REAL DEFAULT 0,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    amount REAL,
    method TEXT,
    date TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
'''

def ensure_admin(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = ?", ('admin@example.com',))
    if cur.fetchone():
        return
    pw = 'Admin@123'.encode('utf-8')
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    cur.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,?)",
                ('Admin','admin@example.com', hashed, 'admin'))
    conn.commit()

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.executescript(schema)
    ensure_admin(conn)
    conn.close()
    print("Initialized DB and ensured default admin (admin@example.com / Admin@123)")

if __name__ == '__main__':
    main()
