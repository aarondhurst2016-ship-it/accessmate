#!/usr/bin/env python3
"""
Test script to verify that AccessMate can build in CI environments
This simulates the build process with minimal dependencies
"""

import sys
import os
import importlib

def test_import(module_name, description):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {description}: {module_name} - {e}")
        return False

def test_ci_build():
    """Test CI build compatibility"""
    print("🔍 Testing CI Build Compatibility")
    print("=" * 50)
    
    # Test essential imports
    essential_imports = [
        ("tkinter", "GUI Framework"),
        ("pyttsx3", "Text-to-Speech"),
        ("requests", "HTTP Requests"),
        ("PIL", "Image Processing (Pillow)"),
        ("gtts", "Google Text-to-Speech"),
        ("bs4", "Web Scraping (BeautifulSoup4)"),
    ]
    
    # Test optional imports (should gracefully fail)
    optional_imports = [
        ("pygame", "Game Engine"),
        ("kivy", "Mobile GUI Framework"),
        ("pyaudio", "Audio Processing"),
        ("sounddevice", "Sound Device"),
    ]
    
    essential_success = 0
    optional_success = 0
    
    print("\\n📋 Essential Dependencies:")
    for module, desc in essential_imports:
        if test_import(module, desc):
            essential_success += 1
    
    print("\\n📋 Optional Dependencies:")
    for module, desc in optional_imports:
        if test_import(module, desc):
            optional_success += 1
    
    print("\\n" + "=" * 50)
    print(f"📊 Results:")
    print(f"   Essential: {essential_success}/{len(essential_imports)} ({'✅ PASS' if essential_success >= 4 else '❌ FAIL'})")
    print(f"   Optional:  {optional_success}/{len(optional_imports)} (Info only)")
    
    # Test main file can be imported
    print("\\n🧪 Testing main file import...")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        # Try importing main components
        import main_desktop
        print("✅ Main desktop file imported successfully")
        main_success = True
    except Exception as e:
        print(f"❌ Main desktop import failed: {e}")
        main_success = False
    
    # Overall result
    print("\\n" + "=" * 50)
    if essential_success >= 4 and main_success:
        print("🎉 CI BUILD COMPATIBILITY: PASS")
        print("✅ Build should succeed in GitHub Actions")
        return 0
    else:
        print("❌ CI BUILD COMPATIBILITY: FAIL")
        print("⚠️  Build may fail in GitHub Actions")
        return 1

if __name__ == "__main__":
    sys.exit(test_ci_build())