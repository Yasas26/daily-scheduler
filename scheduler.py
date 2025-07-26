from db import get_connection

def add_task(user_id, day, time_slot, task):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO schedule (user_id, day, time_slot, task)
        VALUES (%s, %s, %s, %s)
    """, (user_id, day, time_slot, task))
    conn.commit()
    cur.close()
    conn.close()

def get_tasks(user_id, day):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, time_slot, task FROM schedule
        WHERE user_id=%s AND day=%s
        ORDER BY time_slot
    """, (user_id, day))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM schedule WHERE id=%s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()

def update_task(task_id, new_task):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE schedule SET task=%s WHERE id=%s", (new_task, task_id))
    conn.commit()
    cur.close()
    conn.close()
