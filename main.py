import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user

current_user_id = None

def open_schedule_window(user_id):
    global current_user_id
    current_user_id = user_id

    login_win.destroy()

    from scheduler_ui import open_scheduler_ui
    open_scheduler_ui(user_id)

def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    user_id = login_user(username, password)
    if user_id:
        messagebox.showinfo("Success", f"Welcome {username}!")
        open_schedule_window(user_id)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")   

def handle_register():
    username = username_entry.get()
    password = password_entry.get()

    if register_user(username, password):
        messagebox.showinfo("Success", "Registered successfully! You can now log in.")
    else:
        messagebox.showerror("Register Failed", "Username might already exist.")

login_win = tk.Tk()
login_win.title("Daily Scheduler - Login/Register")
login_win.geometry("300x200")

tk.Label(login_win, text="Username").pack()
username_entry = tk.Entry(login_win)
username_entry.pack()

tk.Label(login_win, text="Password").pack()
password_entry = tk.Entry(login_win, show="*")
password_entry.pack()

tk.Button(login_win, text="Login", command=handle_login).pack(pady=5)
tk.Button(login_win, text="Register", command=handle_register).pack()

def restart_login():
    global login_win
    login_win = tk.Tk()
    login_win.title("Daily Scheduler - Login/Register")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Username").pack()
    global username_entry
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password").pack()
    global password_entry
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    tk.Button(login_win, text="Login", command=handle_login).pack(pady=5)
    tk.Button(login_win, text="Register", command=handle_register).pack()

    login_win.mainloop()


login_win.mainloop()