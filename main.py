import tkinter as tk
import random
import time
from threading import Thread

# Game data
choices = ['stone', 'paper', 'scissors']
user_score = 0
computer_score = 0
history = []

# Winner logic
def determine_winner(user, comp):
    global user_score, computer_score
    if user == comp:
        return "Draw"
    elif (user == 'stone' and comp == 'scissors') or \
         (user == 'paper' and comp == 'stone') or \
         (user == 'scissors' and comp == 'paper'):
        user_score += 1
        return "You win!"
    else:
        computer_score += 1
        return "Computer wins!"

# Play logic
def play(user_choice):
    result_label.config(text="Computer is thinking...", fg="cyan")
    window.update()
    time.sleep(0.8)

    comp_choice = random.choice(choices)
    result = determine_winner(user_choice, comp_choice)
    history.append(f"You: {user_choice} | Computer: {comp_choice} → {result}")

    result_label.config(
        text=f"You chose {user_choice}, Computer chose {comp_choice}\nResult: {result}",
        fg="lime" if "You win" in result else "red" if "Computer" in result else "yellow"
    )
    score_label.config(text=f"You: {user_score} | Computer: {computer_score}")
    history_text.delete("1.0", tk.END)
    history_text.insert(tk.END, "\n".join(history[-10:]))

def threaded_play(choice):
    Thread(target=play, args=(choice,)).start()

def reset_game():
    global user_score, computer_score, history
    user_score = 0
    computer_score = 0
    history = []
    result_label.config(text="Game reset. Choose your move!", fg="white")
    score_label.config(text="You: 0 | Computer: 0")
    history_text.delete("1.0", tk.END)

def exit_game():
    window.destroy()

# GUI setup
window = tk.Tk()
window.title("Stone Paper Scissors")
window.geometry("520x440")
window.config(bg="#1e1e2f")  # Dark background
window.resizable(False, False)

# Styling function
def create_button(parent, text, command, bg="#444", fg="white"):
    return tk.Button(parent, text=text, font=("Arial", 12, "bold"),
                     bg=bg, fg=fg, activebackground="#666", activeforeground="white",
                     width=12, command=command)

# Title
tk.Label(window, text="Stone Paper Scissors", font=("Helvetica", 18, "bold"),
         fg="white", bg="#1e1e2f").pack(pady=10)

score_label = tk.Label(window, text="You: 0 | Computer: 0", font=("Helvetica", 13),
                       fg="white", bg="#1e1e2f")
score_label.pack()

result_label = tk.Label(window, text="Start the game!", font=("Helvetica", 12),
                        fg="white", bg="#1e1e2f", pady=10)
result_label.pack()

# Game buttons
button_frame = tk.Frame(window, bg="#1e1e2f")
button_frame.pack(pady=15)

for choice in choices:
    create_button(button_frame, choice.capitalize(), lambda c=choice: threaded_play(c),
                  bg="#2a2a3d").pack(side=tk.LEFT, padx=10)

# History
tk.Label(window, text="Game History (last 10):", font=("Helvetica", 10),
         fg="white", bg="#1e1e2f").pack()
history_text = tk.Text(window, height=6, width=55, bg="#2a2a3d", fg="white")
history_text.pack(pady=5)

# Control buttons
control_frame = tk.Frame(window, bg="#1e1e2f")
control_frame.pack(pady=10)

create_button(control_frame, "Reset", reset_game, bg="#444").pack(side=tk.LEFT, padx=10)
create_button(control_frame, "Exit", exit_game, bg="#d9534f").pack(side=tk.RIGHT, padx=10)

window.mainloop()
