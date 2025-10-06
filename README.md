# 🛡️ Blacklist Management Tool v1.0

A sleek terminal-style GUI application for managing your personal blacklist with style.

## ✨ Features

- **Terminal-Style GUI** - Dark theme with RED text and ASCII art logo
- **Frameless Window** - Custom title bar, draggable, pocket-sized (500x400)
- **Music Player** - Background music support with toggle control
- **Full CRUD** - Add, Remove, Search, Update, and List entries
- **Threat Levels** - Categorize entries by severity (Low, Medium, High, Critical)
- **JSON Storage** - Simple file-based data persistence

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/digitalfoes/Blacklist.git
cd Blacklist
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python gui_terminal.py
```

### Optional: Add Background Music
Place a WAV file named `blacklist_theme.wav` in the project directory for background music.

## 📁 Project Structure

```
Blacklist/
├── gui_terminal.py      # Main GUI application
├── blacklist.py         # Core logic and data management
├── requirements.txt     # Dependencies (PyQt6, pygame)
├── data/               # Data storage directory
│   └── blacklist.json  # Your blacklist entries
└── README.md           # This file
```

## 🎮 Usage

Run the application and use the menu:

1. **Add entry** - Create new blacklist entry with name, reason, threat level
2. **Remove entry** - Delete entry by ID or name
3. **Search** - Find entries by keyword
4. **Update** - Modify existing entries
5. **List all** - View all entries with sorting options
0. **Exit** - Close the application

### Controls
- **Drag window** - Click and hold the red title bar
- **Toggle music** - Click the small checkbox next to "Music:"
- **Close** - Click the ✕ button in title bar
