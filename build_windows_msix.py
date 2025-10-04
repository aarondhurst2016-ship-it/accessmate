#!/usr/bin/env python3
"""
Microsoft Store (MSIX) Build Script for AccessMate
Creates an MSIX package that bypasses Smart App Control automatically
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

def create_msix_manifest():
    """Create AppxManifest.xml for MSIX package"""
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:mp="http://schemas.microsoft.com/appx/2014/phone/manifest"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:uap3="http://schemas.microsoft.com/appx/manifest/uap/windows10/3"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="mp uap uap3 rescap">

  <Identity Name="AccessMateTeam.AccessMate"
            Version="1.0.0.0"
            Publisher="CN=AccessMate Team"
            ProcessorArchitecture="x64" />

  <mp:PhoneIdentity PhoneProductId="12345678-1234-1234-1234-123456789abc" />

  <Properties>
    <DisplayName>AccessMate</DisplayName>
    <PublisherDisplayName>AccessMate Team</PublisherDisplayName>
    <Description>AccessMate - Your complete accessibility assistant for Windows. Text-to-speech, translation, screen reading, and more accessibility features in one app.</Description>
    <Logo>Assets\\StoreLogo.png</Logo>
    <uap:SupportedFileTypes>
      <uap:FileType>.txt</uap:FileType>
      <uap:FileType>.pdf</uap:FileType>
    </uap:SupportedFileTypes>
  </Properties>

  <Dependencies>
    <TargetDeviceFamily Name="Windows.Universal" MinVersion="10.0.17763.0" MaxVersionTested="10.0.22621.0" />
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.22621.0" />
  </Dependencies>

  <Resources>
    <Resource Language="en-US" />
  </Resources>

  <Applications>
    <Application Id="AccessMate" Executable="AccessMate.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements BackgroundColor="transparent"
                          DisplayName="AccessMate"
                          Square150x150Logo="Assets\\Square150x150Logo.png"
                          Square44x44Logo="Assets\\Square44x44Logo.png"
                          Description="AccessMate - Accessibility Assistant">
        <uap:DefaultTile Wide310x150Logo="Assets\\Wide310x150Logo.png"
                         Square310x310Logo="Assets\\LargeTile.png"
                         Square71x71Logo="Assets\\SmallTile.png">
          <uap:ShowNameOnTiles>
            <uap:ShowOn Tile="square150x150Logo" />
            <uap:ShowOn Tile="wide310x150Logo" />
            <uap:ShowOn Tile="square310x310Logo" />
          </uap:ShowNameOnTiles>
        </uap:DefaultTile>
        <uap:SplashScreen Image="Assets\\SplashScreen.png" />
        <uap:InitialRotationPreference>
          <uap:Rotation Preference="landscape" />
          <uap:Rotation Preference="portrait" />
        </uap:InitialRotationPreference>
      </uap:VisualElements>
      
      <Extensions>
        <uap3:Extension Category="windows.appExecutionAlias">
          <uap3:AppExecutionAlias>
            <desktop:ExecutionAlias Alias="accessmate.exe" />
          </uap3:AppExecutionAlias>
        </uap3:Extension>
      </Extensions>
    </Application>
  </Applications>

  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
    <Capability Name="internetClient" />
    <uap:Capability Name="documentsLibrary" />
    <DeviceCapability Name="microphone" />
    <DeviceCapability Name="webcam" />
  </Capabilities>
</Package>'''

    return manifest_content

def create_msix_assets():
    """Create required MSIX assets from the main logo"""
    try:
        from PIL import Image
        
        script_dir = Path(__file__).parent
        logo_path = script_dir / "src" / "accessmate_logo.png"
        assets_dir = Path("msix_build/Assets")
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        if not logo_path.exists():
            print(f"⚠️  Warning: Logo not found at {logo_path}")
            return False
        
        logo = Image.open(logo_path).convert("RGBA")
        
        # MSIX required asset sizes
        assets = {
            "Square44x44Logo.png": (44, 44),
            "Square71x71Logo.png": (71, 71), 
            "Square150x150Logo.png": (150, 150),
            "Square310x310Logo.png": (310, 310),
            "Wide310x150Logo.png": (310, 150),
            "StoreLogo.png": (50, 50),
            "SplashScreen.png": (620, 300),
            "LargeTile.png": (310, 310),
            "SmallTile.png": (71, 71),
        }
        
        for filename, (width, height) in assets.items():
            if "Wide" in filename:
                # Create wide logo with centered square logo
                wide_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                square_size = min(width//2, height)
                resized_logo = logo.resize((square_size, square_size), Image.Resampling.LANCZOS)
                x = (width - square_size) // 2
                y = (height - square_size) // 2
                wide_img.paste(resized_logo, (x, y), resized_logo)
                wide_img.save(assets_dir / filename, "PNG")
            elif "Splash" in filename:
                # Create splash screen
                splash_img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
                logo_size = min(width//3, height)
                resized_logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                x = (width - logo_size) // 2
                y = (height - logo_size) // 2
                splash_img.paste(resized_logo, (x, y), resized_logo)
                splash_img.save(assets_dir / filename, "PNG")
            else:
                # Square logos
                resized = logo.resize((width, height), Image.Resampling.LANCZOS)
                resized.save(assets_dir / filename, "PNG")
            
            print(f"  Created {filename} ({width}x{height})")
        
        return True
        
    except ImportError:
        print("❌ PIL (Pillow) not found. Install with: pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ Error creating assets: {e}")
        return False

def build_msix_package():
    """Build MSIX package for Microsoft Store"""
    
    print("🏪 Building AccessMate MSIX Package for Microsoft Store...")
    print("=" * 60)
    
    # Create build directory
    build_dir = Path("msix_build")
    build_dir.mkdir(exist_ok=True)
    
    # Check if we have the executable
    exe_path = Path("dist/AccessMate.exe")
    if not exe_path.exists():
        print("❌ AccessMate.exe not found. Build the regular executable first:")
        print("   python build_windows.py")
        return False
    
    # Create assets
    print("📸 Creating MSIX assets...")
    if not create_msix_assets():
        return False
    
    # Copy executable to build directory
    shutil.copy2(exe_path, build_dir / "AccessMate.exe")
    print(f"📁 Copied executable to {build_dir / 'AccessMate.exe'}")
    
    # Create manifest
    manifest_path = build_dir / "AppxManifest.xml"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(create_msix_manifest())
    print(f"📝 Created manifest: {manifest_path}")
    
    # Check for makeappx tool
    makeappx_paths = [
        "C:\\Program Files (x86)\\Windows Kits\\10\\bin\\*\\x64\\makeappx.exe",
        "C:\\Program Files\\Windows Kits\\10\\bin\\*\\x64\\makeappx.exe",
    ]
    
    makeappx_exe = None
    for pattern in makeappx_paths:
        import glob
        matches = glob.glob(pattern)
        if matches:
            makeappx_exe = max(matches)  # Get latest version
            break
    
    if not makeappx_exe:
        print("⚠️  Windows SDK not found. Creating manual instructions...")
        print("\\nTo create MSIX package manually:")
        print("1. Install Windows 10/11 SDK")
        print("2. Run: makeappx pack /d msix_build /p AccessMate.msix")
        print("3. Sign with: signtool sign /fd SHA256 /a AccessMate.msix")
        
        # Create a PowerShell script for easy building
        ps_script = build_dir.parent / "build_msix.ps1"
        ps_content = '''# AccessMate MSIX Build Script
# Requires Windows SDK to be installed

Write-Host "Building AccessMate MSIX Package..." -ForegroundColor Green

# Find makeappx.exe
$makeappx = Get-ChildItem "C:\\Program Files*\\Windows Kits\\10\\bin\\*\\x64\\makeappx.exe" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $makeappx) {
    Write-Host "Error: Windows SDK not found. Please install Windows 10/11 SDK." -ForegroundColor Red
    exit 1
}

Write-Host "Using: $($makeappx.FullName)" -ForegroundColor Yellow

# Create MSIX package
& $makeappx.FullName pack /d "msix_build" /p "AccessMate.msix" /o

if ($LASTEXITCODE -eq 0) {
    Write-Host "\\n✅ MSIX package created successfully!" -ForegroundColor Green
    Write-Host "📦 Output: AccessMate.msix" -ForegroundColor Cyan
    Write-Host "🏪 Ready for Microsoft Store submission" -ForegroundColor Cyan
    Write-Host "🛡️ MSIX packages are automatically trusted by Windows" -ForegroundColor Cyan
} else {
    Write-Host "\\n❌ MSIX build failed" -ForegroundColor Red
}

Pause
'''
        
        with open(ps_script, 'w', encoding='utf-8') as f:
            f.write(ps_content)
        
        print(f"💻 Created build script: {ps_script}")
        print("   Run this PowerShell script to build MSIX package")
        return True
    
    # Build MSIX package
    print(f"🔨 Building MSIX with: {makeappx_exe}")
    
    try:
        cmd = [
            makeappx_exe,
            "pack",
            "/d", str(build_dir),
            "/p", "AccessMate.msix",
            "/o"  # Overwrite existing
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("\n✅ MSIX package created successfully!")
            print("📦 Output: AccessMate.msix")
            print("🏪 Ready for Microsoft Store submission")
            print("🛡️ MSIX packages are automatically trusted by Windows")
            print("\n📖 Next steps:")
            print("   1. Test install: Add-AppxPackage -Path AccessMate.msix")
            print("   2. Submit to Microsoft Store for distribution")
            print("   3. Users can install from Store without Smart App Control issues")
            return True
        else:
            print(f"\n❌ MSIX build failed:")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error building MSIX: {e}")
        return False

if __name__ == "__main__":
    print("AccessMate Microsoft Store (MSIX) Build Script")
    print("=============================================") 
    build_msix_package()