import sqlite3
import os

from flask import g, current_app
from werkzeug.security import generate_password_hash


DATABASE_NAME = 'expense_tracker.db'


def get_db():
    """Return a SQLite connection (one per request, stored on g)."""
    if '_database' not in g:
        db_path = os.path.join(current_app.root_path, DATABASE_NAME)
        g._database = sqlite3.connect(db_path)
        g._database.row_factory = sqlite3.Row
        g._database.execute('PRAGMA foreign_keys = ON')
    return g._database


def close_db(exception=None):
    """Close the database connection at the end of a request."""
    db = g.pop('_database', None)
    if db is not None:
        db.close()


def init_db():
    """Create all tables if they don't already exist."""
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')
    db.commit()


def seed_db():
    """Insert sample data for development (skips if data already exists)."""
    db = get_db()

    count = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if count > 0:
        return

    users = [
        ('Nitish Kumar', 'nitish@example.com', generate_password_hash('password123')),
        ('Priya Sharma', 'priya@example.com', generate_password_hash('password123')),
    ]
    db.executemany(
        'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
        users
    )

    expenses = [
        (1, 5200.00, 'Food',   '2026-04-01', 'Monthly groceries from BigBasket'),
        (1, 1450.00, 'Food',   '2026-04-03', 'Dinner at Barbeque Nation'),
        (1, 3500.00, 'Travel', '2026-04-05', 'Uber rides this week'),
        (1, 2100.00, 'Bills',  '2026-04-07', 'Jio Fiber broadband'),
        (1, 1800.00, 'Bills',  '2026-04-08', 'Electricity bill - BESCOM'),
        (1,  890.00, 'Food',   '2026-04-10', 'Swiggy orders'),
        (1, 1500.00, 'Travel', '2026-04-11', 'Metro card recharge'),
        (1, 1800.00, 'Food',   '2026-04-12', 'Weekly vegetables - local market'),
        (2, 4500.00, 'Food',   '2026-04-02', 'Groceries from DMart'),
        (2, 2800.00, 'Travel', '2026-04-06', 'Ola rides'),
        (2, 3200.00, 'Bills',  '2026-04-09', 'Airtel postpaid bill'),
    ]
    db.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        expenses
    )

    db.commit()
