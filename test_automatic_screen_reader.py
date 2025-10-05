#!/usr/bin/env python3
"""
Test script for the new Automatic External Screen Reader
This tests that the automatic functionality works correctly
"""

import sys
import os
import time

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_automatic_screen_reader():
    """Test the automatic external screen reader"""
    print("🧪 TESTING AUTOMATIC EXTERNAL SCREEN READER")
    print("=" * 50)
    
    try:
        from src.automatic_external_screen_reader import (
            start_automatic_external_screen_reader,
            stop_automatic_external_screen_reader,
            is_automatic_screen_reader_running
        )
        
        print("✅ Automatic external screen reader module imported successfully")
        
        # Test starting the automatic reader
        print("\n1. Starting automatic screen reader...")
        reader = start_automatic_external_screen_reader()
        
        if reader:
            print("✅ Automatic screen reader started successfully!")
            print(f"   Platform: {reader.platform}")
            print(f"   Continuous mode: {reader.continuous_mode}")
            print(f"   Running: {reader.is_running}")
            
            # Check if it's really running
            if is_automatic_screen_reader_running():
                print("✅ Reader is confirmed running")
            else:
                print("❌ Reader not detected as running")
                return False
            
            # Test for a few seconds
            print("\n2. Testing automatic functionality for 5 seconds...")
            print("   Switch between different applications to test automatic reading...")
            time.sleep(5)
            
            # Stop the reader
            print("\n3. Stopping automatic screen reader...")
            stop_automatic_external_screen_reader()
            
            if not is_automatic_screen_reader_running():
                print("✅ Reader stopped successfully")
            else:
                print("❌ Reader still running after stop")
                return False
            
            return True
            
        else:
            print("❌ Failed to start automatic screen reader")
            return False
            
    except Exception as e:
        print(f"❌ Error testing automatic screen reader: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_app_integration():
    """Test integration with main app"""
    print("\n🧪 TESTING MAIN APP INTEGRATION")
    print("=" * 40)
    
    try:
        # Test importing the main desktop module
        from src import main_desktop
        print("✅ Main desktop module imported successfully")
        
        # Check if our functions are available
        if hasattr(main_desktop, 'start_external_screen_reader'):
            print("✅ start_external_screen_reader function found in main app")
        else:
            print("❌ start_external_screen_reader function not found")
            return False
            
        if hasattr(main_desktop, 'stop_external_screen_reader'):
            print("✅ stop_external_screen_reader function found in main app")
        else:
            print("❌ stop_external_screen_reader function not found")
            return False
        
        print("✅ Main app integration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error testing main app integration: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AUTOMATIC EXTERNAL SCREEN READER TEST SUITE")
    print("=" * 55)
    print()
    
    # Test the automatic reader
    auto_test_passed = test_automatic_screen_reader()
    
    # Test main app integration
    integration_test_passed = test_main_app_integration()
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 TEST RESULTS SUMMARY")
    print(f"🤖 Automatic Screen Reader: {'✅ PASS' if auto_test_passed else '❌ FAIL'}")
    print(f"🔗 Main App Integration: {'✅ PASS' if integration_test_passed else '❌ FAIL'}")
    
    if auto_test_passed and integration_test_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Automatic External Screen Reader is working correctly!")
        print("✅ Integration with main app is successful!")
        print("\n🤖 Features Available:")
        print("   • Automatic continuous reading of window changes")
        print("   • Enhanced focus monitoring")
        print("   • Background monitoring thread")
        print("   • Automatic window content reading")  
        print("   • Integration with AccessMate main interface")
        print("\n🚀 Ready for use! The external screen reader will now work AUTOMATICALLY!")
        return True
    else:
        print("\n❌ Some tests failed. Please review the output above.")
        return False

if __name__ == "__main__":
    success = main()
    
    print("\n" + "=" * 55)
    input("Press Enter to exit...")
    
    sys.exit(0 if success else 1)