#!/usr/bin/env python3
"""
Quick Status Checker for AccessMate Project
Run this to check the current status of your project
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(cmd, description):
    """Run a command and return the result"""
    print(f"\n🔍 {description}")
    print(f"Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.stdout:
            print(f"✅ Output:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️ Errors:\n{result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def check_git_status():
    """Check git repository status"""
    print("\n" + "="*50)
    print("📋 GIT REPOSITORY STATUS")
    print("="*50)
    
    # Check if we're in a git repo
    run_command("git rev-parse --is-inside-work-tree", "Checking if in git repository")
    
    # Check remote URL
    run_command("git remote -v", "Checking remote repository URL")
    
    # Check recent commits
    run_command("git log --oneline -5", "Showing recent commits")
    
    # Check current status
    run_command("git status --porcelain", "Checking working directory status")

def check_python_processes():
    """Check for running Python processes"""
    print("\n" + "="*50)
    print("🐍 PYTHON PROCESSES")
    print("="*50)
    
    if os.name == 'nt':  # Windows
        run_command("tasklist /FI \"IMAGENAME eq python.exe\"", "Checking Python processes")
        run_command("tasklist /FI \"IMAGENAME eq pythonw.exe\"", "Checking Python GUI processes")
    else:  # Unix-like
        run_command("ps aux | grep python", "Checking Python processes")

def check_project_files():
    """Check important project files"""
    print("\n" + "="*50)
    print("📁 PROJECT FILES STATUS")
    print("="*50)
    
    important_files = [
        "src/main.py",
        "src/gui.py", 
        "mobial/main.py",
        ".github/workflows/android-build.yml",
        "buildozer.spec",
        "requirements.txt"
    ]
    
    for file in important_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ Missing: {file}")

def main():
    print("🚀 ACCESSMATE PROJECT STATUS CHECKER")
    print(f"⏰ Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 Current directory: {os.getcwd()}")
    
    check_git_status()
    check_python_processes()
    check_project_files()
    
    print("\n" + "="*50)
    print("✅ STATUS CHECK COMPLETE")
    print("="*50)
    print("\n📋 MANUAL NEXT STEPS:")
    print("1. Check GitHub Actions: https://github.com/[your-username]/[repo-name]/actions")
    print("2. Test desktop app if it's running")
    print("3. Wait for Android APK build to complete")
    print("\n🎯 If desktop app isn't running, try: python src/main.py")

if __name__ == "__main__":
    main()