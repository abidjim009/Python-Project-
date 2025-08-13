import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ========== Database Setup ==========
conn = sqlite3.connect('quiz_app.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    score INTEGER DEFAULT 0
)
''')
conn.commit()

# ========== Data Structure Questions ==========
QUESTIONS = [
    ("Which data structure uses LIFO principle?", ["Queue", "Stack", "Array", "Linked List"], "Stack"),
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
        self.master.title("Quiz Application")
        self.master.geometry("600x500")
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

    def register_user(self):
        uname = self.username_entry.get()
        pwd = self.password_entry.get()
        email = self.email_entry.get()

        if not (uname and pwd and email):
            messagebox.showerror("Error", "All fields required!")
            return

        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                           (uname, pwd, email))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    def login_user(self):
        uname = self.username_entry.get()
        pwd = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pwd))
        user = cursor.fetchone()

        if user:
            self.current_user = User(user[1], user[3], user[4])
            self.create_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def create_dashboard(self):
        self.clear_screen()

        frame = tk.Frame(self.master, bg="#e8f0fe")
        frame.pack(pady=20)

        tk.Label(frame, text=f"Welcome, {self.current_user.username}", font=("Arial", 22), bg="#e8f0fe").pack(pady=10)

        btn_style = {"font": ("Arial", 14), "width": 22, "pady": 5, "bd": 0}

        tk.Button(frame, text="🎯 Take Quiz", bg="#03a9f4", fg="white", command=self.start_quiz, **btn_style).pack(pady=8)
        tk.Button(frame, text="🏆 View Leaderboard", bg="#ff9800", fg="white", command=self.show_leaderboard, **btn_style).pack(pady=8)
        tk.Button(frame, text="🎓 Generate Certificate", bg="#4caf50", fg="white", command=self.generate_certificate, **btn_style).pack(pady=8)
        tk.Button(frame, text="🚪 Logout", bg="#f44336", fg="white", command=self.create_login_screen, **btn_style).pack(pady=8)

    def start_quiz(self):
        self.clear_screen()
        self.question_index = 0
        self.current_score = 0
        self.show_question()

    def show_question(self):
        if self.question_index >= len(QUESTIONS):
            self.finish_quiz()
            return

        q, options, correct = QUESTIONS[self.question_index]
        self.correct_answer = correct

        tk.Label(self.master, text=f"Q{self.question_index + 1}: {q}", font=("Arial", 16), bg="#e8f0fe", wraplength=500).pack(pady=20)

        self.selected_option = tk.StringVar()

        for opt in options:
            tk.Radiobutton(self.master, text=opt, variable=self.selected_option, value=opt, bg="#e8f0fe",
                           font=("Arial", 12)).pack(anchor="w", padx=50)

        tk.Button(self.master, text="Next", bg="#2196f3", fg="white", font=("Arial", 12), command=self.check_answer).pack(pady=20)

    def check_answer(self):
        selected = self.selected_option.get()
        if selected == self.correct_answer:
            self.current_score += 5

        self.question_index += 1
        self.clear_screen()
        self.show_question()

    def finish_quiz(self):
        cursor.execute("UPDATE users SET score = score + ? WHERE username = ?", (self.current_score, self.current_user.username))
        conn.commit()
        self.current_user.score += self.current_score

        messagebox.showinfo("Quiz Finished", f"You scored {self.current_score} points!")
        self.create_dashboard()

    def show_leaderboard(self):
        self.clear_screen()

        tk.Label(self.master, text="🏆 Top Scorers", font=("Arial", 20), bg="#e8f0fe").pack(pady=20)

        cursor.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 5")
        results = cursor.fetchall()

        for i, (name, score) in enumerate(results):
            tk.Label(self.master, text=f"{i+1}. {name} - {score} points", font=("Arial", 14), bg="#e8f0fe").pack(pady=4)

        tk.Button(self.master, text="Back", bg="#607d8b", fg="white", command=self.create_dashboard).pack(pady=20)

    def generate_certificate(self):
        if self.current_user.score == 0:
            messagebox.showwarning("No Score", "Take a quiz to earn a certificate!")
            return

        cert = f"""
        🎓 Certificate of Completion 🎓\n\n
        This is to certify that {self.current_user.username}
        has successfully completed the quiz session.

        Total Score: {self.current_user.score}
        Date: {datetime.now().strftime('%Y-%m-%d')}
        """
        messagebox.showinfo("Certificate", cert)


# ========== Run App ==========
root = tk.Tk()
app = QuizApp(root)
root.mainloop()