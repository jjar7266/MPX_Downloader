[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-red)](https://github.com/sponsors/jjar7266)

<a href="https://buymeacoffee.com/jjar7266" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
</a>

<!-- Banner -->
<h1 align="center">🎵📥 MPX Downloader 📥🎵</h1>
<p align="center">
  <i>A clean, modern YouTube MP3/MP4 downloader powered by yt‑dlp & FFmpeg</i><br>
  <b>Simple • Reliable • Self‑Updating • Polished</b>
</p>

---

<p align="center">
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  </a>
  <a href="https://github.com/jjar7266/mpx-downloader/releases/tag/v3.0">
    <img src="https://img.shields.io/badge/Release-v3.0-brightgreen" alt="v3.0">
  </a>
</p>

# 🎶 MPX Downloader

**A lightweight, user‑friendly desktop app for downloading YouTube videos as MP3 or MP4.**  
No Python required — just download, extract, and run.

Built with a clean Tkinter interface, powered by yt‑dlp for fast, reliable downloads, and now featuring a robust self‑updater.

---

## 🚀 Overview

**MPX Downloader** wraps yt‑dlp and FFmpeg in a simple, intuitive interface:

- Paste a YouTube link  
- Choose MP3 or MP4  
- Pick a save folder  
- Download instantly  

Everything is bundled — no installs, no setup, no command line.

---

## ✨ Features

- 🎵 **MP3 & MP4 download modes**  
- 📁 **Save‑to folder picker**  
- 🔇 **Silent background downloads** (no black console windows)  
- 🧠 **Thread‑safe UI updates**  
- 🚫 **Close protection during downloads**  
- 🧩 **Self‑contained EXE** (yt‑dlp included)  
- 🪟 **Clean, modern Tkinter interface**  
- 🔄 **Robust self‑updater** with atomic replace and `.bak` backup  
- ⚡ **PowerShell replace helper** for locked‑file scenarios  
- 🔔 **Auto‑update checks** on startup and periodic intervals  
- 🛠️ **Manual update button** — check for updates any time from the UI  
- 📋 **Startup logging** — `BASE_DIR` and paths logged to `log.txt`  

---

## 🆕 What's New in v3.0

### 🔄 Robust Self‑Updater
- **Atomic replace** — downloads to a temp file, then replaces the running binary in one move  
- **`.bak` backup** — previous version is preserved before replacement  
- **PowerShell replace helper** — if the running EXE is locked, a PowerShell one‑liner waits for the process to exit and completes the swap  
- **Pending‑apply on startup** — detects and applies a deferred replace at next launch via `attempt_pending_replace()`  

### 🔔 Auto‑Update Checks
- **Startup check** — queries the latest GitHub release on launch (background thread)  
- **Periodic check** — re‑checks on a configurable interval while the app is running  
- **Manual update button** — trigger a check/download any time from the UI  

### 📦 Packaging
- Nuitka **onefolder** build recommended for clean distribution  
- `BASE_DIR` logged at startup for transparent path resolution  

### 🛠 Other
- `update_ytdlp()` keeps yt‑dlp current alongside app updates  
- Threaded download functions keep UI responsive  

---

## 📦 Download (Windows)

Download the latest release ZIP from the **[Releases](https://github.com/jjar7266/mpx-downloader/releases)** section.

Inside the ZIP:

- `MPX_Downloader.exe`  
- `yt-dlp.exe`  
- `README.txt`  

Extract the ZIP → run **MPX_Downloader.exe**.

No installation required.

---

## 🖥️ How It Works

MPX Downloader uses:

- **yt‑dlp.exe** → downloads video/audio  
- **FFmpeg** → used internally by yt‑dlp when needed  
- **Self‑updater** → checks GitHub releases and applies updates automatically  

The GUI handles everything automatically.

---

## 🔒 Duplicate Download Behavior

MPX Downloader **does not re-download the same link twice**.

If the output file already exists, yt‑dlp will skip the download.  
This prevents accidental duplicates and keeps your folders clean.

This behavior is intentional and documented.

---

## 🧪 Requirements (for developers)

If you want to run from source:

- Python 3.10+  
- `yt-dlp` Python package  
- FFmpeg installed or available in PATH  
- Windows 10 or 11  

---

## ⚙️ Setup (for developers)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python mpx_downloaderV3.py
```

---

## 🏗️ Packaging (Nuitka)

The app is packaged using Nuitka with:

- Tkinter plugin enabled  
- yt‑dlp.exe bundled  
- Console disabled  
- Custom icon included  
- **Onefolder** mode recommended for v3.0  

**Packaging command (onefolder):**

```bash
python -m nuitka --standalone --windows-disable-console --windows-icon-from-ico=app.ico --enable-plugin=tk-inter --include-data-file=yt-dlp.exe=yt-dlp.exe mpx_downloaderV3.py
```

---

## 📁 Folder Layout

```
MPX_Downloader/
│
├── mpx_downloaderV3.py
├── yt-dlp.exe
├── app.ico
├── log.txt             (created at runtime)
│
├── dist/               (created during packaging)
├── build/              (created during packaging)
│
├── mp3/                (created at runtime)
└── mp4/                (created at runtime)
```

---

## 📝 Notes

- Duplicate downloads are intentionally skipped  
- Multi‑threaded downloads keep the UI responsive  
- All downloads run silently without console windows  
- No Python installation required for the packaged EXE  
- The self‑updater creates a `.bak` backup before replacing the binary  
- `BASE_DIR` is logged to `log.txt` at startup for easy debugging  

---

## 👤 Author

**José "Joe" Ruiz**  
📍 Coral Springs, FL  

- 🐙 GitHub: [@jjar7266](https://github.com/jjar7266)  
- ❤️ Sponsor: [github.com/sponsors/jjar7266](https://github.com/sponsors/jjar7266)  
- ☕ Buy Me a Coffee: [buymeacoffee.com/jjar7266](https://buymeacoffee.com/jjar7266)  

---

## 📄 License

This project is licensed under the **MIT License**.
