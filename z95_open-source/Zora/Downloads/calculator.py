import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        result = eval(entry.get())
        result_label.config(text="Result: " + str(result))
    except Exception as e:
        messagebox.showerror("Error", "Invalid input: " + str(e))

# Create the main window
window = tk.Tk()
window.title("Calculator")

# Entry widget for input
entry = tk.Entry(window, width=20, font=("Arial", 14))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Buttons for digits and operators
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row, col = 1, 0
for button in buttons:
    if button == '=':
        tk.Button(window, text=button, width=5, font=("Arial", 14), command=calculate).grid(row=row, column=col, padx=5, pady=5)
    else:
        tk.Button(window, text=button, width=5, font=("Arial", 14), command=lambda x=button: entry.insert(tk.END, x)).grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Label to display result
result_label = tk.Label(window, text="Result: ", font=("Arial", 14))
result_label.grid(row=row, column=0, columnspan=4, padx=10, pady=10)

# Run the main event loop
window.mainloop()
