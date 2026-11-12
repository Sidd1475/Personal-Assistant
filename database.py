
import sqlite3
import uuid

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chat_history.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db():
    with get_db() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_messages_conversation
            ON messages(conversation_id)
        """)

def generate_chat_id():
    return str(uuid.uuid4())


def save_conversation(chat_id, first_message):
    title = first_message.strip().replace("\n", " ")[:35]

    with get_db() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO conversations (id, title)
            VALUES (?, ?)
            """,
            (chat_id, title or "New Chat")
        )

def create_conversation():
    chat_id = str(uuid.uuid4())

    with get_db() as conn:
        conn.execute(
            "INSERT INTO conversations (id, title) VALUES (?, ?)",
            (chat_id, "New Chat")
        )

    return chat_id


def get_conversations():
    with get_db() as conn:
        return conn.execute("""
            SELECT id, title
            FROM conversations
            ORDER BY created_at DESC
        """).fetchall()


def save_message(chat_id, role, content):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO messages
            (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (chat_id, role, content))


def get_messages(chat_id):
    with get_db() as conn:
        return conn.execute("""
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
        """, (chat_id,)).fetchall()


def update_title(chat_id, title):
    with get_db() as conn:
        conn.execute("""
            UPDATE conversations
            SET title = ?
            WHERE id = ?
        """, (title, chat_id))

def delete_conversation(chat_id):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM messages WHERE conversation_id = ?",
            (chat_id,)
        )

        conn.execute(
            "DELETE FROM conversations WHERE id = ?",
            (chat_id,)
        )