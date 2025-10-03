# Cross-Platform Setup Instructions for Talkback Assistant

## Supported Platforms
- Windows 10/11
- macOS (10.15+)
- Linux (Ubuntu, Fedora, Debian, etc.)

## Prerequisites
- Python 3.8+
- Internet connection (for speech and integrations)

## Install Dependencies

### Windows
1. Install Python from https://python.org
2. Open Command Prompt or PowerShell
3. Run:
   pip install -r requirements.txt

### macOS
1. Install Python (brew install python or from https://python.org)
2. Open Terminal
3. Run:
   pip3 install -r requirements.txt

### Linux
1. Install Python (sudo apt install python3 python3-pip)
2. Open Terminal
3. Run:
   pip3 install -r requirements.txt
4. For Tkinter: sudo apt install python3-tk
5. For microphone/sound: sudo apt install portaudio19-dev python3-pyaudio

## Run Platform Check
To verify all dependencies and platform compatibility, run:

    python src/platform_check.py

## Launch the App

    python src/main.py

## Troubleshooting
- If you see missing dependency errors, install the required package using pip.
- For microphone issues, check sound drivers and permissions.
- On Linux, you may need to install additional sound and GUI packages.

## Notes
- All features (GUI, speech, integrations) are designed to work on all platforms.
- If you encounter platform-specific issues, please report them in the project issues.
