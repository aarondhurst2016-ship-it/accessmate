# mac_linux_entry.py
# Entry point for Talkback Assistant on macOS and Linux

import sys
import platform

def main():
    if platform.system() in ["Darwin", "Linux"]:
        try:
            from src import gui
            gui.launch_gui()
        except Exception as e:
            print(f"Error launching GUI: {e}")
    else:
        print("This entry point is for macOS and Linux only.")

if __name__ == "__main__":
    main()
