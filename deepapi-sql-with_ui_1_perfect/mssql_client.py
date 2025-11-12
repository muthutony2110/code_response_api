import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=SYSLP720;'
        'DATABASE=deep;'
        'Trusted_Connection=yes;'
    )

# === Save history ===
def save_history_with_task(user_id, task_name, prompt, message, code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ConversationHistory2 (user_id, task_name, prompt, message, code)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, task_name, prompt, message, code))
    conn.commit()
    conn.close()

# === Get history for a specific task ===
def get_history_by_task(user_id, task_name=None, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    if limit is not None:
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer or None")

    if task_name:
        if limit is None:
            query = """
                SELECT id, prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ? AND task_name = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id, task_name))
        else:
            query = f"""
                SELECT TOP ({limit}) id, prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ? AND task_name = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id, task_name))
    else:
        if limit is None:
            query = """
                SELECT id, prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id,))
        else:
            query = f"""
                SELECT TOP ({limit}) id, prompt, message, code
                FROM ConversationHistory2
                WHERE user_id = ?
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": row[0], "prompt": row[1], "message": row[2], "code": row[3]}
        for row in rows
    ]

# === Get all history for a user ===
def get_all_user_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, task_name, prompt, message, code
        FROM ConversationHistory2
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "task_name": row[1],
            "prompt": row[2],
            "message": row[3],
            "code": row[4]
        }
        for row in rows
    ]

# === Delete all history for a user ===
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
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# === Delete history for a specific task ===
def delete_task_history(user_id, task_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM ConversationHistory2
        WHERE user_id = ? AND task_name = ?
    """, (user_id, task_name))
    conn.commit()
    conn.close()

# === Delete a single history entry ===
def delete_single_history_entry(user_id, task_name, prompt):
    """
    Delete one specific history entry for a user + task + prompt
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM ConversationHistory2
        WHERE user_id = ? AND task_name = ? AND prompt = ?
    """, (user_id, task_name, prompt))
    conn.commit()
    conn.close()
