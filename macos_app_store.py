#!/usr/bin/env python3
"""
macOS App Store Builder for AccessMate  
Creates production-ready .app and .pkg files for Mac App Store submission
"""

import os
import sys
import subprocess
import json
import shutil
import plistlib
from pathlib import Path

class macOSAppStoreBuilder:
    """Builds macOS app for App Store submission"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.app_name = "AccessMate"
        self.bundle_id = "com.accessmate.macos"
        self.version = "1.0.0"
        self.build_number = "1"
        
    def prepare_environment(self):
        """Setup macOS build environment"""
        print("🍎 Preparing macOS build environment...")
        
        if sys.platform != "darwin":
            print("❌ macOS builds require macOS")
            return False
            
        # Check for required tools
        tools = ['python3', 'py2app', 'pkgbuild', 'productbuild']
        missing_tools = []
        
        for tool in tools:
            if not shutil.which(tool) and tool not in ['py2app']:
                missing_tools.append(tool)
                
        # Check py2app separately
        try:
            import py2app
            print("✅ py2app found")
        except ImportError:
            missing_tools.append('py2app')
            
        if missing_tools:
            print(f"❌ Missing tools: {', '.join(missing_tools)}")
            print("Install with: pip install py2app")
            return False
            
        print("✅ macOS build tools verified")
        return True
        
    def create_setup_py(self):
        """Create setup.py for py2app"""
        setup_content = f'''#!/usr/bin/env python3
"""
setup.py for AccessMate macOS App Store build
"""

from setuptools import setup
import py2app
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

APP = ['src/main_desktop_comprehensive.py']
DATA_FILES = [
    ('assets', ['src/assets']),
    ('', ['README.md', 'LICENSE']),
]

OPTIONS = {{
    'argv_emulation': True,
    'iconfile': 'src/icon.icns',
    'plist': {{
        'CFBundleName': '{self.app_name}',
        'CFBundleDisplayName': '{self.app_name}',
        'CFBundleIdentifier': '{self.bundle_id}',
        'CFBundleVersion': '{self.build_number}',
        'CFBundleShortVersionString': '{self.version}',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'ACMT',
        'CFBundleExecutable': '{self.app_name}',
        'CFBundleInfoDictionaryVersion': '6.0',
        'LSMinimumSystemVersion': '10.15.0',
        'NSHighResolutionCapable': True,
        'NSSupportsAutomaticGraphicsSwitching': True,
        'LSApplicationCategoryType': 'public.app-category.medical',
        
        # Accessibility
        'NSAccessibilityEnabled': True,
        'NSSupportsVoiceOver': True,
        
        # Privacy usage descriptions
        'NSMicrophoneUsageDescription': 'AccessMate uses the microphone for voice commands and speech recognition.',
        'NSCameraUsageDescription': 'AccessMate uses the camera for text recognition and visual assistance.',
        'NSContactsUsageDescription': 'AccessMate can help manage contacts with voice commands.',
        'NSCalendarsUsageDescription': 'AccessMate can help manage calendar events.',
        'NSRemindersUsageDescription': 'AccessMate can help manage reminders.',
        'NSSpeechRecognitionUsageDescription': 'AccessMate uses speech recognition for voice commands.',
        'NSSystemAdministrationUsageDescription': 'AccessMate may need system access for accessibility features.',
        
        # Security
        'NSAppTransportSecurity': {{
            'NSAllowsArbitraryLoads': False,
        }},
        
        # Document types
        'CFBundleDocumentTypes': [
            {{
                'CFBundleTypeName': 'Text Document',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': ['public.text'],
            }},
        ],
        
        # URL schemes
        'CFBundleURLTypes': [
            {{
                'CFBundleURLName': 'AccessMate URL',
                'CFBundleURLSchemes': ['accessmate'],
            }},
        ],
        
        # Entitlements for App Store
        'com.apple.security.app-sandbox': True,
        'com.apple.security.files.user-selected.read-write': True,
        'com.apple.security.network.client': True,
        'com.apple.security.microphone': True,
        'com.apple.security.camera': True,
        'com.apple.security.device.audio-input': True,
        'com.apple.security.personal-information.calendars': True,
        'com.apple.security.personal-information.contacts': True,
        'com.apple.security.automation.apple-events': True,
    }},
    'packages': ['tkinter', 'pyscript', 'pygments', 'markdown'],
    'includes': [
        'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox',
        'pyttsx3', 'speech_recognition', 'PIL', 'requests', 'json', 'os', 'sys',
        'threading', 'subprocess', 'webbrowser', 'tempfile', 'pathlib'
    ],
    'excludes': ['matplotlib', 'numpy', 'scipy', 'pandas'],
    'resources': ['src/assets', 'src/support_messages.json'],
    'optimize': 2,
}}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={{'py2app': OPTIONS}},
    setup_requires=['py2app'],
    name='{self.app_name}',
    version='{self.version}',
    description='Complete accessibility solution for macOS',
    author='AccessMate Team',
    author_email='support@accessmate.com',
    url='https://www.accessmate.com',
    license='Proprietary',
)
'''
        
        setup_path = self.project_root / "setup_macos.py"
        setup_path.write_text(setup_content)
        
        print("✅ Created setup.py for macOS")
        return str(setup_path)
        
    def create_icon_set(self):
        """Create .icns icon file for macOS"""
        icon_dir = self.project_root / "src"
        icon_path = icon_dir / "icon.icns"
        
        if not icon_path.exists():
            # Create a basic icon if none exists
            print("⚠️  No icon.icns found, creating placeholder")
            
            # Try to convert from PNG if available
            png_icon = icon_dir / "icon.png"
            if png_icon.exists():
                try:
                    subprocess.run([
                        'sips', '-s', 'format', 'icns',
                        str(png_icon), '--out', str(icon_path)
                    ], check=True)
                    print("✅ Converted PNG to ICNS")
                except subprocess.CalledProcessError:
                    print("⚠️  Could not convert PNG to ICNS")
            else:
                # Create minimal icns file
                icon_path.write_bytes(b'')  # Placeholder
                
        return str(icon_path)
        
    def build_app(self):
        """Build the .app bundle using py2app"""
        print("🔨 Building macOS .app bundle...")
        
        os.chdir(self.project_root)
        
        # Clean previous builds
        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("dist", ignore_errors=True)
        
        try:
            # Build the app
            subprocess.run([
                sys.executable, 'setup_macos.py', 'py2app'
            ], check=True)
            
            app_path = self.project_root / "dist" / f"{self.app_name}.app"
            
            if app_path.exists():
                print(f"✅ App bundle created: {app_path}")
                return str(app_path)
            else:
                print("❌ App bundle not found after build")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ py2app build failed: {e}")
            return None
            
    def sign_app(self, app_path):
        """Code sign the app for App Store submission"""
        print("🔏 Code signing app...")
        
        try:
            # Sign the app (requires valid Developer ID)
            subprocess.run([
                'codesign', '--force', '--verify', '--verbose',
                '--sign', 'Developer ID Application: Your Name',
                '--options', 'runtime',
                app_path
            ], check=True)
            
            print("✅ App signed successfully")
            return True
            
        except subprocess.CalledProcessError:
            print("⚠️  Code signing failed - valid Developer ID required")
            print("    For App Store submission, you need:")
            print("    1. Apple Developer account")
            print("    2. Valid certificates in Keychain")
            print("    3. App Store provisioning profiles")
            return False
            
    def create_pkg_installer(self, app_path):
        """Create .pkg installer for Mac App Store"""
        print("📦 Creating PKG installer...")
        
        pkg_path = self.project_root / f"{self.app_name}.pkg"
        
        try:
            # Create component package
            subprocess.run([
                'pkgbuild',
                '--component', app_path,
                '--install-location', '/Applications',
                '--identifier', self.bundle_id,
                '--version', self.version,
                str(pkg_path)
            ], check=True)
            
            print(f"✅ PKG installer created: {pkg_path}")
            return str(pkg_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ PKG creation failed: {e}")
            return None
            
    def create_dmg(self, app_path):
        """Create DMG disk image for distribution"""
        print("💿 Creating DMG disk image...")
        
        dmg_path = self.project_root / f"{self.app_name}-{self.version}.dmg"
        temp_dmg = self.project_root / "temp.dmg"
        
        try:
            # Create temporary DMG
            subprocess.run([
                'hdiutil', 'create', '-size', '100m', '-fs', 'HFS+',
                '-volname', self.app_name, str(temp_dmg)
            ], check=True)
            
            # Mount the DMG
            mount_result = subprocess.run([
                'hdiutil', 'attach', str(temp_dmg)
            ], capture_output=True, text=True, check=True)
            
            # Extract mount point
            mount_point = None
            for line in mount_result.stdout.split('\n'):
                if '/Volumes/' in line:
                    mount_point = line.split('\t')[-1].strip()
                    break
                    
            if mount_point:
                # Copy app to DMG
                shutil.copytree(app_path, f"{mount_point}/{self.app_name}.app")
                
                # Create Applications symlink
                subprocess.run([
                    'ln', '-s', '/Applications', f"{mount_point}/Applications"
                ], check=True)
                
                # Unmount
                subprocess.run(['hdiutil', 'detach', mount_point], check=True)
                
                # Convert to final DMG
                subprocess.run([
                    'hdiutil', 'convert', str(temp_dmg),
                    '-format', 'UDZO', '-o', str(dmg_path)
                ], check=True)
                
                # Cleanup
                temp_dmg.unlink()
                
                print(f"✅ DMG created: {dmg_path}")
                return str(dmg_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ DMG creation failed: {e}")
            return None
            
    def create_app_store_metadata(self):
        """Create Mac App Store metadata"""
        metadata_dir = self.project_root / "store_metadata" / "macos"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # App Store description
        description = """AccessMate transforms your Mac into a comprehensive accessibility powerhouse, designed specifically for macOS users who need enhanced digital access.

🌟 NATIVE macOS INTEGRATION
Built from the ground up for macOS, AccessMate works seamlessly with VoiceOver, Voice Control, Switch Control, and all built-in accessibility features.

✨ POWERFUL FEATURES:
• Advanced screen reading with natural voice synthesis
• Real-time text recognition and OCR with Vision framework
• Voice commands with Siri Shortcuts integration
• Dynamic Type support and high contrast themes
• Audio descriptions for visual content
• Keyboard navigation optimization
• Multi-language support with system voices

🎯 DESIGNED FOR:
• Users with visual impairments who rely on VoiceOver
• People with motor challenges using Switch Control
• Those with hearing difficulties needing visual feedback
• Cognitive accessibility support with simplified interfaces
• Seniors and caregivers managing accessibility settings
• Anyone seeking enhanced Mac accessibility

🔒 PRIVACY & SECURITY:
• All processing happens locally on your Mac
• No data sent to external servers without consent
• Full sandboxing for App Store security
• Transparent privacy practices

🌍 ACCESSIBILITY FIRST:
AccessMate follows Apple's Human Interface Guidelines and accessibility best practices, ensuring perfect integration with your existing accessibility workflow.

Experience truly inclusive computing on macOS with AccessMate - where accessibility meets innovation."""

        # Store listing files
        (metadata_dir / "app_name.txt").write_text("AccessMate")
        (metadata_dir / "subtitle.txt").write_text("Complete Accessibility for Mac")
        (metadata_dir / "description.txt").write_text(description)
        
        # Keywords for Mac App Store
        keywords = "accessibility,screen reader,voice control,assistive,disability,VoiceOver,inclusive,vision,hearing,motor"
        (metadata_dir / "keywords.txt").write_text(keywords)
        
        # Categories
        categories = {
            "primary_category": "Medical",
            "secondary_category": "Productivity"
        }
        (metadata_dir / "categories.json").write_text(json.dumps(categories, indent=2))
        
        # Mac App Store information
        app_store_info = {
            "sku": "accessmate-macos-001",
            "bundle_id": self.bundle_id,
            "price_tier": "Free",
            "availability": "Global",
            "version": self.version,
            "copyright": "© 2024 AccessMate Team",
            "minimum_os": "macOS 10.15",
            "category": "Medical",
            "age_rating": "4+",
            "review_notes": "AccessMate provides comprehensive accessibility features for macOS users. All features integrate with system accessibility services and follow Apple's accessibility guidelines."
        }
        (metadata_dir / "app_store_info.json").write_text(json.dumps(app_store_info, indent=2))
        
        print("✅ Created Mac App Store metadata")
        
    def generate_release_notes(self):
        """Generate Mac App Store release notes"""
        release_notes = """🎉 AccessMate v1.0.0 - Complete Accessibility for Mac

✨ INTRODUCING ACCESSMATE FOR macOS:
The most comprehensive accessibility solution designed specifically for Mac users, with native integration for all macOS accessibility features.

🌟 NEW FEATURES:
• Seamless VoiceOver integration with enhanced navigation
• Advanced OCR using macOS Vision framework
• Voice commands with Siri Shortcuts support
• Full Dynamic Type and high contrast support
• Keyboard navigation optimization for all users
• Audio descriptions with spatial audio support
• Multi-language accessibility with system voices

🍎 NATIVE macOS INTEGRATION:
• Perfect VoiceOver and Voice Control compatibility
• Switch Control and AssistiveTouch support
• Magnifier and Zoom integration
• Full keyboard navigation support
• Menu bar and Dock accessibility
• Mission Control and Spaces optimization

🔧 POWERFUL TOOLS:
• Real-time text recognition in any app
• Voice-controlled system navigation
• Customizable accessibility shortcuts
• Emergency accessibility features
• Advanced screen reading capabilities
• Context-aware help system

🔒 PRIVACY & SECURITY:
• All processing happens on your Mac
• Full App Store sandboxing
• No data collection without consent
• Transparent privacy practices

Perfect for Mac users with visual, hearing, motor, or cognitive challenges, plus anyone who values enhanced accessibility on macOS.

Experience the future of accessible computing on your Mac!"""

        notes_dir = self.project_root / "store_metadata" / "macos"
        (notes_dir / "release_notes.txt").write_text(release_notes)
        
        print("✅ Generated Mac App Store release notes")
        
    def build(self):
        """Main macOS build process"""
        print("🍎 Starting macOS App Store build process...")
        
        if not self.prepare_environment():
            print("ℹ️  macOS builds require macOS with development tools")
            print("📋 Manual macOS build instructions:")
            print("1. Install Xcode and command line tools")
            print("2. Run: pip install py2app")
            print("3. Create Apple Developer account")
            print("4. Configure code signing certificates")
            print("5. Build with py2app and create PKG/DMG")
            return False
            
        setup_py = self.create_setup_py()
        icon_path = self.create_icon_set()
        self.create_app_store_metadata()
        self.generate_release_notes()
        
        app_path = self.build_app()
        
        if app_path:
            signed = self.sign_app(app_path) 
            pkg_path = self.create_pkg_installer(app_path)
            dmg_path = self.create_dmg(app_path)
            
            print("\n🎉 macOS App Store build completed!")
            print(f"📱 App bundle: {app_path}")
            if pkg_path:
                print(f"📦 PKG installer: {pkg_path}")
            if dmg_path:
                print(f"💿 DMG image: {dmg_path}")
            print(f"📝 Metadata: {self.project_root}/store_metadata/macos/")
            
            print("\n📋 Next Steps:")
            print("1. Upload PKG to App Store Connect")
            print("2. Configure app metadata in App Store Connect")
            print("3. Submit for Mac App Store review")
            print("4. Distribute DMG for direct download")
            
            if not signed:
                print("\n⚠️  Code signing required for App Store submission")
                print("   Set up Apple Developer certificates in Keychain")
                
            return True
        else:
            print("❌ macOS build failed")
            return False

if __name__ == "__main__":
    builder = macOSAppStoreBuilder(".")
    success = builder.build()
    sys.exit(0 if success else 1)