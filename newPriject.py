import tkinter as tk
from time import strftime

# Create the main window
root = tk.Tk()
root.title("Digital Clock")

# Create and pack the label
label = tk.Label(root, font=('calibri', 50, 'bold'), background='yellow', foreground='black')
label.pack(anchor='center')

# Define the clock update function
def time():
    string = strftime('%H:%M:%S %p \n %D')
    label.config(text=string)
    label.after(1000, time)

# Start the clock
time()

# Run the Tkinter event loop
root.mainloop()
