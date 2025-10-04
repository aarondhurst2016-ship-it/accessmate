#!/usr/bin/env python3
"""
iOS App Store Builder for AccessMate
Creates production-ready IPA files for App Store submission
"""

import os
import sys
import subprocess
import json
import shutil
import plistlib
from pathlib import Path

class iOSAppStoreBuilder:
    """Builds iOS app for App Store submission"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.app_name = "AccessMate"
        self.bundle_id = "com.accessmate.app"
        self.version = "1.0.0"
        self.build_number = "1"
        
    def prepare_environment(self):
        """Setup iOS build environment"""
        print("🍎 Preparing iOS build environment...")
        
        # Check for required tools (macOS only)
        if sys.platform != "darwin":
            print("❌ iOS builds require macOS")
            return False
            
        tools = ['kivy-ios', 'xcodebuild', 'python3']
        for tool in tools:
            if not shutil.which(tool):
                print(f"❌ {tool} not found in PATH")
                return False
                
        print("✅ iOS build tools verified")
        return True
        
    def create_ios_project(self):
        """Create iOS project structure"""
        print("📱 Creating iOS project...")
        
        ios_dir = self.project_root / "ios_project"
        ios_dir.mkdir(exist_ok=True)
        
        # Create main iOS entry point
        main_ios = ios_dir / "main.py"
        main_ios.write_text("""#!/usr/bin/env python3
'''
AccessMate iOS Entry Point
Optimized for iOS App Store submission
'''

import sys
import os
from pathlib import Path

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def main():
    '''Main iOS entry point'''
    try:
        # Import and run the iOS-compatible version
        from main_mobile import AccessMateApp
        
        # Configure for iOS
        app = AccessMateApp()
        app.title = "AccessMate"
        app.run()
        
    except Exception as e:
        print(f"iOS startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
""")
        
        # Create iOS-specific requirements
        requirements = ios_dir / "requirements.txt"
        requirements.write_text("""kivy>=2.1.0
pillow>=9.0.0
requests>=2.28.0
pyttsx3>=2.90
speechrecognition>=3.10.0
numpy>=1.21.0
""")
        
        print("✅ iOS project structure created")
        return str(ios_dir)
        
    def create_info_plist(self):
        """Create Info.plist for iOS app"""
        ios_dir = self.project_root / "AccessMate_iOS"
        ios_dir.mkdir(exist_ok=True)
        
        info_plist = {
            'CFBundleName': 'AccessMate',
            'CFBundleDisplayName': 'AccessMate',
            'CFBundleIdentifier': self.bundle_id,
            'CFBundleVersion': self.build_number,
            'CFBundleShortVersionString': self.version,
            'CFBundlePackageType': 'APPL',
            'CFBundleSignature': 'ACMT',
            'CFBundleExecutable': 'AccessMate',
            'CFBundleInfoDictionaryVersion': '6.0',
            'LSRequiresIPhoneOS': True,
            'LSSupportsOpeningDocumentsInPlace': False,
            'UIFileSharingEnabled': False,
            'UILaunchStoryboardName': 'LaunchScreen',
            'UIMainStoryboardFile': 'Main',
            'UIRequiredDeviceCapabilities': ['armv7'],
            'UISupportedInterfaceOrientations': [
                'UIInterfaceOrientationPortrait',
                'UIInterfaceOrientationPortraitUpsideDown'
            ],
            'UISupportedInterfaceOrientations~ipad': [
                'UIInterfaceOrientationPortrait',
                'UIInterfaceOrientationPortraitUpsideDown',
                'UIInterfaceOrientationLandscapeLeft',
                'UIInterfaceOrientationLandscapeRight'
            ],
            'UIStatusBarStyle': 'UIStatusBarStyleDefault',
            'UIViewControllerBasedStatusBarAppearance': False,
            
            # Accessibility features
            'UIAccessibilityEnabled': True,
            'UIRequiresFullScreen': False,
            'UISupportsDocumentBrowser': False,
            
            # Privacy usage descriptions (required for App Store)
            'NSMicrophoneUsageDescription': 'AccessMate uses the microphone for voice commands and speech recognition to enhance accessibility.',
            'NSCameraUsageDescription': 'AccessMate uses the camera for text recognition and visual assistance features.',
            'NSLocationWhenInUseUsageDescription': 'AccessMate may use location for context-aware accessibility features.',
            'NSPhotoLibraryUsageDescription': 'AccessMate can analyze photos to provide accessibility descriptions.',
            'NSContactsUsageDescription': 'AccessMate can help manage contacts with voice commands.',
            'NSCalendarsUsageDescription': 'AccessMate can help manage calendar events with voice commands.',
            'NSRemindersUsageDescription': 'AccessMate can help manage reminders with voice commands.',
            'NSSpeechRecognitionUsageDescription': 'AccessMate uses speech recognition for voice commands and dictation.',
            'NSBluetoothAlwaysUsageDescription': 'AccessMate can connect to Bluetooth accessibility devices.',
            
            # Supported languages
            'CFBundleLocalizations': [
                'en', 'es', 'fr', 'de', 'it', 'pt', 'ja', 'ko', 'zh-Hans', 'zh-Hant'
            ],
            
            # App Transport Security
            'NSAppTransportSecurity': {
                'NSAllowsArbitraryLoads': False,
                'NSExceptionDomains': {}
            },
            
            # Background modes
            'UIBackgroundModes': [
                'background-processing',
                'background-fetch'
            ],
            
            # iOS deployment target
            'MinimumOSVersion': '12.0',
            'DTPlatformVersion': '16.0',
            'DTSDKName': 'iphoneos16.0',
            
            # Accessibility support
            'UIApplicationSupportsIndirectInputEvents': True,
            'UISupportsDocumentBrowser': False,
            'ITSAppUsesNonExemptEncryption': False,
        }
        
        plist_path = ios_dir / "Info.plist"
        with open(plist_path, 'wb') as f:
            plistlib.dump(info_plist, f)
            
        print("✅ Created Info.plist")
        return str(plist_path)
        
    def setup_xcode_project(self):
        """Setup Xcode project configuration"""
        print("🔨 Setting up Xcode project...")
        
        # Run kivy-ios to create project
        ios_project_dir = self.project_root / "ios_project"
        
        try:
            # Create iOS project using kivy-ios
            subprocess.run([
                'kivy-ios', 'create', 'AccessMate', str(ios_project_dir)
            ], check=True, cwd=self.project_root)
            
            print("✅ Xcode project created")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create Xcode project: {e}")
            return False
            
    def create_app_store_metadata(self):
        """Create App Store metadata"""
        metadata_dir = self.project_root / "store_metadata" / "ios"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # App Store description
        description = """AccessMate brings comprehensive accessibility features to your iOS device, making technology truly inclusive for everyone.

🌟 DESIGNED FOR ACCESSIBILITY
Every feature in AccessMate is crafted with accessibility in mind, providing seamless integration with VoiceOver, Switch Control, and other iOS accessibility features.

✨ KEY FEATURES:
• Advanced screen reading with natural voice synthesis
• Real-time text recognition and OCR
• Voice commands and speech-to-text
• High contrast themes and adjustable text sizes
• Audio descriptions for visual content
• Emergency accessibility shortcuts
• Multi-language support

🎯 PERFECT FOR:
• Users with visual impairments
• People with hearing difficulties
• Those with motor challenges
• Cognitive accessibility needs
• Seniors and caregivers
• Anyone seeking enhanced accessibility

🔒 PRIVACY FIRST:
• Local processing when possible
• No data collection without consent
• Transparent privacy practices
• Secure data handling

🌍 INCLUSIVE DESIGN:
AccessMate follows Apple's accessibility guidelines and works seamlessly with iOS built-in features like VoiceOver, Magnifier, and AssistiveTouch.

Transform your iOS experience with AccessMate - where accessibility meets innovation."""

        # Store listing files
        (metadata_dir / "app_name.txt").write_text("AccessMate")
        (metadata_dir / "subtitle.txt").write_text("Complete Accessibility Companion")
        (metadata_dir / "description.txt").write_text(description)
        
        # Keywords (max 100 characters)
        keywords = "accessibility,screen reader,voice control,assistive,disability,inclusive,vision,hearing,motor"
        (metadata_dir / "keywords.txt").write_text(keywords)
        
        # App Store categories
        categories = {
            "primary_category": "Medical",
            "secondary_category": "Productivity"
        }
        (metadata_dir / "categories.json").write_text(json.dumps(categories, indent=2))
        
        # Age rating and content
        content_rating = {
            "age_rating": "4+",
            "content_warnings": [],
            "medical_disclaimer": "This app provides accessibility assistance but is not a substitute for professional medical advice."
        }
        (metadata_dir / "content_rating.json").write_text(json.dumps(content_rating, indent=2))
        
        # App Store Connect information
        app_store_info = {
            "sku": "accessmate-ios-001",
            "bundle_id": self.bundle_id,
            "price_tier": "Free",
            "availability": "Global",
            "version": self.version,
            "copyright": "© 2024 AccessMate Team",
            "review_notes": "AccessMate is designed to enhance accessibility for iOS users. All features comply with iOS accessibility guidelines and integrate seamlessly with system accessibility services."
        }
        (metadata_dir / "app_store_info.json").write_text(json.dumps(app_store_info, indent=2))
        
        print("✅ Created App Store metadata")
        
    def build_for_device(self):
        """Build for iOS device/App Store"""
        print("📱 Building for iOS device...")
        
        xcode_project = self.project_root / "ios_project" / "AccessMate.xcodeproj"
        
        if not xcode_project.exists():
            print("❌ Xcode project not found")
            return False
            
        try:
            # Build for device
            subprocess.run([
                'xcodebuild',
                '-project', str(xcode_project),
                '-scheme', 'AccessMate',
                '-configuration', 'Release',
                '-destination', 'generic/platform=iOS',
                'archive',
                '-archivePath', str(self.project_root / "AccessMate.xcarchive")
            ], check=True)
            
            print("✅ iOS archive created")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ iOS build failed: {e}")
            return False
            
    def create_ipa(self):
        """Create IPA file for App Store submission"""
        print("📦 Creating IPA file...")
        
        archive_path = self.project_root / "AccessMate.xcarchive"
        ipa_path = self.project_root / "AccessMate.ipa"
        
        try:
            # Export IPA
            subprocess.run([
                'xcodebuild',
                '-exportArchive',
                '-archivePath', str(archive_path),
                '-exportPath', str(self.project_root),
                '-exportOptionsPlist', str(self.create_export_options())
            ], check=True)
            
            print(f"✅ IPA created: {ipa_path}")
            return str(ipa_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ IPA creation failed: {e}")
            return None
            
    def create_export_options(self):
        """Create export options plist"""
        export_options = {
            'method': 'app-store',
            'uploadBitcode': False,
            'uploadSymbols': True,
            'compileBitcode': False,
            'stripSwiftSymbols': True,
            'teamID': 'YOUR_TEAM_ID',  # Replace with actual Team ID
            'provisioningProfiles': {
                self.bundle_id: 'AccessMate App Store'  # Replace with actual provisioning profile
            }
        }
        
        export_plist = self.project_root / "ExportOptions.plist"
        with open(export_plist, 'wb') as f:
            plistlib.dump(export_options, f)
            
        return str(export_plist)
        
    def generate_release_notes(self):
        """Generate App Store release notes"""
        release_notes = """🎉 AccessMate v1.0.0 - Welcome to Inclusive iOS!

✨ INTRODUCING ACCESSMATE:
The most comprehensive accessibility app for iOS, designed to make your device truly accessible for everyone.

🌟 NEW FEATURES:
• Seamless VoiceOver integration with enhanced screen reading
• Advanced text recognition with real-time OCR
• Voice commands with Siri Shortcuts support
• Dynamic Type and high contrast theme support
• Audio descriptions for visual content
• Emergency accessibility features with quick actions
• Multi-language support with localized voices

🎯 iOS INTEGRATION:
• Works perfectly with VoiceOver and Voice Control
• Supports iOS Switch Control and AssistiveTouch
• Integrates with Magnifier and other accessibility tools
• Optimized for iOS 16+ accessibility features
• Full Dynamic Type and Smart Invert support

🔒 PRIVACY & SECURITY:
• All processing happens on-device when possible
• No personal data collection without explicit consent
• Full compliance with iOS privacy guidelines
• Transparent data usage

Perfect for users with visual, hearing, motor, or cognitive challenges, and anyone who values enhanced accessibility on iOS.

Experience truly inclusive technology on your iPhone and iPad!"""

        notes_dir = self.project_root / "store_metadata" / "ios"
        (notes_dir / "release_notes.txt").write_text(release_notes)
        
        print("✅ Generated App Store release notes")
        
    def build(self):
        """Main iOS build process"""
        print("🍎 Starting iOS App Store build process...")
        
        if not self.prepare_environment():
            print("ℹ️  iOS builds require macOS with Xcode")
            print("📋 Manual iOS build instructions:")
            print("1. Install Xcode and kivy-ios on macOS")
            print("2. Run: pip install kivy-ios")
            print("3. Run: kivy-ios create AccessMate ios_project/")
            print("4. Open Xcode project and configure signing")
            print("5. Build and archive for App Store")
            return False
            
        ios_project = self.create_ios_project()
        info_plist = self.create_info_plist()
        self.create_app_store_metadata()
        self.generate_release_notes()
        
        if self.setup_xcode_project():
            if self.build_for_device():
                ipa_path = self.create_ipa()
                
                if ipa_path:
                    print("\n🎉 iOS App Store build completed!")
                    print(f"📱 IPA file: {ipa_path}")
                    print(f"📝 Metadata: {self.project_root}/store_metadata/ios/")
                    print("\n📋 Next Steps:")
                    print("1. Upload IPA to App Store Connect")
                    print("2. Configure app metadata in App Store Connect")
                    print("3. Submit for App Store review")
                    print("4. Manage TestFlight beta testing")
                    
                    return True
                    
        print("❌ iOS build process incomplete")
        return False

if __name__ == "__main__":
    builder = iOSAppStoreBuilder(".")
    success = builder.build()
    sys.exit(0 if success else 1)