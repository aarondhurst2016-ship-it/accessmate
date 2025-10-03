#!/bin/bash
# build_macos.sh - Comprehensive macOS build script for AccessMate

set -e  # Exit on any error

echo "🍎 AccessMate macOS Build Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="AccessMate"
VERSION="1.0.0"
BUNDLE_ID="com.accessmate.app"  # Change to your unique bundle ID
DEVELOPER_TEAM="${ACCESSMATE_TEAM_ID:-}"  # Set via env var or edit here
SIGNING_IDENTITY="${ACCESSMATE_SIGNING_IDENTITY:-}"  # Optional: specific signing identity
BUILD_DIR="build_macos"
DIST_DIR="dist_macos"
RESOURCES_DIR="resources"

# Notarization settings (optional)
NOTARY_KEY_ID="${ACCESSMATE_NOTARY_KEY_ID:-}"
NOTARY_ISSUER_ID="${ACCESSMATE_NOTARY_ISSUER_ID:-}"
NOTARY_KEY_PATH="${ACCESSMATE_NOTARY_KEY_PATH:-}"

echo -e "${BLUE}Checking macOS environment...${NC}"

# Check we're on macOS
if [ "$(uname)" != "Darwin" ]; then
    echo -e "${RED}❌ This script must be run on macOS${NC}"
    exit 1
fi

# Check for required tools
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}❌ python3 is required but not installed${NC}"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo -e "${RED}❌ pip3 is required but not installed${NC}"; exit 1; }

echo -e "${GREEN}✅ macOS environment verified${NC}"

# Create build directories
echo -e "${BLUE}Creating build directories...${NC}"
mkdir -p "$BUILD_DIR"
mkdir -p "$DIST_DIR"
mkdir -p "$RESOURCES_DIR"

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf "$BUILD_DIR"/*
rm -rf "$DIST_DIR"/*
rm -rf build/
rm -rf dist/
rm -rf *.spec

echo -e "${GREEN}✅ Build directories prepared${NC}"

# Install/update dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install pyinstaller py2app

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Fix the macOS entry point to work with current codebase
echo -e "${BLUE}Creating macOS entry point...${NC}"
cat > mac_entry.py << 'EOF'
#!/usr/bin/env python3
"""
macOS Entry Point for AccessMate
Handles macOS-specific initialization and launches the main GUI
"""

import sys
import os
import platform

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point for macOS"""
    try:
        # Import and launch GUI
        import gui
        
        # Create a dummy GUI instance for compatibility
        class DummyGUIInstance:
            pass
        
        gui_instance = DummyGUIInstance()
        gui.launch(gui_instance)
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all required modules are installed")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching AccessMate: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

echo -e "${GREEN}✅ macOS entry point created${NC}"

# Create macOS-specific PyInstaller spec file
echo -e "${BLUE}Creating PyInstaller spec file...${NC}"
cat > AccessMate-macOS.spec << EOF
# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# Get Python installation path for Tcl/Tk
python_path = sys.executable
python_dir = os.path.dirname(python_path)

# Try multiple possible Tcl/Tk paths on macOS
tcl_paths = [
    '/usr/local/lib/tcl8.6',
    '/opt/homebrew/lib/tcl8.6', 
    '/System/Library/Frameworks/Tcl.framework/Versions/8.6/Resources/Scripts',
    os.path.join(python_dir, '../lib/tcl8.6')
]

tk_paths = [
    '/usr/local/lib/tk8.6',
    '/opt/homebrew/lib/tk8.6',
    '/System/Library/Frameworks/Tk.framework/Versions/8.6/Resources/Scripts', 
    os.path.join(python_dir, '../lib/tk8.6')
]

# Find existing Tcl/Tk paths
tcl_path = None
tk_path = None

for path in tcl_paths:
    if os.path.exists(path):
        tcl_path = path
        break

for path in tk_paths:
    if os.path.exists(path):
        tk_path = path
        break

datas = []
if tcl_path:
    datas.append((tcl_path, 'tcl'))
if tk_path:
    datas.append((tk_path, 'tk'))

# Add application resources
datas.extend([
    ('src/accessmate_logo.png', '.'),
    ('src/accessmate_logo_uploaded.png', '.'),
    ('requirements.txt', '.'),
    ('README.md', '.'),
    ('ACCESSIBILITY.txt', '.'),
])

a = Analysis(
    ['mac_entry.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'tkinter.scrolledtext',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'pygame',
        'numpy',
        'requests',
        'speechrecognition',
        'pyttsx3',
        'psutil',
        'winreg',  # Will be ignored on macOS
        'pystray',
        'plyer',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='$APP_NAME',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='$APP_NAME.app',
    icon='src/accessmate_logo.png',
    bundle_identifier='$BUNDLE_ID',
    version='$VERSION',
    info_plist={
        'CFBundleName': '$APP_NAME',
        'CFBundleDisplayName': '$APP_NAME',
        'CFBundleIdentifier': '$BUNDLE_ID',
        'CFBundleVersion': '$VERSION',
        'CFBundleShortVersionString': '$VERSION',
        'NSHumanReadableCopyright': 'Copyright © 2025 AccessMate Team',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
        'NSMicrophoneUsageDescription': 'AccessMate needs microphone access for speech recognition features.',
        'NSCameraUsageDescription': 'AccessMate needs camera access for object recognition and barcode scanning.',
        'NSLocationUsageDescription': 'AccessMate needs location access for navigation and emergency features.',
        'LSApplicationCategoryType': 'public.app-category.accessibility',
    },
)
EOF

echo -e "${GREEN}✅ PyInstaller spec file created${NC}"

# Build the application
echo -e "${BLUE}Building AccessMate with PyInstaller...${NC}"
pyinstaller --clean AccessMate-macOS.spec

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PyInstaller build completed successfully${NC}"
else
    echo -e "${RED}❌ PyInstaller build failed${NC}"
    exit 1
fi

# Move the .app bundle to our dist directory
echo -e "${BLUE}Moving app bundle to dist directory...${NC}"
if [ -d "dist/AccessMate.app" ]; then
    mv "dist/AccessMate.app" "$DIST_DIR/"
    echo -e "${GREEN}✅ App bundle moved to $DIST_DIR/${NC}"
else
    echo -e "${RED}❌ App bundle not found after build${NC}"
    exit 1
fi

# Create a simple installer DMG (optional)
echo -e "${BLUE}Creating DMG installer...${NC}"
if command -v create-dmg >/dev/null 2>&1; then
    create-dmg \
        --volname "AccessMate Installer" \
        --volicon "src/accessmate_logo.png" \
        --window-pos 200 120 \
        --window-size 600 300 \
        --icon-size 100 \
        --icon "AccessMate.app" 175 120 \
        --hide-extension "AccessMate.app" \
        --app-drop-link 425 120 \
        "$DIST_DIR/AccessMate-$VERSION.dmg" \
        "$DIST_DIR/"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ DMG installer created: $DIST_DIR/AccessMate-$VERSION.dmg${NC}"
    else
        echo -e "${YELLOW}⚠️  DMG creation failed, but app bundle is ready${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  create-dmg not installed. Install with: brew install create-dmg${NC}"
    echo -e "${BLUE}Creating simple DMG with hdiutil...${NC}"
    
    # Create a temporary directory for DMG contents
    DMG_TEMP_DIR="$BUILD_DIR/dmg_temp"
    mkdir -p "$DMG_TEMP_DIR"
    
    # Copy the app bundle
    cp -R "$DIST_DIR/AccessMate.app" "$DMG_TEMP_DIR/"
    
    # Create symbolic link to Applications folder
    ln -s /Applications "$DMG_TEMP_DIR/Applications"
    
    # Create DMG
    hdiutil create -format UDZO -srcfolder "$DMG_TEMP_DIR" -volname "AccessMate Installer" "$DIST_DIR/AccessMate-$VERSION.dmg"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Simple DMG created: $DIST_DIR/AccessMate-$VERSION.dmg${NC}"
    else
        echo -e "${YELLOW}⚠️  DMG creation failed, but app bundle is ready${NC}"
    fi
fi

# Code signing (if developer team or identity is set)
if [ -n "$DEVELOPER_TEAM" ] || [ -n "$SIGNING_IDENTITY" ]; then
    echo -e "${BLUE}Code signing application...${NC}"
    
    # Determine signing identity
    if [ -n "$SIGNING_IDENTITY" ]; then
        SIGN_ID="$SIGNING_IDENTITY"
        echo -e "${BLUE}Using specific signing identity: $SIGN_ID${NC}"
    elif [ -n "$DEVELOPER_TEAM" ]; then
        SIGN_ID="$DEVELOPER_TEAM"
        echo -e "${BLUE}Using developer team ID: $SIGN_ID${NC}"
    fi
    
    # Sign the application
    codesign --force --deep --sign "$SIGN_ID" "$DIST_DIR/AccessMate.app"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Code signing completed${NC}"
        
        # Verify the signature
        echo -e "${BLUE}Verifying signature...${NC}"
        codesign --verify --deep --strict "$DIST_DIR/AccessMate.app"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Signature verification passed${NC}"
            
            # Display signature information
            echo -e "${BLUE}Signature details:${NC}"
            codesign --display --verbose=2 "$DIST_DIR/AccessMate.app" 2>&1 | head -10
            
            # Check Gatekeeper status
            echo -e "${BLUE}Checking Gatekeeper assessment...${NC}"
            spctl --assess --verbose "$DIST_DIR/AccessMate.app" 2>&1 || {
                echo -e "${YELLOW}⚠️  Gatekeeper assessment failed - app may need notarization${NC}"
            }
            
        else
            echo -e "${YELLOW}⚠️  Signature verification failed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Code signing failed${NC}"
        echo -e "${BLUE}Available signing identities:${NC}"
        security find-identity -v -p codesigning | head -10
    fi
    
    # Notarization (if configured)
    if [ -n "$NOTARY_KEY_ID" ] && [ -n "$NOTARY_ISSUER_ID" ] && [ -n "$NOTARY_KEY_PATH" ] && [ -f "$NOTARY_KEY_PATH" ]; then
        echo -e "${BLUE}Submitting for notarization...${NC}"
        
        # Create a ZIP for notarization (apps must be in ZIP or DMG)
        NOTARY_ZIP="$DIST_DIR/AccessMate-notarization.zip"
        (cd "$DIST_DIR" && zip -r "$(basename "$NOTARY_ZIP")" AccessMate.app)
        
        xcrun notarytool submit "$NOTARY_ZIP" \
            --key-id "$NOTARY_KEY_ID" \
            --issuer-id "$NOTARY_ISSUER_ID" \
            --key "$NOTARY_KEY_PATH" \
            --wait
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Notarization completed${NC}"
            
            # Staple the notarization ticket
            echo -e "${BLUE}Stapling notarization ticket...${NC}"
            xcrun stapler staple "$DIST_DIR/AccessMate.app"
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ Notarization ticket stapled${NC}"
                
                # Clean up notarization ZIP
                rm -f "$NOTARY_ZIP"
            else
                echo -e "${YELLOW}⚠️  Failed to staple notarization ticket${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  Notarization failed${NC}"
        fi
    elif [ -n "$DEVELOPER_TEAM" ]; then
        echo -e "${YELLOW}⚠️  Notarization not configured. For public distribution, set:${NC}"
        echo -e "${BLUE}  ACCESSMATE_NOTARY_KEY_ID${NC}"
        echo -e "${BLUE}  ACCESSMATE_NOTARY_ISSUER_ID${NC}" 
        echo -e "${BLUE}  ACCESSMATE_NOTARY_KEY_PATH${NC}"
    fi
    
else
    echo -e "${YELLOW}⚠️  No code signing configured.${NC}"
    echo -e "${BLUE}To enable code signing, set one of:${NC}"
    echo -e "${BLUE}  ACCESSMATE_TEAM_ID=\"YOUR_TEAM_ID\"${NC}"
    echo -e "${BLUE}  ACCESSMATE_SIGNING_IDENTITY=\"Developer ID Application: Your Name\"${NC}"
    echo -e "${BLUE}Or edit DEVELOPER_TEAM in this script${NC}"
    echo ""
    echo -e "${BLUE}Available signing identities on this system:${NC}"
    security find-identity -v -p codesigning | head -5 || echo -e "${YELLOW}No signing identities found${NC}"
fi

# Generate build summary
echo -e "${BLUE}Generating build summary...${NC}"
APP_SIZE=$(du -sh "$DIST_DIR/AccessMate.app" | cut -f1)
BUILD_DATE=$(date)

cat > "$DIST_DIR/BUILD_INFO.txt" << EOF
AccessMate macOS Build Information
=================================

Build Date: $BUILD_DATE
Version: $VERSION
Bundle ID: $BUNDLE_ID
App Size: $APP_SIZE
macOS Version: $(sw_vers -productVersion)
Xcode Version: $(xcode-select --version 2>/dev/null || echo "Not installed")

Files Created:
- AccessMate.app (Application Bundle)
$([ -f "$DIST_DIR/AccessMate-$VERSION.dmg" ] && echo "- AccessMate-$VERSION.dmg (Installer)")

Installation:
1. Double-click AccessMate-$VERSION.dmg (if available)
2. Drag AccessMate.app to Applications folder
3. Launch from Applications or Spotlight

Notes:
- First launch may show security warning (Gatekeeper)
- Go to System Preferences > Security & Privacy to allow if needed
- The app includes accessibility features and may request permissions

For distribution:
- Code sign the app bundle for distribution
- Notarize with Apple for Gatekeeper compatibility
- Create installer DMG for easy distribution
EOF

echo -e "${GREEN}✅ Build summary created${NC}"

# Final status
echo ""
echo -e "${GREEN}🎉 macOS Build Complete!${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "App Bundle: ${YELLOW}$DIST_DIR/AccessMate.app${NC}"
if [ -f "$DIST_DIR/AccessMate-$VERSION.dmg" ]; then
    echo -e "Installer DMG: ${YELLOW}$DIST_DIR/AccessMate-$VERSION.dmg${NC}"
fi
echo -e "Build Info: ${YELLOW}$DIST_DIR/BUILD_INFO.txt${NC}"
echo ""
echo -e "${BLUE}To test the app:${NC}"
echo -e "  open $DIST_DIR/AccessMate.app"
echo ""
echo -e "${BLUE}To install:${NC}"
echo -e "  cp -R $DIST_DIR/AccessMate.app /Applications/"
echo ""

# Clean up temporary files
echo -e "${BLUE}Cleaning up temporary files...${NC}"
rm -rf build/
rm -rf dist/
rm -f *.spec
rm -f mac_entry.py

echo -e "${GREEN}✅ Cleanup completed${NC}"
echo -e "${GREEN}macOS build process finished successfully!${NC}"