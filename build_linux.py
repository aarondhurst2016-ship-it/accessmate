#!/usr/bin/env python3
"""
Linux Build Script for AccessMate
Creates a Linux executable with proper icon and desktop integration
"""

import PyInstaller.__main__
import sys
import os
import shutil
from pathlib import Path

def create_linux_icons():
    """Create Linux icons in various sizes"""
    try:
        from PIL import Image
        
        logo_path = os.path.join("src", "accessmate_logo.png")
        if not os.path.exists(logo_path):
            print("❌ Logo file not found")
            return False
            
        logo = Image.open(logo_path).convert("RGBA")
        
        # Linux icon sizes (freedesktop.org standard)
        sizes = [16, 22, 24, 32, 48, 64, 128, 256, 512]
        
        # Create hicolor icon theme structure
        icons_dir = "linux_icons"
        os.makedirs(icons_dir, exist_ok=True)
        
        for size in sizes:
            size_dir = os.path.join(icons_dir, f"{size}x{size}")
            os.makedirs(size_dir, exist_ok=True)
            
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            icon_path = os.path.join(size_dir, "accessmate.png")
            resized.save(icon_path, "PNG")
            print(f"  Created Linux icon: {icon_path} ({size}x{size})")
        
        # Create scalable SVG (optional - convert PNG to SVG-like)
        scalable_dir = os.path.join(icons_dir, "scalable")
        os.makedirs(scalable_dir, exist_ok=True)
        
        # Copy the largest PNG as scalable
        large_icon = logo.resize((512, 512), Image.Resampling.LANCZOS)
        scalable_path = os.path.join(scalable_dir, "accessmate.png")
        large_icon.save(scalable_path, "PNG")
        print(f"  Created scalable icon: {scalable_path}")
        
        return True
        
    except ImportError:
        print("❌ PIL not available for icon creation")
        return False
    except Exception as e:
        print(f"❌ Icon creation failed: {e}")
        return False

def create_desktop_file():
    """Create .desktop file for Linux application menu"""
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=AccessMate
GenericName=Accessibility Assistant
Comment=AI-powered accessibility assistant for vision, hearing, and mobility support
Keywords=accessibility;speech;vision;assistant;
Exec=accessmate
Icon=accessmate
Terminal=false
Categories=Accessibility;Utility;AudioVideo;
StartupNotify=true
MimeType=text/plain;audio/mpeg;image/png;image/jpeg;
StartupWMClass=AccessMate

[Desktop Action Settings]
Name=Settings
Exec=accessmate --settings
Icon=accessmate

[Desktop Action Emergency]
Name=Emergency SOS
Exec=accessmate --emergency
Icon=accessmate
"""
    
    desktop_path = "accessmate.desktop"
    with open(desktop_path, 'w') as f:
        f.write(desktop_content)
    
    print(f"✅ Created desktop file: {desktop_path}")
    return desktop_path

def create_appimage_appdir():
    """Create AppDir structure for AppImage (optional)"""
    appdir = "AccessMate.AppDir"
    os.makedirs(appdir, exist_ok=True)
    
    # Create basic AppDir structure
    dirs = ["usr/bin", "usr/share/applications", "usr/share/icons/hicolor"]
    for dir_path in dirs:
        os.makedirs(os.path.join(appdir, dir_path), exist_ok=True)
    
    print(f"✅ Created AppDir structure: {appdir}")
    return appdir

def build_linux_executable():
    """Build Linux executable"""
    print("AccessMate Linux Build Script")
    print("============================")
    
    if sys.platform == "win32":
        print("⚠️  Building Linux executable on Windows. Cross-compilation may not work.")
    elif sys.platform != "linux":
        print("⚠️  This script is optimized for Linux builds.")
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "src", "main_desktop.py")
    
    if not os.path.exists(main_script):
        print(f"❌ Main script not found: {main_script}")
        return False
    
    # Create icons and desktop file
    create_linux_icons()
    desktop_file = create_desktop_file()
    create_appimage_appdir()
    
    # PyInstaller arguments for Linux
    args = [
        "--onefile",
        "--name=accessmate",
        "--clean", 
        "--noconfirm",
        f"--add-data={os.path.join(script_dir, 'src')}{os.pathsep}src",
        f"--paths={os.path.join(script_dir, 'src')}",
    ]
    
    # Add icon (use the 256x256 version)
    icon_path = os.path.join("linux_icons", "256x256", "accessmate.png")
    if os.path.exists(icon_path):
        args.append(f"--icon={icon_path}")
    
    # Hidden imports for Linux
    hidden_imports = [
        "pyttsx3.drivers",
        "pyttsx3.drivers.espeak",    # Linux speech driver
        "pygame.mixer",
        "tkinter.messagebox", 
        "tkinter.filedialog",
        "PIL.Image",
        "PIL.ImageTk",
        "requests.adapters",
        "urllib3.util.retry",
        "gi.repository.Gtk",         # GTK for Linux GUI
        "gi.repository.GLib",        # GLib for Linux
    ]
    
    for module in hidden_imports:
        args.extend(["--hidden-import", module])
    
    args.append(main_script)
    
    print("Building Linux executable with arguments:")
    for arg in args:
        print(f"  {arg}")
    
    try:
        PyInstaller.__main__.run(args)
        
        executable_path = os.path.join("dist", "accessmate")
        if os.path.exists(executable_path):
            # Make executable
            os.chmod(executable_path, 0o755)
            
            print(f"\n✅ Linux executable created: {executable_path}")
            print(f"🖥️  Desktop file created: {desktop_file}")
            print("📱 Icons created for system integration")
            
            print("\n📋 Installation instructions:")
            print("1. Copy 'accessmate' to /usr/local/bin/ or ~/bin/")
            print("2. Copy 'accessmate.desktop' to ~/.local/share/applications/")
            print("3. Copy icons from 'linux_icons/' to ~/.local/share/icons/hicolor/")
            print("4. Run: update-desktop-database ~/.local/share/applications/")
            
            return True
        else:
            print("\n❌ Executable not found after build")
            return False
            
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    build_linux_executable()