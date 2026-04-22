import sqlite3
import os

# 根據架構文件，資料庫放置於 instance/database.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳的資料可以用字典的方式存取欄位
    return conn

def init_db():
    """初始化資料庫與資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()

def create_task(title, description=""):
    """新增任務"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, description) VALUES (?, ?)',
        (title, description)
    )
    conn.commit()
    conn.close()

def get_all_tasks():
    """取得所有任務"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id):
    """根據 ID 取得單一任務"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_task(task_id, title, description):
    """更新任務內容"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tasks SET title = ?, description = ? WHERE id = ?',
        (title, description, task_id)
    )
    conn.commit()
    conn.close()

def toggle_task_status(task_id):
    """切換任務完成狀態"""
    task = get_task_by_id(task_id)
    if task:
        new_status = 0 if task['is_completed'] else 1
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET is_completed = ? WHERE id = ?',
            (new_status, task_id)
        )
        conn.commit()
        conn.close()

def delete_task(task_id):
    """刪除任務"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
