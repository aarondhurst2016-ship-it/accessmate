#!/usr/bin/env python3
"""
Linux Distribution Builder for AccessMate
Creates AppImage, DEB, RPM, and Flatpak packages for Linux distribution
"""

import os
import sys
import subprocess
import json
import shutil
import tempfile
from pathlib import Path

class LinuxDistributionBuilder:
    """Builds Linux packages for various distributions"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.app_name = "AccessMate"
        self.app_id = "com.accessmate.AccessMate"
        self.version = "1.0.0"
        self.description = "Complete accessibility solution for Linux"
        
    def prepare_environment(self):
        """Setup Linux build environment"""
        print("🐧 Preparing Linux build environment...")
        
        # Check for required tools
        tools = ['python3', 'pip3']
        missing_tools = []
        
        for tool in tools:
            if not shutil.which(tool):
                missing_tools.append(tool)
                
        if missing_tools:
            print(f"❌ Missing tools: {', '.join(missing_tools)}")
            return False
            
        # Check optional tools
        optional_tools = ['appimage-builder', 'dpkg-deb', 'rpmbuild', 'flatpak-builder']
        available_tools = []
        
        for tool in optional_tools:
            if shutil.which(tool):
                available_tools.append(tool)
                
        print(f"✅ Available build tools: {', '.join(available_tools) if available_tools else 'PyInstaller only'}")
        return True
        
    def create_desktop_file(self):
        """Create .desktop file for Linux integration"""
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={self.app_name}
GenericName=Accessibility Companion
Comment={self.description}
Exec=accessmate %F
Icon=accessmate
Terminal=false
Categories=Accessibility;AudioVideo;Office;Productivity;Utility;
Keywords=accessibility;screen-reader;voice;speech;disability;assistive;inclusive;
MimeType=text/plain;text/xml;application/json;
StartupNotify=true
StartupWMClass=AccessMate

# Accessibility
X-GNOME-UsesNotifications=true
X-KDE-StartupNotify=true

# Localization
Name[es]=AccessMate
Comment[es]=Solución completa de accesibilidad para Linux
Name[fr]=AccessMate  
Comment[fr]=Solution d'accessibilité complète pour Linux
Name[de]=AccessMate
Comment[de]=Vollständige Barrierefreiheitslösung für Linux
"""
        
        desktop_path = self.project_root / "accessmate.desktop"
        desktop_path.write_text(desktop_content)
        
        print("✅ Created .desktop file")
        return str(desktop_path)
        
    def create_appimage_recipe(self):
        """Create AppImageBuilder recipe"""
        recipe = {
            "version": 1,
            "AppDir": {
                "path": str(self.project_root / "AccessMate.AppDir"),
                "app_info": {
                    "id": self.app_id,
                    "name": self.app_name,
                    "icon": "accessmate",
                    "version": self.version,
                    "exec": "usr/bin/python3",
                    "exec_args": "$APPDIR/usr/bin/accessmate $@"
                },
                "apt": {
                    "arch": "amd64",
                    "sources": [
                        {
                            "sourceline": "deb http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse",
                            "key_url": "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x871920D1991BC93C"
                        }
                    ],
                    "include": [
                        "python3",
                        "python3-tk",
                        "python3-pip",
                        "libgtk-3-0",
                        "libpulse0",
                        "libasound2",
                        "espeak-ng",
                        "festival",
                        "speech-dispatcher"
                    ]
                },
                "files": {
                    "include": [
                        "src/**",
                        "README.md",
                        "LICENSE"
                    ],
                    "exclude": [
                        "**/__pycache__",
                        "**/*.pyc",
                        "build/**",
                        "dist/**"
                    ]
                },
                "runtime": {
                    "env": {
                        "PYTHONPATH": "$APPDIR/usr/lib/python3/dist-packages:$APPDIR/src",
                        "PATH": "$APPDIR/usr/bin:$PATH"
                    }
                }
            },
            "AppImage": {
                "arch": "x86_64",
                "file_name": f"{self.app_name}-{self.version}-x86_64.AppImage",
                "update_info": f"gh-releases-zsync|accessmate|accessmate|latest|{self.app_name}-*-x86_64.AppImage.zsync",
                "sign_key": None
            }
        }
        
        recipe_path = self.project_root / "appimage-recipe.yml"
        import yaml
        with open(recipe_path, 'w') as f:
            yaml.dump(recipe, f, default_flow_style=False)
            
        print("✅ Created AppImage recipe")
        return str(recipe_path)
        
    def build_appimage(self):
        """Build AppImage package"""
        print("📦 Building AppImage...")
        
        if not shutil.which('appimage-builder'):
            print("⚠️  appimage-builder not found, creating manual AppDir")
            return self.create_manual_appimage()
            
        try:
            # Build AppImage using appimage-builder
            subprocess.run([
                'appimage-builder', '--recipe', 'appimage-recipe.yml'
            ], check=True, cwd=self.project_root)
            
            # Find created AppImage
            appimages = list(self.project_root.glob("*.AppImage"))
            if appimages:
                appimage_path = appimages[0]
                print(f"✅ AppImage created: {appimage_path}")
                return str(appimage_path)
            else:
                print("❌ AppImage not found after build")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ AppImage build failed: {e}")
            return None
            
    def create_manual_appimage(self):
        """Create AppImage manually using PyInstaller"""
        print("🔨 Creating manual AppImage with PyInstaller...")
        
        appdir = self.project_root / "AccessMate.AppDir"
        appdir.mkdir(exist_ok=True)
        
        # Create AppDir structure
        (appdir / "usr" / "bin").mkdir(parents=True, exist_ok=True)
        (appdir / "usr" / "share" / "applications").mkdir(parents=True, exist_ok=True)
        (appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True, exist_ok=True)
        
        # Build executable with PyInstaller
        try:
            subprocess.run([
                'pyinstaller',
                '--onefile',
                '--name', 'accessmate',
                '--distpath', str(appdir / "usr" / "bin"),
                '--add-data', 'src:src',
                '--hidden-import', 'tkinter',
                '--hidden-import', 'pyttsx3',
                '--hidden-import', 'speech_recognition',
                'src/main_desktop_comprehensive.py'
            ], check=True, cwd=self.project_root)
            
            # Copy desktop file
            shutil.copy(
                self.project_root / "accessmate.desktop",
                appdir / "AccessMate.desktop"
            )
            
            # Copy icon if available
            icon_sources = ["src/icon.png", "src/assets/icon.png", "icon.png"]
            for icon_src in icon_sources:
                icon_path = self.project_root / icon_src
                if icon_path.exists():
                    shutil.copy(
                        icon_path,
                        appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps" / "accessmate.png"
                    )
                    break
                    
            # Create AppRun script
            apprun_content = """#!/bin/bash
APPDIR="$(dirname "$(readlink -f "$0")")"
export PATH="$APPDIR/usr/bin:$PATH"
export PYTHONPATH="$APPDIR/src:$PYTHONPATH"
exec "$APPDIR/usr/bin/accessmate" "$@"
"""
            apprun_path = appdir / "AppRun"
            apprun_path.write_text(apprun_content)
            apprun_path.chmod(0o755)
            
            print(f"✅ Manual AppDir created: {appdir}")
            
            # Create AppImage if appimagetool is available
            if shutil.which('appimagetool'):
                appimage_path = self.project_root / f"{self.app_name}-{self.version}-x86_64.AppImage"
                subprocess.run([
                    'appimagetool', str(appdir), str(appimage_path)
                ], check=True)
                print(f"✅ AppImage created: {appimage_path}")
                return str(appimage_path)
            else:
                print("⚠️  appimagetool not found - AppDir created but no AppImage")
                return str(appdir)
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Manual AppImage creation failed: {e}")
            return None
            
    def create_deb_package(self):
        """Create Debian package"""
        print("📦 Creating DEB package...")
        
        deb_dir = self.project_root / "debian_package"
        deb_dir.mkdir(exist_ok=True)
        
        # Create DEBIAN control directory
        control_dir = deb_dir / "DEBIAN"
        control_dir.mkdir(exist_ok=True)
        
        # Create control file
        control_content = f"""Package: accessmate
Version: {self.version}
Section: accessibility
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.8), python3-tk, libgtk-3-0, pulseaudio, espeak-ng
Maintainer: AccessMate Team <support@accessmate.com>
Description: {self.description}
 AccessMate provides comprehensive accessibility features for Linux users,
 including screen reading, voice commands, text recognition, and more.
 .
 Perfect for users with visual, hearing, motor, or cognitive challenges.
Homepage: https://www.accessmate.com
"""
        (control_dir / "control").write_text(control_content)
        
        # Create postinst script
        postinst_content = """#!/bin/bash
set -e

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q /usr/share/applications
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor
fi

# Configure accessibility services
if command -v gsettings >/dev/null 2>&1; then
    # Enable accessibility features
    gsettings set org.gnome.desktop.interface toolkit-accessibility true
fi

exit 0
"""
        postinst_path = control_dir / "postinst"
        postinst_path.write_text(postinst_content)
        postinst_path.chmod(0o755)
        
        # Create directory structure
        usr_dir = deb_dir / "usr"
        (usr_dir / "bin").mkdir(parents=True, exist_ok=True)
        (usr_dir / "share" / "applications").mkdir(parents=True, exist_ok=True)
        (usr_dir / "share" / "accessmate").mkdir(parents=True, exist_ok=True)
        (usr_dir / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True, exist_ok=True)
        
        # Copy application files
        shutil.copytree(
            self.project_root / "src",
            usr_dir / "share" / "accessmate" / "src"
        )
        
        # Create launcher script
        launcher_content = f"""#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/usr/share/accessmate/src')
os.chdir('/usr/share/accessmate')
from main_desktop_comprehensive import main
if __name__ == "__main__":
    main()
"""
        launcher_path = usr_dir / "bin" / "accessmate"
        launcher_path.write_text(launcher_content)
        launcher_path.chmod(0o755)
        
        # Copy desktop file
        shutil.copy(
            self.project_root / "accessmate.desktop",
            usr_dir / "share" / "applications"
        )
        
        try:
            # Build DEB package
            deb_file = self.project_root / f"accessmate_{self.version}_amd64.deb"
            subprocess.run([
                'dpkg-deb', '--build', str(deb_dir), str(deb_file)
            ], check=True)
            
            print(f"✅ DEB package created: {deb_file}")
            return str(deb_file)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ DEB package creation failed: {e}")
            return None
        except FileNotFoundError:
            print("⚠️  dpkg-deb not found - DEB creation skipped")
            return None
            
    def create_rpm_package(self):
        """Create RPM package"""
        print("📦 Creating RPM package...")
        
        if not shutil.which('rpmbuild'):
            print("⚠️  rpmbuild not found - RPM creation skipped")
            return None
            
        # Create RPM build directories
        rpm_root = self.project_root / "rpmbuild"
        for dir_name in ["BUILD", "RPMS", "SOURCES", "SPECS", "SRPMS"]:
            (rpm_root / dir_name).mkdir(parents=True, exist_ok=True)
            
        # Create spec file
        spec_content = f"""Name:           accessmate
Version:        {self.version}
Release:        1%{{?dist}}
Summary:        {self.description}

License:        Proprietary
URL:            https://www.accessmate.com
Source0:        %{{name}}-%{{version}}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       python3 >= 3.8, python3-tkinter, gtk3, pulseaudio, espeak-ng

%description
AccessMate provides comprehensive accessibility features for Linux users,
including screen reading, voice commands, text recognition, and more.
Perfect for users with visual, hearing, motor, or cognitive challenges.

%prep
%autosetup

%build
# Nothing to build for Python application

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/accessmate
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/256x256/apps

# Copy application files
cp -r src/ $RPM_BUILD_ROOT/usr/share/accessmate/
cp accessmate.desktop $RPM_BUILD_ROOT/usr/share/applications/

# Create launcher script
cat > $RPM_BUILD_ROOT/usr/bin/accessmate << 'EOF'
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/usr/share/accessmate/src')
os.chdir('/usr/share/accessmate')
from main_desktop_comprehensive import main
if __name__ == "__main__":
    main()
EOF
chmod +x $RPM_BUILD_ROOT/usr/bin/accessmate

%files
/usr/bin/accessmate
/usr/share/accessmate/
/usr/share/applications/accessmate.desktop

%post
# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q /usr/share/applications
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor
fi

%changelog
* Wed Dec 04 2024 AccessMate Team <support@accessmate.com> - {self.version}-1
- Initial release
"""
        
        spec_path = rpm_root / "SPECS" / "accessmate.spec"
        spec_path.write_text(spec_content)
        
        # Create source tarball
        sources_dir = rpm_root / "SOURCES"
        tarball_path = sources_dir / f"accessmate-{self.version}.tar.gz"
        
        try:
            subprocess.run([
                'tar', '-czf', str(tarball_path),
                '--exclude-vcs',
                '--exclude=__pycache__',
                '--exclude=*.pyc',
                '--exclude=build',
                '--exclude=dist',
                '--exclude=rpmbuild',
                'src/', 'accessmate.desktop'
            ], check=True, cwd=self.project_root)
            
            # Build RPM
            subprocess.run([
                'rpmbuild',
                '--define', f'_topdir {rpm_root}',
                '-ba', str(spec_path)
            ], check=True)
            
            # Find created RPM
            rpm_files = list((rpm_root / "RPMS").rglob("*.rpm"))
            if rpm_files:
                rpm_file = rpm_files[0]
                final_rpm = self.project_root / rpm_file.name
                shutil.copy(rpm_file, final_rpm)
                print(f"✅ RPM package created: {final_rpm}")
                return str(final_rpm)
            else:
                print("❌ RPM file not found after build")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ RPM package creation failed: {e}")
            return None
            
    def create_flatpak_manifest(self):
        """Create Flatpak manifest"""
        manifest = {
            "app-id": self.app_id,
            "runtime": "org.freedesktop.Platform",
            "runtime-version": "22.08",
            "sdk": "org.freedesktop.Sdk",
            "command": "accessmate",
            "finish-args": [
                "--share=ipc",
                "--socket=x11",
                "--socket=wayland",
                "--socket=pulseaudio",
                "--device=dri",
                "--share=network",
                "--filesystem=home",
                "--filesystem=xdg-documents",
                "--talk-name=org.freedesktop.Notifications",
                "--talk-name=org.gnome.SessionManager",
                "--talk-name=org.kde.StatusNotifierWatcher",
                "--system-talk-name=org.freedesktop.UPower"
            ],
            "modules": [
                {
                    "name": "python3-pyttsx3",
                    "buildsystem": "simple",
                    "build-commands": [
                        "pip3 install --verbose --exists-action=i --no-index --find-links=\"file://${PWD}\" --prefix=${FLATPAK_DEST} \"pyttsx3\" --no-build-isolation"
                    ],
                    "sources": [
                        {
                            "type": "file",
                            "url": "https://files.pythonhosted.org/packages/source/p/pyttsx3/pyttsx3-2.90.tar.gz",
                            "sha256": "917dc0b4e7d4e4a9b7ad8a98ddd79b60d0c6f4c97d75c5fcf2ed889a94b5e6d9"
                        }
                    ]
                },
                {
                    "name": "accessmate",
                    "buildsystem": "simple",
                    "build-commands": [
                        "install -Dm755 src/main_desktop_comprehensive.py /app/bin/accessmate",
                        "cp -r src /app/share/accessmate/",
                        "install -Dm644 accessmate.desktop /app/share/applications/com.accessmate.AccessMate.desktop",
                        "install -Dm644 src/icon.png /app/share/icons/hicolor/256x256/apps/com.accessmate.AccessMate.png"
                    ],
                    "sources": [
                        {
                            "type": "dir",
                            "path": "."
                        }
                    ]
                }
            ]
        }
        
        manifest_path = self.project_root / "com.accessmate.AccessMate.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
            
        print("✅ Created Flatpak manifest")
        return str(manifest_path)
        
    def create_store_metadata(self):
        """Create Linux distribution metadata"""
        metadata_dir = self.project_root / "store_metadata" / "linux"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # Package descriptions
        descriptions = {
            "short": "Complete accessibility solution for Linux",
            "long": """AccessMate transforms your Linux desktop into a comprehensive accessibility powerhouse, designed for users who need enhanced digital access.

🌟 NATIVE LINUX INTEGRATION
Built specifically for Linux distributions, AccessMate integrates seamlessly with GNOME, KDE, XFCE, and other desktop environments, working perfectly with existing accessibility services.

✨ POWERFUL FEATURES:
• Advanced screen reading with natural voice synthesis
• Real-time text recognition and OCR
• Voice commands and speech-to-text
• High contrast themes and font scaling
• Audio descriptions for visual content
• Keyboard navigation optimization
• Multi-language support with system integration

🎯 DESIGNED FOR:
• Users with visual impairments using Orca screen reader
• People with motor challenges using on-screen keyboards
• Those with hearing difficulties needing visual feedback
• Cognitive accessibility support with simplified interfaces
• Anyone seeking enhanced Linux accessibility

🔒 PRIVACY & SECURITY:
• All processing happens locally on your system
• No data sent to external servers
• Open source components where possible
• Transparent privacy practices

🌍 ACCESSIBILITY FIRST:
AccessMate follows accessibility standards and integrates with AT-SPI, ensuring perfect compatibility with your existing accessibility workflow on Linux.

Perfect for users of Ubuntu, Fedora, openSUSE, Debian, Arch Linux, and other distributions."""
        }
        
        # Write descriptions
        (metadata_dir / "short_description.txt").write_text(descriptions["short"])
        (metadata_dir / "long_description.txt").write_text(descriptions["long"])
        
        # Package information
        package_info = {
            "name": "accessmate",
            "version": self.version,
            "homepage": "https://www.accessmate.com",
            "bugtracker": "https://github.com/accessmate/accessmate/issues",
            "repository": "https://github.com/accessmate/accessmate",
            "license": "Proprietary",
            "maintainer": {
                "name": "AccessMate Team",
                "email": "support@accessmate.com"
            },
            "categories": [
                "Accessibility",
                "AudioVideo", 
                "Office",
                "Productivity",
                "Utility"
            ],
            "keywords": [
                "accessibility", "screen-reader", "voice", "speech", 
                "disability", "assistive", "inclusive", "linux"
            ]
        }
        
        (metadata_dir / "package_info.json").write_text(json.dumps(package_info, indent=2))
        
        print("✅ Created Linux distribution metadata")
        
    def build(self):
        """Main Linux build process"""
        print("🐧 Starting Linux distribution build process...")
        
        if not self.prepare_environment():
            return False
            
        desktop_file = self.create_desktop_file()
        self.create_store_metadata()
        
        # Build packages
        results = {}
        
        # AppImage
        print("\n📦 Building AppImage...")
        appimage = self.build_appimage()
        if appimage:
            results["appimage"] = appimage
            
        # DEB package
        print("\n📦 Building DEB package...")
        deb = self.create_deb_package()
        if deb:
            results["deb"] = deb
            
        # RPM package  
        print("\n📦 Building RPM package...")
        rpm = self.create_rpm_package()
        if rpm:
            results["rpm"] = rpm
            
        # Flatpak manifest
        print("\n📦 Creating Flatpak manifest...")
        flatpak = self.create_flatpak_manifest()
        if flatpak:
            results["flatpak"] = flatpak
            
        # Summary
        print("\n🎉 Linux distribution build completed!")
        print(f"📄 Desktop file: {desktop_file}")
        
        for package_type, path in results.items():
            print(f"📦 {package_type.upper()}: {path}")
            
        print(f"📝 Metadata: {self.project_root}/store_metadata/linux/")
        
        print("\n📋 Distribution Instructions:")
        if "appimage" in results:
            print("• AppImage: Distribute directly or upload to AppImageHub")
        if "deb" in results:
            print("• DEB: Upload to Ubuntu PPA or Debian repository")
        if "rpm" in results:
            print("• RPM: Submit to Fedora/openSUSE repositories") 
        if "flatpak" in results:
            print("• Flatpak: Submit to Flathub for distribution")
            
        return len(results) > 0

if __name__ == "__main__":
    builder = LinuxDistributionBuilder(".")
    success = builder.build()
    sys.exit(0 if success else 1)