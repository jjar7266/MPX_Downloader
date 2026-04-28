"""
MPX Downloader with Robust Updater (teacher / student mode)
----------------------------------------------------------

Teacher voice (explanatory comments): This script is a complete, runnable Tkinter
desktop app that downloads audio/video via a bundled yt-dlp.exe and includes a
robust updater that can:

  - Auto-check for updates at startup and periodically.
  - Allow manual updates via a button.
  - Download a replacement yt-dlp.exe to yt-dlp.exe.new.
  - Create a .bak backup of the current yt-dlp.exe before replacing.
  - Attempt an atomic os.replace() immediately.
  - If the running file is locked, schedule a detached PowerShell helper that
    waits for the process to exit and then performs the replace (no extra EXE).
  - On next app start, attempt to apply any pending .new file.

Student voice (concise inline notes): Read the comments near each function to
understand what it does. The helper uses PowerShell (Windows) to perform the
post-exit replace; this avoids trying to overwrite a running executable.

Important packaging notes (teacher summary):
  - Ship yt-dlp.exe as a separate file next to your packaged EXE (not embedded).
  - Install to a writable location (per-user) or run updater with elevation.
  - PowerShell is required on the target machine (Windows default).
"""

import os
import sys
import subprocess
import threading
import tempfile
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import logging
import shutil
import requests

# -------------------------
# Configuration / Constants
# -------------------------
CREATE_NO_WINDOW = 0x08000000  # Windows flag to hide subprocess windows
BACKUP_SUFFIX = ".bak"

# -------------------------
# Environment helpers
# -------------------------
def get_base_dir():
    """
    Teacher: Determine the folder where the app should look for yt-dlp.exe.

    - When frozen (PyInstaller/Nuitka), sys.executable points to the running EXE.
    - When running as a script, __file__ points to the script file.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

BASE_DIR = get_base_dir()
LOCAL_YTDLP = os.path.join(BASE_DIR, "yt-dlp.exe")
TEMP_REPLACE = os.path.join(BASE_DIR, "yt-dlp.exe.new")
LOG_PATH = os.path.join(BASE_DIR, "log.txt")
default_path = os.path.join(os.path.expanduser("~"), "Downloads")
downloads_root = os.path.join(BASE_DIR, "downloads")

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# -------------------------
# Simple UI helpers
# -------------------------
def set_status(status_label, text, delay=3000, reset_to="Ready"):
    """Teacher: update the status label and reset after delay (ms)."""
    status_label.config(text=text)
    status_label.after(delay, lambda: status_label.config(text=reset_to))

def thread_safe_status(root, status_label, text, delay=3000, reset_to="Ready"):
    """Student: call this from background threads to update the UI safely."""
    root.after(0, lambda: set_status(status_label, text, delay, reset_to))

# -------------------------
# Filesystem helpers
# -------------------------
def ensure_folders():
    """Create runtime download folders used by the app."""
    os.makedirs(os.path.join(downloads_root, "mp3"), exist_ok=True)
    os.makedirs(os.path.join(downloads_root, "mp4"), exist_ok=True)

def try_replace_atomic(src: str, dst: str) -> bool:
    """
    Attempt an atomic replace using os.replace.

    Returns True on success, False on PermissionError (file locked).
    Raises on unexpected errors.
    """
    try:
        os.replace(src, dst)
        logging.info("Atomic replace succeeded: %s -> %s", src, dst)
        return True
    except PermissionError:
        logging.warning("Atomic replace failed due to PermissionError (file locked): %s -> %s", src, dst)
        return False
    except Exception:
        logging.exception("Atomic replace failed with unexpected error")
        raise

# -------------------------
# Replace helper (PowerShell)
# -------------------------
def _launch_replace_helper(tmp_path: str, target_path: str, backup_path: str, restart_app: bool = False):
    """
    Teacher: When the running file is locked, we cannot replace it immediately.
    This function writes a small PowerShell script to a temp file and launches
    it detached. The script will:

      - Wait (loop) until it can move tmp_path -> target_path (Move-Item).
      - Remove the backup if present.
      - Optionally restart the main app.
      - Delete itself when done.

    Student: This avoids bundling a separate updater EXE. PowerShell is available
    by default on modern Windows systems.
    """
    tmp_abs = os.path.abspath(tmp_path)
    dst_abs = os.path.abspath(target_path)
    bak_abs = os.path.abspath(backup_path)
    exe_restart = os.path.abspath(sys.executable) if restart_app else ""

    # PowerShell script content (keeps attempts and sleeps)
    ps_script = f"""
$ErrorActionPreference = 'Stop'
$tmp = '{tmp_abs}'
$dst = '{dst_abs}'
$bak = '{bak_abs}'
$maxAttempts = 600
$attempt = 0
while ($attempt -lt $maxAttempts) {{
    try {{
        Move-Item -Path $tmp -Destination $dst -Force
        if (Test-Path $bak) {{
            Remove-Item -Path $bak -Force
        }}
        break
    }} catch {{
        Start-Sleep -Seconds 1
        $attempt += 1
    }}
}}
if ('{exe_restart}' -ne '') {{
    try {{
        Start-Process -FilePath '{exe_restart}' -WindowStyle Hidden
    }} catch {{}}
}}
try {{
    Remove-Item -Path $MyInvocation.MyCommand.Path -Force
}} catch {{}}
"""

    # Write the script to a temp file
    fd, script_path = tempfile.mkstemp(suffix=".ps1", text=True)
    os.close(fd)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(ps_script)

    # Launch PowerShell detached
    try:
        subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW
        )
        logging.info("Launched replace helper PowerShell script: %s", script_path)
    except Exception:
        logging.exception("Failed to launch PowerShell helper; user must restart to apply update.")

# -------------------------
# Pending replace attempt
# -------------------------
def attempt_pending_replace(status_label, root):
    """
    Teacher: On startup we check for a previously downloaded .new file and try
    to apply it. This handles the case where the updater downloaded the file
    but couldn't replace it because the app was running.
    """
    if os.path.exists(TEMP_REPLACE):
        logging.info("Found pending update file: %s", TEMP_REPLACE)
        thread_safe_status(root, status_label, "Applying pending yt-dlp update...", delay=5000)
        try:
            backup_path = LOCAL_YTDLP + BACKUP_SUFFIX
            try:
                if os.path.exists(LOCAL_YTDLP):
                    shutil.copy2(LOCAL_YTDLP, backup_path)
                    logging.info("Backup created: %s", backup_path)
            except Exception as _backup_exc:
                logging.exception("Failed to create backup before pending replace; continuing")

            if try_replace_atomic(TEMP_REPLACE, LOCAL_YTDLP):
                try:
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                        logging.info("Removed backup after successful replace: %s", backup_path)
                except Exception:
                    logging.warning("Could not remove backup: %s", backup_path)
                thread_safe_status(root, status_label, "Pending update applied.")
                logging.info("Pending update applied successfully.")
            else:
                thread_safe_status(root, status_label, "Pending update present but file locked.")
                logging.info("Pending update present but file locked; will retry on next start.")
        except Exception as _exc:
            logging.exception("Error applying pending update")
            thread_safe_status(root, status_label, "Error applying pending update")
            root.after(0, lambda: messagebox.showerror("Update Error", str(_exc)))    # noqa

# -------------------------
# Updater (download + replace)
# -------------------------
def update_ytdlp(status_label, root, restart_app_after_replace: bool = False):
    """
    Teacher: This function performs the update flow:

      1. Try yt-dlp's built-in self-updater (yt-dlp.exe --update).
      2. If that fails, download the latest yt-dlp.exe to yt-dlp.exe.new.
      3. Create a .bak backup of the current yt-dlp.exe.
      4. Attempt atomic os.replace(tmp -> yt-dlp.exe).
      5. If replace fails due to lock, schedule a PowerShell helper to replace
         after the app exits.

    Student: Call this from a background thread. The UI will be updated via
    thread_safe_status.
    """
    def update_status(msg):
        thread_safe_status(root, status_label, msg, delay=999999)

    update_status("Checking for yt-dlp updates...")
    local_ytdlp = LOCAL_YTDLP

    # STEP 0: If a pending .new exists, try to apply it first
    if os.path.exists(TEMP_REPLACE):
        logging.info("Attempting to apply pending update before running updater.")
        attempt_pending_replace(status_label, root)

    # STEP 1: Try yt-dlp's self-update
    update_status("Running yt-dlp self-update...")
    try:
        result = subprocess.run(
            [local_ytdlp, "--update"],
            capture_output=True,
            text=True,
            creationflags=CREATE_NO_WINDOW
        )
        logging.info("Self-update returncode=%s stdout=%s stderr=%s", result.returncode, result.stdout, result.stderr)
        if result.returncode == 0:
            update_status("yt-dlp updated successfully (self-update).")
            return
        else:
            logging.info("Self-update did not apply; falling back to manual download.")
    except Exception as _self_exc:
        logging.exception("Exception while attempting self-update; falling back to manual download.")

    # STEP 2: Manual download fallback
    update_status("Downloading latest yt-dlp.exe...")
    download_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"

    try:
        with requests.get(download_url, stream=True, timeout=60) as response:
            response.raise_for_status()
            tmp_path = TEMP_REPLACE
            logging.info("Streaming download to temporary file: %s", tmp_path)
            with open(tmp_path, "wb") as out_f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        out_f.write(chunk)
                        out_f.flush()

        # Create backup
        backup_path = LOCAL_YTDLP + BACKUP_SUFFIX
        try:
            if os.path.exists(LOCAL_YTDLP):
                shutil.copy2(LOCAL_YTDLP, backup_path)
                logging.info("Backup created: %s", backup_path)
        except Exception as _backup_exc:
            logging.exception("Failed to create backup; continuing with replace attempt")

        # Attempt atomic replace
        if try_replace_atomic(tmp_path, local_ytdlp):
            # Success: remove backup if present
            try:
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                    logging.info("Removed backup after successful replace: %s", backup_path)
            except Exception:
                logging.warning("Could not remove backup: %s", backup_path)
            update_status("yt-dlp updated successfully!")
            logging.info("Manual update applied successfully.")
            if restart_app_after_replace:
                # Optionally restart the app (teacher: be careful with UX)
                try:
                    subprocess.Popen([sys.executable], creationflags=CREATE_NO_WINDOW)
                except Exception:
                    logging.exception("Failed to restart app after update")
            return
        else:
            # Replace failed due to lock: schedule helper and prompt user
            logging.info("Manual update downloaded but replace failed due to lock; scheduling helper.")
            _launch_replace_helper(tmp_path, local_ytdlp, backup_path, restart_app=restart_app_after_replace)
            update_status("Update downloaded; will apply after you close the app.")
            root.after(
                0,
                lambda: messagebox.showinfo(
                    "Update Scheduled",
                    "The update has been downloaded. Close MPX Downloader to allow the update to be applied automatically."
                )
            )
            return

    except requests.RequestException as _req_exc:
        logging.exception("Network error during manual update download")
        update_status("Update failed (network)")
        root.after(0, lambda: messagebox.showerror("Update Error", str(_req_exc)))  # noqa
    except Exception as _exc:
        logging.exception("Unexpected error during manual update")
        update_status("Update failed")
        root.after(0, lambda: messagebox.showerror("Update Error", str(_exc)))      # noqa

# -------------------------
# Download functions (MP3 / MP4)
# -------------------------
def download_mp3(url, save_path, status_label, root):
    """
    Student: This uses the bundled yt-dlp.exe as a subprocess to download an MP3.
    It does not attempt to parse progress here (keeps code simple). If you want
    live progress, replace subprocess.run with a streaming Popen reader and parse
    yt-dlp's output lines.
    """
    mp3_folder = os.path.join(save_path, "mp3")
    os.makedirs(mp3_folder, exist_ok=True)
    root.is_downloading = True
    thread_safe_status(root, status_label, "Downloading MP3...", delay=999999)

    output_template = os.path.join(mp3_folder, "%(title)s.%(ext)s").replace("\\", "/")
    command = [
        LOCAL_YTDLP,
        "-c",
        "--no-playlist",
        "-x", "--audio-format", "mp3",
        "-o", output_template,
        url
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            creationflags=CREATE_NO_WINDOW
        )
        logging.info("MP3 download returncode=%s stdout=%s stderr=%s", result.returncode, result.stdout, result.stderr)
        if result.returncode == 0:
            thread_safe_status(root, status_label, "MP3 download complete!")
        else:
            thread_safe_status(root, status_label, "Error during MP3 download")
            root.after(0, lambda: messagebox.showerror("Download Error", result.stderr))
    except Exception as _exc:
        logging.exception("Unexpected error during MP3 download")
        thread_safe_status(root, status_label, "Unexpected error")
        root.after(0, lambda: messagebox.showerror("Error", str(_exc)))  # noqa
    finally:
        root.is_downloading = False

def download_mp4(url, save_path, status_label, root):
    """
    Student: Similar to download_mp3 but for MP4. Uses yt-dlp subprocess.
    """
    mp4_folder = os.path.join(save_path, "mp4")
    os.makedirs(mp4_folder, exist_ok=True)
    root.is_downloading = True
    thread_safe_status(root, status_label, "Downloading MP4...", delay=999999)

    output_template = os.path.join(mp4_folder, "%(title)s.%(ext)s").replace("\\", "/")
    command = [
        LOCAL_YTDLP,
        "-c",
        "--no-playlist",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "-o", output_template,
        url
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            creationflags=CREATE_NO_WINDOW
        )
        logging.info("MP4 download returncode=%s stdout=%s stderr=%s", result.returncode, result.stdout, result.stderr)
        if result.returncode == 0:
            thread_safe_status(root, status_label, "MP4 download complete!")
        else:
            thread_safe_status(root, status_label, "Error during MP4 download")
            root.after(0, lambda: messagebox.showerror("Download Error", result.stderr))
    except Exception as _exc:
        logging.exception("Unexpected error during MP4 download")
        thread_safe_status(root, status_label, "Unexpected error")
        root.after(0, lambda: messagebox.showerror("Error", str(_exc)))  # noqa
    finally:
        root.is_downloading = False

# -------------------------
# UI wiring
# -------------------------
def show_default_folder():
    messagebox.showinfo("Default Folder", f"Your default download folder is:\n\n{default_path}")

def handle_download(mode_var, url_entry, status_label, root, save_path):
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a YouTube URL before downloading.")
        return
    mode = mode_var.get()
    url_entry.delete(0, tk.END)
    url_entry.focus_set()
    if mode == "mp3":
        threading.Thread(target=download_mp3, args=(url, save_path, status_label, root), daemon=True).start()
    else:
        threading.Thread(target=download_mp4, args=(url, save_path, status_label, root), daemon=True).start()

# -------------------------
# Main application
# -------------------------
def main():
    ensure_folders()

    root = tk.Tk()
    root.title("MPX Downloader")
    root.geometry("520x300")
    root.resizable(False, False)
    root.is_downloading = False

    save_path_var = tk.StringVar(value=default_path)

    def choose_save_folder():
        folder = filedialog.askdirectory()
        if folder:
            save_path_var.set(folder)

    # Top save folder row
    save_frame = tk.Frame(root)
    save_frame.pack(pady=5, fill="x")
    tk.Label(save_frame, text="Save To:").pack(side="left", padx=5)
    save_display = tk.Label(save_frame, textvariable=save_path_var, anchor="w")
    save_display.pack(side="left", padx=5)
    tk.Button(save_frame, text="Browse...", command=choose_save_folder).pack(side="left", padx=5)
    tk.Button(save_frame, text="Default Folder", command=show_default_folder).pack(side="left", padx=5)

    # Title
    title_label = tk.Label(root, text="MPX Downloader", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Mode radio buttons
    mode_var = tk.StringVar(value="mp3")
    mode_frame = tk.Frame(root)
    mode_frame.pack()
    tk.Radiobutton(mode_frame, text="MP3", variable=mode_var, value="mp3").pack(side="left", padx=10)
    tk.Radiobutton(mode_frame, text="MP4", variable=mode_var, value="mp4").pack(side="left", padx=10)

    # URL entry
    url_label = tk.Label(root, text="YouTube URL:")
    url_label.pack(pady=(15, 5))
    url_entry = tk.Entry(root, width=60)
    url_entry.pack()
    url_entry.focus_set()

    # Context menu for paste
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Paste", command=lambda: url_entry.insert(tk.END, root.clipboard_get()))
    url_entry.bind(
        "<Button-3>",
        lambda event: (
            context_menu.tk_popup(event.x_root, event.y_root),
            context_menu.grab_release()
        )
    )

    # Status label
    status_label = tk.Label(root, text="Ready", anchor="w")
    status_label.pack(fill="x", padx=10, pady=(5, 0))

    # Buttons
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=12)

    tk.Button(
        buttons_frame,
        text="Download",
        width=12,
        command=lambda: handle_download(mode_var, url_entry, status_label, root, save_path_var.get())
    ).pack(side="left", padx=10)

    # Manual update button: calls update_ytdlp in background
    tk.Button(
        buttons_frame,
        text="Update yt-dlp",
        width=12,
        command=lambda: threading.Thread(
            target=update_ytdlp,
            args=(status_label, root, False),
            daemon=True
        ).start()
    ).pack(side="left", padx=10)

    # Attempt to apply any pending update at startup (non-blocking)
    try:
        threading.Thread(target=attempt_pending_replace, args=(status_label, root), daemon=True).start()
    except Exception as _exc:
        logging.exception("Failed to start pending-replace thread")

    # -------------------------
    # Auto-update: startup check and periodic checks
    # -------------------------
    def _auto_check_startup():
        """Teacher: run a one-time check at startup in background."""
        try:
            update_ytdlp(status_label, root, restart_app_after_replace=False)
        except Exception:
            logging.exception("Auto update check failed at startup")

    threading.Thread(target=_auto_check_startup, daemon=True).start()

    def _periodic_update_check(interval_seconds=24 * 3600):
        """
        Student: runs forever in a daemon thread and checks for updates every interval.
        For testing, set interval_seconds to a small value (e.g., 60).
        """
        while True:
            try:
                update_ytdlp(status_label, root, restart_app_after_replace=False)
            except Exception:
                logging.exception("Periodic update check failed")
            time.sleep(interval_seconds)

    # Start periodic checker (daemon)
    threading.Thread(target=_periodic_update_check, args=(24 * 3600,), daemon=True).start()

    # -------------------------
    # Window close handling
    # -------------------------
    def on_close():
        if getattr(root, "is_downloading", False):
            if messagebox.askyesno("Exit?", "A download is still in progress. Exit anyway?"):
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    main()
