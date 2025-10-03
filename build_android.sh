#!/bin/bash
# build_android.sh - Comprehensive Android build script for AccessMate

set -e  # Exit on any error

echo "🤖 AccessMate Android Build Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="AccessMate"
VERSION="1.0.0"
BUILD_TYPE="${BUILD_TYPE:-debug}"  # debug or release
CLEAN_BUILD="${CLEAN_BUILD:-false}"
ARCH="${ARCH:-arm64-v8a,armeabi-v7a}"

echo -e "${BLUE}Build configuration:${NC}"
echo -e "App: ${YELLOW}$APP_NAME${NC}"
echo -e "Version: ${YELLOW}$VERSION${NC}"
echo -e "Build Type: ${YELLOW}$BUILD_TYPE${NC}"
echo -e "Architecture: ${YELLOW}$ARCH${NC}"
echo -e "Clean Build: ${YELLOW}$CLEAN_BUILD${NC}"
echo ""

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

# Check if buildozer is installed
if ! python -m buildozer --version >/dev/null 2>&1; then
    echo -e "${RED}❌ Buildozer not found. Installing...${NC}"
    pip install buildozer
    echo -e "${GREEN}✅ Buildozer installed${NC}"
else
    echo -e "${GREEN}✅ Buildozer found${NC}"
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"

# Check for Java (required for Android builds)
if command -v java >/dev/null 2>&1; then
    JAVA_VERSION=$(java -version 2>&1 | head -n1 | cut -d'"' -f2)
    echo -e "${GREEN}✅ Java $JAVA_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Java not found. Android build may fail.${NC}"
    echo -e "${BLUE}Install Java JDK 11 or later for Android builds${NC}"
fi

# Check buildozer.spec exists
if [ ! -f "buildozer.spec" ]; then
    echo -e "${RED}❌ buildozer.spec not found${NC}"
    echo -e "${BLUE}Run 'buildozer init' to create initial configuration${NC}"
    exit 1
else
    echo -e "${GREEN}✅ buildozer.spec found${NC}"
fi

# Check mobial directory
if [ ! -d "mobial" ]; then
    echo -e "${RED}❌ mobial directory not found${NC}"
    echo -e "${BLUE}The mobial directory contains the mobile version of AccessMate${NC}"
    exit 1
else
    echo -e "${GREEN}✅ mobial directory found${NC}"
fi

echo ""

# Pre-build setup
echo -e "${BLUE}Setting up build environment...${NC}"

# Create required directories
mkdir -p bin
mkdir -p .buildozer

# Clean build if requested
if [ "$CLEAN_BUILD" = true ]; then
    echo -e "${BLUE}Cleaning previous build...${NC}"
    python -m buildozer android clean
    rm -rf .buildozer/android/
    echo -e "${GREEN}✅ Build cleaned${NC}"
fi

# Update buildozer.spec with current configuration
echo -e "${BLUE}Updating buildozer configuration...${NC}"

# Update version in buildozer.spec
sed -i.bak "s/^version = .*/version = $VERSION/" buildozer.spec

# Update architecture if specified
if [ -n "$ARCH" ]; then
    sed -i.bak "s/^android.archs = .*/android.archs = $ARCH/" buildozer.spec
fi

echo -e "${GREEN}✅ Configuration updated${NC}"

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Main dependencies installed${NC}"
fi

if [ -f "mobial/requirements.txt" ]; then
    pip install -r mobial/requirements.txt
    echo -e "${GREEN}✅ Mobile dependencies installed${NC}"
fi

# Install buildozer dependencies
echo -e "${BLUE}Installing buildozer dependencies...${NC}"
pip install cython

echo ""

# Build APK
echo -e "${BLUE}Building Android APK...${NC}"
echo -e "${YELLOW}This may take 15-30 minutes on first build...${NC}"

START_TIME=$(date +%s)

if [ "$BUILD_TYPE" = "release" ]; then
    echo -e "${BLUE}Building release APK...${NC}"
    python -m buildozer android release
    
    APK_FILE="bin/accessmate-$VERSION-arm64-v8a-release.apk"
    
elif [ "$BUILD_TYPE" = "debug" ]; then
    echo -e "${BLUE}Building debug APK...${NC}"
    python -m buildozer android debug
    
    APK_FILE="bin/accessmate-$VERSION-arm64-v8a-debug.apk"
else
    echo -e "${RED}❌ Invalid build type: $BUILD_TYPE${NC}"
    echo -e "${BLUE}Use 'debug' or 'release'${NC}"
    exit 1
fi

END_TIME=$(date +%s)
BUILD_TIME=$((END_TIME - START_TIME))

# Check if build was successful
if [ -f "$APK_FILE" ]; then
    echo -e "${GREEN}✅ Android APK build completed successfully!${NC}"
    
    # Get APK information
    APK_SIZE=$(du -sh "$APK_FILE" | cut -f1)
    
    echo ""
    echo -e "${GREEN}🎉 Build Summary${NC}"
    echo -e "${BLUE}===============${NC}"
    echo -e "APK File: ${YELLOW}$APK_FILE${NC}"
    echo -e "Size: ${YELLOW}$APK_SIZE${NC}"
    echo -e "Build Type: ${YELLOW}$BUILD_TYPE${NC}"
    echo -e "Build Time: ${YELLOW}${BUILD_TIME}s${NC}"
    echo -e "Architecture: ${YELLOW}$ARCH${NC}"
    
    # APK information using aapt if available
    if command -v aapt >/dev/null 2>&1; then
        echo ""
        echo -e "${BLUE}APK Information:${NC}"
        aapt dump badging "$APK_FILE" | head -5
    fi
    
else
    echo -e "${RED}❌ Android APK build failed${NC}"
    echo -e "${BLUE}Check the build log above for errors${NC}"
    
    # Common troubleshooting tips
    echo ""
    echo -e "${YELLOW}Common build issues:${NC}"
    echo -e "1. Java not installed or wrong version"
    echo -e "2. Android SDK/NDK download issues (check internet)"
    echo -e "3. Missing Python dependencies"
    echo -e "4. Insufficient disk space (need ~10GB)"
    echo -e "5. Permission issues with build directories"
    echo ""
    echo -e "${BLUE}Try running with clean build: CLEAN_BUILD=true ./build_android.sh${NC}"
    exit 1
fi

# Installation instructions
echo ""
echo -e "${BLUE}Installation Instructions:${NC}"
echo -e "${BLUE}========================${NC}"

if [ "$BUILD_TYPE" = "debug" ]; then
    echo -e "Debug APK (for testing):"
    echo -e "1. Enable 'Unknown Sources' in Android Settings"
    echo -e "2. Transfer APK to Android device"
    echo -e "3. Install: ${YELLOW}adb install $APK_FILE${NC}"
    echo -e "4. Or open APK file on device to install"
elif [ "$BUILD_TYPE" = "release" ]; then
    echo -e "Release APK (for distribution):"
    echo -e "1. Sign APK for Google Play Store"
    echo -e "2. Or distribute as-is for direct installation"
    echo -e "3. Install: ${YELLOW}adb install $APK_FILE${NC}"
fi

echo ""
echo -e "${BLUE}Testing Instructions:${NC}"
echo -e "1. Install APK on Android device"
echo -e "2. Grant accessibility permissions in Settings"
echo -e "3. Grant microphone and camera permissions"
echo -e "4. Test speech recognition and TTS features"
echo -e "5. Test accessibility service integration"

echo ""
echo -e "${BLUE}Next Steps:${NC}"
if [ "$BUILD_TYPE" = "debug" ]; then
    echo -e "• Test thoroughly on Android devices"
    echo -e "• Build release version: ${YELLOW}BUILD_TYPE=release ./build_android.sh${NC}"
    echo -e "• Sign APK for Play Store distribution"
elif [ "$BUILD_TYPE" = "release" ]; then
    echo -e "• Test release APK on multiple Android devices"
    echo -e "• Sign APK with your keystore for Play Store"
    echo -e "• Upload to Google Play Console"
fi

# Build information file
echo -e "${BLUE}Creating build information file...${NC}"

cat > "bin/BUILD_INFO_ANDROID.txt" << EOF
AccessMate Android Build Information
===================================

Build Date: $(date)
Version: $VERSION
Build Type: $BUILD_TYPE
Architecture: $ARCH
APK File: $APK_FILE
APK Size: $APK_SIZE
Build Time: ${BUILD_TIME}s

Android Configuration:
- Target API: 34
- Minimum API: 21
- NDK: 25b
- Architecture: $ARCH

Permissions:
- Accessibility Service
- Microphone (speech recognition)
- Camera (object recognition)
- Storage (settings and logs)
- Network (integrations)
- Location (navigation assistance)
- Bluetooth (accessibility devices)

Installation:
1. Enable 'Unknown Sources' in Android Settings > Security
2. Transfer APK to Android device via USB, email, or cloud
3. Tap APK file to install, or use: adb install $APK_FILE
4. Grant accessibility permissions: Settings > Accessibility > AccessMate
5. Grant microphone and camera permissions when prompted

First Run:
- App will request accessibility service permissions
- Enable AccessMate in Accessibility Settings
- Grant microphone permission for speech recognition
- Grant camera permission for object recognition (optional)
- Configure TTS settings if needed

Troubleshooting:
- If app crashes, check Android system logs: adb logcat
- Ensure all permissions are granted in App Settings
- For accessibility features, enable AccessMate service in Settings
- Speech recognition requires internet connection
- TTS should work offline with system voices

Distribution:
- Debug APK: For testing only, not suitable for Play Store
- Release APK: Sign with your keystore for distribution
- Google Play: Requires signed release APK and Play Console account
EOF

echo -e "${GREEN}✅ Build information saved to bin/BUILD_INFO_ANDROID.txt${NC}"

echo ""
echo -e "${GREEN}🚀 Android build process completed successfully!${NC}"

# Cleanup
rm -f buildozer.spec.bak 2>/dev/null || true

echo -e "${BLUE}APK ready for testing: ${YELLOW}$APK_FILE${NC}"