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

Built with a clean Tkinter interface, powered by yt‑dlp for fast, reliable downloads, and now featuring a **full production‑grade updater system**.

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
- 🔇 **Silent background downloads** (no console windows)  
- 🧠 **Thread‑safe UI updates**  
- 🚫 **Close protection during downloads**  
- 🧩 **Self‑contained EXE** (yt‑dlp included)  
- 🪟 **Clean, modern Tkinter interface**  
- 🔄 **Robust updater system**  
- ⚡ **PowerShell replace helper** for locked‑file scenarios  
- 🔔 **Auto‑update checks** (startup + periodic)  
- 🛠️ **Manual update button**  
- 📝 **Logging system** (`log.txt`)  
- 📦 **Automatic first‑run bootstrap** (downloads yt‑dlp.exe if missing)  

---

## 🆕 What's New in v3.0

### 🔄 Full Robust Updater System
The new updater is engineered for reliability and safety:

#### Self‑Update Stage
- Runs `yt-dlp.exe --update` silently  
- Logs stdout/stderr  
- If successful → done  
- If not → falls back to manual update  

#### Manual Update Stage
- Downloads latest yt‑dlp.exe to `yt-dlp.exe.new`  
- Creates `.bak` backup of current yt‑dlp.exe  
- Attempts atomic replace using `os.replace()`  
- If locked → launches a **detached PowerShell helper** that:  
  - Waits for the EXE to unlock  
  - Moves `.new` → `yt-dlp.exe`  
  - Removes `.bak`  
  - Optionally restarts the app  
  - Deletes itself  

#### Pending Update Handling
- On startup, the app checks for `yt-dlp.exe.new`  
- Attempts atomic replace  
- If locked → defers to next launch  

### 🔔 Auto‑Update Checks
- One‑time startup check  
- 24‑hour periodic background checks  
- Fully threaded, non‑blocking  

### 📦 Packaging Improvements
- Nuitka onefile/onefolder compatible  
- Tkinter plugin enabled  
- Silent execution (no console window)  
- Bundled yt‑dlp.exe  

### 🛠 Other Improvements
- Logging system (`log.txt`)  
- Runtime folder creation  
- Thread‑safe status updates  
- First‑run bootstrap downloader  

---

## 📦 Download (Windows)

Download the latest release ZIP from the **[Releases](https://github.com/jjar7266/mpx-downloader/releases)** page.

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
- **FFmpeg** → used internally by yt‑dlp  
- **Updater system** → keeps yt‑dlp current  
- **Threaded workers** → keep UI responsive  

The GUI handles everything automatically.

---

## 🔒 Duplicate Download Behavior

MPX Downloader **does not re-download the same link twice**.

If the output file already exists, yt‑dlp will skip the download.  
This prevents accidental duplicates and keeps your folders clean.

This behavior is intentional.

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

Recommended: **onefolder** mode for clarity.

**Packaging command:**

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

## 📁 Folder Layout

```
MPX_Downloader/
│
├── mpx_downloaderV3.py
├── yt-dlp.exe
├── yt-dlp.exe.new        (pending update, if present)
├── yt-dlp.exe.bak        (backup during update)
├── log.txt               (runtime log)
├── app.ico
│
├── downloads/
│   ├── mp3/
│   └── mp4/
│
├── dist/                 (Nuitka EXE output)
└── build/                (Nuitka build artifacts)
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
