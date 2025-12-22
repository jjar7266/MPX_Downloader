"""
MPX Downloader
--------------

A simple Tkinter-based GUI application for downloading YouTube content
as MP3 audio or MP4 video. This app uses the standalone yt-dlp.exe binary
(bundled with the project) and saves files into organized download folders.

Features:
- MP3 or MP4 mode selection
- URL input with right-click paste support
- Download progress via status label
- Built-in yt-dlp updater
- Clean folder structure for saved files

Created by: Jose Ruiz

TODO: 
- Implement real MP3 download logic (subprocess + safe filenames)
- Implement real MP4 download logic
- Add error handling for network failures
- Add "Open downloads folder" button
- Add progress or activity indicator
- Add version number and update notes
"""
# Import modules

import tkinter as tk            #  GUI framework
from tkinter import messagebox  #  Popup dialogs 
import subprocess               #  Run yt-dlp.exe
import os                       #  Folder creation and fle paths


def ensure_folders():
    """
    Create the required download directories if they don't exist.
    This keeps MP3 and MP4 downloads organized.
    """
    os.makedirs("downloads/mp3", exist_ok= True)
    os.makedirs("downloads/mp4", exist_ok= True)

def main():
    # Make sure the download folders exist before the GUI loads

    ensure_folders()

    # Create the main application window

    root = tk.Tk()
    root.title("MPX Downloader")
    root.geometry("450x250")       # Fixed window size

    root.resizable(False, False)   # Prevent resizing for clean layout

    # Title Label

    title_label = tk.Label(
        root,
        text = "MPX Downloader",
        font = ("Arial", 16, "bold")
    )
    title_label.pack(pady = 10)

    # Mode Selector (MP3 / MP4)

    mode_var = tk.StringVar(value = "mp3")  # Default mode is MP3

    mode_frame = tk.Frame(root)             # Holds the radio buttons side-by-side

    mode_frame.pack()

    mp3_radio = tk.Radiobutton(
        mode_frame,
        text = "MP3",
        variable = mode_var,
        value = "mp3"
    )
    mp3_radio.pack(side = "left", padx = 10)

    mp4_radio = tk.Radiobutton(
        mode_frame,
        text = "MP4",
        variable = mode_var,
        value = "mp4"
    )
    mp4_radio.pack(side = "left", padx = 10)

    # URL Label + Entry Box

    url_label = tk.Label(root, text = "YouTube URL:")
    url_label.pack(pady = (15, 5))

    url_entry = tk.Entry(root, width = 50)
    url_entry.pack()
    url_entry.focus_set()  # Cursor starts here when the app opens


    # Right-click Paste Menu

    context_menu = tk.Menu(root, tearoff = 0)
    context_menu.add_command(
        label = "Paste",
        command = lambda: url_entry.insert(tk.END, root.clipboard_get())
    )

    # Bind right-click to show the paste menu

    url_entry.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))

    # Start the Tkinter event loop (required for the window to stay open)

    root.mainloop()









































if __name__ == "__main__":
    main()
