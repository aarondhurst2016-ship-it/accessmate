# Main entry point for AccessMate
# This file redirects to the appropriate platform-specific main file
# For desktop: use main_desktop.py (has welcome popup and voice setup)
# For mobile: use main_android.py (has mobile welcome and voice setup)

import sys
import os

def detect_platform():
    """Detect current platform and redirect to appropriate main"""
    try:
        # Check for Android environment
        if 'ANDROID_ROOT' in os.environ or hasattr(sys, 'platform') and sys.platform == 'android':
            print("Detected Android platform - launching mobile version with welcome system")
            from main_android import main
            main()
            return
        
        # Check for iOS (Kivy-iOS environment)
        try:
            import ios
            print("Detected iOS platform - launching mobile version with welcome system")
            from main_android import main
            main()
            return
        except ImportError:
            pass
        
        # Default to desktop version for Windows/macOS/Linux
        print("Detected desktop platform - launching desktop version with welcome system")
        from main_desktop import launch
        launch()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Falling back to basic console mode...")
        print("AccessMate - Comprehensive Accessibility Assistant")
        print("Please ensure all dependencies are installed.")
        input("Press Enter to exit...")

# Legacy support - maintain existing functionality for backwards compatibility
from battery_monitor import BatteryMonitor

# Windows startup option
def set_startup(enable=True):
    import sys, os
    if sys.platform.startswith('win'):
        import shutil
        import winreg
        exe_path = os.path.abspath(sys.argv[0])
        app_name = "TalkbackAssistantWin"
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as regkey:
            if enable:
                winreg.SetValueEx(regkey, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(regkey, app_name)
                except FileNotFoundError:
                    pass
        print(f"Startup {'enabled' if enable else 'disabled'}.")
    else:
        print("Startup option is only available on Windows.")

# Handle CLI startup command before anything else
import sys
if len(sys.argv) > 1 and sys.argv[1] == "startup":
    if len(sys.argv) == 3 and sys.argv[2] in ("on", "off"):
        set_startup(sys.argv[2] == "on")
    else:
        print("Usage: python main.py startup on|off")
    sys.exit(0)

# Windows startup option
def set_startup(enable=True):
    import sys, os
    if sys.platform.startswith('win'):
        import shutil
        import winreg
        exe_path = os.path.abspath(sys.argv[0])
        app_name = "TalkbackAssistantWin"
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as regkey:
            if enable:
                winreg.SetValueEx(regkey, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(regkey, app_name)
                except FileNotFoundError:
                    pass
        print(f"Startup {'enabled' if enable else 'disabled'}.")
    else:
        print("Startup option is only available on Windows.")


if __name__ == "__main__":  # Fixed: was **name** now __name__
    import sys
    import subprocess
    # Start the global screen reader in the background (if available)
    try:
        global_reader_path = os.path.join(os.path.dirname(__file__), "universal_screen_reader.py")
        if os.path.exists(global_reader_path):
            subprocess.Popen([sys.executable, global_reader_path])
    except Exception as e:
        print(f"[WARN] Could not start global screen reader: {e}")
    # Enable app to start on Windows startup
    try:
        set_startup(True)
    except Exception as e:
        print(f"[WARN] Could not set app to start on Windows startup: {e}")
    from settings import Settings
    user_settings = Settings()
    user_settings.load("user_settings.json")
    def print_features():
        toggles = [
            ("enable_barcode", "Barcode Scanner"),
            ("enable_object_detection", "Object Recognition"),
            ("enable_ocr", "OCR Screen Reader"),
            ("enable_face_recognition", "Face Recognition"),
            ("enable_currency_recognition", "Currency Recognition"),
            ("enable_color_recognition", "Color Recognition"),
            ("enable_pdf_reader", "PDF Reader"),
            ("enable_word_reader", "Word Reader"),
            ("enable_speech_recognition", "Speech Recognition"),
            ("enable_tts", "Text-to-Speech (TTS)"),
            ("enable_app_launch", "App Launcher"),
            ("enable_navigation", "Navigation"),
            ("enable_encryption", "Encryption"),
            ("enable_weather", "Weather"),
            ("enable_reminders", "Reminders"),
            ("enable_accessibility", "Accessibility"),
            ("enable_emergency_contact", "Emergency Contact"),
        ]
        print("Feature toggles:")
        for attr, label in toggles:
            print(f"  {label}: {'ON' if getattr(user_settings, attr, True) else 'OFF'}")
    if len(sys.argv) > 1 and sys.argv[1] == "features":
        if len(sys.argv) == 2:
            print_features()
        elif len(sys.argv) == 4 and sys.argv[2] in ("on", "off"):
            feature = sys.argv[3].lower().replace(" ", "_")
            attr = f"enable_{feature}"
            if hasattr(user_settings, attr):
                setattr(user_settings, attr, sys.argv[2] == "on")
                user_settings.save("user_settings.json")
                print(f"Set {attr} to {sys.argv[2].upper()}")
            else:
                print(f"Unknown feature: {feature}")
        else:
            print("Usage:\n  python main.py features\n  python main.py features on|off <feature_name>")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "startup":
        if len(sys.argv) == 3 and sys.argv[2] in ("on", "off"):
            set_startup(sys.argv[2] == "on")
        else:
            print("Usage: python main.py startup on|off")
        sys.exit(0)
    # Launch platform-specific main with welcome system
    detect_platform()

# To run the application, use the following commands:
# cd c:\Users\aaron\Talkback app\src
# python main.py
# See README.md for build instructions (PyInstaller, Inno Setup)
# See .github/copilot-instructions.md for project structure and dependencies
# The Inno Setup script has been moved to 'installer/TalkbackAssistant.iss'.
# Build your app with PyInstaller first:
# pyinstaller --onefile --windowed src/main.py
# Then run the .iss script with Inno Setup Compiler.

# The following block is for PyInstaller .spec files only and should not be in main.py
# a = Analysis(
#     ['src\\main.py'],
#     pathex=[os.path.abspath('src')],
#     # ...existing code...
# )