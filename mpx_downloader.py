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

import tkinter as tk
from tkinter import messagebox
import subprocess
import os


def ensure_folders():
    os.makedirs("downloads/mp3", exist_ok= True)
    os.makedirs("downloads/mp4", exist_ok= True)

def main():
    ensure_folders()

    root = tk.Tk()
    root.title("MPX Downloader")
    root.geometry("450x250")
    root.resizable(False, False)

    title_label = tk.Label(
        root,
        text = "MPX Downloader",
        font = ("Arial", 16, "bold")
    )
    title_label.pack(pady = 10)

    mode_var = tk.StringVar(value = "mp3")

    mode_frame = tk.Frame(root)
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
    


















    root.mainloop()









































if __name__ == "__main__":
    main()
