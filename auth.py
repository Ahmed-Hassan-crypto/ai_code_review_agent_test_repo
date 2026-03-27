"""User authentication module with critical security issues."""

import sqlite3
import hashlib
import os


def create_user(username, password):
    """Create a new user in the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: SQL Injection
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    cursor.execute(query)
    
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    """Authenticate user - has SQL injection vulnerability."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    conn.close()
    return result is not None


def get_user_by_id(user_id):
    """Get user details by ID."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Using string formatting - potential SQL injection
    query = f"SELECT username, email FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    
    conn.close()
    return result


def update_password(username, new_password):
    """Update user password - stores plain text!"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: Storing plain text password
    query = f"UPDATE users SET password = '{new_password}' WHERE username = '{username}'"
    cursor.execute(query)
    
    conn.commit()
    conn.close()


def get_all_users():
    """Get all users - exposes sensitive data."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Exposes password hash
    cursor.execute("SELECT id, username, password, email FROM users")
    users = cursor.fetchall()
    
    conn.close()
    return users


def delete_user(username):
    """Delete user account."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SQL injection vulnerability
    query = f"DELETE FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    conn.commit()
    conn.close()


# Global database connection - bad practice
DB_PATH = 'users.db'


def init_db():
    """Initialize database with users table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()