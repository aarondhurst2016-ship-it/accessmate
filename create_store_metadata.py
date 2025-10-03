#!/usr/bin/env python3
"""
App Store Submission Helper for AccessMate
Prepares builds for submission to various app stores
"""

import os
import json
import shutil
from pathlib import Path

def create_store_metadata():
    """Create metadata files for various app stores"""
    
    # Common app metadata
    app_metadata = {
        "name": "AccessMate",
        "version": "1.0.0",
        "description": "AI-powered accessibility assistant providing vision, hearing, and mobility support with voice commands, object recognition, and screen reading capabilities.",
        "short_description": "AI accessibility assistant with voice commands and object recognition",
        "keywords": ["accessibility", "vision", "hearing", "mobility", "AI", "voice", "screen reader"],
        "category": "Accessibility",
        "rating": "4+",
        "developer": "AccessMate Team",
        "contact_email": "support@accessmate.app",
        "privacy_policy": "https://accessmate.app/privacy",
        "website": "https://accessmate.app"
    }
    
    # Create store-specific metadata
    create_google_play_metadata(app_metadata)
    create_apple_app_store_metadata(app_metadata)
    create_microsoft_store_metadata(app_metadata)
    create_mac_app_store_metadata(app_metadata)
    create_linux_store_metadata(app_metadata)

def create_google_play_metadata(metadata):
    """Create Google Play Store metadata"""
    print("📱 Creating Google Play Store metadata...")
    
    play_store_dir = "store_metadata/google_play"
    os.makedirs(play_store_dir, exist_ok=True)
    
    # Play Store listing
    listing = {
        "title": metadata["name"],
        "short_description": metadata["short_description"],
        "full_description": f"""
{metadata["description"]}

KEY FEATURES:
• Voice commands and speech recognition
• Object recognition and identification  
• Screen reader for visual accessibility
• Battery monitoring with voice notifications
• Emergency SOS features
• Smart home integration
• Navigation assistance
• Medication reminders
• Weather and news updates
• Customizable accessibility profiles

ACCESSIBILITY SUPPORT:
• Vision impairment assistance
• Hearing impairment support  
• Mobility assistance features
• Cognitive accessibility tools
• Voice-first interface design
• High contrast visual themes
• Large text and button options
• Screen reader compatibility

PRIVACY & SECURITY:
• Local processing where possible
• Encrypted data transmission
• No unnecessary data collection
• Full privacy policy compliance
• User control over all permissions

Perfect for users with disabilities, elderly users, or anyone who benefits from voice-controlled accessibility features.
        """.strip(),
        "category": "ACCESSIBILITY",
        "content_rating": "Everyone",
        "tags": metadata["keywords"],
        "contact_email": metadata["contact_email"],
        "privacy_policy_url": metadata["privacy_policy"],
        "website_url": metadata["website"]
    }
    
    with open(f"{play_store_dir}/listing.json", 'w', encoding='utf-8') as f:
        json.dump(listing, f, indent=2)
    
    # Release notes
    release_notes = """
Welcome to AccessMate v1.0.0!

NEW FEATURES:
* AI-powered voice commands
* Real-time object recognition  
* Advanced screen reading
* Battery monitoring with alerts
* Emergency SOS functionality
* Smart home device control
* Navigation assistance
* Medication reminders

ACCESSIBILITY IMPROVEMENTS:
* Full voice interface support
* High contrast themes
* Customizable text sizes
* Screen reader optimization
* Gesture-based controls

TECHNICAL FEATURES:
* Cross-platform compatibility
* Offline functionality
* Privacy-focused design
* Low battery consumption
* Multi-language support

Perfect for users with visual, hearing, or mobility challenges!
    """.strip()
    
    with open(f"{play_store_dir}/release_notes.txt", 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print(f"✅ Google Play Store metadata: {play_store_dir}")

def create_apple_app_store_metadata(metadata):
    """Create Apple App Store metadata"""
    print("🍎 Creating Apple App Store metadata...")
    
    app_store_dir = "store_metadata/apple_app_store"
    os.makedirs(app_store_dir, exist_ok=True)
    
    # App Store Connect metadata
    app_store_listing = {
        "name": metadata["name"],
        "subtitle": "AI Accessibility Assistant",
        "description": f"""
{metadata["description"]}

POWERFUL ACCESSIBILITY FEATURES:
• Advanced voice command system with natural language processing
• Real-time object recognition using computer vision
• Comprehensive screen reader with customizable voices
• Smart battery monitoring with voice notifications
• One-touch emergency SOS with location sharing
• Smart home device integration and control
• GPS navigation with voice guidance
• Medication reminder system with voice alerts
• Weather updates and news reading
• Personalized accessibility profiles

DESIGNED FOR EVERYONE:
Perfect for users with visual impairments, hearing loss, mobility challenges, or anyone who prefers voice-controlled interfaces. AccessMate makes technology more accessible and independent living easier.

PRIVACY FIRST:
Your privacy matters. AccessMate processes data locally when possible, uses encrypted connections, and never collects unnecessary personal information.

COMPATIBILITY:
Works seamlessly across iPhone, iPad, and integrates with VoiceOver, Switch Control, and other iOS accessibility features.
        """.strip(),
        "keywords": ", ".join(metadata["keywords"]),
        "category": "MEDICAL",
        "age_rating": "4+",
        "version": metadata["version"],
        "copyright": f"© 2025 {metadata['developer']}",
        "contact_email": metadata["contact_email"],
        "privacy_policy_url": metadata["privacy_policy"],
        "support_url": metadata["website"]
    }
    
    with open(f"{app_store_dir}/metadata.json", 'w', encoding='utf-8') as f:
        json.dump(app_store_listing, f, indent=2)
    
    # App Store review information
    review_info = {
        "demo_account": {
            "username": "demo@accessmate.app",
            "password": "DemoUser2025!"
        },
        "review_notes": """
AccessMate is an accessibility-focused application designed to help users with disabilities.

TESTING INSTRUCTIONS:
1. Enable VoiceOver to test screen reader integration
2. Try voice commands: "What do you see?", "Read this screen", "Check battery"
3. Test object recognition by pointing camera at objects
4. Emergency features can be tested safely in demo mode

ACCESSIBILITY COMPLIANCE:
- Full VoiceOver support
- High contrast mode compatibility  
- Large text support
- Voice control integration
- Switch control compatibility

The app requests camera and microphone permissions for core accessibility features (object recognition and voice commands).
        """.strip(),
        "testing_notes": "App includes comprehensive accessibility features. Please test with VoiceOver enabled for full experience."
    }
    
    with open(f"{app_store_dir}/review_info.json", 'w', encoding='utf-8') as f:
        json.dump(review_info, f, indent=2)
    
    print(f"✅ Apple App Store metadata: {app_store_dir}")

def create_microsoft_store_metadata(metadata):
    """Create Microsoft Store metadata"""
    print("🪟 Creating Microsoft Store metadata...")
    
    ms_store_dir = "store_metadata/microsoft_store"
    os.makedirs(ms_store_dir, exist_ok=True)
    
    # Microsoft Store listing
    ms_listing = {
        "display_name": metadata["name"],
        "description": f"""
{metadata["description"]}

🎯 KEY ACCESSIBILITY FEATURES:
• Voice-First Interface: Complete voice command system
• Smart Screen Reader: Advanced text-to-speech with customization
• Object Recognition: AI-powered visual assistance
• Battery Alerts: Voice notifications for power management
• Emergency SOS: Quick access to emergency services
• Smart Home Control: Voice control for connected devices
• Navigation Help: GPS assistance with voice guidance
• Medication Reminders: Voice alerts for health management

🌟 WINDOWS INTEGRATION:
• Narrator compatibility and enhancement
• Windows Hello integration
• Cortana voice command extension
• High contrast theme support
• Windows accessibility API integration
• Keyboard shortcut customization

👥 PERFECT FOR:
• Users with visual impairments
• People with hearing difficulties  
• Individuals with mobility challenges
• Elderly users seeking independence
• Anyone preferring voice interfaces
• Caregivers and family members

🔒 PRIVACY & SECURITY:
• Local data processing when possible
• Encrypted communications
• No unnecessary data collection
• Full GDPR compliance
• User-controlled permissions
        """.strip(),
        "category": "Accessibility",
        "age_rating": "Everyone",
        "features": [
            "Voice commands",
            "Screen reading", 
            "Object recognition",
            "Emergency assistance",
            "Smart home integration",
            "Accessibility tools"
        ],
        "system_requirements": {
            "minimum": {
                "os": "Windows 10 version 19041.0 or higher",
                "architecture": "x64, x86, ARM64",
                "memory": "4 GB RAM",
                "storage": "500 MB available space"
            },
            "recommended": {
                "os": "Windows 11",
                "memory": "8 GB RAM", 
                "storage": "1 GB available space",
                "additional": "Microphone and camera for full functionality"
            }
        }
    }
    
    with open(f"{ms_store_dir}/listing.json", 'w', encoding='utf-8') as f:
        json.dump(ms_listing, f, indent=2)
    
    print(f"✅ Microsoft Store metadata: {ms_store_dir}")

def create_mac_app_store_metadata(metadata):
    """Create Mac App Store metadata"""
    print("🍎 Creating Mac App Store metadata...")
    
    mac_store_dir = "store_metadata/mac_app_store"
    os.makedirs(mac_store_dir, exist_ok=True)
    
    # Mac App Store specific metadata
    mac_listing = {
        "name": metadata["name"],
        "category": "Medical",  # Accessibility apps often go in Medical category
        "description": f"""
{metadata["description"]}

🎯 MACOS OPTIMIZED FEATURES:
• Native VoiceOver enhancement and integration
• Siri Shortcuts for quick accessibility commands
• Touch Bar support for MacBook Pro users
• macOS accessibility API integration
• System-wide voice commands
• Menu bar quick access
• Multi-desktop support

🌟 ACCESSIBILITY EXCELLENCE:
• Advanced screen reading with customizable voices
• AI-powered object recognition through camera
• Voice-controlled smart home integration  
• Battery monitoring with spoken alerts
• Emergency SOS with location services
• Medication reminders with voice notifications
• Weather and news updates via speech

🔧 SYSTEM INTEGRATION:
• Works seamlessly with existing macOS accessibility features
• Respects system accessibility preferences
• Integrates with Notification Center
• Supports Dark Mode and high contrast themes
• Keyboard navigation and shortcuts
• Multi-language support

Perfect for Mac users who need enhanced accessibility features or prefer voice-controlled interfaces.
        """.strip(),
        "age_rating": "4+",
        "version": metadata["version"],
        "system_requirements": {
            "minimum_os": "macOS 10.15",
            "recommended_os": "macOS 12.0 or later",
            "architecture": ["x86_64", "arm64"]
        }
    }
    
    with open(f"{mac_store_dir}/metadata.json", 'w', encoding='utf-8') as f:
        json.dump(mac_listing, f, indent=2)
    
    print(f"✅ Mac App Store metadata: {mac_store_dir}")

def create_linux_store_metadata(metadata):
    """Create Linux store metadata (Flatpak, Snap, etc.)"""
    print("🐧 Creating Linux store metadata...")
    
    linux_store_dir = "store_metadata/linux_stores"
    os.makedirs(linux_store_dir, exist_ok=True)
    
    # Flatpak metadata
    flatpak_manifest = {
        "app-id": "com.accessmate.app",
        "runtime": "org.freedesktop.Platform",
        "runtime-version": "23.08",
        "sdk": "org.freedesktop.Sdk",
        "command": "accessmate",
        "finish-args": [
            "--share=ipc",
            "--socket=x11",
            "--socket=wayland", 
            "--socket=pulseaudio",
            "--device=all",  # For camera and other devices
            "--share=network",
            "--filesystem=home:ro",  # Read-only home access
            "--talk-name=org.freedesktop.Notifications",
            "--talk-name=org.a11y.*"  # Accessibility services
        ],
        "modules": [
            {
                "name": "accessmate",
                "buildsystem": "simple",
                "build-commands": [
                    "install -D accessmate /app/bin/accessmate",
                    "install -D accessmate.desktop /app/share/applications/com.accessmate.app.desktop",
                    "install -D linux_icons/256x256/accessmate.png /app/share/icons/hicolor/256x256/apps/com.accessmate.app.png"
                ],
                "sources": [
                    {
                        "type": "file",
                        "path": "../../dist/accessmate"
                    },
                    {
                        "type": "file", 
                        "path": "../../accessmate.desktop"
                    },
                    {
                        "type": "dir",
                        "path": "../../linux_icons"
                    }
                ]
            }
        ]
    }
    
    with open(f"{linux_store_dir}/com.accessmate.app.json", 'w', encoding='utf-8') as f:
        json.dump(flatpak_manifest, f, indent=2)
    
    # Snapcraft metadata
    snapcraft_yaml = f"""
name: accessmate
version: '{metadata["version"]}'
summary: {metadata["short_description"]}
description: |
  {metadata["description"]}
  
  Key Features:
  - Voice commands and speech recognition
  - Object recognition and identification
  - Screen reader functionality
  - Battery monitoring with alerts
  - Emergency SOS features
  - Smart home integration
  - Navigation assistance
  - Medication reminders

grade: stable
confinement: strict
base: core22

apps:
  accessmate:
    command: bin/accessmate
    plugs:
      - home
      - network
      - audio-playback
      - audio-record
      - camera
      - desktop
      - desktop-legacy
      - wayland
      - x11
      - unity7

parts:
  accessmate:
    plugin: dump
    source: ../../dist/
    organize:
      accessmate: bin/accessmate
    stage-packages:
      - libgtk-3-0
      - libgstreamer1.0-0
"""
    
    with open(f"{linux_store_dir}/snapcraft.yaml", 'w', encoding='utf-8') as f:
        f.write(snapcraft_yaml)
    
    # AppStream metadata for software centers
    appstream_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>com.accessmate.app</id>
  <metadata_license>MIT</metadata_license>
  <project_license>MIT</project_license>
  <name>{metadata["name"]}</name>
  <summary>{metadata["short_description"]}</summary>
  <description>
    <p>{metadata["description"]}</p>
    <p>Features include voice commands, object recognition, screen reading, battery monitoring, emergency SOS, smart home integration, and navigation assistance.</p>
  </description>
  <launchable type="desktop-id">com.accessmate.app.desktop</launchable>
  <url type="homepage">{metadata["website"]}</url>
  <developer_name>{metadata["developer"]}</developer_name>
  <provides>
    <binary>accessmate</binary>
  </provides>
  <categories>
    <category>Accessibility</category>
    <category>Utility</category>
  </categories>
  <keywords>
    <keyword>accessibility</keyword>
    <keyword>voice</keyword>
    <keyword>vision</keyword>
    <keyword>hearing</keyword>
    <keyword>screen-reader</keyword>
  </keywords>
  <screenshots>
    <screenshot type="default">
      <caption>AccessMate main interface</caption>
    </screenshot>
  </screenshots>
  <releases>
    <release version="{metadata["version"]}" date="2025-10-03">
      <description>
        <p>Initial release of AccessMate with full accessibility features.</p>
      </description>
    </release>
  </releases>
</component>
"""
    
    with open(f"{linux_store_dir}/com.accessmate.app.metainfo.xml", 'w', encoding='utf-8') as f:
        f.write(appstream_xml)
    
    print(f"✅ Linux store metadata: {linux_store_dir}")

def create_submission_checklist():
    """Create a submission checklist for all stores"""
    checklist = """
# App Store Submission Checklist

## Google Play Store
- [ ] APK signed with release keystore
- [ ] App bundle (.aab) generated
- [ ] Privacy policy URL configured
- [ ] Store listing screenshots (phone, tablet, TV)
- [ ] Feature graphic (1024x500)
- [ ] App icon (512x512)
- [ ] Age rating questionnaire completed
- [ ] Content rating certificates
- [ ] Developer account verified

## Apple App Store (iOS)
- [ ] iOS app signed with distribution certificate
- [ ] Provisioning profile configured
- [ ] App Store Connect listing complete
- [ ] Screenshots for all device sizes
- [ ] App icon in all required sizes
- [ ] Privacy nutrition labels configured
- [ ] Age rating selected
- [ ] TestFlight testing completed
- [ ] App Review information provided

## Microsoft Store (Windows)
- [ ] MSIX package created and signed
- [ ] Partner Center listing complete
- [ ] Store screenshots (1920x1080, 1366x768)
- [ ] Store logos in required sizes
- [ ] Age rating and content declarations
- [ ] Privacy policy linked
- [ ] Microsoft Store certification requirements met

## Mac App Store (macOS)
- [ ] macOS app signed and notarized
- [ ] Mac App Store distribution certificate
- [ ] App Store Connect listing complete
- [ ] macOS-specific screenshots
- [ ] App sandbox configured properly
- [ ] Hardened runtime enabled
- [ ] Privacy usage descriptions in Info.plist

## Linux Stores
### Flatpak (Flathub)
- [ ] Flatpak manifest tested locally
- [ ] Runtime dependencies verified
- [ ] Desktop file validated
- [ ] AppStream metadata complete
- [ ] Icon in required sizes and formats

### Snap Store
- [ ] Snapcraft.yaml configured
- [ ] Snap tested locally with different confinement
- [ ] Store listing complete
- [ ] Icon uploaded (256x256)

### AppImage
- [ ] AppImage builds successfully
- [ ] Desktop integration working
- [ ] Distributed via GitHub Releases

## Universal Requirements
- [ ] App tested on target platforms
- [ ] Privacy policy published and accessible
- [ ] Terms of service available
- [ ] Support email/website configured
- [ ] App descriptions translated (if needed)
- [ ] Keywords and categories optimized
- [ ] Age ratings consistent across stores
- [ ] Icons and screenshots high quality
- [ ] App functionality fully working
- [ ] Accessibility features tested
- [ ] Performance optimized
- [ ] Error handling robust
- [ ] Offline functionality working (where applicable)

## Security & Compliance
- [ ] Code signing certificates obtained
- [ ] Apps scanned for malware/vulnerabilities  
- [ ] GDPR compliance verified
- [ ] Accessibility standards met (WCAG, Section 508)
- [ ] Data encryption implemented
- [ ] Secure API communications
- [ ] User consent mechanisms in place

## Analytics & Monitoring
- [ ] Crash reporting configured
- [ ] Usage analytics implemented (privacy-compliant)
- [ ] Performance monitoring enabled
- [ ] User feedback collection system
- [ ] Update mechanism tested

## Post-Launch
- [ ] App store optimization (ASO) ongoing
- [ ] User reviews monitoring
- [ ] Regular updates planned
- [ ] Customer support ready
- [ ] Marketing materials prepared
- [ ] Press kit available
- [ ] Social media accounts set up
"""
    
    with open("STORE_SUBMISSION_CHECKLIST.md", 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print("✅ Created submission checklist: STORE_SUBMISSION_CHECKLIST.md")

def main():
    """Main function to create all store metadata"""
    print("AccessMate Store Submission Helper")
    print("=" * 40)
    
    # Create all metadata
    create_store_metadata()
    create_submission_checklist()
    
    print("\nSTORE METADATA COMPLETE!")
    print("\nNext Steps:")
    print("1. Review generated metadata in store_metadata/ directory")
    print("2. Customize descriptions and keywords as needed")
    print("3. Prepare store screenshots and promotional materials")
    print("4. Follow the submission checklist")
    print("5. Submit to app stores using GitHub Actions builds")
    
    print("\nReady for app store submission!")

if __name__ == "__main__":
    main()