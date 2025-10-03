# Linux Distribution Testing Guide for AccessMate

This guide helps you test AccessMate packages across different Linux distributions to ensure compatibility and functionality.

## 🧪 **Testing Matrix**

### **Primary Target Distributions**
- **Ubuntu** 20.04 LTS, 22.04 LTS, 24.04 LTS
- **Debian** 11 (Bullseye), 12 (Bookworm)
- **Fedora** 38, 39, 40
- **openSUSE** Leap 15.5, Tumbleweed
- **Arch Linux** (Rolling)
- **Linux Mint** 21.x (Ubuntu-based)

### **Secondary Distributions**
- **CentOS Stream** 9
- **Rocky Linux** 9
- **Elementary OS** 7.x
- **Pop!_OS** 22.04
- **Manjaro** (Arch-based)

## 📦 **Package Testing Workflow**

### **1. AppImage Testing (Universal)**
```bash
# Download and test AppImage
chmod +x AccessMate-1.0.0-x86_64.AppImage
./AccessMate-1.0.0-x86_64.AppImage

# Test on different desktop environments
# GNOME, KDE, XFCE, LXDE, etc.
```

**Expected Results:**
- ✅ Launches without dependencies issues
- ✅ GUI appears correctly
- ✅ Audio systems work (PulseAudio/ALSA)
- ✅ File access permissions work
- ✅ Desktop integration (if available)

### **2. Debian Package Testing**
```bash
# Ubuntu/Debian/Mint
sudo dpkg -i accessmate_1.0.0_amd64.deb
sudo apt-get install -f  # Fix any dependency issues

# Test installation
accessmate --version
accessmate --help

# Test desktop integration
ls /usr/share/applications/*accessmate*
```

**Expected Results:**
- ✅ Installs without dependency conflicts
- ✅ Desktop entry appears in applications menu
- ✅ Icon displays correctly
- ✅ Uninstalls cleanly with `sudo apt remove accessmate`

### **3. Flatpak Testing**
```bash
# Install Flatpak (if not already installed)
sudo apt install flatpak  # Ubuntu/Debian
sudo dnf install flatpak  # Fedora
sudo pacman -S flatpak    # Arch

# Add Flathub repository
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Build and install local Flatpak
flatpak-builder build-dir com.accessmate.app.json --force-clean
flatpak-builder --user --install --force-clean build-dir com.accessmate.app.json

# Test launch
flatpak run com.accessmate.app
```

**Expected Results:**
- ✅ Builds without errors
- ✅ Sandbox permissions work correctly
- ✅ Audio/microphone access granted
- ✅ File system access appropriate

## 🖥️ **Desktop Environment Testing**

### **GNOME (Ubuntu, Fedora default)**
- Test with Wayland and X11 sessions
- Check accessibility integration (Orca compatibility)
- Verify notification system works
- Test with different themes (light/dark)

### **KDE Plasma (openSUSE, Kubuntu)**
- Test with Plasma desktop integration
- Check with KDE accessibility tools
- Verify system tray integration
- Test with different Plasma themes

### **XFCE (Xubuntu, Mint XFCE)**
- Test with lightweight desktop environment
- Check resource usage
- Verify basic functionality works
- Test with XFCE accessibility features

### **Other DEs**
- **LXDE/LXQt**: Basic functionality test
- **MATE**: Compatibility with MATE accessibility
- **Cinnamon**: Linux Mint Cinnamon edition
- **Budgie**: Solus/Ubuntu Budgie

## 🔧 **Automated Testing Script**

Create this script to automate basic testing:

```bash
#!/bin/bash
# test_linux_package.sh - Automated AccessMate testing

echo "🧪 AccessMate Linux Package Testing"
echo "==================================="

# System information
echo "Distribution: $(lsb_release -d 2>/dev/null | cut -f2 || cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "Kernel: $(uname -r)"
echo "Desktop: $XDG_CURRENT_DESKTOP"
echo "Session: $XDG_SESSION_TYPE"
echo ""

# Test 1: AppImage
if [ -f "AccessMate-1.0.0-x86_64.AppImage" ]; then
    echo "Testing AppImage..."
    chmod +x AccessMate-1.0.0-x86_64.AppImage
    timeout 10 ./AccessMate-1.0.0-x86_64.AppImage --version && echo "✅ AppImage works" || echo "❌ AppImage failed"
fi

# Test 2: Debian package
if [ -f "accessmate_1.0.0_amd64.deb" ]; then
    echo "Testing Debian package..."
    if command -v dpkg >/dev/null 2>&1; then
        dpkg -I accessmate_1.0.0_amd64.deb && echo "✅ Package info readable" || echo "❌ Package info failed"
    fi
fi

# Test 3: Desktop integration
echo "Testing desktop integration..."
if [ -f "/usr/share/applications/com.accessmate.app.desktop" ] || [ -f "$HOME/.local/share/applications/com.accessmate.app.desktop" ]; then
    echo "✅ Desktop entry found"
else
    echo "❌ Desktop entry not found"
fi

# Test 4: Dependencies
echo "Testing dependencies..."
python3 -c "import tkinter; print('✅ Tkinter available')" 2>/dev/null || echo "❌ Tkinter missing"
python3 -c "import sqlite3; print('✅ SQLite available')" 2>/dev/null || echo "❌ SQLite missing"

# Test 5: Audio system
echo "Testing audio system..."
if command -v pulseaudio >/dev/null 2>&1 || pgrep -x pulseaudio >/dev/null; then
    echo "✅ PulseAudio detected"
elif command -v pipewire >/dev/null 2>&1 || pgrep -x pipewire >/dev/null; then
    echo "✅ PipeWire detected"
else
    echo "⚠️  No audio system detected"
fi

echo ""
echo "Testing complete. Check results above."
```

## 📋 **Test Checklist**

### **Basic Functionality**
- [ ] Application launches without errors
- [ ] GUI appears with correct layout
- [ ] All menu items are accessible
- [ ] Settings can be opened and modified
- [ ] Application closes properly

### **Accessibility Features**
- [ ] Text-to-speech works
- [ ] Speech recognition functions
- [ ] Keyboard shortcuts respond
- [ ] High contrast mode works
- [ ] Screen reader compatibility (if available)

### **System Integration**
- [ ] Desktop entry appears in application menu
- [ ] Icon displays correctly in menu and window
- [ ] File associations work (if applicable)
- [ ] Notification system integration
- [ ] System tray integration (if implemented)

### **Resource Usage**
- [ ] Memory usage reasonable (<500MB at startup)
- [ ] CPU usage low when idle
- [ ] No memory leaks during extended use
- [ ] Clean shutdown releases resources

### **Audio System**
- [ ] Microphone access works
- [ ] Speaker output functions
- [ ] Audio settings can be changed
- [ ] Multiple audio devices supported
- [ ] Latency acceptable for speech recognition

## 🚨 **Common Issues and Solutions**

### **AppImage Issues**
- **FUSE not available**: Use `--appimage-extract-and-run`
- **Permission denied**: `chmod +x` the AppImage file
- **Missing libraries**: Check with `ldd` command

### **Debian Package Issues**
- **Dependency conflicts**: Use `apt-get install -f`
- **Architecture mismatch**: Ensure amd64 package on 64-bit system
- **Repository conflicts**: May need to resolve manually

### **Flatpak Issues**
- **Sandbox permissions**: Check Flatpak permissions with Flatseal
- **Runtime missing**: Install required Flatpak runtimes
- **Build failures**: Check build dependencies

### **Audio Issues**
- **No microphone**: Check PulseAudio/PipeWire configuration
- **No sound output**: Verify audio system and permissions
- **Crackling audio**: Adjust buffer sizes in audio configuration

## 📊 **Test Results Template**

Create a test results file for each distribution:

```
AccessMate Linux Test Results
============================

Distribution: Ubuntu 22.04 LTS
Kernel: 5.15.0-x-generic
Desktop: GNOME 42
Date: 2025-10-03

Package Type: AppImage
Result: ✅ PASS
Notes: Launched successfully, all features working

Package Type: .deb
Result: ✅ PASS  
Notes: Installed cleanly, desktop integration working

Package Type: Flatpak
Result: ⚠️  PARTIAL
Notes: Builds successfully, microphone permission issue

Overall Rating: 8/10
Recommended for production: YES
```

## 🎯 **Testing Priority**

### **High Priority (Must Test)**
1. Ubuntu 22.04 LTS (most popular)
2. Fedora 39 (latest stable)
3. AppImage on various distributions

### **Medium Priority (Should Test)**
4. Debian 12 Stable
5. openSUSE Leap 15.5
6. Linux Mint 21.x

### **Low Priority (Nice to Test)**
7. Arch Linux
8. Other derivatives

Testing on the high-priority distributions will cover ~80% of Linux desktop users.