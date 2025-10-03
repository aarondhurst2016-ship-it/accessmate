#!/usr/bin/env python3
"""
Dependency checker and installer for Talkback Assistant
Run this before running the main application
"""

import subprocess
import sys
import importlib

# Required packages
REQUIRED_PACKAGES = [
    'pyttsx3',
    'speechrecognition', 
    'pygame',
    'requests',
    'pyaudio'  # Needed for microphone input
]

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def check_package(package):
    """Check if a package is installed"""
    try:
        if package == 'speechrecognition':
            importlib.import_module('speech_recognition')
        else:
            importlib.import_module(package)
        print(f"✓ {package} is already installed")
        return True
    except ImportError:
        print(f"✗ {package} is not installed")
        return False

def main():
    """Main dependency check and install function"""
    print("Checking Talkback Assistant dependencies...")
    print("=" * 50)
    
    missing_packages = []
    
    # Check each required package
    for package in REQUIRED_PACKAGES:
        if not check_package(package):
            missing_packages.append(package)
    
    # Install missing packages
    if missing_packages:
        print(f"\nInstalling {len(missing_packages)} missing packages...")
        print("=" * 50)
        
        for package in missing_packages:
            print(f"Installing {package}...")
            install_package(package)
    else:
        print("\n✓ All required packages are installed!")
    
    # Test critical imports
    print("\nTesting critical imports...")
    print("=" * 30)
    
    try:
        import pyttsx3
        print("✓ Text-to-Speech engine available")
    except ImportError:
        print("❌ pyttsx3 not found - speech features may not work")
        
    try:
        import speech_recognition
        print("✓ Speech recognition available")
    except ImportError:
        print("❌ speech_recognition not found - voice commands may not work")
        
    print("\n" + "=" * 30)
    print("Installation check complete!")


if __name__ == "__main__":
    main()