#!/usr/bin/env python3
"""
Local Build Script - When GitHub Actions is unavailable
Builds AccessMate on your local machine for distribution
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors gracefully"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def main():
    """Main build process"""
    print("🏗️  AccessMate Local Build Script")
    print("=" * 40)
    
    # Detect platform
    current_platform = platform.system().lower()
    print(f"🖥️  Platform detected: {current_platform}")
    
    # Create directories
    os.makedirs("dist", exist_ok=True)
    os.makedirs("build", exist_ok=True)
    
    # Install minimal dependencies
    print("\n📦 Installing minimal dependencies...")
    deps = ["pyinstaller", "pillow", "requests", "pyttsx3", "gtts"]
    
    for dep in deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️  Failed to install {dep}, continuing anyway...")
    
    # Copy main file
    if not os.path.exists("src/main_desktop.py"):
        print("❌ src/main_desktop.py not found!")
        return False
    
    shutil.copy2("src/main_desktop.py", "src/main.py")
    print("✅ Copied main_desktop.py to main.py")
    
    # Build executable
    app_name = f"AccessMate-{current_platform.title()}"
    
    build_cmd = f"pyinstaller --onefile"
    
    # Platform-specific options
    if current_platform == "windows":
        build_cmd += " --windowed"
    
    build_cmd += f" --name={app_name} src/main.py --distpath=dist"
    
    if run_command(build_cmd, f"Building {app_name}"):
        print(f"\n🎉 Build completed successfully!")
        print(f"📁 Executable location: dist/{app_name}")
        
        # List built files
        dist_files = list(Path("dist").glob("*"))
        if dist_files:
            print("\n📋 Built files:")
            for file in dist_files:
                size = file.stat().st_size / (1024*1024)  # MB
                print(f"   • {file.name} ({size:.1f} MB)")
        
        return True
    else:
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)