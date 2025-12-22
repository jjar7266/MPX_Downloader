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
import os                       #  Folder creation and file paths
import threading                #  Run downloads in a background thread so GUI stays responsive 

# ---------------------------------------------------------
# Ensure download folders exist before the GUI loads
# ---------------------------------------------------------
def ensure_folders():
    """Create required download directories."""
    os.makedirs("downloads/mp3", exist_ok=True)
    os.makedirs("downloads/mp4", exist_ok=True)


# ---------------------------------------------------------
# Status label helper — updates the label text and resets it
# ---------------------------------------------------------
def set_status(status_label, text, delay=3000, reset_to="Ready"):
    """
    Update the status label with text, then reset after delay.
    delay is in milliseconds (default 3 seconds).
    """
    status_label.config(text=text)
    status_label.after(delay, lambda: status_label.config(text=reset_to))


# ---------------------------------------------------------
# Thread-safe wrapper for updating Tkinter widgets
# Tkinter CANNOT be updated from background threads directly.
# This schedules the update on the main GUI thread.
# ---------------------------------------------------------
def thread_safe_status(root, status_label, text, delay=3000, reset_to="Ready"):
    """Safely update Tkinter widgets from a background thread."""
    root.after(0, lambda: set_status(status_label, text, delay, reset_to))


# ---------------------------------------------------------
# MP3 Download Logic (runs inside a background thread)
# ---------------------------------------------------------
def download_mp3(url, status_label, root):
    """
    Download a YouTube URL as MP3 using yt-dlp.exe.
    - Runs in a background thread.
    - All GUI updates routed through thread_safe_status().
    """

    # Long-running task → don't auto-reset the status quickly
    thread_safe_status(root, status_label, "Downloading MP3...", delay=999999)

    # Build absolute path to yt-dlp.exe (guaranteed to work regardless of cwd)
    yt_dlp_path = os.path.join(os.path.dirname(__file__), "yt-dlp.exe")

    # yt-dlp command for MP3 extraction
    command = [
        yt_dlp_path,
        "-x", "--audio-format", "mp3",
        "-o", "downloads/mp3/%(title)s.%(ext)s",
        url
    ]

    try:
        # Run yt-dlp and capture output for error reporting
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        # Check exit code
        if result.returncode == 0:
            thread_safe_status(root, status_label, "MP3 download complete!")
        else:
            thread_safe_status(root, status_label, "Error during MP3 download")
            # Show error dialog safely on main thread
            root.after(0, lambda: messagebox.showerror("Download Error", result.stderr))

    except Exception as e:
        # Python-side error (not yt-dlp)
        thread_safe_status(root, status_label, "Unexpected error")
        root.after(0, lambda: messagebox.showerror("Error", str(e)))


# ---------------------------------------------------------
# Handle Download Button Click
# ---------------------------------------------------------
def handle_download(mode_var, url_entry, status_label, root):
    """
    Validate URL, clear input, and dispatch to MP3/MP4 download.
    MP3 downloads run in a background thread to keep GUI responsive.
    """

    url = url_entry.get().strip()

    # Validate input
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a YouTube URL before downloading.")
        return

    mode = mode_var.get()

    # Clear input box and refocus
    url_entry.delete(0, tk.END)
    url_entry.focus_set()

    # MP3 mode
    if mode == "mp3":
        threading.Thread(
            target=download_mp3,
            args=(url, status_label, root),
            daemon=True  # Thread won't block app exit
        ).start()

    # MP4 mode (not implemented yet)
    else:
        thread_safe_status(root, status_label, "Download requested: MP4 (not implemented yet)")


# ---------------------------------------------------------
# Handle yt-dlp Update Button
# ---------------------------------------------------------
def handle_update_yt_dlp(status_label, root):
    """
    Stub for updating yt-dlp.exe.
    Currently just shows a message and updates status.
    """
    root.after(0, lambda: messagebox.showinfo("Update yt-dlp", "yt-dlp update functionality is not implemented yet."))
    thread_safe_status(root, status_label, "yt-dlp update requested (stub)")


# ---------------------------------------------------------
# Main GUI Setup
# ---------------------------------------------------------
def main():
    # Ensure folder structure exists
    ensure_folders()

    # Create main window
    root = tk.Tk()
    root.title("MPX Downloader")
    root.geometry("450x250")
    root.resizable(False, False)

    # Title label
    title_label = tk.Label(root, text="MPX Downloader", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Mode selector (MP3 / MP4)
    mode_var = tk.StringVar(value="mp3")
    mode_frame = tk.Frame(root)
    mode_frame.pack()

    tk.Radiobutton(mode_frame, text="MP3", variable=mode_var, value="mp3").pack(side="left", padx=10)
    tk.Radiobutton(mode_frame, text="MP4", variable=mode_var, value="mp4").pack(side="left", padx=10)

    # URL label + entry box
    url_label = tk.Label(root, text="YouTube URL:")
    url_label.pack(pady=(15, 5))

    url_entry = tk.Entry(root, width=50)
    url_entry.pack()
    url_entry.focus_set()

    # Right-click paste menu
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Paste", command=lambda: url_entry.insert(tk.END, root.clipboard_get()))
    url_entry.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))

    # Status label (created BEFORE buttons so callbacks can reference it)
    status_label = tk.Label(root, text="Ready", anchor="w")
    status_label.pack(fill="x", padx=10, pady=(5, 0))

    # Buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=15)

    # Download button
    tk.Button(
        buttons_frame,
        text="Download",
        width=12,
        command=lambda: handle_download(mode_var, url_entry, status_label, root)
    ).pack(side="left", padx=10)

    # Update yt-dlp button
    tk.Button(
        buttons_frame,
        text="Update yt-dlp",
        width=12,
        command=lambda: handle_update_yt_dlp(status_label, root)
    ).pack(side="left", padx=10)

    # Start Tkinter event loop
    root.mainloop()


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    main()