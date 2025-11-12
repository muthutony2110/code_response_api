import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=SYSLP720;'
        'DATABASE=deep;'
        'Trusted_Connection=yes;'
    )


def save_history_with_task(user_id, task_name, prompt, message, code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ConversationHistory2 (user_id, task_name, prompt, message, code)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, task_name, prompt, message, code))
    conn.commit()
    conn.close()


def get_history_by_task(user_id, task_name=None, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    if limit is not None:
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer or None")

    if task_name:
        if limit is None:
            # No limit: fetch all rows for user_id and task_name
            query = """
                SELECT prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ? AND task_name = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id, task_name))
        else:
            # Limit present: use TOP clause (safe interpolation after validation)
            query = f"""
                SELECT TOP ({limit}) prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ? AND task_name = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id, task_name))
    else:
        if limit is None:
            # No task_name, fetch all rows for user_id
            query = """
                SELECT prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id,))
        else:
            # Use TOP clause with limit for user_id only
            query = f"""
                SELECT TOP ({limit}) prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return [{"prompt": row[0], "message": row[1], "code": row[2]} for row in rows]




def get_all_user_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_name, prompt, message, code
        FROM ConversationHistory2
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "task_name": row[0],
            "prompt": row[1],
            "message": row[2],
            "code": row[3]
        }
        for row in rows
    ]


def delete_user_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ConversationHistory2 WHERE user_id = ?", (user_id,))
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM ConversationHistory2")
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            cursor.execute("DBCC CHECKIDENT ('ConversationHistory2', RESEED, 0)")
            conn.commit()
    except Exception as e:
        conn.rollback()
        # Optionally log the exception here
        raise
    finally:
        conn.close()



def delete_task_history(user_id, task_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM ConversationHistory2
        WHERE user_id = ? AND task_name = ?
    """, (user_id, task_name))
    conn.commit()
    conn.close()


