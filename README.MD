[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-red)](https://github.com/sponsors/jjar7266)

<a href="https://buymeacoffee.com/jjar7266" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
</a>

<h1 align="center">🎵📥 MPX Downloader v4.0 📥🎵</h1>
<p align="center">
  <i>A clean, modern YouTube MP3/MP4 downloader powered by yt‑dlp, FFmpeg, and a fully‑integrated runtime detection system.</i><br>
  <b>Simple • Reliable • Self‑Updating • Region‑Aware • Polished</b>
</p>

---

<p align="center">
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.13+-blue?logo=python" alt="Python">
  </a>
  <a href="https://github.com/jjar7266/mpx-downloader/releases">
    <img src="https://img.shields.io/badge/Release-v4.0-brightgreen" alt="v4.0">
  </a>
</p>

# 🎶 MPX Downloader

**MPX Downloader** is a lightweight, user‑friendly desktop app for downloading YouTube videos as MP3 or MP4 — no Python installation required.
Just download, extract, and run.

Built with a clean Tkinter interface, powered by yt‑dlp for fast, reliable downloads, and packaged via **Nuitka standalone** for maximum portability.

---

# 🚀 Overview

MPX Downloader wraps yt‑dlp and FFmpeg in a simple, intuitive interface:

- Paste a YouTube link
- Choose MP3 or MP4
- Pick a save folder
- Download instantly

Everything is bundled — no installs, no command line, no configuration.

---

# ✨ Features

- 🎵 **MP3 & MP4 download modes**
- 📁 **Save‑to folder picker**
- 🔇 **Silent background downloads**
- 🧠 **Thread‑safe UI updates**
- 🚫 **Close protection during downloads**
- 🧩 **Self‑contained folder distribution**
- 🪟 **Clean, modern Tkinter interface**
- 🔄 **Robust yt‑dlp updater system**
- 🔔 **Auto‑update checks at startup**
- 📝 **Logging system (`log.txt`)**
- 📦 **Automatic first‑run bootstrap**
- 🧭 **Region‑lock awareness (403 detection)**
- 🧪 **Node.js runtime detection**
- 🔐 **Optional cookies.txt support for restricted videos**

---

# 🆕 What’s New in v4.0

### 🧠 Node.js Runtime Detection
yt‑dlp uses JavaScript runtimes (like Node.js) to decrypt certain YouTube signatures.
Without Node.js, some videos fail with 403 errors.

MPX Downloader v4.0 now:

- Detects Node.js at startup
- Logs detection status
- Automatically enables JS‑runtime compatibility mode
- Improves reliability for signature‑cipher videos

### 🌍 Region‑Lock Awareness
Some videos are blocked in certain countries or VPN locations.
MPX Downloader v4.0 now:

- Detects 403 errors caused by region locks
- Logs region‑related failures
- Suggests fixes (cookies, VPN change, Node.js)

### 🔄 Improved Updater System
The v4.0 updater is cleaner, safer, and more predictable:

- Startup self‑update check
- Manual update button
- Atomic `.new` + `.bak` replacement
- PowerShell helper for locked file replacement
- Automatic bootstrap if `yt-dlp.exe` is missing
- Clear logging of update results

### 📦 Packaging Improvements
- Updated to **Python 3.13 Nuitka standalone**
- Cleaner folder layout
- More reliable path resolution
- Faster startup
- Smaller footprint

---

# 📦 Download (Windows)

Download the latest release ZIP from the **[Releases](https://github.com/jjar7266/mpx-downloader/releases)** page.

Extract the ZIP → open the folder → run **MPX_Downloader.exe**.

```
⚠️ IMPORTANT:
Do NOT move the EXE out of the folder.
The entire folder is the application.
```

---

# 📁 Distribution Folder Layout (v4.0)

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

---

# 🖥️ How It Works

MPX Downloader uses:

- **yt‑dlp.exe** → downloads video/audio
- **FFmpeg** → used internally by yt‑dlp
- **Node.js (optional)** → decrypts signature‑cipher videos
- **Updater system** → keeps yt‑dlp current
- **Threaded workers** → keep UI responsive

The GUI handles everything automatically.

---

# 🔒 Duplicate Download Behavior

MPX Downloader **does not re-download the same link twice**.

If the output file already exists, yt‑dlp will skip the download.

---

# 🧪 Requirements (for developers)

If running from source:

- Python 3.13+
- `yt-dlp` Python package
- FFmpeg installed or available in PATH
- Windows 10 or 11

---

# ⚙️ Setup (for developers)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python mpx_downloaderV4.py
```

---

# 🏗️ Packaging (Nuitka)

Recommended: **standalone onefolder** mode.

```bash
python -m nuitka ^
  --standalone ^
  --windows-disable-console ^
  --windows-icon-from-ico=app.ico ^
  --enable-plugin=tk-inter ^
  --include-data-file=yt-dlp.exe=yt-dlp.exe ^
  mpx_downloaderV4.py
```

---

# 📝 Notes

- Node.js improves reliability for certain videos
- Region‑locked videos may require cookies or VPN adjustments
- Duplicate downloads are skipped
- All downloads run silently
- UI stays responsive
- Updater uses `.new` + `.bak` for safety
- PowerShell helper ensures updates apply even when locked
- `BASE_DIR` and paths logged to `log.txt`

---

# 👤 Author

**José "Joe" Ruiz**
📍 Coral Springs, FL

- 🐙 GitHub: [@jjar7266](https://github.com/jjar7266)
- ❤️ Sponsor: [github.com/sponsors/jjar7266](https://github.com/sponsors/jjar7266)
- ☕ Buy Me a Coffee: [buymeacoffee.com/jjar7266](https://buymeacoffee.com/jjar7266)

---

# 📄 License

This project is licensed under the **MIT License**.

## 🚀 Upcoming Improvements — v4.01
The next incremental update (v4.01) will focus on UI polish and user‑experience upgrades:

- Dark Mode / Light Mode toggle
- Drag‑and‑drop support for YouTube links
- Friendlier error popups and clearer status messages
- “Open Download Folder” button after downloads
- Small “About” window with version + runtime info

For the full roadmap of planned updates (v4.01 → v5.0), see:
👉 https://github.com/jjar7266/MPX_Downloader/blob/main/TODO.md
