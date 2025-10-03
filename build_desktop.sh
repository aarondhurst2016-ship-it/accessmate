#!/bin/bash
# Enhanced cross-platform build script for AccessMate

set -e  # Exit on any error

echo "🚀 AccessMate Cross-Platform Build Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect platform
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    PLATFORM="windows"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
else
    echo -e "${RED}❌ Unsupported platform: $OSTYPE${NC}"
    exit 1
fi

echo -e "${BLUE}Detected platform: ${YELLOW}$PLATFORM${NC}"

# Install base requirements
echo -e "${BLUE}Installing base requirements...${NC}"
pip install -r requirements.txt
pip install pyinstaller

# Platform-specific builds
case $PLATFORM in
    "windows")
        echo -e "${BLUE}Building for Windows...${NC}"
        echo -e "${YELLOW}Note: For full Windows build with installer, use build_windows.bat${NC}"
        
        # Check if we have the enhanced spec file
        if [ -f "AccessMate-Fixed.spec" ]; then
            echo -e "${BLUE}Using enhanced Windows spec file...${NC}"
            pyinstaller --clean AccessMate-Fixed.spec
        else
            echo -e "${BLUE}Using basic PyInstaller build...${NC}"
            pyinstaller --onefile --windowed src/gui.py --name AccessMate
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Windows build completed${NC}"
            echo -e "${BLUE}Executable: ${YELLOW}dist/AccessMate.exe${NC}"
        else
            echo -e "${RED}❌ Windows build failed${NC}"
            exit 1
        fi
        ;;
        
    "macos")
        echo -e "${BLUE}Building for macOS...${NC}"
        echo -e "${YELLOW}For full macOS build with DMG installer, use: ./build_macos.sh${NC}"
        
        # Install macOS-specific requirements
        if [ -f "requirements-macos.txt" ]; then
            echo -e "${BLUE}Installing macOS-specific requirements...${NC}"
            pip install -r requirements-macos.txt
        fi
        
        # Use enhanced macOS entry point
        if [ -f "macos_entry.py" ]; then
            echo -e "${BLUE}Using enhanced macOS entry point...${NC}"
            pyinstaller --onefile --windowed macos_entry.py --name AccessMate
        elif [ -f "mac_linux_entry.py" ]; then
            echo -e "${BLUE}Using basic macOS entry point...${NC}"
            pyinstaller --onefile --windowed mac_linux_entry.py --name AccessMate
        else
            echo -e "${RED}❌ No macOS entry point found${NC}"
            exit 1
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ macOS build completed${NC}"
            echo -e "${BLUE}Executable: ${YELLOW}dist/AccessMate${NC}"
            echo -e "${YELLOW}For .app bundle with proper macOS integration, run: ./build_macos.sh${NC}"
        else
            echo -e "${RED}❌ macOS build failed${NC}"
            exit 1
        fi
        ;;
        
    "linux")
        echo -e "${BLUE}Building for Linux...${NC}"
        
        # Use the existing entry point
        if [ -f "mac_linux_entry.py" ]; then
            echo -e "${BLUE}Using Linux entry point...${NC}"
            pyinstaller --onefile --windowed mac_linux_entry.py --name AccessMate
        else
            echo -e "${RED}❌ No Linux entry point found${NC}"
            exit 1
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Linux build completed${NC}"
            echo -e "${BLUE}Executable: ${YELLOW}dist/AccessMate${NC}"
        else
            echo -e "${RED}❌ Linux build failed${NC}"
            exit 1
        fi
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Build complete for $PLATFORM!${NC}"
echo -e "${BLUE}Check the ${YELLOW}dist/${NC} ${BLUE}directory for your executable${NC}"

# Platform-specific next steps
case $PLATFORM in
    "windows")
        echo -e "${BLUE}Next steps for Windows:${NC}"
        echo -e "  • Test: ${YELLOW}dist/AccessMate.exe${NC}"
        echo -e "  • For installer: Run ${YELLOW}build_windows.bat${NC}"
        ;;
    "macos")
        echo -e "${BLUE}Next steps for macOS:${NC}"
        echo -e "  • Test: ${YELLOW}./dist/AccessMate${NC}"
        echo -e "  • For .app bundle: ${YELLOW}./build_macos.sh${NC}"
        echo -e "  • For App Store: See ${YELLOW}MACOS_BUILD_GUIDE.md${NC}"
        ;;
    "linux")
        echo -e "${BLUE}Next steps for Linux:${NC}"
        echo -e "  • Test: ${YELLOW}./dist/AccessMate${NC}"
        echo -e "  • Make executable: ${YELLOW}chmod +x dist/AccessMate${NC}"
        ;;
esac
