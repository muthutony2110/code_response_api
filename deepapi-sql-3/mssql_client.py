import pyodbc

# Database connection
def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=SYSLP720;'
        'DATABASE=deep;'
        'Trusted_Connection=yes;'
    )

# Save conversation to DB
def save_history_with_task(user_id, task_name, prompt, message, code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ConversationHistory2 (user_id, task_name, prompt, message, code)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, task_name, prompt, message, code))
    conn.commit()
    conn.close()

# Get recent conversation history for user & task
def get_history_by_task(user_id, task_name, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    if limit:
        cursor.execute("""
            SELECT TOP (?) prompt, message, code
            FROM ConversationHistory2
            WHERE user_id = ? AND task_name = ?
            ORDER BY id ASC
        """, (limit, user_id, task_name))
    else:
        cursor.execute("""
            SELECT prompt, message, code
            FROM ConversationHistory2
            WHERE user_id = ? AND task_name = ?
            ORDER BY id ASC
        """, (user_id, task_name))
    rows = cursor.fetchall()
    conn.close()
    return [{"prompt": row[0], "message": row[1], "code": row[2]} for row in rows]

# Get all history for a user
def get_all_user_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_name, prompt, message, code
        FROM ConversationHistory2
        WHERE user_id = ?
        ORDER BY id ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"task_name": row[0], "prompt": row[1], "message": row[2], "code": row[3]}
        for row in rows
    ]

# Delete all history of a user
def delete_user_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ConversationHistory2 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# Delete a specific task history for a user
def delete_task_history(user_id, task_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM ConversationHistory2
        WHERE user_id = ? AND task_name = ?
    """, (user_id, task_name))
    conn.commit()
    conn.close()
