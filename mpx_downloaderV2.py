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
"""

# Import modules
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import threading
import requests
from tkinter import filedialog

# Create the default folder path ONCE
default_path = os.path.join(os.path.expanduser("~"), "Downloads")

# ---------------------------------------------------------
# Base directory for bundled resources (Nuitka-friendly)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
yt_dlp_path = os.path.join(BASE_DIR, "yt-dlp.exe")
downloads_root = os.path.join(BASE_DIR, "downloads")

# ---------------------------------------------------------
# Ensure download folders exist before the GUI loads
# ---------------------------------------------------------
def ensure_folders():
    """Create required download directories."""
    os.makedirs(os.path.join(downloads_root, "mp3"), exist_ok=True)
    os.makedirs(os.path.join(downloads_root, "mp4"), exist_ok=True)

# ---------------------------------------------------------
# Status label helper
# ---------------------------------------------------------
def set_status(status_label, text, delay=3000, reset_to="Ready"):
    status_label.config(text=text)
    status_label.after(delay, lambda: status_label.config(text=reset_to))

# ---------------------------------------------------------
# Thread-safe wrapper for Tkinter updates
# ---------------------------------------------------------
def thread_safe_status(root, status_label, text, delay=3000, reset_to="Ready"):
    root.after(0, lambda: set_status(status_label, text, delay, reset_to))

# ---------------------------------------------------------
# MP3 Download Logic
# ---------------------------------------------------------
def download_mp3(url, save_path, status_label, root):
    # Create mp3 subfolder inside the chosen save_path

    mp3_folder = os.path.join(save_path, "mp3")
    os.makedirs(mp3_folder, exist_ok=True)

    # Redirect save_path to the mp3 folder

    save_path = mp3_folder

    # Mark download as active

    root.is_downloading = True

    # Update status label

    thread_safe_status(root, status_label, "Downloading MP3...", delay=999999)

    # Use Nuitka-friendly path
    local_ytdlp = os.path.join(BASE_DIR, "yt-dlp.exe")

    output_template = os.path.join(save_path, "%(title)s_%(autonumber)s.%(ext)s").replace("\\", "/")

    command = [
        local_ytdlp,
        "-c",
        "--no-playlist",
        "-x", "--audio-format", "mp3",
        "-o", output_template,
        url
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            thread_safe_status(root, status_label, "MP3 download complete!")
        else:
            thread_safe_status(root, status_label, "Error during MP3 download")
            root.after(0, lambda: messagebox.showerror("Download Error", result.stderr))

    except Exception as e:  # noqa
        thread_safe_status(root, status_label, "Unexpected error")
        root.after(0, lambda: messagebox.showerror("Error", str(e)))  # noqa

    finally:
        root.is_downloading = False

# ---------------------------------------------------------
# MP4 Download Logic
# ---------------------------------------------------------
def download_mp4(url, save_path, status_label, root):
    # Create mp4 subfolder inside the chosen save_path

    mp4_folder = os.path.join(save_path, "mp4")
    os.makedirs(mp4_folder, exist_ok=True)

    # Redirect save_path to the mp4 folder

    save_path = mp4_folder

    # Mark download as active

    root.is_downloading = True

    # Update status label

    thread_safe_status(root, status_label, "Downloading MP4...", delay=999999)

    # Path to yt-dlp.exe (Nuitka-friendly)

    local_ytdlp = os.path.join(BASE_DIR, "yt-dlp.exe")

    # Output template

    output_template = os.path.join(save_path, "%(title)s_%(autonumber)s.%(ext)s").replace("\\", "/")

    command = [
        local_ytdlp,
        "-c",
        "--no-playlist",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "-o", output_template,
        url
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            thread_safe_status(root, status_label, "MP4 download complete!")
        else:
            thread_safe_status(root, status_label, "Error during MP4 download")
            root.after(0, lambda: messagebox.showerror("Download Error", result.stderr))

    except Exception as e:  # noqa
        thread_safe_status(root, status_label, "Unexpected error")
        root.after(0, lambda: messagebox.showerror("Error", str(e)))  # noqa

    finally:
        root.is_downloading = False

# ---------------------------------------------------------
# Update yt-dlp.exe
# ---------------------------------------------------------
def update_ytdlp(status_label, root):
    thread_safe_status(root, status_label, "Updating yt-dlp...", delay=999999)

    # Step 1: Update pip package (optional)
    try:
        subprocess.run(
            ["python", "-m", "pip", "install", "--upgrade", "yt-dlp"],
            check=True
        )
    except Exception:
        pass

    # Step 2: Download latest yt-dlp.exe
    download_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    exe_path = os.path.join(BASE_DIR, "yt-dlp.exe")  # FIXED for Nuitka

    try:
        thread_safe_status(root, status_label, "Downloading latest yt-dlp.exe...", delay=999999)

        response = requests.get(download_url, timeout=30)
        response.raise_for_status()

        with open(exe_path, "wb") as f:
            f.write(response.content)

        thread_safe_status(root, status_label, "yt-dlp updated successfully!")

    except Exception as e:  # noqa
        thread_safe_status(root, status_label, "Update failed")
        root.after(0, lambda: messagebox.showerror("Update Error", str(e)))  # noqa

# ---------------------------------------------------------
# Default folder popup
# ---------------------------------------------------------
def show_default_folder():
    messagebox.showinfo(
        "Default Folder",
        f"Your default download folder is:\n\n{default_path}"
    )

# ---------------------------------------------------------
# Handle Download Button
# ---------------------------------------------------------
def handle_download(mode_var, url_entry, status_label, root, save_path):
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a YouTube URL before downloading.")
        return

    mode = mode_var.get()

    url_entry.delete(0, tk.END)
    url_entry.focus_set()

    if mode == "mp3":
        threading.Thread(
            target=download_mp3,
            args=(url, save_path, status_label, root),
            daemon=True
        ).start()
    else:
        threading.Thread(
            target=download_mp4,
            args=(url, save_path, status_label, root),
            daemon=True
        ).start()

# ---------------------------------------------------------
# Main GUI
# ---------------------------------------------------------
def main():
    ensure_folders()

    root = tk.Tk()
    root.title("MPX Downloader")
    root.geometry("450x250")
    root.resizable(False, False)

    root.is_downloading = False

    save_path_var = tk.StringVar()
    save_path_var.set(default_path)

    def choose_save_folder():
        folder = filedialog.askdirectory()
        if folder:
            save_path_var.set(folder)

    save_frame = tk.Frame(root)
    save_frame.pack(pady=5, fill="x")

    tk.Label(save_frame, text="Save To:").pack(side="left", padx=5)

    save_display = tk.Label(save_frame, textvariable=save_path_var, anchor="w")
    save_display.pack(side="left", padx=5)

    browse_button = tk.Button(save_frame, text="Browse...", command=choose_save_folder)
    browse_button.pack(side="left", padx=5)

    tk.Button(save_frame, text="Default Folder", command=show_default_folder).pack(side="left", padx=5)

    title_label = tk.Label(root, text="MPX Downloader", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    mode_var = tk.StringVar(value="mp3")
    mode_frame = tk.Frame(root)
    mode_frame.pack()

    tk.Radiobutton(mode_frame, text="MP3", variable=mode_var, value="mp3").pack(side="left", padx=10)
    tk.Radiobutton(mode_frame, text="MP4", variable=mode_var, value="mp4").pack(side="left", padx=10)

    url_label = tk.Label(root, text="YouTube URL:")
    url_label.pack(pady=(15, 5))

    url_entry = tk.Entry(root, width=50)
    url_entry.pack()
    url_entry.focus_set()

    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Paste", command=lambda: url_entry.insert(tk.END, root.clipboard_get()))
    url_entry.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))

    status_label = tk.Label(root, text="Ready", anchor="w")
    status_label.pack(fill="x", padx=10, pady=(5, 0))

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=15)

    tk.Button(
        buttons_frame,
        text="Download",
        width=12,
        command=lambda: handle_download(mode_var, url_entry, status_label, root, save_path_var.get())
    ).pack(side="left", padx=10)

    tk.Button(
        buttons_frame,
        text="Update yt-dlp",
        width=12,
        command=lambda: threading.Thread(
            target=update_ytdlp,
            args=(status_label, root),
            daemon=True
        ).start()
    ).pack(side="left", padx=10)

    def on_close():
        if getattr(root, "is_downloading", False):
            if messagebox.askyesno("Exit?", "A download is still in progress. Exit anyway?"):
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    main()