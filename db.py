import sqlite3
from werkzeug.security import check_password_hash,generate_password_hash
import datetime

DB_NAME = "tasks.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_tasks_by_user(user_id, status=None, limit=10, offset=0, sort="created_at"):
    conn = get_connection()
    cursor = conn.cursor()

    base_query = """
        SELECT id, title, status, created_at, due_date, priority, subject
        FROM tasks
        WHERE user_id = ?
    """

    params = [user_id]

    if status:
        base_query += " AND status = ?"
        params.append(status)

    base_query += f" ORDER BY {sort} LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(base_query, params)

    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "status": row[2],
            "created_at": row[3],
            "due_date": row[4],
            "priority": row[5],
            "subject": row[6]
        })

    return tasks


def add_task(title, user_id, due_date=None, priority="medium",subject=None):
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    cursor.execute(
        """
        INSERT INTO tasks (title, status, user_id, created_at, due_date, priority,subject)
        VALUES (?, ?, ?, ?, ?, ?,?)
        """,
        (title, "pending", user_id, created_at, due_date, priority,subject)
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {
        "id": task_id,
        "title": title,
        "status": "pending",
        "user_id": user_id,
        "created_at": created_at,
        "due_date": due_date,
        "priority": priority,
        "subject":subject
    }


def update_task(task_id, user_id, title=None, status=None,due_date=None,priority=None,subject=None):
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if title:
        fields.append("title = ?")
        values.append(title)

    if status:
        fields.append("status = ?")
        values.append(status)
    if due_date:
        fields.append("due_date = ?")
        values.append(due_date)
    if priority:
        fields.append("priority = ?")
        values.append(priority)
    if subject:
        fields.append("subject=?")
        values.append(subject)

    values.append(task_id)
    values.append(user_id)

    query = f"""
    UPDATE tasks SET {", ".join(fields)}
    WHERE id = ? AND user_id = ?
    """

    cursor.execute(query, values)
    conn.commit()

    updated = cursor.rowcount
    conn.close()

    return updated


def delete_task(task_id,user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id,user_id)
    )

    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    return deleted

def create_user(username,password):
    conn=get_connection()
    cursor=conn.cursor()

    hashed_password=generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username,password) VALUES(?,?)",
            (username,hashed_password)
        )
        conn.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None
        
    finally:
        conn.close()

def get_user_by_username(username):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        "SELECT id,username,password FROM users WHERE username=?",
        (username,)
    )

    user=cursor.fetchone()
    conn.close()

    return user
