# iOS Development Guide for AccessMate

## Overview

This guide covers building, testing, and distributing AccessMate on iOS using kivy-ios and Xcode.

## Prerequisites

### Required Software

1. **macOS** (iOS development requires macOS)
2. **Xcode** (latest version from Mac App Store)
3. **Python 3.11+** 
4. **kivy-ios** (installed via pip)
5. **Apple Developer Account** (for device testing and App Store distribution)

### Installation Steps

```bash
# Install Xcode command line tools
xcode-select --install

# Install kivy-ios
pip3 install kivy-ios

# Verify installation
kivy-ios --version
```

### Apple Developer Setup

1. **Apple Developer Account**: Required for device testing and App Store distribution
2. **Certificates**: Download development and distribution certificates
3. **Provisioning Profiles**: Create profiles for your app bundle ID
4. **Bundle ID**: Register your unique bundle identifier (e.g., `com.yourcompany.accessmate`)

## Build Process

### Quick Build

```bash
# Make build script executable
chmod +x build_ios.sh

# Build for iOS simulator (debug)
./build_ios.sh

# Build for iOS device (release)
./build_ios.sh --release --team-id YOUR_TEAM_ID
```

### Manual Build Steps

1. **Create iOS Project**:
   ```bash
   kivy-ios create accessmate-ios ios_entry.py
   ```

2. **Build Dependencies**:
   ```bash
   kivy-ios build python3 kivy pillow requests
   ```

3. **Configure Project**:
   - Open `accessmate-ios/accessmate-ios.xcodeproj` in Xcode
   - Set bundle identifier: `com.yourcompany.accessmate`
   - Configure code signing with your Apple Developer account
   - Set deployment target to iOS 12.0+

4. **Build and Run**:
   - Select target device or simulator
   - Click "Run" in Xcode

## Configuration

### Bundle Identifier

Update in multiple places:
- `ios_config.ini`: `bundle_id = com.yourcompany.accessmate`
- Xcode project settings
- Apple Developer Console (App ID registration)

### App Permissions

AccessMate requires these iOS permissions:
- **Microphone**: For voice commands
- **Speech Recognition**: For speech-to-text
- **Camera**: For object detection (optional)

These are automatically added to Info.plist during build.

### App Icons

iOS app icons are located in `mobile_icons/ios/`:
- Various sizes from 29x29 to 1024x1024
- Automatically copied during build process
- Follow Apple's Human Interface Guidelines

## Code Signing

### Development Signing

1. **Automatic Signing** (Recommended for development):
   - Open project in Xcode
   - Select your development team
   - Xcode handles certificates automatically

2. **Manual Signing**:
   ```bash
   # Set team ID environment variable
   export ACCESSMATE_TEAM_ID="ABC123DEF4"
   
   # Build with specific team
   ./build_ios.sh --team-id ABC123DEF4
   ```

### Distribution Signing

For App Store distribution:
1. Create Distribution Certificate in Apple Developer Console
2. Create App Store Provisioning Profile
3. Archive app in Xcode
4. Upload to App Store Connect

## Testing

### iOS Simulator

```bash
# Build for simulator
./build_ios.sh

# Open in Xcode and run on simulator
open accessmate-ios/accessmate-ios.xcodeproj
```

### Physical Device

```bash
# Build for device with your team ID
./build_ios.sh --release --team-id YOUR_TEAM_ID

# Open in Xcode
# Select your connected device
# Click Run
```

### TestFlight Beta Testing

1. Archive app in Xcode (Product → Archive)
2. Upload to App Store Connect
3. Add beta testers
4. Distribute via TestFlight

## App Store Distribution

### Preparation

1. **App Store Connect Setup**:
   - Create app record
   - Upload app metadata
   - Add screenshots
   - Set pricing and availability

2. **App Review Preparation**:
   - Test all accessibility features
   - Ensure proper permission requests
   - Add app description and keywords
   - Include privacy policy

### Submission Process

1. **Archive in Xcode**:
   ```
   Product → Archive
   ```

2. **Upload to App Store**:
   - Use Xcode Organizer
   - Validate archive
   - Upload to App Store Connect

3. **Submit for Review**:
   - Complete app information
   - Submit for App Store review
   - Monitor review status

## Troubleshooting

### Common Issues

1. **Code Signing Errors**:
   - Verify Apple Developer account
   - Check certificate expiration
   - Ensure correct provisioning profile

2. **Build Failures**:
   - Update Xcode to latest version
   - Clean build folder (Product → Clean Build Folder)
   - Verify kivy-ios dependencies

3. **Runtime Crashes**:
   - Check device logs in Xcode (Window → Devices and Simulators)
   - Verify all required frameworks are linked
   - Test on multiple iOS versions

### Debug Commands

```bash
# Clean kivy-ios build
kivy-ios clean

# Rebuild with verbose output
kivy-ios build python3 -v

# Check iOS SDK
xcodebuild -showsdks

# List connected devices
xcrun xctrace list devices
```

## Performance Optimization

### App Size Reduction

1. **Exclude Unused Modules**:
   - Edit `ios_config.ini` exclude_modules list
   - Remove unnecessary Python packages

2. **Optimize Assets**:
   - Compress images
   - Use appropriate icon sizes
   - Remove unused resources

### Runtime Performance

1. **Memory Management**:
   - Monitor memory usage on device
   - Use Xcode Instruments for profiling
   - Optimize Kivy widgets

2. **Battery Optimization**:
   - Minimize background processing
   - Use efficient audio processing
   - Follow iOS energy guidelines

## Continuous Integration

### GitHub Actions Setup

Create `.github/workflows/ios.yml`:

```yaml
name: iOS Build
on: [push, pull_request]

jobs:
  ios-build:
    runs-on: macos-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install kivy-ios
    
    - name: Build iOS
      run: |
        chmod +x build_ios.sh
        ./build_ios.sh
    
    - name: Archive build
      uses: actions/upload-artifact@v3
      with:
        name: ios-build
        path: accessmate-ios/
```

### Required Secrets

Set these in GitHub repository secrets:
- `APPLE_DEVELOPER_TEAM_ID`
- `APPLE_BUNDLE_ID`
- `APPLE_SIGNING_CERTIFICATE_P12`
- `APPLE_SIGNING_CERTIFICATE_PASSWORD`

## Maintenance

### Updates

1. **iOS Version Support**:
   - Test on new iOS versions
   - Update deployment target as needed
   - Monitor deprecated APIs

2. **Dependencies**:
   - Keep kivy-ios updated
   - Monitor Python package compatibility
   - Test with Xcode updates

3. **App Store Guidelines**:
   - Follow accessibility guidelines
   - Monitor policy changes
   - Update privacy descriptions

## Support and Resources

### Official Documentation

- [Kivy-iOS Documentation](https://github.com/kivy/kivy-ios)
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [iOS Accessibility Guidelines](https://developer.apple.com/accessibility/ios/)

### Useful Commands

```bash
# Show iOS simulators
xcrun simctl list devices

# Install app on simulator
xcrun simctl install booted path/to/app.app

# View iOS device logs
xcrun devicectl list devices
xcrun devicectl device install app --device DEVICE_ID path/to/app.ipa

# Archive for distribution
xcodebuild archive -project accessmate-ios.xcodeproj -scheme accessmate-ios -archivePath build/accessmate-ios.xcarchive
```

### Getting Help

1. **Kivy Community**: [Discord](https://chat.kivy.org/)
2. **Apple Developer Forums**: [developer.apple.com/forums](https://developer.apple.com/forums/)
3. **AccessMate Issues**: Create GitHub issue in this repository

## Next Steps

1. **Set up Apple Developer account**
2. **Run first build on simulator**
3. **Test on physical iOS device**
4. **Prepare for App Store submission**
5. **Set up automated builds (optional)**