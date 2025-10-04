#!/usr/bin/env python3
"""
Test script to verify all modules are properly integrated
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_module_imports():
    """Test importing all the modules used in the GUI"""
    results = {}
    
    # Test voice commands module
    try:
        from voice_commands import voice_command_loop
        results['voice_commands'] = "✅ Available"
    except ImportError as e:
        # Try alternative import to work around circular import issues
        try:
            import voice_commands
            if hasattr(voice_commands, 'voice_command_loop'):
                results['voice_commands'] = "✅ Available"
            else:
                results['voice_commands'] = f"❌ Not available: voice_command_loop function not found"
        except Exception as _:
            results['voice_commands'] = f"❌ Not available: {e}"
    
    # Test screen reader module
    try:
        from screen_reader import ScreenReader
        results['screen_reader'] = "✅ Available"
    except ImportError as e:
        results['screen_reader'] = f"❌ Not available: {e}"
    
    # Test object recognition module
    try:
        from object_recognition import ObjectRecognizer
        results['object_recognition'] = "✅ Available"
    except ImportError as e:
        results['object_recognition'] = f"❌ Not available: {e}"
    
    # Test smart home module
    try:
        from smart_home import SmartHomeController
        results['smart_home'] = "✅ Available"
    except ImportError as e:
        results['smart_home'] = f"❌ Not available: {e}"
    
    # Test settings module
    try:
        from settings import SettingsWindow
        results['settings'] = "✅ Available"
    except ImportError as e:
        results['settings'] = f"❌ Not available: {e}"
    
    return results

def main():
    print("AccessMate Module Integration Test")
    print("=" * 40)
    
    results = test_module_imports()
    
    for module, status in results.items():
        print(f"{module:20} : {status}")
    
    print("\n" + "=" * 40)
    
    available = sum(1 for status in results.values() if status.startswith("✅"))
    total = len(results)
    
    print(f"Modules available: {available}/{total}")
    
    if available == total:
        print("🎉 All modules are properly integrated!")
    elif available > 0:
        print("⚠️  Some modules are missing - GUI will use fallback methods")
    else:
        print("❌ No modules available - please check your installation")

if __name__ == "__main__":
    main()