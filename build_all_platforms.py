#!/usr/bin/env python3
"""
Universal Build Script for AccessMate
Builds for all supported platforms with proper icons and i        if target in ["windows", "macos", "linux", "android", "ios"]:
            build_for_platform(target)
        else:
            print("Usage: python build_all_platforms.py [windows|macos|linux|android|ios|all]")ration
"""

import sys
import os
import subprocess
import platform

def detect_platform():
    """Detect current platform"""
    system = platform.system().lower()
    
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def build_for_platform(target_platform=None):
    """Build AccessMate for specified platform or current platform"""
    
    if target_platform is None:
        target_platform = detect_platform()
    
    print(f"🚀 Building AccessMate for {target_platform.upper()}")
    print("=" * 50)
    
    build_scripts = {
        "windows": "build_windows.py",
        "macos": "build_macos.py", 
        "linux": "build_linux.py",
        "ios": "build_ios.py",
        "android": "buildozer android debug"  # Special case
    }
    
    if target_platform == "android":
        print("Building Android APK...")
        try:
            result = subprocess.run(["buildozer", "android", "debug"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Android APK built successfully!")
                print("📱 APK will show AccessMate logo on device")
                return True
            else:
                print(f"❌ Android build failed:\n{result.stderr}")
                return False
        except FileNotFoundError:
            print("❌ Buildozer not found. Install with: pip install buildozer")
            return False
    
    elif target_platform in build_scripts:
        script = build_scripts[target_platform]
        if os.path.exists(script):
            print(f"Running {script}...")
            try:
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {target_platform.upper()} build completed!")
                    print(result.stdout)
                    return True
                else:
                    print(f"❌ {target_platform.upper()} build failed:")
                    print(result.stderr)
                    return False
            except Exception as e:
                print(f"❌ Build error: {e}")
                return False
        else:
            print(f"❌ Build script not found: {script}")
            return False
    else:
        print(f"❌ Unsupported platform: {target_platform}")
        return False

def build_all_platforms():
    """Build for all supported platforms"""
    current_platform = detect_platform()
    
    print("🌍 Building AccessMate for ALL platforms")
    print("=" * 50)
    
    platforms = ["windows", "macos", "linux", "android", "ios"]
    results = {}
    
    for platform_name in platforms:
        print(f"\n🔨 Building for {platform_name.upper()}...")
        
        if platform_name != current_platform and platform_name != "android":
            print(f"⚠️  Cross-platform build (current: {current_platform})")
        
        results[platform_name] = build_for_platform(platform_name)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 BUILD SUMMARY")
    print("=" * 50)
    
    for platform_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{platform_name.upper():10} {status}")
    
    successful_builds = sum(results.values())
    total_builds = len(results)
    
    print(f"\n🎯 {successful_builds}/{total_builds} platforms built successfully")
    
    if successful_builds == total_builds:
        print("🎉 ALL PLATFORMS READY! Logo will show on all devices!")
    
    return results

def main():
    """Main build function"""
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        
        if target == "all":
            build_all_platforms()
        elif target in ["windows", "macos", "linux", "android"]:
            build_for_platform(target)
        else:
            print("Usage: python build_all_platforms.py [windows|macos|linux|android|all]")
            print("       python build_all_platforms.py  (builds for current platform)")
    else:
        # Build for current platform
        build_for_platform()

if __name__ == "__main__":
    main()