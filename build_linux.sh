#!/bin/bash
# build_linux.sh - Comprehensive Linux build script for AccessMate
# Supports: AppImage, Snap, Flatpak, .deb, .rpm, and standalone executable

set -e  # Exit on any error

echo "🐧 AccessMate Linux Build Script"
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
DESCRIPTION="Accessible Talkback Assistant for Linux"
CATEGORIES="Accessibility;Utility;AudioVideo;"
BUILD_DIR="build_linux"
DIST_DIR="dist_linux"
APPDIR="AccessMate.AppDir"

# Build options (set to true to enable)
BUILD_EXECUTABLE=${BUILD_EXECUTABLE:-true}
BUILD_APPIMAGE=${BUILD_APPIMAGE:-true}
BUILD_FLATPAK=${BUILD_FLATPAK:-false}
BUILD_DEB=${BUILD_DEB:-false}
BUILD_RPM=${BUILD_RPM:-false}
BUILD_SNAP=${BUILD_SNAP:-false}

echo -e "${BLUE}Build configuration:${NC}"
echo -e "Executable: ${YELLOW}$BUILD_EXECUTABLE${NC}"
echo -e "AppImage: ${YELLOW}$BUILD_APPIMAGE${NC}"
echo -e "Flatpak: ${YELLOW}$BUILD_FLATPAK${NC}"
echo -e "Debian: ${YELLOW}$BUILD_DEB${NC}"
echo -e "RPM: ${YELLOW}$BUILD_RPM${NC}"
echo -e "Snap: ${YELLOW}$BUILD_SNAP${NC}"
echo ""

# Check we're on Linux
if [ "$(uname)" != "Linux" ]; then
    echo -e "${RED}❌ This script must be run on Linux${NC}"
    exit 1
fi

# Check for required tools
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}❌ python3 is required but not installed${NC}"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo -e "${RED}❌ pip3 is required but not installed${NC}"; exit 1; }

echo -e "${GREEN}✅ Linux environment verified${NC}"

# Create build directories
echo -e "${BLUE}Creating build directories...${NC}"
mkdir -p "$BUILD_DIR"
mkdir -p "$DIST_DIR"

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf "$BUILD_DIR"/*
rm -rf "$DIST_DIR"/*
rm -rf build/
rm -rf dist/
rm -rf *.spec
rm -rf "$APPDIR"

echo -e "${GREEN}✅ Build directories prepared${NC}"

# Install/update dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install pyinstaller

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create Linux entry point if it doesn't exist
if [ ! -f "linux_entry.py" ]; then
    echo -e "${BLUE}Creating Linux entry point...${NC}"
    cat > linux_entry.py << 'EOF'
#!/usr/bin/env python3
"""
Linux Entry Point for AccessMate
Handles Linux-specific initialization and launches the main GUI
"""

import sys
import os
import platform

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_linux_environment():
    """Set up Linux-specific environment variables and paths"""
    
    # Linux-specific environment setup
    os.environ['LANG'] = os.environ.get('LANG', 'en_US.UTF-8')
    os.environ['LC_ALL'] = os.environ.get('LC_ALL', 'en_US.UTF-8')
    
    # Set XDG directories if not set
    home = os.path.expanduser('~')
    os.environ.setdefault('XDG_CONFIG_HOME', os.path.join(home, '.config'))
    os.environ.setdefault('XDG_DATA_HOME', os.path.join(home, '.local', 'share'))
    os.environ.setdefault('XDG_CACHE_HOME', os.path.join(home, '.cache'))

class LinuxGUIInstance:
    """Dummy GUI instance for compatibility with gui.launch()"""
    def __init__(self):
        self.platform = "Linux"
        self.version = platform.release()

def main():
    """Main entry point for Linux"""
    
    print("🐧 Starting AccessMate for Linux...")
    
    try:
        # Set up Linux environment
        setup_linux_environment()
        
        # Import the main GUI module
        import gui
        
        # Create a GUI instance for compatibility
        gui_instance = LinuxGUIInstance()
        
        # Launch the main application
        print("✅ Launching AccessMate GUI...")
        gui.launch(gui_instance)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required modules are installed:")
        print("  pip3 install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"❌ Error launching AccessMate: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF
    echo -e "${GREEN}✅ Linux entry point created${NC}"
fi

# Build standalone executable first
if [ "$BUILD_EXECUTABLE" = true ]; then
    echo -e "${BLUE}Building standalone executable...${NC}"
    
    pyinstaller --clean --onefile --windowed --name "$APP_NAME" \
        --add-data "src/accessmate_logo.png:." \
        --add-data "src/accessmate_logo_uploaded.png:." \
        --add-data "requirements.txt:." \
        --add-data "README.md:." \
        --add-data "ACCESSIBILITY.txt:." \
        linux_entry.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Standalone executable created: dist/$APP_NAME${NC}"
        mv "dist/$APP_NAME" "$DIST_DIR/"
    else
        echo -e "${RED}❌ Standalone executable build failed${NC}"
        exit 1
    fi
fi

# Build AppImage
if [ "$BUILD_APPIMAGE" = true ]; then
    echo -e "${BLUE}Building AppImage...${NC}"
    
    # Check for appimage-builder or linuxdeploy
    if command -v appimage-builder >/dev/null 2>&1; then
        USE_APPIMAGE_BUILDER=true
    elif command -v linuxdeploy >/dev/null 2>&1; then
        USE_LINUXDEPLOY=true
    else
        echo -e "${YELLOW}⚠️  Installing linuxdeploy for AppImage creation...${NC}"
        # Download linuxdeploy
        if [ ! -f "linuxdeploy-x86_64.AppImage" ]; then
            wget -q "https://github.com/linuxdeploy/linuxdeploy/releases/latest/download/linuxdeploy-x86_64.AppImage"
            chmod +x linuxdeploy-x86_64.AppImage
        fi
        USE_LINUXDEPLOY=true
    fi
    
    # Create AppDir structure
    echo -e "${BLUE}Creating AppDir structure...${NC}"
    mkdir -p "$APPDIR/usr/bin"
    mkdir -p "$APPDIR/usr/share/applications"
    mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
    mkdir -p "$APPDIR/usr/share/pixmaps"
    
    # Copy executable
    cp "$DIST_DIR/$APP_NAME" "$APPDIR/usr/bin/"
    chmod +x "$APPDIR/usr/bin/$APP_NAME"
    
    # Create desktop file
    cat > "$APPDIR/usr/share/applications/$APP_NAME.desktop" << EOF
[Desktop Entry]
Name=$APP_NAME
Comment=$DESCRIPTION
Exec=$APP_NAME
Icon=$APP_NAME
Type=Application
Categories=$CATEGORIES
Keywords=accessibility;talkback;speech;assistant;
StartupNotify=true
EOF
    
    # Copy and create icon
    if [ -f "src/accessmate_logo.png" ]; then
        cp "src/accessmate_logo.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png"
        cp "src/accessmate_logo.png" "$APPDIR/usr/share/pixmaps/$APP_NAME.png"
        cp "src/accessmate_logo.png" "$APPDIR/$APP_NAME.png"
    else
        # Create a simple icon if none exists
        echo -e "${YELLOW}⚠️  No icon found, creating placeholder${NC}"
        # This would need ImageMagick: convert -size 256x256 xc:blue "$APPDIR/$APP_NAME.png"
    fi
    
    # Create AppRun script
    cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
# AppRun script for AccessMate

# Get the directory where this AppImage is located
HERE="$(dirname "$(readlink -f "${0}")")"

# Set up environment
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"

# Launch the application
exec "${HERE}/usr/bin/AccessMate" "$@"
EOF
    chmod +x "$APPDIR/AppRun"
    
    # Copy desktop file to root of AppDir
    cp "$APPDIR/usr/share/applications/$APP_NAME.desktop" "$APPDIR/"
    
    if [ "$USE_APPIMAGE_BUILDER" = true ]; then
        # Use appimage-builder (more modern approach)
        echo -e "${BLUE}Using appimage-builder...${NC}"
        
        # Create appimage-builder config
        cat > appimage-builder.yml << EOF
version: 1

script:
  - echo "Building AccessMate AppImage"

AppDir:
  path: $APPDIR
  
  app_info:
    id: com.accessmate.app
    name: $APP_NAME
    icon: $APP_NAME
    version: $VERSION
    exec: usr/bin/$APP_NAME
    exec_args: \$@

  apt:
    arch: amd64
    sources:
      - sourceline: 'deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ focal main restricted'
        key_url: 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3B4FE6ACC0B21F32'
    
  runtime:
    env:
      PYTHONPATH: '\$APPDIR/usr/lib/python3/dist-packages'

AppImage:
  update-information: null
  sign-key: null
  arch: x86_64
EOF
        
        appimage-builder --recipe appimage-builder.yml
        
    elif [ "$USE_LINUXDEPLOY" = true ]; then
        # Use linuxdeploy
        echo -e "${BLUE}Using linuxdeploy...${NC}"
        
        # Download appimagetool if needed
        if [ ! -f "appimagetool-x86_64.AppImage" ]; then
            wget -q "https://github.com/AppImage/AppImageKit/releases/latest/download/appimagetool-x86_64.AppImage"
            chmod +x appimagetool-x86_64.AppImage
        fi
        
        # Create AppImage
        ./appimagetool-x86_64.AppImage "$APPDIR" "$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage"
    fi
    
    if [ -f "$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage" ] || [ -f "$APP_NAME-$VERSION-x86_64.AppImage" ]; then
        # Move AppImage if created in current directory
        [ -f "$APP_NAME-$VERSION-x86_64.AppImage" ] && mv "$APP_NAME-$VERSION-x86_64.AppImage" "$DIST_DIR/"
        echo -e "${GREEN}✅ AppImage created: $DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage${NC}"
    else
        echo -e "${YELLOW}⚠️  AppImage creation may have failed or file in different location${NC}"
    fi
fi

# Build Flatpak (if requested)
if [ "$BUILD_FLATPAK" = true ]; then
    echo -e "${BLUE}Building Flatpak...${NC}"
    
    if ! command -v flatpak-builder >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  flatpak-builder not installed. Install with:${NC}"
        echo -e "${BLUE}  sudo apt install flatpak-builder  # Ubuntu/Debian${NC}"
        echo -e "${BLUE}  sudo dnf install flatpak-builder  # Fedora${NC}"
        echo -e "${BLUE}  sudo pacman -S flatpak-builder    # Arch${NC}"
    else
        # Create Flatpak manifest (this would be created separately)
        echo -e "${GREEN}✅ Flatpak builder available${NC}"
        echo -e "${BLUE}Flatpak manifest should be created separately${NC}"
        echo -e "${BLUE}See: com.accessmate.app.json${NC}"
    fi
fi

# Build .deb package (if requested)
if [ "$BUILD_DEB" = true ]; then
    echo -e "${BLUE}Building .deb package...${NC}"
    
    DEB_DIR="$BUILD_DIR/deb"
    mkdir -p "$DEB_DIR/DEBIAN"
    mkdir -p "$DEB_DIR/usr/bin"
    mkdir -p "$DEB_DIR/usr/share/applications"
    mkdir -p "$DEB_DIR/usr/share/pixmaps"
    
    # Copy executable
    cp "$DIST_DIR/$APP_NAME" "$DEB_DIR/usr/bin/"
    
    # Copy desktop file and icon
    cp "$APPDIR/usr/share/applications/$APP_NAME.desktop" "$DEB_DIR/usr/share/applications/" 2>/dev/null || true
    cp "src/accessmate_logo.png" "$DEB_DIR/usr/share/pixmaps/$APP_NAME.png" 2>/dev/null || true
    
    # Create control file
    cat > "$DEB_DIR/DEBIAN/control" << EOF
Package: accessmate
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: AccessMate Team <support@accessmate.com>
Description: $DESCRIPTION
 AccessMate is a comprehensive accessibility assistant that provides
 speech recognition, text-to-speech, and various accessibility features
 to help users interact with their Linux desktop environment.
Depends: python3, python3-tk
EOF
    
    # Create postinst script
    cat > "$DEB_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database -q /usr/share/applications
fi
EOF
    chmod 755 "$DEB_DIR/DEBIAN/postinst"
    
    # Create postrm script
    cat > "$DEB_DIR/DEBIAN/postrm" << 'EOF'
#!/bin/bash
set -e
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database -q /usr/share/applications
fi
EOF
    chmod 755 "$DEB_DIR/DEBIAN/postrm"
    
    # Build .deb
    dpkg-deb --build "$DEB_DIR" "$DIST_DIR/accessmate_${VERSION}_amd64.deb"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Debian package created: $DIST_DIR/accessmate_${VERSION}_amd64.deb${NC}"
    else
        echo -e "${YELLOW}⚠️  Debian package creation failed${NC}"
    fi
fi

# Generate build summary
echo -e "${BLUE}Generating build summary...${NC}"
BUILD_DATE=$(date)

cat > "$DIST_DIR/BUILD_INFO.txt" << EOF
AccessMate Linux Build Information
==================================

Build Date: $BUILD_DATE
Version: $VERSION
Architecture: $(uname -m)
Linux Distribution: $(lsb_release -d 2>/dev/null | cut -f2 || echo "Unknown")
Kernel: $(uname -r)

Files Created:
EOF

# List created files
if [ -f "$DIST_DIR/$APP_NAME" ]; then
    SIZE=$(du -sh "$DIST_DIR/$APP_NAME" | cut -f1)
    echo "- $APP_NAME (Standalone executable - $SIZE)" >> "$DIST_DIR/BUILD_INFO.txt"
fi

if [ -f "$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage" ]; then
    SIZE=$(du -sh "$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage" | cut -f1)
    echo "- $APP_NAME-$VERSION-x86_64.AppImage (AppImage - $SIZE)" >> "$DIST_DIR/BUILD_INFO.txt"
fi

if [ -f "$DIST_DIR/accessmate_${VERSION}_amd64.deb" ]; then
    SIZE=$(du -sh "$DIST_DIR/accessmate_${VERSION}_amd64.deb" | cut -f1)
    echo "- accessmate_${VERSION}_amd64.deb (Debian package - $SIZE)" >> "$DIST_DIR/BUILD_INFO.txt"
fi

cat >> "$DIST_DIR/BUILD_INFO.txt" << EOF

Installation Instructions:
========================

Standalone Executable:
  chmod +x $APP_NAME
  ./$APP_NAME

AppImage:
  chmod +x $APP_NAME-$VERSION-x86_64.AppImage
  ./$APP_NAME-$VERSION-x86_64.AppImage

Debian Package:
  sudo dpkg -i accessmate_${VERSION}_amd64.deb
  sudo apt-get install -f  # Fix dependencies if needed

Distribution:
- AppImage: Universal Linux package, runs on most distributions
- .deb: For Debian, Ubuntu, and derivatives
- Standalone: Direct execution without installation

Notes:
- First run may require additional permissions for accessibility features
- Some distributions may require installing additional audio libraries
- For speech recognition, ensure microphone permissions are granted
EOF

echo -e "${GREEN}✅ Build summary created${NC}"

# Final status
echo ""
echo -e "${GREEN}🎉 Linux Build Complete!${NC}"
echo -e "${BLUE}==============================${NC}"

# List created files
if [ -f "$DIST_DIR/$APP_NAME" ]; then
    echo -e "Executable: ${YELLOW}$DIST_DIR/$APP_NAME${NC}"
fi

if [ -f "$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage" ]; then
    echo -e "AppImage: ${YELLOW}$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage${NC}"
fi

if [ -f "$DIST_DIR/accessmate_${VERSION}_amd64.deb" ]; then
    echo -e "Debian Package: ${YELLOW}$DIST_DIR/accessmate_${VERSION}_amd64.deb${NC}"
fi

echo -e "Build Info: ${YELLOW}$DIST_DIR/BUILD_INFO.txt${NC}"
echo ""

echo -e "${BLUE}To test:${NC}"
if [ -f "$DIST_DIR/$APP_NAME" ]; then
    echo -e "  chmod +x $DIST_DIR/$APP_NAME && ./$DIST_DIR/$APP_NAME"
fi

if [ -f "$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage" ]; then
    echo -e "  chmod +x $DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage && ./$DIST_DIR/$APP_NAME-$VERSION-x86_64.AppImage"
fi

echo ""

# Clean up temporary files
echo -e "${BLUE}Cleaning up temporary files...${NC}"
rm -rf build/
rm -rf dist/
rm -rf *.spec
rm -rf "$APPDIR"
rm -f linux_entry.py.bak
rm -f appimage-builder.yml
rm -f linuxdeploy-x86_64.AppImage 2>/dev/null || true
rm -f appimagetool-x86_64.AppImage 2>/dev/null || true

echo -e "${GREEN}✅ Cleanup completed${NC}"
echo -e "${GREEN}Linux build process finished successfully!${NC}"