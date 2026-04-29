# Flashcard Generator

Flashcard Generator is a script desktop application developed in Python designed to facilitate mnemonic learning through customizable card decks.

## Technical Specifications
*   **User Interface**: Developed using CustomTkinter for a modern dark-mode experience.
*   **Data Management**: Powered by SQLite with full referential integrity and parameterized queries.
*   **Data Visualization**: Integrated performance tracking via Matplotlib bar charts.
*   **Export Logic**: Capability to generate A4 PDF documents in a two-column layout (Front/Back) using ReportLab. 

## System Requirements

The software requires Python 3.x and the appropriate system-level graphics libraries for Tkinter.

### Python Dependencies
Required libraries are listed in `requirements.txt` and include:
*   customtkinter
*   reportlab
*   pillow
*   matplotlib

## Installation Guide

### Linux (Fedora)
1. Install system dependencies:
   ```bash
   sudo dnf install python3-tkinter python3-pillow-tk python3-matplotlib-tk
   ```
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Linux (Ubuntu/Debian)
1. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-tk
   ```
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### macOS
1. Install Python (if not present) using Homebrew:
   ```bash
   brew install python tcl-tk
   ```
2. Install Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

### Windows
1. Download and install Python from [python.org](https://www.python.org/downloads/). Ensure the "Add Python to PATH" and "tcl/tk and IDLE" options are checked during installation.
2. Open PowerShell or Command Prompt and install packages:
   ```powershell
   pip install -r requirements.txt
   ```

## Execution

To start the application, navigate to the project root directory and run:

```bash
python3 flashcard_app/main.py
```

## Project Structure

*   `flashcard_app/main.py`: Application entry point and main window.
*   `flashcard_app/database.py`: Data persistence layer and SQLite management.
*   `flashcard_app/ui/`: Graphical user interface components.
*   `flashcard_app/export/`: Modules for PDF and image generation.
*   `flashcard_app/assets/`: Graphics resources and theme configurations.

## License

This project is distributed under the MIT License. Refer to the `LICENSE` file for further details.
