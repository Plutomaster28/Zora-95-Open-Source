import tkinter as tk
from tkinter import messagebox
import subprocess


def login():

  def validate():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password match
    if username == "Miya" and password == "admin":
      messagebox.showinfo("Success", "You have successfully logged in!")
      login_window.destroy()  # Close the login window
      subprocess.Popen(["python", "home.py"])
    else:
      messagebox.showerror("Error", "Invalid username or password")

  # Create the login window
  login_window = tk.Tk()
  login_window.title("Login")
  login_window.geometry("320x240")
  login_window.resizable(False, False)
  login_window.configure(bg="#008080")  # Windows 95 background color

  # Username label and entry
  username_label = tk.Label(login_window, text="Username:",
                            bg="#008080")  # Windows 95 background color
  username_label.place(relx=0.1, rely=0.3)
  username_entry = tk.Entry(login_window)
  username_entry.place(relx=0.4, rely=0.3)

  # Password label and entry
  password_label = tk.Label(login_window, text="Password:",
                            bg="#008080")  # Windows 95 background color
  password_label.place(relx=0.1, rely=0.45)
  password_entry = tk.Entry(login_window, show="*")
  password_entry.place(relx=0.4, rely=0.45)

  # Sign-in button
  sign_in_button = tk.Button(login_window, text="Login", command=validate)
  sign_in_button.place(relx=0.35, rely=0.6)

  login_window.mainloop()


login()
