# 🎵 Music Time Machine

[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Music Time Machine** is a desktop app that lets you create Spotify playlists from historical **Billboard Hot 100** charts. Pick a date, and the app will scrape Billboard, search for the songs on Spotify, and create a playlist in your account.  

---

## 🚀 Features

- Create private Spotify playlists from any Billboard Hot 100 date.  
- Automatic searching and matching of songs by title and year.  
- Interactive **Flet-based desktop UI**.  
- Spotify OAuth via **copy-paste flow** for desktop apps.  
- Cached Spotify tokens — no repeated logins.  
- Logs songs not found on Spotify.  

---

## 📸 Screenshots / GIFs

*(Add images or GIFs here for visual appeal)*  

![App screenshot](./assets/screenshot1.png)  
![Playlist creation screenshot](./assets/screenshot2.png)  
![Optional GIF showing workflow](./assets/demo.gif)  

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/MusicTimeMachine.git
cd MusicTimeMachine
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### 📦 Dependencies

#### Runtime dependencies (needed to run the app)
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```ini
beautifulsoup4==4.13.5
flet==0.28.3
requests==2.32.5
spotipy==2.25.1
soupsieve==2.8
```

#### Development / Build dependencies (needed to build EXE)
```bash
pip install -r requirements-dev.txt
```

**requirements-dev.txt:**
```diff
-r requirements.txt
pyinstaller==6.15.0
```

This keeps your runtime environment clean while allowing EXE packaging.

---

## 🔑 Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Log in and create a new app.
3. Set the Redirect URI to:
   ```
   https://example.com/callback
   ```
4. Copy your **Client ID** and **Client Secret**.
5. Open the app, click **Configure Spotify API**, and paste the credentials.
6. On first run, you'll complete login via copy-paste OAuth. Subsequent playlist creation uses the cached token.

---

## 🖥️ Usage

1. Run the app:
   ```bash
   python main.py
   ```

2. Enter a date (YYYY-MM-DD).

3. Click **🎶 Create Playlist**.

4. On first run:
   - Browser opens for Spotify login.
   - Click **Agree**, copy the full redirect URL, and paste it into the Flet dialog.
   - Playlist will be created automatically in your Spotify account.

---

## 💾 Download EXE (Windows)

Download the latest pre-built Windows executable from [GitHub Releases](https://github.com/USERNAME/MusicTimeMachine/releases):

**MusicTimeMachine_v01.exe**

### Instructions:
1. Download the `.exe` file.
2. Double-click to run the app.
3. Complete the first-time Spotify login as described above (copy-paste OAuth).
4. Enter a date and click **🎶 Create Playlist**.

⚠️ **Cached token ensures you won't need to repeat login for future uses.**

---

## 🗂️ Project Structure

```
MusicTimeMachine/
│
├─ App_oop/
│  ├─ app.py               # Flet app entry point
│  ├─ logic/
│  │  ├─ spotify.py        # Spotify client & playlist creation
│  │  └─ billboard.py      # Billboard scraping
│  ├─ ui/
│  │  ├─ layout.py         # Flet UI layout builder
│  │  └─ component.py      # Custom components for easy styling & reuse
│  └─ config/
│     └─ settings.py       # Save/load Spotify credentials
│
├─ main.py                 # Launch script
├─ requirements.txt        # Runtime dependencies
├─ requirements-dev.txt    # Dev/build dependencies
├─ icon.ico                # App icon
└─ README.md

---

## 💡 Notes & Tips

- **Scraping Billboard:** Changes to Billboard HTML may break scraping.
- **Spotify tracks:** Not every song may be available; missing songs are logged.
- **EXE packaging:** Create a standalone Windows EXE using:
  ```bash
  flet pack main.py --name MusicTimeMachine_v01 --icon icon.ico
  ```
---

## 🤝 Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push (`git push origin feature-name`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
