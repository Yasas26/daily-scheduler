import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
import main  # For returning to login window on logout

# Correct and clean time slots
time_slots = [
    "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "12:00", "12:30", "13:00",
    "13:30", "14:00", "14:30", "15:00", "15:30",
    "16:00", "16:30", "17:00", "17:30"
]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def open_scheduler_ui(user_id):
    root = tk.Tk()
    root.title("Weekly Scheduler")
    root.geometry("900x650")  # Increased screen size

    selected_day = tk.StringVar(value="Monday")
    entry_list = []

    def load_schedule():
        day = selected_day.get()
        for widget in task_frame.winfo_children():
            widget.destroy()
        entry_list.clear()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT time_slot, task FROM schedule WHERE user_id = %s AND day = %s",
            (user_id, day)
        )
        schedule = dict(cur.fetchall())
        conn.close()

        for i, slot in enumerate(time_slots):
            ttk.Label(task_frame, text=slot, width=10).grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(task_frame, width=60)
            entry.insert(0, schedule.get(slot, ""))
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            entry_list.append((slot, entry))

    def save_schedule():
        conn = get_connection()
        cur = conn.cursor()
        day = selected_day.get()
        cur.execute("DELETE FROM schedule WHERE user_id = %s AND day = %s", (user_id, day))

        for slot, entry in entry_list:
            task = entry.get().strip()
            if task:
                cur.execute(
                    "INSERT INTO schedule (user_id, day, time_slot, task) VALUES (%s, %s, %s, %s)",
                    (user_id, day, slot, task)
                )
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", f"{day}'s schedule saved!")

    def handle_logout():
        root.destroy()
        main.restart_login()

    # Top bar
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)

    ttk.Label(top_frame, text="Select Day:").pack(side=tk.LEFT, padx=5)
    day_menu = ttk.Combobox(top_frame, values=days, textvariable=selected_day, state="readonly", width=12)
    day_menu.pack(side=tk.LEFT, padx=5)

    ttk.Button(top_frame, text="Load", command=load_schedule).pack(side=tk.LEFT, padx=10)
    ttk.Button(top_frame, text="Save", command=save_schedule).pack(side=tk.LEFT)
    ttk.Button(top_frame, text="Logout", command=handle_logout).pack(side=tk.LEFT, padx=20)

    # Scrollable area
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    task_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=task_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    task_frame.bind("<Configure>", on_configure)

    load_schedule()
    root.mainloop()
