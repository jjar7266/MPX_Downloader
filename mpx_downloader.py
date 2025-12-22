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

# Status label helper    

def set_status(status_label, text, delay = 3000, reset_to = "Ready"):
    """  
    Update the status label with text, then clear if after 'delay' ms.
    Default delay is 3000 ms (3 seconds).
    """
    status_label.config(text = text)
    status_label.after(delay, lambda: status_label.config(text = reset_to))

def handle_download(mode_var, url_entry, status_label):
    """
    Decide whether to download as MP3 or MP4 based on the selected mode.
    For now, this is a stub that just updates the status label.
    """
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a YouTube URL before downloading.")
        return
    
    mode = mode_var.get()

    # Clear the input box immediately after a valid request
    url_entry.delete(0, tk.END)
    url_entry.focus_set()

    if mode == "mp3":
        set_status(status_label, "Download requested: MP3 (stub, not implemented yet)")
        # TODO: Call real MP3 download function here

    else:
        set_status(status_label, "Download requested: MP4 (stub, not implemented yet)")
        # TODO: Call real MP4 download function here

def handle_update_yt_dlp(status_label):
    """
    Stub for updating the yt-dlp.exe binary.
    For now, it just shows a message and updates the status label.  
    """
    messagebox.showinfo("Update yt-dlp", "yt-dlp update functionality is not implemented yet.")
    set_status(status_label, "yt-dlp update requested (stub)")

# Main GUI

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

    # Buttons (Download / Update)

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady = 15)

    download_button = tk.Button(
        buttons_frame,
        text = "Download",
        width = 12,
        command = lambda: handle_download(mode_var, url_entry, status_label)
    )
    download_button.pack(side = "left", padx = 10)

    update_button = tk.Button(
        buttons_frame,
        text = "Update yt-dlp",
        width = 12,
        command = lambda: handle_update_yt_dlp(status_label)
    )
    update_button.pack(side = "left", padx = 10)

    # Status Label

    status_label = tk.Label(root, text = "Ready", anchor = "w")
    status_label.pack(fill = "x", padx = 10, pady = (5, 0))









    # Start the Tkinter event loop (required for the window to stay open)

    root.mainloop()









































if __name__ == "__main__":
    main()
