[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-red)](https://github.com/sponsors/jjar7266)

<a href="https://buymeacoffee.com/jjar7266" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
</a>

<!-- Banner -->
<h1 align="center">🎵📥 MPX Downloader 📥🎵</h1>
<p align="center">
  <i>A clean, modern YouTube MP3/MP4 downloader powered by yt‑dlp & FFmpeg</i><br>
  <b>Simple • Reliable • Polished</b>
</p>

---

<p align="center">
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  </a>
</p>

# 🎶 MPX Downloader

**A lightweight, user‑friendly desktop app for downloading YouTube videos as MP3 or MP4.**  
No Python required — just download, extract, and run.

Built with a clean Tkinter interface and powered by yt‑dlp for fast, reliable downloads.

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
- 🔄 **Auto‑numbered filenames** (no overwrites)
- ⚙️ **Built‑in yt‑dlp updater**
- 🧩 **Self‑contained EXE** (yt‑dlp included)
- 🧠 **Thread‑safe UI updates**
- 🚫 **Close protection during downloads**
- 🪟 **Clean, modern Tkinter interface**

---

## 📦 Download (Windows)

Download the latest release ZIP from the **Releases** section.

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

The GUI handles everything automatically.

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
python mpx_downloaderV2.py