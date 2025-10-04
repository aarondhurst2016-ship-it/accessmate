#!/usr/bin/env python3
"""
Android App Bundle (AAB) Creator for AccessMate
Creates production-ready AAB files for Google Play Store submission
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

class AndroidAppBundleBuilder:
    """Builds Android App Bundle for Google Play Store"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.app_name = "AccessMate"
        self.package_name = "com.accessmate.app"
        self.version_code = 1
        self.version_name = "1.0.0"
        
    def prepare_environment(self):
        """Setup Android build environment"""
        print("🔧 Preparing Android build environment...")
        
        # Check for required tools
        tools = ['buildozer', 'java', 'python']
        for tool in tools:
            if not shutil.which(tool):
                print(f"❌ {tool} not found in PATH")
                return False
                
        print("✅ Build tools verified")
        return True
        
    def update_buildozer_spec(self):
        """Update buildozer.spec for AAB production"""
        spec_path = self.project_root / "buildozer.spec"
        
        # Read current spec
        with open(spec_path, 'r') as f:
            content = f.read()
            
        # Update for production build
        updates = {
            'android.release_artifact': 'aab',  # Create AAB instead of APK
            'android.debug': '0',  # Production build
            'android.private_storage': 'True',
            'android.arch': 'arm64-v8a,armeabi-v7a',  # Multi-architecture
            'android.accept_sdk_license': 'True',
            'android.gradle_dependencies': 'androidx.core:core:1.8.0',
            'android.add_compile_options': 'sourceCompatibility = 1.8\ntargetCompatibility = 1.8',
        }
        
        # Apply updates
        lines = content.split('\n')
        for i, line in enumerate(lines):
            for key, value in updates.items():
                if line.strip().startswith(f'{key} =') or line.strip().startswith(f'#{key} ='):
                    lines[i] = f'{key} = {value}'
                    break
                    
        # Write updated spec
        with open(spec_path, 'w') as f:
            f.write('\n'.join(lines))
            
        print("✅ Updated buildozer.spec for AAB production")
        
    def create_metadata(self):
        """Create Google Play Store metadata"""
        metadata_dir = self.project_root / "store_metadata" / "android"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # App description
        description = """AccessMate - Complete Accessibility Companion

Transform your digital experience with AccessMate, the comprehensive accessibility app designed for users with visual, hearing, motor, and cognitive challenges.

🎯 KEY FEATURES:
• Advanced screen reading with natural voice synthesis
• Real-time text recognition and OCR
• Voice commands and speech-to-text
• High contrast themes and font scaling
• Audio descriptions and sound enhancement
• Customizable interface with large buttons
• Emergency accessibility features
• Multi-language support

🌟 ACCESSIBILITY FIRST:
AccessMate is built from the ground up with accessibility in mind. Every feature is designed to work seamlessly with existing assistive technologies while providing powerful standalone functionality.

💡 SMART FEATURES:
• AI-powered content recognition
• Contextual help and tutorials
• Customizable gestures and shortcuts
• Cloud sync across devices
• Offline functionality
• Battery optimization

🔒 PRIVACY & SECURITY:
• Local processing when possible
• Encrypted data storage
• No unnecessary permissions
• Transparent privacy practices
• GDPR compliant

Perfect for individuals with disabilities, seniors, and anyone who needs enhanced accessibility features. AccessMate makes technology truly accessible for everyone.

Download now and experience the future of accessible computing!"""
        
        # Write store listing files
        (metadata_dir / "title.txt").write_text("AccessMate - Accessibility Companion")
        (metadata_dir / "short_description.txt").write_text("Complete accessibility solution for enhanced digital experiences")
        (metadata_dir / "full_description.txt").write_text(description)
        
        # Keywords and categories
        keywords = [
            "accessibility", "screen reader", "voice control", "assistive technology",
            "visual impairment", "hearing impairment", "motor disability", "cognitive support",
            "text to speech", "speech to text", "OCR", "high contrast", "large fonts",
            "disability support", "inclusive design", "universal access", "digital inclusion"
        ]
        
        (metadata_dir / "keywords.txt").write_text(", ".join(keywords))
        (metadata_dir / "category.txt").write_text("Medical")  # Primary category
        (metadata_dir / "content_rating.txt").write_text("Everyone")
        
        # Contact information
        contact_info = {
            "developer_name": "AccessMate Team",
            "developer_email": "support@accessmate.com",
            "website": "https://www.accessmate.com",
            "privacy_policy": "https://www.accessmate.com/privacy",
            "support_url": "https://www.accessmate.com/support"
        }
        
        (metadata_dir / "contact_info.json").write_text(json.dumps(contact_info, indent=2))
        
        print("✅ Created Google Play Store metadata")
        
    def build_aab(self):
        """Build the Android App Bundle"""
        print("🚀 Building Android App Bundle...")
        
        os.chdir(self.project_root)
        
        # Clean previous builds
        subprocess.run(['buildozer', 'android', 'clean'], check=False)
        
        # Build AAB
        result = subprocess.run([
            'buildozer', 'android', 'release'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ AAB build completed successfully")
            
            # Find the built AAB
            bin_dir = self.project_root / "bin"
            aab_files = list(bin_dir.glob("*.aab"))
            
            if aab_files:
                aab_file = aab_files[0]
                print(f"📦 AAB created: {aab_file}")
                return str(aab_file)
            else:
                print("❌ AAB file not found")
                return None
        else:
            print(f"❌ AAB build failed: {result.stderr}")
            return None
            
    def create_signing_config(self):
        """Create keystore and signing configuration"""
        keystore_dir = self.project_root / "android_keystore"
        keystore_dir.mkdir(exist_ok=True)
        
        keystore_path = keystore_dir / "accessmate.keystore"
        
        if not keystore_path.exists():
            print("🔐 Creating Android keystore...")
            
            # Generate keystore
            subprocess.run([
                'keytool', '-genkey', '-v',
                '-keystore', str(keystore_path),
                '-alias', 'accessmate',
                '-keyalg', 'RSA',
                '-keysize', '2048',
                '-validity', '10000',
                '-storepass', 'accessmate123',
                '-keypass', 'accessmate123',
                '-dname', 'CN=AccessMate, OU=Accessibility, O=AccessMate, L=Global, ST=Global, C=US'
            ], check=True)
            
            print("✅ Keystore created")
        else:
            print("✅ Using existing keystore")
            
        return str(keystore_path)
    
    def optimize_aab(self, aab_path):
        """Optimize AAB for Google Play Store"""
        print("⚡ Optimizing AAB...")
        
        # Use bundletool to validate and optimize
        try:
            # Validate AAB
            subprocess.run([
                'bundletool', 'validate',
                '--bundle', aab_path
            ], check=True)
            
            print("✅ AAB validation passed")
            
            # Generate universal APK for testing
            universal_apk = str(Path(aab_path).with_suffix('.apk'))
            subprocess.run([
                'bundletool', 'build-apks',
                '--bundle', aab_path,
                '--output', universal_apk,
                '--mode', 'universal'
            ], check=False)  # May fail without signing
            
        except subprocess.CalledProcessError:
            print("⚠️  bundletool not available - skipping validation")
        except FileNotFoundError:
            print("⚠️  bundletool not found - install from Android SDK")
            
    def generate_release_notes(self):
        """Generate release notes"""
        release_notes = """🎉 AccessMate v1.0.0 - Initial Release

✨ NEW FEATURES:
• Complete accessibility suite for all users
• Advanced screen reading with natural voices
• Real-time text recognition and OCR
• Voice commands and speech-to-text
• High contrast themes and customizable fonts
• Audio descriptions and sound enhancement
• Emergency accessibility features
• Multi-language support

🔧 TECHNICAL IMPROVEMENTS:
• Optimized for Android 13+
• Battery-efficient background processing
• Seamless integration with Android accessibility services
• Offline functionality for core features
• Enhanced security and privacy protection

🌟 ACCESSIBILITY HIGHLIGHTS:
• Works with TalkBack and other screen readers
• Large touch targets and clear navigation
• Voice feedback for all interactions
• Customizable gestures and shortcuts
• Support for external accessibility devices

Perfect for users with visual, hearing, motor, or cognitive challenges, and anyone who values enhanced accessibility features.

Download now and experience truly inclusive technology!"""

        notes_dir = self.project_root / "store_metadata" / "android"
        (notes_dir / "release_notes.txt").write_text(release_notes)
        
        print("✅ Generated release notes")
        
    def build(self):
        """Main build process"""
        print("🚀 Starting Android App Bundle build process...")
        
        if not self.prepare_environment():
            return False
            
        self.update_buildozer_spec()
        self.create_metadata()
        self.generate_release_notes()
        keystore = self.create_signing_config()
        
        aab_path = self.build_aab()
        if aab_path:
            self.optimize_aab(aab_path)
            
            print("\n🎉 Android App Bundle build completed!")
            print(f"📦 AAB file: {aab_path}")
            print(f"🔐 Keystore: {keystore}")
            print(f"📝 Metadata: {self.project_root}/store_metadata/android/")
            print("\n📋 Next Steps:")
            print("1. Upload AAB to Google Play Console")
            print("2. Configure store listing with metadata")
            print("3. Set up release management")
            print("4. Submit for review")
            
            return True
        else:
            print("❌ Build failed")
            return False

if __name__ == "__main__":
    builder = AndroidAppBundleBuilder(".")
    success = builder.build()
    sys.exit(0 if success else 1)