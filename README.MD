[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-red)](https://github.com/sponsors/jjar7266)

<a href="https://buymeacoffee.com/jjar7266" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
</a>

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
  <a href="https://github.com/jjar7266/mpx-downloader/releases">
    <img src="https://img.shields.io/badge/Release-v3.0-brightgreen" alt="v3.0">
  </a>
</p>

# 🎶 MPX Downloader

**A lightweight, user‑friendly desktop app for downloading YouTube videos as MP3 or MP4.**  
No Python required — just download, extract, and run.

Built with a clean Tkinter interface, powered by yt‑dlp for fast, reliable downloads, and now featuring a **full production‑grade updater system** and a **standalone Nuitka distribution**.

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
- 🔇 **Silent background downloads**  
- 🧠 **Thread‑safe UI updates**  
- 🚫 **Close protection during downloads**  
- 🧩 **Self‑contained folder distribution** (EXE + runtime + yt‑dlp)  
- 🪟 **Clean, modern Tkinter interface**  
- 🔄 **Robust updater system**  
- 🔔 **Auto‑update checks**  
- 🛠️ **Manual update button**  
- 📝 **Logging system (`log.txt`)**  
- 📦 **Automatic first‑run bootstrap** (downloads yt‑dlp.exe if missing)  

---

## 🆕 What's New in v3.0

### 🔄 Full Robust Updater System
A two‑stage update process ensures yt‑dlp stays current:

#### Stage 1 — Self‑Update
- Runs `yt-dlp.exe --update` silently  
- Logs stdout/stderr  
- If successful → done  

#### Stage 2 — Manual Update Fallback
- Downloads latest yt‑dlp.exe to `yt-dlp.exe.new`  
- Creates `.bak` backup  
- Attempts atomic replace  
- If locked → launches a detached PowerShell helper that:  
  - Waits for unlock  
  - Replaces the file  
  - Cleans up `.bak` and `.new`  

#### Pending Update Handling
- On startup, the app checks for `yt-dlp.exe.new`  
- Applies it automatically if possible  
- Defers if locked  

### 🔔 Auto‑Update Checks
- Startup check  
- Periodic background checks  
- Fully threaded, non‑blocking  

### 📦 Packaging Improvements
- Switched to **Nuitka standalone (onefolder)**  
- All required DLLs, Python runtime, Tkinter, SSL, and extension modules included  
- `yt-dlp.exe` shipped externally and fully updatable  
- `BASE_DIR` logic fixed for standalone builds  

### 🛠 Other Improvements
- Logging system (`log.txt`)  
- Thread‑safe status updates  
- First‑run bootstrap downloader  
- Cleaner path resolution and error handling  

---

## 📦 Download (Windows)

Download the latest release ZIP from the **[Releases](https://github.com/jjar7266/mpx-downloader/releases)** page.

Extract the ZIP → open the folder → run **MPX_Downloader.exe**.

```
⚠️ IMPORTANT:
Do NOT move the EXE out of the folder.
The entire folder is the application.
```

---

## 📁 Distribution Folder Layout

```
MPX_Downloader/
│
├── MPX_Downloader.exe        (main application)
├── yt-dlp.exe                (download engine, auto-updated)
├── python313.dll             (embedded Python runtime)
├── _tkinter.pyd              (Tkinter GUI engine)
├── libssl-3.dll              (SSL support)
├── libcrypto-3.dll           (crypto backend)
├── vcruntime140.dll          (MSVC runtime)
├── vcruntime140_1.dll
├── zlib1.dll
│
├── certifi/                  (certificate bundle)
├── charset_normalizer/       (HTTP parsing)
├── tcl/                      (Tkinter dependency)
└── tk/                       (Tkinter dependency)
```

This is the exact structure included in the release ZIP.

---

## 🖥️ How It Works

MPX Downloader uses:

- **yt‑dlp.exe** → downloads video/audio  
- **FFmpeg** → used internally by yt‑dlp  
- **Updater system** → keeps yt‑dlp current  
- **Threaded workers** → keep UI responsive  

The GUI handles everything automatically.

---

## 🔒 Duplicate Download Behavior

MPX Downloader **does not re-download the same link twice**.

If the output file already exists, yt‑dlp will skip the download.  
This prevents accidental duplicates and keeps your folders clean.

---

## 🧪 Requirements (for developers)

If running from source:

- Python 3.10+  
- `yt-dlp` Python package  
- FFmpeg installed or available in PATH  
- Windows 10 or 11  

---

## ⚙️ Setup (for developers)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python mpx_downloaderV3.py
```

---

## 🏗️ Packaging (Nuitka)

Recommended: **standalone onefolder** mode.

```bash
python -m nuitka ^
  --standalone ^
  --windows-disable-console ^
  --windows-icon-from-ico=app.ico ^
  --enable-plugin=tk-inter ^
  --include-data-file=yt-dlp.exe=yt-dlp.exe ^
  mpx_downloaderV3.py
```

---

## 📝 Notes

- Duplicate downloads are intentionally skipped  
- All downloads run silently  
- UI stays responsive during downloads  
- No Python installation required for packaged EXE  
- Updater uses `.new` + `.bak` for safety  
- PowerShell helper ensures updates apply even when locked  
- `BASE_DIR` and paths logged to `log.txt`  

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
