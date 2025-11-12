import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=SYSLP720;'
        'DATABASE=deep;'
        'Trusted_Connection=yes;'
    )

def save_history(user_id, prompt, message, code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ConversationHistory (user_id, prompt, message, code)
        VALUES (?, ?, ?, ?)
    """, (user_id, prompt, message, code))
    conn.commit()
    conn.close()

def get_history(user_id, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP (?) prompt, message, code
        FROM ConversationHistory
        WHERE user_id = ?
        ORDER BY id DESC
    """, (limit, user_id))
    rows = cursor.fetchall()
    conn.close()
    return [{"prompt": row[0], "message": row[1], "code": row[2]} for row in rows]

def get_all_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, prompt, message, code FROM ConversationHistory ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"user_id": row[0], "prompt": row[1], "message": row[2], "code": row[3]} for row in rows]

def delete_user_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ConversationHistory WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def delete_specific_prompt(user_id, prompt):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM ConversationHistory
        WHERE user_id = ? AND prompt = ?
    """, (user_id, prompt))
    conn.commit()
    conn.close()

def delete_guest_history():
    delete_user_history("guest")
