# -*- coding: utf-8 -*-
# AccessMate Windows Executable Build Script
# This script creates a Windows executable with proper icon and metadata

import PyInstaller.__main__
import sys
import os
import tempfile

def create_version_info():
    """Create version info file for Windows executable"""
    version_info = """
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'AccessMate Team'),
        StringStruct(u'FileDescription', u'AccessMate - Accessibility Assistant'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'AccessMate'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2025 AccessMate Team'),
        StringStruct(u'OriginalFilename', u'AccessMate.exe'),
        StringStruct(u'ProductName', u'AccessMate'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    # Write version info to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(version_info)
        return f.name

def build_windows_exe():
    """Build Windows executable with proper configuration and metadata"""
    
    # Get version info file
    version_file = create_version_info()
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths
    main_script = os.path.join(script_dir, "src", "main_desktop.py")
    icon_path = os.path.join(script_dir, "src", "accessmate_logo.ico")
    
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
        f"--version-file={version_file}",  # Add version info for Windows
        "--uac-admin",         # Request admin privileges if needed for accessibility
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
    potential_hidden_imports = [
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
        "gtts",
        "gtts.tts",
        "gtts.lang",
        "httpx",
        "httpcore",
        "h11",
        "sniffio",
        "certifi",
    ]
    
    # Only include hidden imports for modules that are actually available
    hidden_imports = []
    for module in potential_hidden_imports:
        try:
            __import__(module)
            hidden_imports.append(module)
            print(f"[INFO] Including hidden import: {module}")
        except ImportError:
            print(f"[WARNING] Skipping unavailable module: {module}")
    
    for module in hidden_imports:
        args.extend(["--hidden-import", module])
    
    # Add the main script
    args.append(main_script)
    
    print("Building Windows executable with arguments:")
    for arg in args:
        print(f"  {arg}")
    
    try:
        PyInstaller.__main__.run(args)
        print("\n[SUCCESS] Windows executable built successfully!")
        print("[OUTPUT] dist/AccessMate.exe")
        print("[INFO] Includes version info for better Windows security recognition")
        print("[WARNING] Smart App Control may still block unsigned executables")
        print("[INFO] See SMART_APP_CONTROL_SOLUTION.md for bypass instructions")
        return True
    except Exception as e:
        print(f"\n[ERROR] Build failed: {e}")
        return False
    finally:
        # Clean up temporary version file
        try:
            os.unlink(version_file)
        except:
            pass

if __name__ == "__main__":
    print("AccessMate Windows Build Script")
    print("==============================")
    build_windows_exe()
