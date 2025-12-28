import sqlite3

DB_NAME = "tasks.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_tasks_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, status FROM tasks WHERE user_id = ?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "status": row[2]
        })

    return tasks


def add_task(title,user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, status,user_id) VALUES (?, ?,?)",
        (title, "pending",user_id)
    )

    conn.commit()

    task_id = cursor.lastrowid
    conn.close()

    return {
        "id": task_id,
        "title": title,
        "status": "pending",
        "user_id":user_id
    }

def update_task_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )

    conn.commit()

    updated = cursor.rowcount
    conn.close()

    return updated

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    return deleted

def create_user(username,password):
    conn=get_connection()
    cursor=conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username,password) VALUES(?,?)",
            (username,password)
        )
        conn.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None
        
    finally:
        conn.close()

def login_user(username):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        "SELECT id,username,password FROM users WHERE username=?",
        (username,)
    )

    user=cursor.fetchone()
    conn.close()

    return user
