# macOS Deployment Guide for AccessMate

This guide covers building, signing, and distributing AccessMate on macOS.

## Prerequisites

### Required Software
- macOS 10.13 or later
- Python 3.9 or later
- Xcode Command Line Tools: `xcode-select --install`
- PyInstaller: `pip3 install pyinstaller`

### Optional (for professional distribution)
- Apple Developer Account (for code signing and App Store)
- Xcode (full version, from App Store)
- create-dmg: `brew install create-dmg`

## Quick Build

For a simple build to test locally:

```bash
chmod +x build_macos.sh
./build_macos.sh
```

This will create:
- `dist_macos/AccessMate.app` - The application bundle
- `dist_macos/AccessMate-1.0.0.dmg` - Installer DMG (if create-dmg available)
- `dist_macos/BUILD_INFO.txt` - Build information

## Manual Build Steps

If you prefer to build manually or customize the process:

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
pip3 install -r requirements-macos.txt
```

### 2. Build with PyInstaller
```bash
pyinstaller --clean AccessMate-macOS.spec
```

### 3. Create App Bundle
The spec file will automatically create an `.app` bundle with proper Info.plist.

### 4. Test the Application
```bash
open dist/AccessMate.app
```

## Code Signing (For Distribution)

### Quick Setup (Recommended)
Run the interactive setup script:
```bash
chmod +x setup_macos_signing.sh
./setup_macos_signing.sh
```

This will guide you through:
- Checking for existing certificates
- Configuring Bundle ID and Team ID
- Setting up notarization (optional)
- Testing the configuration

### Manual Setup
1. Join Apple Developer Program ($99/year)
2. Create certificates in Xcode or Developer Portal
3. Configure signing in one of these ways:

**Option A: Edit build_macos.sh**
```bash
DEVELOPER_TEAM="YOUR_TEAM_ID_HERE"
BUNDLE_ID="com.yourname.accessmate"
```

**Option B: Environment variables**
```bash
export ACCESSMATE_TEAM_ID="YOUR_TEAM_ID"
export ACCESSMATE_BUNDLE_ID="com.yourname.accessmate"
./build_macos.sh
```

**Option C: Use generated environment file**
```bash
source macos_signing_env.sh
./build_macos.sh
```

### Verify Signature
The build script automatically verifies signatures, or check manually:
```bash
codesign --verify --deep --strict dist_macos/AccessMate.app
spctl --assess --verbose dist_macos/AccessMate.app
```

## Notarization (Required for Gatekeeper)

### 1. Create App Store Connect API Key
- Log into App Store Connect
- Go to Users and Access > Keys
- Create a new API key with Developer role
- Download the .p8 file

### 2. Submit for Notarization
```bash
xcrun notarytool submit dist_macos/AccessMate-1.0.0.dmg \
  --key-id YOUR_KEY_ID \
  --issuer-id YOUR_ISSUER_ID \
  --key AuthKey_YOUR_KEY_ID.p8 \
  --wait
```

### 3. Staple the Notarization
```bash
xcrun stapler staple dist_macos/AccessMate.app
xcrun stapler staple dist_macos/AccessMate-1.0.0.dmg
```

## App Store Distribution

### 1. Create App Store Version Spec
Use `py2app` instead of PyInstaller for App Store builds:

```bash
python3 setup_macos_appstore.py py2app
```

### 2. App Store Requirements
- Code signing with Distribution certificate
- Sandbox entitlements
- App review guidelines compliance
- Privacy policy for accessibility features

### 3. Upload to App Store Connect
```bash
xcrun altool --upload-app --file AccessMate.pkg \
  --username YOUR_APPLE_ID \
  --password YOUR_APP_PASSWORD
```

## DMG Installer Creation

### Using create-dmg (Recommended)
```bash
create-dmg \
  --volname "AccessMate Installer" \
  --volicon "src/accessmate_logo.png" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "AccessMate.app" 175 120 \
  --hide-extension "AccessMate.app" \
  --app-drop-link 425 120 \
  "AccessMate-1.0.0.dmg" \
  "dist_macos/"
```

### Using hdiutil (Basic)
```bash
hdiutil create -format UDZO -srcfolder "dist_macos/" -volname "AccessMate Installer" "AccessMate-1.0.0.dmg"
```

## Troubleshooting

### Common Issues

**"AccessMate.app is damaged and can't be opened"**
- App needs to be code signed
- Run: `codesign --force --deep --sign - AccessMate.app`

**"AccessMate can't be opened because Apple cannot check it for malicious software"**
- App needs notarization for Gatekeeper
- Users can bypass: System Preferences > Security & Privacy > Allow

**Tkinter/Tcl issues**
- The build script handles Tcl/Tk path setup automatically
- Verify paths in the PyInstaller spec file match your system

**Import errors**
- Check all dependencies are installed
- Use `pip3 list` to verify packages
- Check Python path in the entry point

**Audio/microphone not working**
- Add usage descriptions to Info.plist (handled by spec file)
- User must grant permissions in System Preferences

### Build Script Configuration

Edit variables at the top of `build_macos.sh`:

```bash
APP_NAME="AccessMate"
VERSION="1.0.0"
BUNDLE_ID="com.accessmate.app" 
DEVELOPER_TEAM=""  # Your Apple Developer Team ID
```

## File Structure After Build

```
dist_macos/
├── AccessMate.app/                 # Main application bundle
│   ├── Contents/
│   │   ├── Info.plist             # App metadata
│   │   ├── MacOS/AccessMate        # Executable
│   │   └── Resources/             # App resources
├── AccessMate-1.0.0.dmg           # Installer DMG
└── BUILD_INFO.txt                 # Build information
```

## Distribution Checklist

- [ ] App builds and launches correctly
- [ ] All features work (speech, camera, microphone)
- [ ] Code signed with valid certificate
- [ ] Notarized (if distributing outside App Store)
- [ ] DMG installer created and tested
- [ ] Privacy policy updated for macOS features
- [ ] Installation instructions provided
- [ ] Support documentation updated

## Automated CI/CD

For automated builds, consider using GitHub Actions with macOS runners:

```yaml
- name: Build macOS App
  run: |
    chmod +x build_macos.sh
    ./build_macos.sh
  
- name: Upload DMG
  uses: actions/upload-artifact@v3
  with:
    name: AccessMate-macOS
    path: dist_macos/AccessMate-*.dmg
```

## Support

For build issues specific to macOS:
1. Check the build log in terminal
2. Verify all dependencies are installed
3. Test on a clean macOS system
4. Check Apple Developer documentation for code signing

The build script provides detailed output and creates a BUILD_INFO.txt file with system information for debugging.