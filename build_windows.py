# AccessMate Windows Executable Build Script
# This script creates a Windows executable with proper icon

import PyInstaller.__main__
import sys
import os

def build_windows_exe():
    """Build Windows executable with proper configuration"""
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths
    main_script = os.path.join(script_dir, "src", "main_desktop.py")
    icon_path = os.path.join(script_dir, "src", "accessmate_logo_multisize.ico")
    
    # Verify files exist
    if not os.path.exists(main_script):
        print(f"Error: Main script not found at {main_script}")
        return False
    
    if not os.path.exists(icon_path):
        print(f"Warning: Icon not found at {icon_path}, building without icon")
        icon_path = None
    
    # PyInstaller arguments
    args = [
        "--onefile",           # Create single executable
        "--windowed",          # No console window (GUI app)
        "--name=AccessMate",   # Executable name
        "--clean",             # Clean build
        "--noconfirm",         # Don't ask for confirmation
    ]
    
    # Add icon if available
    if icon_path:
        args.append(f"--icon={icon_path}")
    
    # Add paths for imports
    args.extend([
        f"--add-data={os.path.join(script_dir, 'src')}{os.pathsep}src",
        f"--paths={os.path.join(script_dir, 'src')}",
    ])
    
    # Hidden imports for modules that might not be detected
    hidden_imports = [
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "pygame.mixer",
        "tkinter.messagebox",
        "tkinter.filedialog",
        "PIL.Image",
        "PIL.ImageTk",
        "requests.adapters",
        "urllib3.util.retry",
        "googletrans",
        "googletrans.client",
        "googletrans.constants",
        "googletrans.models",
        "httpx",
        "httpcore",
        "h11",
        "sniffio",
        "certifi",
    ]
    
    for module in hidden_imports:
        args.extend(["--hidden-import", module])
    
    # Add the main script
    args.append(main_script)
    
    print("Building Windows executable with arguments:")
    for arg in args:
        print(f"  {arg}")
    
    try:
        PyInstaller.__main__.run(args)
        print(f"\nBuild completed! Check the 'dist' folder for AccessMate.exe")
        return True
    except Exception as e:
        print(f"\nBuild failed: {e}")
        return False

if __name__ == "__main__":
    print("AccessMate Windows Build Script")
    print("==============================")
    build_windows_exe()
