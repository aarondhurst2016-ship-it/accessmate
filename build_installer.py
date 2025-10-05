#!/usr/bin/env python3
"""
AccessMate Installer Builder
Creates a proper Windows installer using Inno Setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def find_inno_setup():
    """Find Inno Setup installation"""
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def ensure_files_exist():
    """Ensure all required files exist for the installer"""
    required_files = [
        "dist/AccessMate.exe",
        "src/accessmate_logo_multisize.ico",
        "AccessMate-Installer.iss"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    
    return True

def create_license_file():
    """Create a basic LICENSE.txt if it doesn't exist"""
    if not os.path.exists("LICENSE.txt"):
        license_content = """AccessMate License

Copyright (C) 2025 AccessMate Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open("LICENSE.txt", "w", encoding="utf-8") as f:
            f.write(license_content)
        print("✅ Created LICENSE.txt")

def build_installer():
    """Build the Windows installer using Inno Setup"""
    print("🏗️  AccessMate Installer Builder")
    print("=" * 40)
    
    # Check if Inno Setup is installed
    iscc_path = find_inno_setup()
    if not iscc_path:
        print("❌ Inno Setup not found!")
        print("📥 Please install Inno Setup from: https://jrsoftware.org/isdownload.php")
        print("   Then run this script again.")
        return False
    
    print(f"✅ Found Inno Setup: {iscc_path}")
    
    # Ensure required files exist
    if not ensure_files_exist():
        print("\n🔧 Build the executable first:")
        print("   python build_windows.py")
        return False
    
    # Create license file if missing
    create_license_file()
    
    # Create installers directory
    os.makedirs("dist/installers", exist_ok=True)
    
    # Build the installer
    print("\n🔨 Building installer...")
    try:
        result = subprocess.run([
            iscc_path,
            "AccessMate-Installer.iss"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Installer built successfully!")
            
            # List created installers
            installer_dir = Path("dist/installers")
            if installer_dir.exists():
                installers = list(installer_dir.glob("*.exe"))
                if installers:
                    print("\n📦 Created installers:")
                    for installer in installers:
                        size = installer.stat().st_size / (1024*1024)  # MB
                        print(f"   • {installer.name} ({size:.1f} MB)")
                        print(f"     Location: {installer.resolve()}")
                        
            return True
        else:
            print("❌ Installer build failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def main():
    """Main function"""
    if not build_installer():
        print("\n💡 Troubleshooting:")
        print("1. Install Inno Setup: https://jrsoftware.org/isdownload.php")
        print("2. Build executable: python build_windows.py")
        print("3. Run this script again: python build_installer.py")
        sys.exit(1)
    
    print("\n🎉 Installer creation complete!")
    print("📁 Check the dist/installers/ folder for your installer")

if __name__ == "__main__":
    main()