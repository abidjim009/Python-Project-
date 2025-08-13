import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ========== Database Setup ==========`
conn = sqlite3.connect('quiz_app.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    score INTEGER DEFAULT 0
)
''')

conn.commit()

# ========== Data Structure Questions ==========
questions = [
    ("Which data structure user LIFO principle?", ["Queue", "Stack", "Array", "Linked List"], "Stack"),
    ("Which data structure is used for BFS traversal?", ["Stack", "Queue", "Heap", "Tree"], "Queue"),
    ("What is the time complexity of binary search?", ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "O(log n)"),
    ("Which structure is ideal for implementing recursion?", ["Queue", "Heap", "Stack", "Graph"], "Stack"),
    ("Which tree is a self-balancing binary search tree?", ["AVL Tree", "Binary Tree", "B Tree", "Red Black Tree"], "AVL Tree"),

]

# ========== Classes ==========
class User:
    def __init__(self, username, email, score=0):
        self.username = username
        self.email = email
        self.score = score

# ========== GUI ==========
class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.titlae("Quiz Application")
        self.master.geometry("500x300")
        self.master.configure(bg="#e8f0fe")
        self.current_user = None
        self.question_index = 0
        self.current_score = 0
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.master, text="Login or Register", font=("Arial", 20), bg="#e8f0fe").pack(pady=20)

        tk.Label(self.master, text="Username", bg="#e8f0fe").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Password", bg="#e8f0fe").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        tk.Label(self.master, text="Email (for registration)", bg="#e8f0fe").pack()
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack()

        tk.Button(self.master, text="Register", bg="#4caf50", fg="white", command=self.register_user).pack(pady=5)
        tk.Button(self.master, text="Login", bg="#2196f3", fg="white", command=self.login_user).pack(pady=5)

         

    