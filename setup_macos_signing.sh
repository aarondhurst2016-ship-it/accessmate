#!/bin/bash
# setup_macos_signing.sh - Interactive setup for macOS code signing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🍎 AccessMate macOS Code Signing Setup${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Check if we're on macOS
if [ "$(uname)" != "Darwin" ]; then
    echo -e "${RED}❌ This script must be run on macOS${NC}"
    exit 1
fi

# Check for existing certificates
echo -e "${BLUE}Checking for existing code signing certificates...${NC}"
CERTS=$(security find-identity -v -p codesigning 2>/dev/null | grep "Developer ID Application" | wc -l)

if [ "$CERTS" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No Developer ID Application certificates found${NC}"
    echo ""
    echo -e "${BLUE}You need to:${NC}"
    echo -e "1. Join Apple Developer Program: ${YELLOW}https://developer.apple.com/programs/${NC}"
    echo -e "2. Create a Developer ID Application certificate"
    echo -e "3. Install the certificate in Keychain Access"
    echo ""
    echo -e "${BLUE}See MACOS_CODE_SIGNING.md for detailed instructions${NC}"
    echo ""
    read -p "Do you want to continue with manual configuration? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
else
    echo -e "${GREEN}✅ Found $CERTS Developer ID Application certificate(s)${NC}"
    echo ""
    echo -e "${BLUE}Available certificates:${NC}"
    security find-identity -v -p codesigning | grep "Developer ID Application"
fi

echo ""
echo -e "${BLUE}Current configuration:${NC}"

# Check current build script configuration
if [ -f "build_macos.sh" ]; then
    CURRENT_TEAM=$(grep "DEVELOPER_TEAM=" build_macos.sh | head -1 | cut -d'"' -f2)
    CURRENT_BUNDLE=$(grep "BUNDLE_ID=" build_macos.sh | head -1 | cut -d'"' -f2)
    
    echo -e "Bundle ID: ${YELLOW}$CURRENT_BUNDLE${NC}"
    echo -e "Team ID: ${YELLOW}${CURRENT_TEAM:-Not set}${NC}"
else
    echo -e "${RED}❌ build_macos.sh not found${NC}"
    exit 1
fi

echo ""

# Get user input for configuration
echo -e "${BLUE}Configuration Setup:${NC}"
echo ""

# Bundle ID
echo -e "${BLUE}1. Bundle ID${NC}"
echo -e "Current: ${YELLOW}$CURRENT_BUNDLE${NC}"
echo -e "Format: com.yourname.accessmate or com.yourcompany.accessmate"
read -p "New Bundle ID (or press Enter to keep current): " NEW_BUNDLE
if [ -z "$NEW_BUNDLE" ]; then
    NEW_BUNDLE="$CURRENT_BUNDLE"
fi

echo ""

# Team ID or Signing Identity
echo -e "${BLUE}2. Code Signing Identity${NC}"
echo ""
echo -e "Choose an option:"
echo -e "1) Use Team ID (e.g., ABCD123456)"
echo -e "2) Use full certificate name (e.g., 'Developer ID Application: Your Name (TEAMID)')"
echo -e "3) Skip code signing"

read -p "Enter choice (1-3): " SIGNING_CHOICE

case $SIGNING_CHOICE in
    1)
        echo ""
        echo -e "${BLUE}Enter your Apple Developer Team ID:${NC}"
        echo -e "Find this in Apple Developer Portal > Membership"
        echo -e "Format: 10-character alphanumeric (e.g., ABCD123456)"
        read -p "Team ID: " TEAM_ID
        SIGNING_METHOD="team"
        ;;
    2)
        echo ""
        echo -e "${BLUE}Available signing identities:${NC}"
        security find-identity -v -p codesigning | grep "Developer ID Application" | nl
        echo ""
        read -p "Enter the full certificate name: " CERT_NAME
        SIGNING_METHOD="cert"
        ;;
    3)
        echo -e "${YELLOW}Skipping code signing setup${NC}"
        SIGNING_METHOD="none"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""

# Notarization setup (optional)
if [ "$SIGNING_METHOD" != "none" ]; then
    echo -e "${BLUE}3. Notarization Setup (Optional but Recommended)${NC}"
    echo -e "Notarization is required for apps distributed outside the App Store"
    echo -e "to avoid Gatekeeper warnings on macOS 10.15+"
    echo ""
    read -p "Do you want to set up notarization? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo -e "${BLUE}You need to create an App Store Connect API key:${NC}"
        echo -e "1. Go to App Store Connect > Users and Access > Keys"
        echo -e "2. Create a new key with Developer role"
        echo -e "3. Download the .p8 file"
        echo ""
        
        read -p "Key ID (from App Store Connect): " NOTARY_KEY_ID
        read -p "Issuer ID (from App Store Connect): " NOTARY_ISSUER_ID
        read -p "Path to .p8 key file: " NOTARY_KEY_PATH
        
        # Expand tilde in path
        NOTARY_KEY_PATH="${NOTARY_KEY_PATH/#\~/$HOME}"
        
        if [ ! -f "$NOTARY_KEY_PATH" ]; then
            echo -e "${YELLOW}⚠️  Key file not found: $NOTARY_KEY_PATH${NC}"
            echo -e "${YELLOW}Continuing without notarization setup${NC}"
            SETUP_NOTARIZATION="no"
        else
            SETUP_NOTARIZATION="yes"
        fi
    else
        SETUP_NOTARIZATION="no"
    fi
fi

echo ""
echo -e "${BLUE}4. Configuration Summary${NC}"
echo -e "Bundle ID: ${YELLOW}$NEW_BUNDLE${NC}"

case $SIGNING_METHOD in
    "team")
        echo -e "Team ID: ${YELLOW}$TEAM_ID${NC}"
        ;;
    "cert") 
        echo -e "Certificate: ${YELLOW}$CERT_NAME${NC}"
        ;;
    "none")
        echo -e "Code Signing: ${YELLOW}Disabled${NC}"
        ;;
esac

if [ "$SETUP_NOTARIZATION" = "yes" ]; then
    echo -e "Notarization: ${GREEN}Enabled${NC}"
    echo -e "Key ID: ${YELLOW}$NOTARY_KEY_ID${NC}"
    echo -e "Key Path: ${YELLOW}$NOTARY_KEY_PATH${NC}"
else
    echo -e "Notarization: ${YELLOW}Not configured${NC}"
fi

echo ""
read -p "Apply this configuration? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Configuration cancelled${NC}"
    exit 0
fi

# Apply configuration
echo ""
echo -e "${BLUE}Applying configuration...${NC}"

# Update build_macos.sh
if [ "$SIGNING_METHOD" = "team" ]; then
    sed -i.bak "s/DEVELOPER_TEAM=\".*\"/DEVELOPER_TEAM=\"$TEAM_ID\"/" build_macos.sh
elif [ "$SIGNING_METHOD" = "cert" ]; then
    sed -i.bak "s/DEVELOPER_TEAM=\".*\"/DEVELOPER_TEAM=\"\"/" build_macos.sh
    sed -i.bak "s/SIGNING_IDENTITY=\".*\"/SIGNING_IDENTITY=\"$CERT_NAME\"/" build_macos.sh
else  
    sed -i.bak "s/DEVELOPER_TEAM=\".*\"/DEVELOPER_TEAM=\"\"/" build_macos.sh
fi

# Update Bundle ID
sed -i.bak "s/BUNDLE_ID=\".*\"/BUNDLE_ID=\"$NEW_BUNDLE\"/" build_macos.sh

echo -e "${GREEN}✅ build_macos.sh updated${NC}"

# Create environment file for convenience
cat > macos_signing_env.sh << EOF
#!/bin/bash
# AccessMate macOS Signing Environment
# Source this file before building: source macos_signing_env.sh

export ACCESSMATE_BUNDLE_ID="$NEW_BUNDLE"
EOF

if [ "$SIGNING_METHOD" = "team" ]; then
    echo "export ACCESSMATE_TEAM_ID=\"$TEAM_ID\"" >> macos_signing_env.sh
elif [ "$SIGNING_METHOD" = "cert" ]; then
    echo "export ACCESSMATE_SIGNING_IDENTITY=\"$CERT_NAME\"" >> macos_signing_env.sh
fi

if [ "$SETUP_NOTARIZATION" = "yes" ]; then
    cat >> macos_signing_env.sh << EOF
export ACCESSMATE_NOTARY_KEY_ID="$NOTARY_KEY_ID"
export ACCESSMATE_NOTARY_ISSUER_ID="$NOTARY_ISSUER_ID"
export ACCESSMATE_NOTARY_KEY_PATH="$NOTARY_KEY_PATH"
EOF
fi

chmod +x macos_signing_env.sh
echo -e "${GREEN}✅ Environment file created: macos_signing_env.sh${NC}"

# Test the configuration
echo ""
echo -e "${BLUE}Testing configuration...${NC}"

if [ "$SIGNING_METHOD" = "team" ]; then
    # Try to find certificate with team ID
    FOUND_CERT=$(security find-identity -v -p codesigning | grep "$TEAM_ID" | head -1)
    if [ -n "$FOUND_CERT" ]; then
        echo -e "${GREEN}✅ Found certificate for Team ID: $TEAM_ID${NC}"
    else
        echo -e "${YELLOW}⚠️  No certificate found for Team ID: $TEAM_ID${NC}"
        echo -e "${BLUE}Make sure your certificate is installed in Keychain Access${NC}"
    fi
elif [ "$SIGNING_METHOD" = "cert" ]; then
    # Check if the certificate exists
    FOUND_CERT=$(security find-identity -v -p codesigning | grep "$CERT_NAME")
    if [ -n "$FOUND_CERT" ]; then
        echo -e "${GREEN}✅ Found certificate: $CERT_NAME${NC}"
    else
        echo -e "${YELLOW}⚠️  Certificate not found: $CERT_NAME${NC}"
        echo -e "${BLUE}Available certificates:${NC}"
        security find-identity -v -p codesigning | grep "Developer ID Application"
    fi
fi

echo ""
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "1. Test build: ${YELLOW}./build_macos.sh${NC}"
echo -e "2. Or with environment: ${YELLOW}source macos_signing_env.sh && ./build_macos.sh${NC}"
echo ""

if [ "$SIGNING_METHOD" = "none" ]; then
    echo -e "${YELLOW}Note: Code signing is disabled. The app will show security warnings on other Macs.${NC}"
    echo -e "${BLUE}To enable later, run this script again or see MACOS_CODE_SIGNING.md${NC}"
fi

if [ "$SETUP_NOTARIZATION" = "no" ] && [ "$SIGNING_METHOD" != "none" ]; then
    echo -e "${YELLOW}Note: Notarization not configured. For public distribution, see MACOS_CODE_SIGNING.md${NC}"
fi

echo ""
echo -e "${BLUE}Documentation: MACOS_CODE_SIGNING.md${NC}"