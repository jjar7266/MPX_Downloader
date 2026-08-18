# 📌 MPX Downloader — Future Improvements Roadmap

# -----------------------------------------
# v4.01 — UI Polish & User Experience
# -----------------------------------------
- Add Dark Mode / Light Mode toggle
- Add drag‑and‑drop support for YouTube links
- Add “Open Download Folder” button after download
- Add “Clear URL field after download” toggle (optional)
- Improve error popups with friendlier explanations
- Add a small “About” window with version + runtime info

# -----------------------------------------
# v4.02 — Download Feedback Improvements
# -----------------------------------------
- Add progress bar for MP3/MP4 downloads
- Add download speed + ETA display
- Add stage indicators (Fetching Info / Downloading / Post‑Processing)
- Add retry logic for network failures (auto‑retry 2–3 times)
- Add clearer duplicate‑file detection messages

# -----------------------------------------
# v4.03 — Logging & Diagnostics Expansion
# -----------------------------------------
- Add “View Log” button inside the UI
- Add log categories (INFO / WARNING / ERROR)
- Add optional verbose logging mode
- Add region‑lock detection messages in the UI (not just log)

# -----------------------------------------
# v4.04 — Runtime & Engine Options
# -----------------------------------------
- Add optional bundled FFmpeg.exe (advanced users)
- Add FFmpeg selection: internal vs external
- Add proxy support (SOCKS5 / HTTP)
- Add cookies.txt selector UI (currently supported but not exposed)

# -----------------------------------------
# v4.05 — Output Control & File Naming
# -----------------------------------------
- Add filename template presets:
  - {title}.mp3
  - {title} - {channel}.mp4
  - {upload_date}_{title}.mp3
- Add custom naming rules editor
- Add option to embed thumbnails into MP3 metadata

# -----------------------------------------
# v4.06 — Download History System
# -----------------------------------------
- Add “Download History” panel
- Show last X downloads with timestamps
- Show status (Success / Skipped / Failed)
- Add “Open File” and “Open Folder” buttons
- Add “Clear History” option

# -----------------------------------------
# v4.07 — Playlist Foundations
# -----------------------------------------
- Detect playlist URLs automatically
- Show playlist video count
- Allow user to choose:
  - Download all
  - Download selected items
- Add playlist preview window

# -----------------------------------------
# v4.08 — Batch Queue System
# -----------------------------------------
- Add multi‑link queue manager
- Add per‑item progress bars
- Add pause / resume / cancel per item
- Add reorder queue items
- Add “Add to Queue” button for multiple links

# -----------------------------------------
# v4.09 — UI Modernization Pass
# -----------------------------------------
- Convert all widgets to ttk themed widgets
- Add modern spacing/padding rules
- Add compact mode
- Add large‑text accessibility mode

# -----------------------------------------
# v5.0 — Major Feature Release
# -----------------------------------------
- Full playlist support (selective download, metadata preview)
- Full batch download manager (parallel/sequential)
- Complete UI redesign with themes + animations
- Smart filename templates + metadata editor
- Auto‑organize downloads into Music/Video folders
- Proxy/VPN integration for region‑locked content
- Enhanced updater with GUI progress + changelog viewer
