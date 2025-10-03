# macOS Code Signing Quick Reference

## 🚀 Quick Start
```bash
# 1. Run interactive setup (on macOS)
./setup_macos_signing.sh

# 2. Build with signing
./build_macos.sh
```

## 📋 Prerequisites Checklist
- [ ] Apple Developer Program membership ($99/year)
- [ ] Developer ID Application certificate installed
- [ ] Team ID from Apple Developer Portal
- [ ] Unique Bundle ID chosen

## 🔧 Configuration Methods

### Method 1: Interactive Setup (Recommended)
```bash
./setup_macos_signing.sh
```
Guides you through complete setup with validation.

### Method 2: Environment Variables
```bash
export ACCESSMATE_TEAM_ID="ABCD123456"
export ACCESSMATE_BUNDLE_ID="com.yourname.accessmate"
./build_macos.sh
```

### Method 3: Edit build_macos.sh
Change these lines in the script:
```bash
BUNDLE_ID="com.yourname.accessmate"
DEVELOPER_TEAM="ABCD123456"
```

## 🔐 Notarization (Optional)
For apps distributed outside App Store:

```bash
export ACCESSMATE_NOTARY_KEY_ID="YOUR_KEY_ID"
export ACCESSMATE_NOTARY_ISSUER_ID="YOUR_ISSUER_ID"  
export ACCESSMATE_NOTARY_KEY_PATH="AuthKey_KEY_ID.p8"
```

## 🩺 Troubleshooting

### Check Certificates
```bash
security find-identity -v -p codesigning
```

### Test Signature
```bash
codesign --verify --deep --strict dist_macos/AccessMate.app
spctl --assess --verbose dist_macos/AccessMate.app
```

### Common Issues
- **"No identity found"**: Install certificate in Keychain Access
- **"App is damaged"**: App needs notarization for Gatekeeper
- **Wrong Team ID**: Check Apple Developer Portal > Membership

## 📁 Generated Files
- `macos_signing_env.sh` - Environment variables (auto-generated)
- `dist_macos/AccessMate.app` - Signed app bundle
- `dist_macos/AccessMate-1.0.0.dmg` - Signed installer
- `dist_macos/BUILD_INFO.txt` - Build details

## 🎯 Distribution Status After Setup
- ✅ **Local Testing**: Ready immediately
- ✅ **Direct Distribution**: Ready with code signing
- ✅ **Professional Distribution**: Ready with notarization
- ✅ **App Store**: Ready with Mac App Store certificate

## 📞 Support
- **Detailed Guide**: `MACOS_CODE_SIGNING.md`
- **Build Guide**: `MACOS_BUILD_GUIDE.md`
- **Apple Documentation**: https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution