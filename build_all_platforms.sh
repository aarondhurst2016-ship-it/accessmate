# build_all_platforms.sh
# Build script for Talkback Assistant (Windows, macOS, Linux, Android, iOS)

# Windows (PyInstaller)
echo "Building Windows executable..."
pyinstaller --onefile --windowed src/gui.py

# macOS/Linux (PyInstaller)
echo "Building macOS/Linux executable..."
pyinstaller --onefile --windowed mac_linux_entry.py

# Android (Buildozer)
echo "Building Android APK..."
if [ ! -f buildozer.spec ]; then
    buildozer init
fi
sed -i 's/^source.*$/source = mobial\/gui.py/' buildozer.spec
buildozer -v android debug

# iOS (Kivy-ios)
echo "Building iOS app..."
kivy-ios toolchain create talkback-ios ios_entry.py
kivy-ios toolchain build talkback-ios

# Instructions
# - Windows/macOS/Linux output in dist/
# - Android APK in bin/
# - iOS Xcode project in kivy-ios/app/talkback-ios/
