#!/usr/bin/env python3
"""
Simple fallback build script for CI environments
Creates basic executables when complex build scripts fail
"""

import os
import sys
import subprocess
import shutil

def simple_build():
    """Build with minimal dependencies and maximum compatibility"""
    
    print("🔧 Starting simple fallback build...")
    
    # Ensure we have src/main.py
    if not os.path.exists("src/main.py"):
        if os.path.exists("src/main_desktop.py"):
            shutil.copy("src/main_desktop.py", "src/main.py")
            print("✅ Copied main_desktop.py to main.py")
        else:
            print("❌ No main file found!")
            return False
    
    # Create dist directory
    os.makedirs("dist", exist_ok=True)
    
    # Platform-specific build
    if sys.platform.startswith("win"):
        return build_windows()
    elif sys.platform.startswith("darwin"):
        return build_macos()
    elif sys.platform.startswith("linux"):
        return build_linux()
    else:
        print(f"❌ Unsupported platform: {sys.platform}")
        return False

def build_windows():
    """Simple Windows build"""
    print("🖥️  Building for Windows...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed", 
        "--name=AccessMate",
        "--add-data=src;src",
        "--hidden-import=tkinter",
        "--hidden-import=pyttsx3",
        "--hidden-import=gtts",
        "--distpath=dist",
        "src/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Windows build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def build_macos():
    """Simple macOS build"""
    print("🍎 Building for macOS...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=AccessMate", 
        "--add-data=src:src",
        "--hidden-import=tkinter",
        "--hidden-import=pyttsx3",
        "--hidden-import=gtts",
        "--distpath=dist",
        "src/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ macOS build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS build failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def build_linux():
    """Simple Linux build"""
    print("🐧 Building for Linux...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=AccessMate",
        "--add-data=src:src", 
        "--hidden-import=tkinter",
        "--hidden-import=pyttsx3",
        "--hidden-import=gtts",
        "--distpath=dist",
        "src/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Linux build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Linux build failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

if __name__ == "__main__":
    success = simple_build()
    sys.exit(0 if success else 1)