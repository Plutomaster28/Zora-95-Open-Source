import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import platform
import os
import subprocess
import time
from PIL import Image, ImageTk
from tkinter import messagebox
import vlc
import pygame
import imageio
import time
import calendar

internet_explorer_window = None
player = None
opened_windows = []


def open_and_run_program():
  root = tk.Tk()
  root.withdraw()  # Hide the main window

  # Create a file selection dialog
  file_path = filedialog.asksaveasfilename(title="Select File Location",
                                           filetypes=[("Python files", "*.py"),
                                                      ("C++ files", "*.cpp"),
                                                      ("C files", "*.c"),
                                                      ("All files", "*.*")],
                                           defaultextension=".py")

  if file_path:
    print("File selected:", file_path)

    # Check if the selected file is a Python, C++, or C file
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == ".py":
      # Open and run the selected Python file
      subprocess.run(["python", file_path])
    elif file_extension == ".cpp":
      # Compile and run the selected C++ file
      subprocess.run(["g++", file_path, "-o", "output.exe"])
      subprocess.run(["./output.exe"])
    elif file_extension == ".c":
      # Compile and run the selected C file
      subprocess.run(["gcc", file_path, "-o", "output"])
      subprocess.run(["./output"])
    else:
      print("Unsupported file type.")
  else:
    print("File selection canceled.")


def open_text_editor():

  def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
      with open(file_path, "r") as file:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, file.read())
        status_label.config(text=f"Opened file: {file_path}")

  def save_file():
    file_path = filedialog.asksaveasfilename(filetypes=[("Text files",
                                                         "*.txt")])
    if file_path:
      with open(file_path, "w") as file:
        file.write(text_area.get(1.0, tk.END))
        status_label.config(text=f"Saved file: {file_path}")

  text_editor_window = tk.Toplevel()
  text_editor_window.title("Text Editor")
  text_editor_window.geometry("600x400")

  text_area = tk.Text(text_editor_window)
  text_area.pack(expand=True, fill="both")

  menu_bar = tk.Menu(text_editor_window)
  file_menu = tk.Menu(menu_bar, tearoff=0)
  file_menu.add_command(label="Open", command=open_file)
  file_menu.add_command(label="Save", command=save_file)
  file_menu.add_separator()
  file_menu.add_command(label="Exit", command=text_editor_window.destroy)
  menu_bar.add_cascade(label="File", menu=file_menu)

  text_editor_window.config(menu=menu_bar)

  status_label = tk.Label(text_editor_window,
                          text="",
                          bd=1,
                          relief=tk.SUNKEN,
                          anchor=tk.W)
  status_label.pack(side=tk.BOTTOM, fill=tk.X)


def start_powershell():

  def display_prompt():
    output_text.insert(tk.END, f"{current_directory}> ")

  def execute_command(event=None):
    command = command_entry.get()
    output_text.insert(tk.END, command + "\n")
    parts = command.split()
    if parts[0] == "cd":
      if len(parts) < 2:
        messagebox.showerror("Error", "Usage: cd <directory>")
      else:
        directory = parts[1]
        if os.path.isdir(directory):
          nonlocal current_directory
          current_directory = directory
          output_text.insert(tk.END, f"Directory changed to '{directory}'.\n")
        else:
          messagebox.showerror("Error", f"Directory '{directory}' not found.")
    elif parts[0] == "create":
      if len(parts) < 2:
        messagebox.showerror("Error", "Usage: create <filename>")
      else:
        filename = parts[1]
        full_path = os.path.join(current_directory, filename)
        with open(full_path, "w") as f:
          pass
        output_text.insert(
            tk.END, f"File '{filename}' created in '{current_directory}'.\n")
    elif parts[0] == "delete":
      if len(parts) < 2:
        messagebox.showerror("Error", "Usage: delete <filename>")
      else:
        filename = parts[1]
        full_path = os.path.join(current_directory, filename)
        if os.path.exists(full_path):
          os.remove(full_path)
          output_text.insert(
              tk.END,
              f"File '{filename}' deleted from '{current_directory}'.\n")
        else:
          messagebox.showerror(
              "Error",
              f"File '{filename}' not found in '{current_directory}'.")
    elif parts[0] == "exit":
      root.destroy()
    else:
      output = os.popen(command).read()
      output_text.insert(tk.END, output)

    display_prompt()
    command_entry.delete(0, tk.END)

  root = tk.Tk()
  root.title("PowerShell")
  root.geometry("600x400")

  current_directory = "Zora"

  # Text area to display output
  output_text = tk.Text(root, wrap="word")
  output_text.pack(fill="both", expand=True)

  # Entry widget to accept commands
  command_entry = tk.Entry(root)
  command_entry.pack(fill="x")
  command_entry.bind(
      "<Return>",
      execute_command)  # Bind Enter key to execute_command function

  display_prompt()


class PaintApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Meisei Paint")

    self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
    self.canvas.pack()

    self.draw_color = "black"
    self.brush_size = 2
    self.setup_menu()

    self.canvas.bind("<B1-Motion>", self.paint)

  def setup_menu(self):
    menu = tk.Menu(self.root)
    self.root.config(menu=menu)

    color_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Colors", menu=color_menu)
    color_menu.add_command(label="Black",
                           command=lambda: self.set_color("black"))
    color_menu.add_command(label="Red", command=lambda: self.set_color("red"))
    color_menu.add_command(label="Green",
                           command=lambda: self.set_color("green"))
    color_menu.add_command(label="Blue",
                           command=lambda: self.set_color("blue"))

    size_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Brush Size", menu=size_menu)
    size_menu.add_command(label="Small",
                          command=lambda: self.set_brush_size(2))
    size_menu.add_command(label="Medium",
                          command=lambda: self.set_brush_size(5))
    size_menu.add_command(label="Large",
                          command=lambda: self.set_brush_size(10))

    clear_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Clear", menu=clear_menu)
    clear_menu.add_command(label="Clear Canvas", command=self.clear_canvas)

  def set_color(self, color):
    self.draw_color = color

  def set_brush_size(self, size):
    self.brush_size = size

  def paint(self, event):
    x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
    x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
    self.canvas.create_oval(x1,
                            y1,
                            x2,
                            y2,
                            fill=self.draw_color,
                            outline=self.draw_color)

  def clear_canvas(self):
    self.canvas.delete("all")


def open_paint_app():
  root = tk.Tk()
  app = PaintApp(root)
  root.mainloop()


def create_music_player():
  root = tk.Tk()
  root.title("Music Player")
  root.geometry("400x300")

  # Create a frame for the file browser
  file_frame = ttk.Frame(root)
  file_frame.pack(pady=10)

  # Create a button to browse files
  browse_button = ttk.Button(file_frame,
                             text="Browse Files",
                             command=browse_files)
  browse_button.pack(side="left", padx=5)

  # Create a button to stop music playback
  stop_button = ttk.Button(file_frame, text="Stop Music", command=stop_music)
  stop_button.pack(side="left", padx=5)


def browse_files():
  file_path = tk.filedialog.askopenfilename(
      filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
  if file_path:
    play_music(file_path)


def stop_music():
  pygame.mixer.music.stop()


def play_music(file_path):
  pygame.mixer.init()
  pygame.mixer.music.load(file_path)
  pygame.mixer.music.play()


def play_media(file_path):
  _, file_extension = os.path.splitext(file_path)
  if file_extension.lower() in ['.mp4', '.avi', '.mkv']:
    play_video(file_path)
  elif file_extension.lower() in ['.jpg', '.jpeg', '.png']:
    show_image(file_path)


def play_video(file_path):
  video = imageio.get_reader(file_path)
  root = tk.Toplevel()
  root.title("Video Player")
  root.geometry("800x600")

  canvas = tk.Canvas(root, width=800, height=600)
  canvas.pack()

  # Play the video
  for frame_data in video.iter_data():
    frame_image = ImageTk.PhotoImage(Image.fromarray(frame_data))
    canvas.create_image(0, 0, anchor=tk.NW, image=frame_image)
    root.update_idletasks()
    root.update()

  # Load and play audio
  audio_path = file_path  # Assuming audio is embedded in the video file
  pygame.mixer.init()
  pygame.mixer.music.load(audio_path)
  pygame.mixer.music.play()

  root.mainloop()


def show_image(file_path):
  root = tk.Toplevel()
  root.title("Image Viewer")

  image = Image.open(file_path)
  image = image.resize((800, 600), Image.ANTIALIAS)
  photo = ImageTk.PhotoImage(image)

  label = tk.Label(root, image=photo)
  label.image = photo
  label.pack()

  root.mainloop()


def stop_media(root):
  pygame.mixer.music.stop()
  root.destroy()


def browse_files_media_center(root):
  file_path = filedialog.askopenfilename()
  if file_path:
    play_media(file_path)


def create_media_center():
  root = tk.Tk()
  root.title("Media Center")
  root.geometry("600x400")

  control_frame = ttk.Frame(root)
  control_frame.pack(pady=5)

  browse_button = ttk.Button(control_frame,
                             text="Browse Files",
                             command=lambda: browse_files_media_center(root))
  browse_button.pack(side="left", padx=5)

  stop_button = ttk.Button(control_frame,
                           text="Stop Media",
                           command=lambda: stop_media(root))
  stop_button.pack(side="left", padx=5)

  root.mainloop()


def open_webview():
  root.geometry("800x600")
  subprocess.Popen(["firefox"])


def open_file_explorer():
  file_explorer_window = tk.Toplevel(root)
  file_explorer_window.title("File Explorer")
  file_explorer_window.geometry("600x400")  # Adjust the size as needed

  # Create a Treeview widget for the file explorer
  tree = ttk.Treeview(file_explorer_window,
                      columns=("Type"),
                      selectmode="browse")
  tree.heading("#0", text="File Explorer")
  tree.column("#0", width=200)
  tree.heading("Type", text="Type")
  tree.column("Type", width=100)

  # Specify the root directory to explore
  root_directory = "Zora"  # Adjust this according to your actual directory structure

  # Function to populate treeview recursively
  def populate_tree(parent, path):
    for item in os.listdir(path):
      item_path = os.path.join(path, item)
      if os.path.isdir(item_path):
        folder_id = tree.insert(parent, "end", text=item, values=("Folder"))
        populate_tree(folder_id,
                      item_path)  # Recursively populate subdirectories
      else:
        file_type = get_file_type(item)
        tree.insert(parent, "end", text=item, values=(file_type, item_path))

  # Function to determine the type of a file based on its extension
  def get_file_type(file_name):
    ext = file_name.split(".")[-1].lower()
    if ext in ("png", "jpg"):
      return "Image"
    elif ext == "txt":
      return "Text File"
    elif ext in ("mp3", "wav"):
      return "Audio"
    elif ext == "mp4":
      return "Video"
    else:
      return "File"

  # Function to handle double-click event on treeview items
  def item_double_click(event):
    item_id = tree.selection()[0]
    item_type = tree.item(item_id)["values"][0]
    item_path = tree.item(item_id)["values"][1]
    if item_type == "Folder":
      # Open the folder
      new_path = os.path.join(root_directory, item_path)
      tree.delete(
          tree.get_children(item_id))  # Clear children before repopulating
      populate_tree(item_id, new_path)
    else:
      # Open the file
      open_file(item_path)

  # Function to open files
  def open_file(file_path):
    file_type = get_file_type(file_path)
    if file_type == "Text File":
      display_text_file(file_path)
    elif file_type == "Image":
      display_image(file_path)
    elif file_type == "Audio":
      play_audio(file_path)
    elif file_type == "Video":
      play_video(file_path)
    else:
      print(f"Opening file: {file_path}")

  # Function to display text file content
  def display_text_file(file_path):
    text_window = tk.Toplevel(root)
    text_window.title("Text Viewer")
    text_window.geometry("600x400")
    with open(file_path, "r") as file:
      content = file.read()
    text_widget = tk.Text(text_window)
    text_widget.insert(tk.END, content)
    text_widget.pack(expand=True, fill="both")

  # Function to display image
  def display_image(file_path):
    image_window = tk.Toplevel(root)
    image_window.title("Image Viewer")
    image_window.geometry("600x400")
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(image_window, image=photo)
    label.image = photo
    label.pack(expand=True, fill="both")

  # Function to play audio
  def play_audio(file_path):
    global player
    if player is not None:
      player.stop()
    player = vlc.MediaPlayer(file_path)
    player.play()

  # Function to play video
  def play_video(file_path):
    global player
    if player is not None:
      player.stop()
    player = vlc.MediaPlayer(file_path)
    player.set_hwnd(int(file_explorer_window.wm_frame(), 16))
    player.play()

  # Bind double-click event to treeview items
  tree.bind("<Double-1>", item_double_click)

  # Call the function to populate treeview
  populate_tree("", root_directory)

  # Pack the Treeview widget
  tree.pack(expand=True, fill="both")


def open_my_computer():
  my_computer_window = tk.Toplevel(root)
  my_computer_window.title("My Computer")
  my_computer_window.geometry("600x400")

  def open_specs():
    specs_window = tk.Toplevel(my_computer_window)
    specs_window.title("System Specs")
    specs_window.geometry("400x300")

    system_info_label = tk.Label(specs_window, text="System Information:")
    system_info_label.pack()
    system_info_text = tk.Text(specs_window, height=10, width=50)
    system_info_text.insert(
        tk.END,
        f"Operating System: {platform.system()} {platform.release()}\n")
    system_info_text.insert(tk.END, f"Processor: {platform.processor()}\n")
    system_info_text.insert(
        tk.END,
        f"Total Memory: {round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.0 ** 3), 2)} GB\n"
    )
    system_info_text.insert(
        tk.END,
        f"Available Memory: {round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES') / (1024.0 ** 3), 2)} GB\n"
    )
    system_info_text.pack()

  def open_control_panel():
    control_panel_window = tk.Toplevel(my_computer_window)
    control_panel_window.title("Control Panel")
    control_panel_window.geometry("400x300")

    settings_button = tk.Button(control_panel_window,
                                text="Settings",
                                command=open_settings)
    settings_button.pack(pady=10)

  def open_settings():

    def change_clock():
      new_time = new_time_entry.get()
      # Update the clock label with the new time
      clock_label.config(text=new_time)

    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    settings_window.geometry("500x300")

    # Add wallpaper setting section
    wallpaper_setting_frame = tk.Frame(settings_window)
    wallpaper_setting_frame.pack(pady=20)

    tk.Label(wallpaper_setting_frame,
             text="Change Wallpaper:",
             font=("Arial", 12, "bold")).grid(row=0,
                                              column=0,
                                              padx=10,
                                              pady=10)
    select_button = tk.Button(wallpaper_setting_frame,
                              text="Select Wallpaper",
                              command=select_wallpaper)
    select_button.grid(row=0, column=1, padx=10, pady=10)

    # Add clock setting section
    clock_setting_frame = tk.Frame(settings_window)
    clock_setting_frame.pack(pady=20)

    tk.Label(clock_setting_frame,
             text="Change Clock:",
             font=("Arial", 12, "bold")).grid(row=0,
                                              column=0,
                                              padx=10,
                                              pady=10)
    new_time_entry = tk.Entry(clock_setting_frame, width=20)
    new_time_entry.grid(row=0, column=1, padx=10, pady=10)
    change_button = tk.Button(clock_setting_frame,
                              text="Change",
                              command=change_clock)
    change_button.grid(row=0, column=2, padx=10, pady=10)

  def select_wallpaper():
    # Open file dialog to select wallpaper
    selected_file = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.png;*.jpeg"), ("All files",
                                                           "*.*")])
    if selected_file:
      # Apply the selected wallpaper as the background
      try:
        # Open the selected image file
        image = Image.open(selected_file)
        # Resize the image to fit the window size
        image = image.resize((root.winfo_width(), root.winfo_height()))
        # Convert the image to a Tkinter-compatible format
        photo = ImageTk.PhotoImage(image)
        # Set the image as the background of the root window
        root.background = photo  # Store a reference to avoid garbage collection
        root.configure(
            bg="white"
        )  # Set background to white to avoid default tkinter background

        # Create a label for the wallpaper image and place it behind other elements
        background_label = tk.Label(root, image=photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.lower()  # Lower the label to be behind other elements

        # Make taskbar background transparent
        taskbar.configure(bg="")

        # Make menu frame background transparent
        menu_frame.configure(bg="")

        # Make clock frame background transparent
        clock_frame.configure(bg="")

        # Make icons and text labels background transparent
        for label in root.winfo_children():
          if isinstance(label, tk.Label):
            label.configure(bg="")
      except Exception as e:
        print("Error applying wallpaper:", e)

  def save_settings(wallpaper, time):
    # Add logic to save wallpaper and time settings
    print("Wallpaper:", wallpaper)
    print("Time:", time)

  specs_button = tk.Button(my_computer_window,
                           text="System Specs",
                           command=open_specs)
  specs_button.pack(pady=10)

  control_panel_button = tk.Button(my_computer_window,
                                   text="Control Panel",
                                   command=open_control_panel)
  control_panel_button.pack(pady=10)


def open_settings():

  def change_clock():
    new_time = new_time_entry.get()
    # Update the clock label with the new time
    clock_label.config(text=new_time)

  settings_window = tk.Toplevel()
  settings_window.title("Settings")
  settings_window.geometry("500x300")

  # Add clock setting section
  clock_setting_frame = tk.Frame(settings_window)
  clock_setting_frame.pack(pady=20)

  tk.Label(clock_setting_frame,
           text="Change Clock:",
           font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
  new_time_entry = tk.Entry(clock_setting_frame, width=20)
  new_time_entry.grid(row=0, column=1, padx=10, pady=10)
  change_button = tk.Button(clock_setting_frame,
                            text="Change",
                            command=change_clock)
  change_button.grid(row=0, column=2, padx=10, pady=10)


# Function to handle clock click event
def clock_click(event):
  if not menu_frame.winfo_ismapped():
    menu_frame.place(x=70, y=0)
  else:
    menu_frame.place_forget()


# Main home GUI Below
root = tk.Tk()
root.title("Zora 95")
root.geometry("800x600")

background_color = "#008080"
root.configure(bg=background_color)


def icon_click(icon_name):
  if icon_name == "Documents":
    open_file_explorer()
  elif icon_name == "Internet Explorer":
    open_webview()
  elif icon_name == "My Computer":
    open_my_computer()
  elif icon_name == "Music Player":
    create_music_player()
  elif icon_name == "Video Player":
    create_media_center()
  elif icon_name == "Paint":
    open_paint_app()
  elif icon_name == "Shell":
    start_powershell()
  elif icon_name == "Notepad":
    open_text_editor()
  elif icon_name == "Wizard":
    open_and_run_program()


icons = {
    "My Computer": ("Sys404/my_computer.png", 50, 50),
    "Documents": ("Sys404/documents.png", 50, 150),
    "Internet Explorer": ("Sys404/internet_explorer.png", 50, 250),
    "Music Player": ("Sys404/music.png", 50, 50),
    "Video Player": ("Sys404/video.png", 50, -250),
    "Paint": ("Sys404/paint.png", 150, -450),
    "Shell": ("Sys404/shell.png", 750, -550),
    "Notepad": ("Sys404/notepad.png", 750, -550),
    "Wizard": ("Sys404/program_wizard.png", 750, -550),
}

icon_spacing = 100  # Adjust the spacing between icons
for index, (icon_name, (image_path, x, y)) in enumerate(icons.items()):
  icon_image = tk.PhotoImage(file=image_path)
  icon_label = tk.Label(root, image=icon_image, bg=background_color)
  icon_label.image = icon_image  # To prevent garbage collection
  icon_label.place(x=x, y=y + index * icon_spacing)
  icon_label.bind("<Button-1>", lambda event, name=icon_name: icon_click(name))

  text_label = tk.Label(root,
                        text=icon_name,
                        bg=background_color,
                        fg="white",
                        font=("Arial", 10))
  text_label.place(x=x +
                   (icon_image.width() - text_label.winfo_reqwidth()) / 2,
                   y=y + icon_image.height() + 10 + index * icon_spacing)

taskbar = tk.Frame(root, bg="gray", height=40)
taskbar.pack(side="bottom", fill="x")

start_button = tk.Button(taskbar, text="Start", width=10)
start_button.pack(side="left", padx=5, pady=5)

# Create a clock frame
clock_frame = tk.Frame(taskbar, bg="gray", height=40)
clock_frame.pack(side="right", padx=10)

# Add clock label to the clock frame
clock_label = tk.Label(clock_frame,
                       text="",
                       bg="gray",
                       fg="white",
                       font=("Arial", 12, "bold"),
                       width=10)
clock_label.pack()

# Add a menu frame above the clock
menu_frame = tk.Frame(root, bg="gray", height=100, width=800)
menu_frame.place(x=70, y=-180)

# Add calendar label to the menu frame
cal = calendar.TextCalendar(calendar.SUNDAY)
calendar_label = tk.Label(menu_frame,
                          text=cal.formatmonth(2024, 4),
                          bg="gray",
                          fg="white")
calendar_label.pack()

# Add a button to open settings
settings_button = tk.Button(menu_frame, text="Settings", command=open_settings)
settings_button.pack(pady=10)


# Update clock function
def update_clock():
  current_time = time.strftime("%I:%M %p")
  clock_label.config(text=current_time)
  clock_label.after(1000, update_clock)  # Update every 1 second


update_clock()  # Start updating the clock

# Bind clock label to click event
clock_label.bind("<Button-1>", clock_click)

root.mainloop()
