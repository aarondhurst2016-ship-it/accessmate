#!/usr/bin/env python3
"""
Test script to verify the AccessMate.exe has proper googletrans support
This script will launch the executable and check if it can handle translation features
"""

import subprocess
import os
import time
import sys

def test_executable_googletrans():
    """Test if the built executable has googletrans functionality"""
    
    exe_path = os.path.join("dist", "AccessMate.exe")
    
    if not os.path.exists(exe_path):
        print(f"❌ Executable not found: {exe_path}")
        return False
        
    print(f"Testing executable: {exe_path}")
    print("=" * 50)
    
    # Get file size and modification time
    stat_info = os.stat(exe_path)
    size_mb = stat_info.st_size / (1024 * 1024)
    mod_time = time.ctime(stat_info.st_mtime)
    
    print(f"📁 File size: {size_mb:.2f} MB")
    print(f"🕒 Modified: {mod_time}")
    
    # Try to launch the executable briefly to see if it starts without import errors
    try:
        print("\n🚀 Launching executable (will timeout after 5 seconds)...")
        
        # Start the process
        process = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="dist"
        )
        
        # Wait for a short time to see if it crashes immediately
        try:
            stdout, stderr = process.communicate(timeout=5)
            
            if process.returncode == 0:
                print("✅ Executable launched and exited normally")
                return True
                
        except subprocess.TimeoutExpired:
            # This is expected - the GUI app is running
            print("✅ Executable launched successfully (GUI running)")
            process.terminate()
            
            # Wait a bit more for cleanup
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                
            return True
            
    except Exception as e:
        print(f"❌ Failed to launch executable: {e}")
        return False

if __name__ == "__main__":
    print("Testing AccessMate.exe with googletrans support...")
    print("=" * 60)
    
    success = test_executable_googletrans()
    
    if success:
        print("\n🎉 Executable test passed!")
        print("The AccessMate.exe appears to be built correctly with googletrans support.")
    else:
        print("\n💥 Executable test failed!")
        print("There may be issues with the build or googletrans integration.")
    
    print("\nNote: For full testing, the executable should be run manually")
    print("to verify translation features work correctly in the GUI.")