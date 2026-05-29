import mysql.connector

def conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="simple_db"
    )

def read_tasks():
    c = conn()
    cur = c.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    cur.close()
    c.close()
    return rows

def insert_task(title):
    c = conn()
    cur = c.cursor()
    cur.execute("INSERT INTO tasks(title) VALUES(%s)", (title,))
    c.commit()
    cur.close()
    c.close()
    return {"status": "inserted"}

def update_task(task_id, title):
    c = conn()
    cur = c.cursor()
    cur.execute("UPDATE tasks SET title=%s WHERE id=%s", (title, task_id))
    c.commit()
    cur.close()
    c.close()
    return {"status": "updated"}