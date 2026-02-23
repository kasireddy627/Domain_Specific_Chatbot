from database.db_connection import get_connection


def create_user(name: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email)
        VALUES (?, ?)
        """,
        (name, email),
    )

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return user_id


def get_user_by_email(email: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users WHERE email = ?
        """,
        (email,),
    )

    user = cursor.fetchone()
    conn.close()

    return user