#!/usr/bin/env python3
"""
Mobile icon integration script for AccessMate
This script ensures icons are properly configured for Android and iOS builds
"""

import os
import json
import shutil

def setup_android_icons():
    """Setup Android icons in the buildozer build directory"""
    print("Setting up Android icons...")
    
    # Create android folder structure in src
    android_dir = os.path.join("src", "android")
    os.makedirs(android_dir, exist_ok=True)
    
    # Copy icon densities
    densities = ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
    
    for density in densities:
        src_icon = os.path.join("android_icons", f"mipmap-{density}", "ic_launcher.png")
        dest_dir = os.path.join(android_dir, f"mipmap-{density}")
        os.makedirs(dest_dir, exist_ok=True)
        dest_icon = os.path.join(dest_dir, "ic_launcher.png")
        
        if os.path.exists(src_icon):
            shutil.copy2(src_icon, dest_icon)
            print(f"  Copied {density} icon: {dest_icon}")
    
    print("Android icons setup complete")

def setup_ios_icons():
    """Setup iOS icons"""
    print("Setting up iOS icons...")
    
    # Create iOS folder structure
    ios_dir = os.path.join("src", "ios")
    os.makedirs(ios_dir, exist_ok=True)
    
    # Copy all iOS icons
    if os.path.exists("ios_icons"):
        for icon_file in os.listdir("ios_icons"):
            if icon_file.endswith(".png"):
                src_path = os.path.join("ios_icons", icon_file)
                dest_path = os.path.join(ios_dir, icon_file)
                shutil.copy2(src_path, dest_path)
                print(f"  Copied iOS icon: {dest_path}")
    
    print("iOS icons setup complete")

def update_buildozer_spec():
    """Update buildozer.spec with proper icon paths"""
    print("Updating buildozer.spec...")
    
    # Read current buildozer.spec
    spec_path = "buildozer.spec"
    if not os.path.exists(spec_path):
        print("buildozer.spec not found")
        return False
    
    with open(spec_path, 'r') as f:
        content = f.read()
    
    # Ensure proper icon configuration
    replacements = [
        ("icon.filename = %(source.dir)s/accessmate_logo.png", "icon.filename = %(source.dir)s/android_icon.png"),
        ("presplash.filename = %(source.dir)s/accessmate_logo.png", "presplash.filename = %(source.dir)s/android_icon.png"),
    ]
    
    for old, new in replacements:
        if old in content and new not in content:
            content = content.replace(old, new)
            print(f"  Updated: {old} -> {new}")
    
    # Add Android specific configurations if not present
    android_configs = [
        "\n# Android specific configurations for better icon support",
        "android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS",
        "android.api = 33",
        "android.minapi = 21",
        "android.ndk = 25b",
        "android.gradle_dependencies = com.google.android.material:material:1.6.1",
    ]
    
    # Add configs if not already present
    for config in android_configs:
        if config.split('=')[0].strip() not in content:
            content += f"\n{config}"
    
    # Write back to file
    with open(spec_path, 'w') as f:
        f.write(content)
    
    print("buildozer.spec updated")
    return True

def create_windows_task():
    """Update VS Code tasks for Windows builds with proper icon"""
    print("Creating Windows build task...")
    
    tasks_dir = ".vscode"
    os.makedirs(tasks_dir, exist_ok=True)
    
    tasks_file = os.path.join(tasks_dir, "tasks.json")
    
    # Windows build task with proper icon
    windows_task = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Build AccessMate Windows",
                "type": "shell", 
                "command": "python",
                "args": ["build_windows.py"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                },
                "problemMatcher": []
            },
            {
                "label": "Build AccessMate Android",
                "type": "shell",
                "command": "buildozer",
                "args": ["android", "debug"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always", 
                    "focus": False,
                    "panel": "shared"
                },
                "problemMatcher": []
            }
        ]
    }
    
    with open(tasks_file, 'w') as f:
        json.dump(windows_task, f, indent=2)
    
    print(f"VS Code tasks created: {tasks_file}")

def main():
    print("AccessMate Mobile Icon Integration")
    print("=================================")
    
    # Check if we're in the right directory
    if not os.path.exists("src") or not os.path.exists("buildozer.spec"):
        print("Run this script from the AccessMate root directory")
        return
    
    # Setup platform icons
    setup_android_icons()
    setup_ios_icons() 
    update_buildozer_spec()
    create_windows_task()
    
    print("\n🎉 Icon integration complete!")
    print("\nNext steps:")
    print("1. Build Android: buildozer android debug")
    print("2. Build Windows: python build_windows.py")
    print("3. Icons will now appear on device home screens")

if __name__ == "__main__":
    main()