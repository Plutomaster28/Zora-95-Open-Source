import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import pygame


def show_main_gui():
  # Launch the main.py script using subprocess
  subprocess.Popen(["python", "login.py"])


# Create a splash screen
splash_screen = tk.Tk()
splash_screen.overrideredirect(True)  # Remove window decorations
splash_screen.title("Startup Screen")
splash_screen.geometry("800x600")

pygame.mixer.init()


def play_startup_music():
  # Load and play startup music
  pygame.mixer.music.load("Sys404/startup_sound.wav")
  pygame.mixer.music.play()


# Load the logo image
image = Image.open("Sys404/logo.png")
image = image.resize(
    (800, 600))  # Resize image to fit the window with antialiasing
logo_image = ImageTk.PhotoImage(image)

# Add your splash screen components here
canvas = tk.Canvas(splash_screen, width=800, height=600)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=logo_image)

# Withdraw the splash screen after 3 seconds and show the main GUI
splash_screen.after(7000, splash_screen.withdraw)
splash_screen.after(7000, show_main_gui)

play_startup_music()

splash_screen.mainloop()
