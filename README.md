# 🛡️ Blacklist Management Tool v1.0

A powerful blacklist management system with a sleek terminal-style GUI, featuring custom music playback and modern Python architecture.

## ✨ Features

### 🎨 Terminal-Style GUI
- **Custom RED theme** - Dark terminal aesthetic with red text
- **ASCII art logo** - "BLACKLIST" in stylized text
- **Frameless window** - Custom title bar with draggable interface
- **Pocket-sized** - Compact 500x400 window
- **Music player** - Background music with toggle control

### 🛠️ Core Functionality
- **Add/Remove entries** - Manage blacklist with ease
- **Search** - Find entries quickly
- **Update** - Modify existing entries
- **List all** - View all entries with sorting

### 🎵 Audio Features
- **Background music** - Custom theme song plays on loop
- **Music toggle** - Small checkbox to enable/disable music
- **Git LFS support** - Large audio files managed efficiently

### 🤖 AI-Powered (Optional)
- **CrewAI agents** - Intelligent blacklist management
- **Python Pro Agent** - Code review and optimization tools
- **Multi-agent system** - Specialized agents for different tasks

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Git LFS (for audio files)

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd new_project
```

2. **Install Git LFS (if not already installed):**
```bash
git lfs install
git lfs pull  # Download audio files
```

3. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the GUI application:**
```bash
python gui_terminal.py
```

### Alternative Versions
- **GUI (Table-based):** `python gui.py`
- **CLI (Simple):** `python main_simple.py`
- **CLI (with AI):** `python main.py` (requires API key)

## Project Structure

- `main.py` - Main entry point
- `agents.py` - CrewAI agent definitions
- `tasks.py` - Task definitions for agents
- `crew.py` - Crew configuration
- `blacklist.py` - Core blacklist management logic
- `data/blacklist.json` - Blacklist data storage

## CrewAI Agents

### Blacklist Management Agents
1. **Blacklist Manager**: Handles CRUD operations on the blacklist
2. **Threat Analyzer**: Analyzes and categorizes threats with risk assessment
3. **Report Generator**: Creates comprehensive reports and summaries
4. **Search Specialist**: Handles complex search queries and pattern matching

### Python Pro Agent
5. **Python Pro - Code Quality Expert**: Modern Python 3.12+ expert for:
   - **Code Review**: Comprehensive reviews with PEP 8, type hints, performance, and security analysis
   - **Code Optimization**: Performance, memory, and readability improvements
   - **Refactoring**: Apply SOLID principles, design patterns, and modern Python features
   - **Testing Strategy**: Design comprehensive test suites with pytest
   - **Modernization**: Upgrade code to Python 3.12+ with async/await, dataclasses, pattern matching, etc.

## Usage

The tool provides an interactive CLI with 15+ operations:

### Blacklist Operations (1-10)
- Add, remove, search, update, and list blacklist entries
- Generate reports and analyze threats
- View statistics and export/import data

### Python Pro Operations (11-15)
- **Option 11**: Review code for quality, performance, and security
- **Option 12**: Optimize code for performance, memory, or readability
- **Option 13**: Refactor code with modern patterns and best practices
- **Option 14**: Create comprehensive testing strategies
- **Option 15**: Modernize legacy code to Python 3.12+

## Example Workflows

### Blacklist Management
```bash
# Add a new threat with AI analysis
1. Select option 1
2. Enter threat details
3. AI analyzes threat level and categorizes it

# Generate a security report
1. Select option 6
2. Choose report type (summary, detailed, statistics)
3. AI generates comprehensive report
```

### Code Quality with Python Pro
```bash
# Review your Python code
1. Select option 11
2. Enter file path (e.g., blacklist.py)
3. Optionally specify focus areas (performance, security, etc.)
4. Receive detailed code review with recommendations

# Modernize legacy code
1. Select option 15
2. Enter file path
3. AI upgrades code to Python 3.12+ with modern features
```
