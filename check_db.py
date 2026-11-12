
from database import get_db

with get_db() as conn:
    cursor = conn.execute("""
        DELETE FROM conversations
        WHERE id NOT IN (
            SELECT DISTINCT conversation_id
            FROM messages
        )
    """)

    print(f"Deleted {cursor.rowcount} empty conversations.")
