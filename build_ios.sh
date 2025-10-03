#!/bin/bash
# build_ios.sh - Comprehensive iOS build script for AccessMate using kivy-ios

set -e  # Exit on any error

echo "📱 AccessMate iOS Build Script"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="AccessMate"
PROJECT_NAME="accessmate-ios"
VERSION="1.0.0"
BUNDLE_ID="com.accessmate.app"  # Change to your unique bundle ID
DEVELOPER_TEAM="${ACCESSMATE_TEAM_ID:-}"  # Set via env var
SIGNING_IDENTITY="${ACCESSMATE_SIGNING_IDENTITY:-}"  
BUILD_TYPE="debug"  # debug or release
CLEAN_BUILD=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --release)
            BUILD_TYPE="release"
            shift
            ;;
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        --team-id)
            DEVELOPER_TEAM="$2"
            shift 2
            ;;
        --bundle-id)
            BUNDLE_ID="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --release          Build release version (default: debug)"
            echo "  --clean            Clean build (removes all cached data)"
            echo "  --team-id ID       Apple Developer Team ID"
            echo "  --bundle-id ID     App Bundle Identifier"
            echo "  -h, --help         Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

log_info() {
    echo -e "${BLUE}$1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo "Build Configuration:"
echo "- App Name: $APP_NAME"
echo "- Project: $PROJECT_NAME"
echo "- Version: $VERSION"
echo "- Bundle ID: $BUNDLE_ID"
echo "- Build Type: $BUILD_TYPE"
echo "- Clean Build: $CLEAN_BUILD"
if [ -n "$DEVELOPER_TEAM" ]; then
    echo "- Team ID: $DEVELOPER_TEAM"
fi
echo

# Check we're on macOS
if [ "$(uname)" != "Darwin" ]; then
    log_error "This script must be run on macOS"
    exit 1
fi

log_success "Running on macOS"

# Check prerequisites
log_info "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
log_success "Python $PYTHON_VERSION found"

# Check Xcode
if ! command -v xcodebuild &> /dev/null; then
    log_error "Xcode is not installed or command line tools not available"
    echo "Install Xcode from App Store and run: xcode-select --install"
    exit 1
fi

XCODE_VERSION=$(xcodebuild -version | head -n1 | cut -d' ' -f2)
log_success "Xcode $XCODE_VERSION found"

# Check iOS SDK
IOS_SDK=$(xcodebuild -showsdks | grep iphoneos | tail -n1 | sed 's/.*iphoneos//' | tr -d ' ')
if [ -z "$IOS_SDK" ]; then
    log_error "iOS SDK not found"
    exit 1
fi
log_success "iOS SDK $IOS_SDK found"

# Check kivy-ios installation
if ! command -v kivy-ios &> /dev/null; then
    log_warning "kivy-ios not found. Installing..."
    pip3 install kivy-ios
    log_success "kivy-ios installed"
else
    log_success "kivy-ios found"
fi

# Verify kivy-ios can run
if ! kivy-ios --version &> /dev/null; then
    log_error "kivy-ios installation appears broken"
    echo "Try: pip3 install --upgrade kivy-ios"
    exit 1
fi

# Check for required files
if [ ! -f "ios_entry.py" ]; then
    log_error "ios_entry.py not found in current directory"
    exit 1
fi

if [ ! -d "mobial" ]; then
    log_error "mobial/ directory not found"
    echo "Make sure you're running from the AccessMate project root"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    log_error "requirements.txt not found"
    exit 1
fi

log_success "All prerequisites met"

# Clean build if requested
if [ "$CLEAN_BUILD" = true ]; then
    log_info "Performing clean build..."
    rm -rf .kivy-ios-build
    rm -rf kivy-ios-build
    kivy-ios clean || true
    log_success "Clean completed"
fi

# Create the iOS project
log_info "Creating iOS project with kivy-ios..."

# Generate project with kivy-ios
kivy-ios create "$PROJECT_NAME" ios_entry.py

if [ ! -d "$PROJECT_NAME-ios" ]; then
    log_error "Failed to create iOS project directory"
    exit 1
fi

log_success "iOS project created: $PROJECT_NAME-ios/"

# Build Python dependencies
log_info "Building Python dependencies for iOS..."

# Common dependencies for accessibility apps
DEPENDENCIES="python3 kivy pillow requests"

# Try to parse additional dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    log_info "Reading additional dependencies from requirements.txt..."
    # Filter out iOS-incompatible or already included packages
    EXTRA_DEPS=$(grep -v '^#' requirements.txt | grep -v '^$' | \
                grep -v 'kivy-ios' | grep -v 'pyaudio' | grep -v 'pygame' | \
                grep -v 'sounddevice' | grep -v 'pyinstaller' | grep -v 'buildozer' | \
                grep -v 'matplotlib' | grep -v 'scipy' | grep -v 'pandas' | \
                tr '\n' ' ')
    
    if [ -n "$EXTRA_DEPS" ]; then
        log_info "Additional dependencies: $EXTRA_DEPS"
        DEPENDENCIES="$DEPENDENCIES $EXTRA_DEPS"
    fi
fi

echo "Building dependencies: $DEPENDENCIES"

# Build each dependency
for dep in $DEPENDENCIES; do
    log_info "Building $dep..."
    if ! kivy-ios build "$dep"; then
        log_warning "Failed to build $dep - continuing without it"
    else
        log_success "Built $dep"
    fi
done

# Update the iOS project
log_info "Updating iOS project configuration..."

PROJECT_DIR="$PROJECT_NAME-ios"

# Update Info.plist with app information
PLIST_FILE="$PROJECT_DIR/$PROJECT_NAME-Info.plist"
if [ -f "$PLIST_FILE" ]; then
    # Update bundle identifier
    /usr/libexec/PlistBuddy -c "Set :CFBundleIdentifier $BUNDLE_ID" "$PLIST_FILE" 2>/dev/null || true
    
    # Update app name
    /usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName $APP_NAME" "$PLIST_FILE" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Set :CFBundleName $APP_NAME" "$PLIST_FILE" 2>/dev/null || true
    
    # Update version
    /usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $VERSION" "$PLIST_FILE" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Set :CFBundleVersion $VERSION" "$PLIST_FILE" 2>/dev/null || true
    
    # Add accessibility requirements
    /usr/libexec/PlistBuddy -c "Add :NSMicrophoneUsageDescription string 'AccessMate requires microphone access for voice commands and speech recognition.'" "$PLIST_FILE" 2>/dev/null || true
    /usr/libexec/PlistBuddy -c "Add :NSSpeechRecognitionUsageDescription string 'AccessMate uses speech recognition to provide voice-controlled accessibility features.'" "$PLIST_FILE" 2>/dev/null || true
    
    log_success "Updated Info.plist"
else
    log_warning "Info.plist not found at $PLIST_FILE"
fi

# Copy app icons if they exist
if [ -d "mobile_icons/ios" ]; then
    log_info "Copying iOS app icons..."
    ICON_DIR="$PROJECT_DIR/data"
    mkdir -p "$ICON_DIR"
    cp -r mobile_icons/ios/* "$ICON_DIR/" || true
    log_success "App icons copied"
fi

# Build the iOS project using Xcode
log_info "Building iOS project with Xcode..."

cd "$PROJECT_DIR"

# Set up code signing if team ID is provided
XCODE_ARGS=""
if [ -n "$DEVELOPER_TEAM" ]; then
    XCODE_ARGS="DEVELOPMENT_TEAM=$DEVELOPER_TEAM"
    log_info "Using development team: $DEVELOPER_TEAM"
fi

# Build for simulator or device based on build type
if [ "$BUILD_TYPE" = "release" ]; then
    log_info "Building for iOS device (release)..."
    xcodebuild -project "$PROJECT_NAME.xcodeproj" \
               -scheme "$PROJECT_NAME" \
               -configuration Release \
               -destination generic/platform=iOS \
               $XCODE_ARGS \
               build
else
    log_info "Building for iOS Simulator (debug)..."
    xcodebuild -project "$PROJECT_NAME.xcodeproj" \
               -scheme "$PROJECT_NAME" \
               -configuration Debug \
               -destination "platform=iOS Simulator,name=iPhone 15" \
               $XCODE_ARGS \
               build
fi

if [ $? -eq 0 ]; then
    log_success "iOS build completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Open $PROJECT_DIR/$PROJECT_NAME.xcodeproj in Xcode"
    echo "2. Configure code signing with your Apple Developer account"
    echo "3. Select your target device or simulator"
    echo "4. Click Run to install and test the app"
    
    if [ "$BUILD_TYPE" = "release" ]; then
        echo "5. Archive the app for App Store distribution"
    fi
    
else
    log_error "iOS build failed"
    echo
    echo "Common solutions:"
    echo "- Open Xcode and resolve any signing issues"
    echo "- Ensure your Apple Developer account is set up"
    echo "- Check that all required certificates are installed"
    echo "- Try building in Xcode directly for more detailed error messages"
    exit 1
fi

cd ..

echo
log_success "iOS build process completed!"
echo "Project location: $PROJECT_DIR/"