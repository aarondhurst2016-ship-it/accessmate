# macOS Code Signing Setup Guide for AccessMate

This guide walks you through setting up Apple Developer certificates for code signing and distributing AccessMate on macOS.

## 🍎 Apple Developer Program Requirements

### Step 1: Join Apple Developer Program
1. **Visit**: https://developer.apple.com/programs/
2. **Cost**: $99/year (Individual) or $299/year (Organization)
3. **Sign up** with your Apple ID
4. **Complete enrollment** (may take 24-48 hours for approval)

### Step 2: Create Certificates

#### A. Developer ID Application Certificate (For Direct Distribution)
1. Open **Keychain Access** on your Mac
2. Go to **Keychain Access > Certificate Assistant > Request a Certificate from a Certificate Authority**
3. Enter your email and name, select "Saved to disk"
4. Go to **Apple Developer Portal** > **Certificates, Identifiers & Profiles**
5. Click **+** to create new certificate
6. Select **Developer ID Application** (for apps distributed outside App Store)
7. Upload the certificate request file
8. Download and install the certificate

#### B. Mac App Store Certificate (For App Store Distribution)
1. In Apple Developer Portal, create **Mac App Store** certificate
2. Follow same process as above
3. This is needed for App Store submissions

### Step 3: Find Your Team ID
1. Go to **Apple Developer Portal**
2. Click on **Membership** in the sidebar
3. Your **Team ID** is displayed (10-character alphanumeric)
4. Example: `ABCD123456`

## 🔧 Configure AccessMate for Code Signing

### Method 1: Edit build_macos.sh (Recommended)
Open `build_macos.sh` and update the configuration:

```bash
# Configuration
APP_NAME="AccessMate"
VERSION="1.0.0"
BUNDLE_ID="com.accessmate.app"  # Change this to your unique bundle ID
DEVELOPER_TEAM="YOUR_TEAM_ID_HERE"  # Your 10-character Team ID
```

### Method 2: Environment Variables
Set environment variables before building:

```bash
export ACCESSMATE_TEAM_ID="YOUR_TEAM_ID_HERE"
export ACCESSMATE_BUNDLE_ID="com.yourcompany.accessmate"
./build_macos.sh
```

### Method 3: Command Line Override
Pass parameters to the build script:

```bash
DEVELOPER_TEAM="YOUR_TEAM_ID" ./build_macos.sh
```

## 📝 Bundle ID Requirements

Your Bundle ID must be:
- **Unique**: Not used by any other app
- **Reverse domain format**: `com.yourcompany.appname`
- **Registered**: In Apple Developer Portal (for App Store)

### Recommended Bundle IDs:
- `com.yourname.accessmate` (Personal)
- `com.yourcompany.accessmate` (Company)
- `com.accessmate.desktop` (Generic)

## 🛠️ Code Signing Commands

### Manual Code Signing
```bash
# Sign the app bundle
codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" dist_macos/AccessMate.app

# Sign with specific certificate
codesign --force --deep --sign "SHA-1-HASH-OF-CERTIFICATE" dist_macos/AccessMate.app

# Verify signature
codesign --verify --deep --strict dist_macos/AccessMate.app

# Display signature info
codesign --display --verbose=4 dist_macos/AccessMate.app
```

### Automated Build with Signing
The build script will automatically:
1. Sign the app bundle with your certificate
2. Verify the signature
3. Prepare for notarization (if configured)

## 🔐 Notarization Setup (Required for macOS 10.15+)

### Step 1: Create App Store Connect API Key
1. Go to **App Store Connect** > **Users and Access** > **Keys**
2. Click **+** to create new key
3. Select **Developer** role
4. Download the `.p8` file
5. Note the **Key ID** and **Issuer ID**

### Step 2: Configure Notarization
Create `notarization_config.sh`:

```bash
#!/bin/bash
# Notarization configuration
NOTARY_KEY_ID="YOUR_KEY_ID"
NOTARY_ISSUER_ID="YOUR_ISSUER_ID"  
NOTARY_KEY_PATH="AuthKey_YOUR_KEY_ID.p8"
APPLE_ID="your.apple.id@email.com"
TEAM_ID="YOUR_TEAM_ID"
```

### Step 3: Notarize the App
```bash
# Submit for notarization
xcrun notarytool submit dist_macos/AccessMate-1.0.0.dmg \
  --key-id $NOTARY_KEY_ID \
  --issuer-id $NOTARY_ISSUER_ID \
  --key $NOTARY_KEY_PATH \
  --wait

# Staple the notarization ticket
xcrun stapler staple dist_macos/AccessMate.app
xcrun stapler staple dist_macos/AccessMate-1.0.0.dmg
```

## 🚀 Quick Setup Checklist

- [ ] **Join Apple Developer Program** ($99/year)
- [ ] **Create Developer ID Application certificate**
- [ ] **Find your Team ID** in Apple Developer Portal
- [ ] **Choose unique Bundle ID** (com.yourname.accessmate)
- [ ] **Update build_macos.sh** with your Team ID and Bundle ID
- [ ] **Test code signing** with a build
- [ ] **Set up notarization** (optional but recommended)
- [ ] **Create App Store Connect API key** (for notarization)

## 🔍 Troubleshooting Code Signing

### Common Issues:

**"No identity found"**
```bash
# List available certificates
security find-identity -v -p codesigning

# Install certificate if missing
open downloaded_certificate.cer
```

**"Invalid signature"**
```bash
# Check certificate validity
security dump-keychain | grep "Developer ID"

# Re-sign with correct certificate
codesign --force --deep --sign "Developer ID Application: Your Name" AccessMate.app
```

**"App is damaged" error on other Macs**
- App needs notarization for Gatekeeper
- Or users must go to System Preferences > Security & Privacy > Allow

### Certificate Names:
- **Developer ID Application**: For direct distribution
- **Mac App Store**: For App Store distribution
- **Mac Developer**: For development/testing only

## 💰 Cost Breakdown

### Apple Developer Program: $99/year
- Individual developer account
- Access to certificates and provisioning
- App Store distribution rights
- Beta testing with TestFlight

### Additional Costs (Optional):
- **App Store Review**: Free (but may require multiple submissions)
- **Notarization**: Free (but requires API key setup)
- **Extended Validation**: Not available for macOS apps

## 📊 Distribution Options

### 1. Direct Distribution (Developer ID)
- **Pros**: Full control, no App Store review
- **Cons**: Users get security warnings initially
- **Requirements**: Developer ID certificate + notarization

### 2. App Store Distribution
- **Pros**: Trusted by users, no security warnings
- **Cons**: App Store review process, 30% revenue share
- **Requirements**: Mac App Store certificate + App Store guidelines

### 3. Enterprise Distribution
- **Requirements**: Apple Developer Enterprise Program ($299/year)
- **Use case**: Internal company apps only

## 🎯 Next Steps

1. **Join Apple Developer Program**
2. **Update your Bundle ID** in `build_macos.sh`
3. **Create certificates** in Apple Developer Portal
4. **Test build with code signing**:
   ```bash
   DEVELOPER_TEAM="YOUR_TEAM_ID" ./build_macos.sh
   ```
5. **Set up notarization** for public distribution

Once you have your Apple Developer account and certificates, AccessMate will be **100% ready** for professional macOS distribution!