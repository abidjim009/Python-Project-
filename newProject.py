import tkinter as tk
from tkinter import messagebox

# Global game variables
current_player = "Ayesha"
winner = False

def check_winner():
    global winner
    winning_combos = [
        [0,1,2],[3,4,5],[6,7,8],   # rows
        [0,3,6],[1,4,7],[2,5,8],   # columns
        [0,4,8],[2,4,6]            # diagonals
    ]
    for combo in winning_combos:
        if (buttons[combo[0]]['text'] == buttons[combo[1]]['text'] == buttons[combo[2]]['text']) and buttons[combo[0]]['text'] != "":
            winner = True
            for index in combo:
                buttons[index].config(bg='green')
            messagebox.showinfo("Game Over", f"{buttons[combo[0]]['text']} wins!")
            reset_game()
            return
    # Check for draw
    if all(button['text'] != "" for button in buttons) and not winner:
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_game()

def button_click(index):
    global current_player, winner
    if buttons[index]['text'] == '' and not winner:
        buttons[index]['text'] = current_player
        check_winner()
        if not winner:
            toggle_player()

def toggle_player():
    global current_player
    current_player = "Jim" if current_player == "Ayesha" else "Ayesha"
    label.config(text=f"{current_player}'s turn")

def reset_game():
    global winner, current_player
    winner = False
    current_player = "Ayesha"
    for button in buttons:
        button.config(text='', bg='SystemButtonFace')
    label.config(text=f"{current_player}'s turn")

# Set up the main window
root = tk.Tk()
root.title("Tic Tac Toe (Jim vs. Ayesha)")

buttons = [tk.Button(root, text="", font=('Arial', 24), width=5, height=2,
                     command=lambda i=i: button_click(i)) for i in range(9)]

for i, button in enumerate(buttons):
    button.grid(row=i//3, column=i%3)

label = tk.Label(root, text=f"{current_player}'s turn", font=('Arial', 16))
label.grid(row=3, column=0, columnspan=3)

root.mainloop()
