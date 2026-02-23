from database.db_connection import get_connection


def save_message(user_id: int, chat_id: str, role: str, message: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (user_id, chat_id, role, message)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, chat_id, role, message),
    )

    conn.commit()
    conn.close()


def get_chat_messages(user_id: int, chat_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM conversations
        WHERE user_id = ? AND chat_id = ?
        ORDER BY timestamp ASC
        """,
        (user_id, chat_id),
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {"role": row["role"], "content": row["message"]}
        for row in rows
    ]


def get_user_chats(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT chat_id, MIN(timestamp) as created_at
        FROM conversations
        WHERE user_id = ?
        GROUP BY chat_id
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "chat_id": row["chat_id"],
            "title": f"Chat {i+1}"
        }
        for i, row in enumerate(rows)
    ]


def delete_all_chats(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM conversations
        WHERE user_id = ?
        """,
        (user_id,),
    )

    conn.commit()
    conn.close()