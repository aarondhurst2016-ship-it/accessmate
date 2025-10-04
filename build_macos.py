#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS Build Script for AccessMate
Creates a macOS app bundle with proper icon and metadata
"""

import PyInstaller.__main__
import sys
import os
import shutil
import plistlib
from pathlib import Path

def create_icns_icon():
    """Create macOS ICNS icon from PNG"""
    try:
        from PIL import Image
        import subprocess
        
        # Path to source logo
        logo_path = os.path.join("src", "accessmate_logo.png")
        if not os.path.exists(logo_path):
            print("Logo file not found")
            return None
            
        # Create iconset directory
        iconset_dir = "AccessMate.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        # macOS icon sizes
        sizes = [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"), 
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png")
        ]
        
        # Load and resize logo for each size
        logo = Image.open(logo_path).convert("RGBA")
        
        for size, filename in sizes:
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(os.path.join(iconset_dir, filename), "PNG")
            print(f"  Created {filename} ({size}x{size})")
        
        # Convert to ICNS using iconutil (macOS only)
        if sys.platform == "darwin":
            icns_path = "src/accessmate_logo.icns"
            result = subprocess.run([
                "iconutil", "-c", "icns", iconset_dir, "-o", icns_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Created macOS icon: {icns_path}")
                # Clean up iconset directory
                shutil.rmtree(iconset_dir)
                return icns_path
            else:
                print(f"iconutil failed: {result.stderr}")
                return None
        else:
            print("⚠️  iconutil not available (not on macOS), keeping PNG files")
            return None
            
    except ImportError:
        print("PIL not available for icon creation")
        return None
    except Exception as e:
        print(f"Icon creation failed: {e}")
        return None

def create_info_plist(app_path):
    """Create Info.plist for the macOS app"""
    info_plist = {
        'CFBundleName': 'AccessMate',
        'CFBundleDisplayName': 'AccessMate',
        'CFBundleIdentifier': 'com.accessmate.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'AMAT',
        'CFBundleExecutable': 'AccessMate',
        'CFBundleIconFile': 'accessmate_logo.icns',
        'LSMinimumSystemVersion': '10.14',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSApplicationCategoryType': 'public.app-category.accessibility',
        'NSMicrophoneUsageDescription': 'AccessMate needs microphone access for voice commands and speech recognition',
        'NSCameraUsageDescription': 'AccessMate needs camera access for object recognition and barcode scanning',
        'NSLocationUsageDescription': 'AccessMate needs location access for navigation assistance',
        'NSAppleEventsUsageDescription': 'AccessMate needs automation access for accessibility features',
        'NSSystemAdministrationUsageDescription': 'AccessMate needs admin access for system accessibility features'
    }
    
    plist_path = os.path.join(app_path, "Contents", "Info.plist")
    os.makedirs(os.path.dirname(plist_path), exist_ok=True)
    
    with open(plist_path, 'wb') as f:
        plistlib.dump(info_plist, f)
    
    print(f"Created Info.plist: {plist_path}")

def build_macos_app():
    """Build macOS app bundle"""
    print("AccessMate macOS Build Script")
    print("============================")
    
    if sys.platform != "darwin":
        print("⚠️  This script is designed for macOS. Cross-compilation may not work properly.")
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "src", "main_desktop.py")
    
    if not os.path.exists(main_script):
        print(f"Main script not found: {main_script}")
        return False
    
    # Create icon
    icns_path = create_icns_icon()
    
    # PyInstaller arguments for macOS
    args = [
        "--onefile",
        "--windowed", 
        "--name=AccessMate",
        "--clean",
        "--noconfirm",
        f"--add-data={os.path.join(script_dir, 'src')}{os.pathsep}src",
        f"--paths={os.path.join(script_dir, 'src')}",
        "--target-arch=universal2",  # Build for both Intel and Apple Silicon
    ]
    
    # Add icon if available
    if icns_path and os.path.exists(icns_path):
        args.append(f"--icon={icns_path}")
    
    # Hidden imports for macOS
    potential_hidden_imports = [
        "pyttsx3.drivers",
        "pyttsx3.drivers.nsss",  # macOS speech driver
        "pygame.mixer",
        "tkinter.messagebox",
        "tkinter.filedialog", 
        "PIL.Image",
        "PIL.ImageTk",
        "requests.adapters",
        "urllib3.util.retry",
        "Foundation",  # macOS framework
        "Cocoa",       # macOS framework
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
    
    args.append(main_script)
    
    print("Building macOS app with arguments:")
    for arg in args:
        print(f"  {arg}")
    
    try:
        PyInstaller.__main__.run(args)
        
        # Create proper app bundle structure
        app_path = os.path.join("dist", "AccessMate.app")
        if os.path.exists(app_path):
            create_info_plist(app_path)
            print(f"\n[SUCCESS] macOS app created: {app_path}")
            print("[INFO] App will show proper icon in Dock and Finder")
            return True
        else:
            print("\nApp bundle not found after build")
            return False
            
    except Exception as e:
        print(f"\nBuild failed: {e}")
        return False

if __name__ == "__main__":
    build_macos_app()
