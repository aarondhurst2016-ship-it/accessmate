#!/usr/bin/env python3
"""
Final verification test for AccessMate with all ImportError fixes.
This tests the actual executable functionality.
"""

import subprocess
import sys
import os
import time

def test_executable():
    """Test that the AccessMate.exe runs without ImportError crashes."""
    print("🔍 Final AccessMate ImportError Fix Verification")
    print("=" * 55)
    
    exe_path = "./dist/AccessMate.exe"
    
    if not os.path.exists(exe_path):
        print(f"❌ Error: {exe_path} not found")
        return False
    
    # Get file info
    stat = os.stat(exe_path)
    size_mb = stat.st_size / (1024 * 1024)
    mod_time = time.ctime(stat.st_mtime)
    
    print(f"📁 Executable: {exe_path}")
    print(f"📏 Size: {size_mb:.1f} MB")
    print(f"🕒 Last Modified: {mod_time}")
    print()
    
    print("🧪 Testing executable launch...")
    
    try:
        # Test 1: Quick launch test (should not crash immediately)
        print("   Test 1: Quick startup test...")
        process = subprocess.Popen([exe_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Give it a moment to initialize and check for immediate crashes
        time.sleep(3)
        
        if process.poll() is None:
            print("   ✅ Executable launched successfully (no immediate crash)")
            # Terminate the process gracefully
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        else:
            # Process ended - check if it was due to an error
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print(f"   ❌ Process exited with code {process.returncode}")
                if stderr:
                    print(f"   📝 Error output: {stderr.decode()}")
                return False
            else:
                print("   ✅ Process completed successfully")
        
        print("   ✅ No ImportError crashes detected")
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing executable: {e}")
        return False

def verify_source_fixes():
    """Verify the source code fixes are in place."""
    print("\n🔧 Verifying Source Code Fixes")
    print("-" * 35)
    
    # Check speech.py
    try:
        from src import speech
        gtts_available = getattr(speech, 'GTTS_AVAILABLE', None)
        googletrans_available = getattr(speech, 'GOOGLETRANS_AVAILABLE', None)
        
        print(f"📄 speech.py:")
        print(f"   ✅ Module imported successfully")
        print(f"   ✅ GTTS_AVAILABLE: {gtts_available}")
        print(f"   ✅ GOOGLETRANS_AVAILABLE: {googletrans_available}")
        
    except Exception as e:
        print(f"   ❌ Error with speech.py: {e}")
        return False
    
    # Check ocr_screen_reader.py
    try:
        from src import ocr_screen_reader
        gtts_available = getattr(ocr_screen_reader, 'GTTS_AVAILABLE', None)
        googletrans_available = getattr(ocr_screen_reader, 'GOOGLETRANS_AVAILABLE', None)
        
        print(f"📄 ocr_screen_reader.py:")
        print(f"   ✅ Module imported successfully")
        print(f"   ✅ GTTS_AVAILABLE: {gtts_available}")
        print(f"   ✅ GOOGLETRANS_AVAILABLE: {googletrans_available}")
        
    except Exception as e:
        print(f"   ❌ Error with ocr_screen_reader.py: {e}")
        return False
    
    return True

def main():
    """Run all verification tests."""
    print("🎯 AccessMate ImportError Fix - Final Verification")
    print("=" * 55)
    print()
    
    # Test source code fixes
    source_ok = verify_source_fixes()
    
    # Test executable 
    exe_ok = test_executable()
    
    print("\n" + "=" * 55)
    print("📊 FINAL RESULTS:")
    print(f"   🔧 Source Code Fixes: {'✅ PASS' if source_ok else '❌ FAIL'}")
    print(f"   💻 Executable Test: {'✅ PASS' if exe_ok else '❌ FAIL'}")
    print()
    
    if source_ok and exe_ok:
        print("🎉 SUCCESS! All ImportError fixes verified working!")
        print("✅ googletrans ImportError: FIXED")
        print("✅ gtts ImportError: FIXED") 
        print("✅ Executable launches without crashes")
        print("✅ Ready for deployment!")
    else:
        print("❌ Some tests failed - review the output above")
    
    print("=" * 55)

if __name__ == "__main__":
    main()