# database.py

import sqlite3


class Database:
    def __init__(self, db_name='bot_database.sqlite'):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                username TEXT,
                nickname TEXT,
                notifications_enabled BOOLEAN
            )
        ''')
        self.connection.commit()

    def add_user(self, user_id, chat_id, username, nickname):
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, chat_id, username, nickname, notifications_enabled)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, chat_id, username, nickname, False))
        self.connection.commit()

    def update_notification(self, user_id, enabled):
        self.cursor.execute('''
            UPDATE users
            SET notifications_enabled = ?
            WHERE user_id = ?
        ''', (enabled, user_id))
        self.connection.commit()

    def get_user(self, user_id):
        self.cursor.execute('''
            SELECT * FROM users WHERE user_id = ?
        ''', (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute('''
            SELECT * FROM users
        ''')
        return self.cursor.fetchall()
