#!/usr/bin/env python3
"""
Portable Windows Build Script for AccessMate
Creates a portable version that's less likely to trigger Smart App Control
"""

import PyInstaller.__main__
import sys
import os
import tempfile
import shutil
from pathlib import Path

def create_portable_structure():
    """Create portable app directory structure"""
    portable_dir = Path("dist/AccessMate_Portable")
    portable_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (portable_dir / "data").mkdir(exist_ok=True)
    (portable_dir / "settings").mkdir(exist_ok=True)
    (portable_dir / "logs").mkdir(exist_ok=True)
    
    return portable_dir

def create_portable_launcher():
    """Create a portable launcher script"""
    launcher_content = '''@echo off
title AccessMate Portable
echo Starting AccessMate in Portable Mode...
echo.

REM Set portable mode environment variable
set ACCESSMATE_PORTABLE=1
set ACCESSMATE_DATA_DIR=%~dp0data
set ACCESSMATE_SETTINGS_DIR=%~dp0settings
set ACCESSMATE_LOGS_DIR=%~dp0logs

REM Create directories if they don't exist
if not exist "%ACCESSMATE_DATA_DIR%" mkdir "%ACCESSMATE_DATA_DIR%"
if not exist "%ACCESSMATE_SETTINGS_DIR%" mkdir "%ACCESSMATE_SETTINGS_DIR%"
if not exist "%ACCESSMATE_LOGS_DIR%" mkdir "%ACCESSMATE_LOGS_DIR%"

REM Run AccessMate
"%~dp0AccessMate.exe" %*

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo AccessMate exited with error code %errorlevel%
    echo See logs directory for more information.
    echo.
    pause
)
'''
    return launcher_content

def create_version_info_portable():
    """Create version info file for portable Windows executable"""
    version_info = """
# UTF-8
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
        StringStruct(u'FileDescription', u'AccessMate Portable - Accessibility Assistant'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'AccessMate'),
        StringStruct(u'LegalCopyright', u'Copyright © 2025 AccessMate Team'),
        StringStruct(u'OriginalFilename', u'AccessMate.exe'),
        StringStruct(u'ProductName', u'AccessMate Portable'),
        StringStruct(u'ProductVersion', u'1.0.0.0'),
        StringStruct(u'Comments', u'Portable accessibility assistant - no installation required')])])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(version_info)
        return f.name

def build_portable_exe():
    """Build portable Windows executable"""
    
    print("🚀 Building AccessMate Portable Edition...")
    print("=" * 50)
    
    # Get version info file
    version_file = create_version_info_portable()
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths
    main_script = os.path.join(script_dir, "src", "main_desktop.py")
    icon_path = os.path.join(script_dir, "src", "accessmate_logo_multisize.ico")
    
    # Verify files exist
    if not os.path.exists(main_script):
        print(f"❌ Error: Main script not found at {main_script}")
        return False
    
    if not os.path.exists(icon_path):
        print(f"⚠️  Warning: Icon not found at {icon_path}, building without icon")
        icon_path = None
    
    # Create portable directory structure
    portable_dir = create_portable_structure()
    
    # PyInstaller arguments for portable build
    args = [
        "--onefile",           # Create single executable
        "--windowed",          # No console window (GUI app)
        "--name=AccessMate",   # Executable name
        "--clean",             # Clean build
        "--noconfirm",         # Don't ask for confirmation
        f"--version-file={version_file}",  # Add version info
        f"--distpath={portable_dir}",      # Output to portable directory
        "--specpath=build",    # Put spec files in build directory
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
        # googletrans and its dependencies
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
    
    args.append(main_script)
    
    print("Building portable executable with arguments:")
    for arg in args:
        print(f"  {arg}")
    
    try:
        PyInstaller.__main__.run(args)
        
        # Create launcher script
        launcher_script = portable_dir / "AccessMate_Portable.bat"
        with open(launcher_script, 'w', encoding='utf-8') as f:
            f.write(create_portable_launcher())
        
        # Create README for portable version
        readme_content = """# AccessMate Portable Edition

## 🚀 Quick Start

1. Run `AccessMate_Portable.bat` to launch AccessMate
2. Or double-click `AccessMate.exe` directly

## 📁 Portable Features

- **No Installation Required**: Run directly from any folder
- **Portable Settings**: All settings saved in `settings/` folder
- **Portable Data**: User data stored in `data/` folder  
- **Portable Logs**: Log files saved in `logs/` folder
- **Move Anywhere**: Copy entire folder to USB drive or other computer

## 🛡️ Smart App Control Issues?

If Windows blocks AccessMate:

1. **Right-click** on `AccessMate.exe`
2. Select **Properties** → **Security** tab
3. Check **"Unblock"** if available
4. Click **OK**

Or run `AccessMate_Portable.bat` which may bypass some restrictions.

## 📖 More Help

See `SMART_APP_CONTROL_SOLUTION.md` in the main directory for detailed instructions.

---
AccessMate Portable v1.0.0 - No installation, maximum accessibility!
"""
        
        readme_path = portable_dir / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("\n✅ Portable Windows build completed successfully!")
        print(f"📁 Output: {portable_dir}")
        print("🚀 Run AccessMate_Portable.bat to launch")
        print("📦 Copy entire folder for truly portable usage")
        print("🛡️ Less likely to trigger Smart App Control restrictions")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Portable build failed: {e}")
        return False
    finally:
        # Clean up temporary version file
        try:
            os.unlink(version_file)
        except:
            pass

if __name__ == "__main__":
    print("AccessMate Portable Windows Build Script")
    print("========================================")
    build_portable_exe()