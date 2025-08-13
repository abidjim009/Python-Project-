import tkinter as tk
from tkinter import messagebox

# Global expression holder
expression = ""

# Function to update expression
def press(num):
    global expression
    expression += str(num)
    input_text.set(expression)

# Function to evaluate final result
def equalpress():
    global expression
    try:
        result = str(eval(expression.replace("×", "*").replace("÷", "/")))
        input_text.set("Result: " + result)
        expression = ""
    except ZeroDivisionError:
        input_text.set("Error: Divide by 0")
        expression = ""
    except:
        input_text.set("Error")
        expression = ""

# Function to clear input
def clear():
    global expression
    expression = ""
    input_text.set("")

# Create GUI
root = tk.Tk()
root.title("🧮 Smart Button Calculator")
root.geometry("360x500")
root.config(bg="#f0f8ff")
root.resizable(False, False)

# Center window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (360 / 2))
y = int((screen_height / 2) - (500 / 2))
root.geometry(f"360x500+{x}+{y}")

input_text = tk.StringVar()

# Display screen
entry_frame = tk.Frame(root, bg="#f0f8ff")
entry_frame.pack(pady=20)

input_field = tk.Entry(entry_frame, font=('Helvetica', 18), textvariable=input_text,
                       width=25, bd=2, relief="sunken", justify="right")
input_field.grid(row=0, column=0, ipady=10)

# Button frame
btn_frame = tk.Frame(root, bg="#f0f8ff")
btn_frame.pack()

# Styling dictionary (font removed to avoid duplication error)
btn_style = {
    "bd": 0,
    "bg": "#87cefa",
    "fg": "black",
    "width": 7,
    "height": 2
}

# Button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
    ('=', 5, 0, 4)
]

# Create buttons dynamically
for (text, row, col, colspan) in [(*btn, 1) if len(btn) == 3 else btn for btn in buttons]:
    if text == '=':
        b = tk.Button(btn_frame, text=text, bg="#4682b4", fg="white", font=('Helvetica', 14, 'bold'),
                      width=32, height=2, command=equalpress)
    elif text == 'C':
        b = tk.Button(btn_frame, text=text, bg="#ff6961", fg="white", font=('Helvetica', 14, 'bold'),
                      command=clear, **btn_style)
    else:
        b = tk.Button(btn_frame, text=text, command=lambda t=text: press(t), font=('Helvetica', 14), **btn_style)
    b.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5)

# Footer
tk.Label(root, text="Created by You ❤️", bg="#f0f8ff", font=("Helvetica", 9, "italic"), fg="#999").pack(side="bottom", pady=5)

# Run the GUI loop
root.mainloop()
