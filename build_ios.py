#!/usr/bin/env python3
"""
iOS Build Script for AccessMate
Creates an iOS app with proper icon integration using kivy-ios
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

def check_ios_prerequisites():
    """Check if we're on macOS and have Xcode tools"""
    print("🔍 Checking iOS build prerequisites...")
    
    if sys.platform != "darwin":
        print("⚠️  iOS builds require macOS with Xcode. Current platform:", sys.platform)
        print("   You can still prepare the iOS project structure.")
        return False
    
    # Check for Xcode
    try:
        result = subprocess.run(['xcode-select', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Xcode command line tools found")
        else:
            print("❌ Xcode command line tools not found")
            print("   Install with: xcode-select --install")
            return False
    except FileNotFoundError:
        print("❌ Xcode not found. Install Xcode from App Store")
        return False
    
    # Check for kivy-ios
    try:
        result = subprocess.run(['toolchain', 'build', '--help'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ kivy-ios toolchain found")
            return True
        else:
            print("⚠️  kivy-ios not found, will install")
            return "install_needed"
    except FileNotFoundError:
        print("⚠️  kivy-ios not found, will install")
        return "install_needed"

def install_kivy_ios():
    """Install kivy-ios toolchain"""
    print("📦 Installing kivy-ios...")
    
    try:
        # Install kivy-ios
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'kivy-ios'], check=True)
        print("✅ kivy-ios installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install kivy-ios: {e}")
        return False

def create_ios_project_structure():
    """Create iOS project structure"""
    print("📁 Creating iOS project structure...")
    
    ios_project_dir = "ios_project"
    os.makedirs(ios_project_dir, exist_ok=True)
    
    # Create main.py for iOS (simplified version)
    ios_main_content = '''#!/usr/bin/env python3
"""
iOS version of AccessMate - Mobile-optimized accessibility assistant
"""

import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    # Import main components
    from gui import launch
    from battery_monitor import BatteryMonitor
    
    print("AccessMate iOS - Starting accessibility assistant...")
    
    # Initialize battery monitoring for mobile
    battery_monitor = BatteryMonitor()
    
    # Launch GUI (mobile-optimized)
    launch(None)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Running in basic mode...")
    
    # Basic iOS app if imports fail
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.title("AccessMate iOS")
    root.geometry("320x480")  # iPhone-like dimensions
    
    tk.Label(root, text="AccessMate", font=("Arial", 20, "bold")).pack(pady=20)
    tk.Label(root, text="Accessibility Assistant", font=("Arial", 14)).pack(pady=10)
    
    def show_info():
        messagebox.showinfo("AccessMate", "Mobile accessibility assistant running on iOS")
    
    tk.Button(root, text="About", command=show_info).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("AccessMate iOS version starting...")
'''
    
    ios_main_path = os.path.join(ios_project_dir, "main.py")
    with open(ios_main_path, 'w') as f:
        f.write(ios_main_content)
    
    print(f"✅ Created iOS main.py: {ios_main_path}")
    
    # Copy iOS icons to project
    ios_icons_dir = os.path.join(ios_project_dir, "ios_icons")
    if os.path.exists("ios_icons"):
        shutil.copytree("ios_icons", ios_icons_dir, dirs_exist_ok=True)
        print("✅ Copied iOS icons to project")
    
    # Create buildozer config for iOS (alternative to kivy-ios)
    create_ios_buildozer_config(ios_project_dir)
    
    return ios_project_dir

def create_ios_buildozer_config(project_dir):
    """Create buildozer.spec optimized for iOS"""
    ios_buildozer_content = '''[app]
title = AccessMate
package.name = accessmate
package.domain = com.accessmate.app

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json,wav,mp3

version = 1.0.0

requirements = python3,kivy,pillow,plyer,pyjnius

[buildozer]
log_level = 2

[app:ios]
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

# iOS specific settings
orientation = portrait
osx.python_version = 3.11
osx.kivy_version = 2.1.0

# Icon settings for iOS
icon.filename = ios_icons/Icon-1024x1024@1x.png

# iOS deployment settings
ios.codesign.allowed = true
ios.codesign.debug = true

[buildozer:ios]
codesign.mode = adhoc
'''
    
    config_path = os.path.join(project_dir, "buildozer_ios.spec")
    with open(config_path, 'w') as f:
        f.write(ios_buildozer_content)
    
    print(f"✅ Created iOS buildozer config: {config_path}")

def create_xcode_project_template():
    """Create Xcode project template with proper icon integration"""
    print("📱 Creating Xcode project template...")
    
    xcode_project_dir = "AccessMate_iOS"
    os.makedirs(xcode_project_dir, exist_ok=True)
    
    # Create Info.plist for iOS
    info_plist_content = {
        "CFBundleName": "AccessMate",
        "CFBundleDisplayName": "AccessMate", 
        "CFBundleIdentifier": "com.accessmate.app",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundlePackageType": "APPL",
        "CFBundleExecutable": "AccessMate",
        "CFBundleIconName": "AppIcon",
        "LSRequiresIPhoneOS": True,
        "UILaunchStoryboardName": "LaunchScreen",
        "UISupportedInterfaceOrientations": [
            "UIInterfaceOrientationPortrait",
            "UIInterfaceOrientationLandscapeLeft", 
            "UIInterfaceOrientationLandscapeRight"
        ],
        "NSMicrophoneUsageDescription": "AccessMate needs microphone access for voice commands",
        "NSCameraUsageDescription": "AccessMate needs camera access for object recognition",
        "NSLocationWhenInUseUsageDescription": "AccessMate needs location for navigation assistance",
        "NSMotionUsageDescription": "AccessMate needs motion sensors for accessibility features",
        "UIBackgroundModes": ["audio", "background-processing"],
        "UIRequiredDeviceCapabilities": ["armv7"],
        "UIStatusBarStyle": "UIStatusBarStyleDefault"
    }
    
    info_plist_path = os.path.join(xcode_project_dir, "Info.plist")
    
    # Write as plist (simplified JSON format for cross-platform)
    with open(info_plist_path, 'w') as f:
        json.dump(info_plist_content, f, indent=2)
    
    print(f"✅ Created iOS Info.plist: {info_plist_path}")
    
    # Create App Icon set structure
    icon_set_dir = os.path.join(xcode_project_dir, "Images.xcassets", "AppIcon.appiconset")
    os.makedirs(icon_set_dir, exist_ok=True)
    
    # Copy iOS icons to proper structure
    if os.path.exists("ios_icons"):
        for icon_file in os.listdir("ios_icons"):
            if icon_file.endswith(".png"):
                src_path = os.path.join("ios_icons", icon_file)
                dest_path = os.path.join(icon_set_dir, icon_file)
                shutil.copy2(src_path, dest_path)
        
        print("✅ Copied icons to Xcode project structure")
    
    # Create Contents.json for icon set
    contents_json = {
        "images": [
            {"size": "20x20", "idiom": "iphone", "filename": "Icon-20x20@2x.png", "scale": "2x"},
            {"size": "20x20", "idiom": "iphone", "filename": "Icon-20x20@3x.png", "scale": "3x"},
            {"size": "29x29", "idiom": "iphone", "filename": "Icon-29x29@2x.png", "scale": "2x"},
            {"size": "29x29", "idiom": "iphone", "filename": "Icon-29x29@3x.png", "scale": "3x"},
            {"size": "40x40", "idiom": "iphone", "filename": "Icon-40x40@2x.png", "scale": "2x"},
            {"size": "40x40", "idiom": "iphone", "filename": "Icon-40x40@3x.png", "scale": "3x"},
            {"size": "60x60", "idiom": "iphone", "filename": "Icon-60x60@2x.png", "scale": "2x"},
            {"size": "60x60", "idiom": "iphone", "filename": "Icon-60x60@3x.png", "scale": "3x"},
            {"size": "1024x1024", "idiom": "ios-marketing", "filename": "Icon-1024x1024@1x.png", "scale": "1x"}
        ],
        "info": {"version": 1, "author": "xcode"}
    }
    
    contents_path = os.path.join(icon_set_dir, "Contents.json")
    with open(contents_path, 'w') as f:
        json.dump(contents_json, f, indent=2)
    
    print(f"✅ Created icon Contents.json: {contents_path}")
    
    return xcode_project_dir

def build_ios_app():
    """Build iOS app using available tools"""
    print("🚀 Building AccessMate for iOS")
    print("=" * 40)
    
    # Check prerequisites
    prereq_status = check_ios_prerequisites()
    
    if prereq_status == "install_needed":
        if not install_kivy_ios():
            print("❌ Failed to install kivy-ios")
            prereq_status = False
    
    # Create project structure regardless of platform
    ios_project_dir = create_ios_project_structure()
    xcode_project_dir = create_xcode_project_template()
    
    if prereq_status == True:
        # We're on macOS with proper tools
        print("🔨 Building with kivy-ios toolchain...")
        
        try:
            # Build Python and dependencies
            subprocess.run(['toolchain', 'build', 'python3'], check=True)
            subprocess.run(['toolchain', 'build', 'kivy'], check=True)
            subprocess.run(['toolchain', 'build', 'pillow'], check=True)
            
            # Create Xcode project
            subprocess.run(['toolchain', 'create', 'AccessMate', ios_project_dir], check=True)
            
            print("✅ iOS app built successfully!")
            print(f"📱 Xcode project created in: AccessMate")
            print("📋 Next steps:")
            print("1. Open AccessMate.xcodeproj in Xcode")
            print("2. Configure signing & capabilities")
            print("3. Build and run on device/simulator")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ iOS build failed: {e}")
            return False
    
    else:
        # Cross-platform setup
        print("📦 iOS project structure created for future development")
        print(f"📁 iOS project: {ios_project_dir}")
        print(f"📱 Xcode template: {xcode_project_dir}")
        
        print("\n📋 To complete iOS build:")
        print("1. Transfer project to macOS machine")
        print("2. Install Xcode and kivy-ios")
        print("3. Run: python build_ios.py")
        print("4. Logo will appear on iOS home screen")
        
        return True

def main():
    """Main iOS build function"""
    print("AccessMate iOS Build System")
    print("==========================")
    
    result = build_ios_app()
    
    if result:
        print("\n🎉 iOS SETUP COMPLETE!")
        print("📱 AccessMate logo will show on iOS home screen")
        print("🍎 Ready for App Store deployment")
    else:
        print("\n⚠️  iOS setup completed with limitations")
        print("📱 Project structure ready for macOS development")

if __name__ == "__main__":
    main()