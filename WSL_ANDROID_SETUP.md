# Quick WSL Setup for Android Builds

## 1. Install WSL2

```powershell
# Run as Administrator in PowerShell
wsl --install
```

**Or install specific Ubuntu version:**
```powershell
wsl --install -d Ubuntu-22.04
```

## 2. Setup Development Environment in WSL

```bash
# Update package manager
sudo apt update && sudo apt upgrade -y

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-venv git

# Install Java (required for Android builds)
sudo apt install -y openjdk-11-jdk

# Install Android SDK dependencies
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y zip unzip wget curl

# Install buildozer and Android dependencies
pip3 install buildozer python-for-android kivy cython

# Add to PATH (add to ~/.bashrc for permanent)
export PATH=$PATH:~/.local/bin
```

## 3. Access Your Project

```bash
# Navigate to your Windows project
cd /mnt/c/Users/aaron/accessmate

# Verify files are accessible
ls -la buildozer.spec
```

## 4. Build Android APK

```bash
# First build (will download Android SDK/NDK - takes time)
buildozer android debug

# Subsequent builds
buildozer android debug

# Clean build if needed
buildozer android clean
buildozer android debug
```

## 5. Access Built APK

The APK will be created in:
- **WSL Path**: `/mnt/c/Users/aaron/accessmate/bin/`
- **Windows Path**: `C:\Users\aaron\accessmate\bin\`

## Common Issues & Solutions

### Permission Issues
```bash
# Fix permissions if needed
sudo chown -R $USER:$USER /mnt/c/Users/aaron/accessmate/.buildozer
```

### Java Version Issues
```bash
# Check Java version
java -version

# Set JAVA_HOME if needed
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Build Failures
```bash
# Clean everything and rebuild
buildozer distclean
buildozer android debug
```

## Quick Test Command

Run this single command after WSL setup:
```bash
cd /mnt/c/Users/aaron/accessmate && buildozer android debug
```

## Automation

Create a Windows batch file to streamline the process:
```batch
@echo off
echo Building Android APK via WSL...
wsl -d Ubuntu-22.04 bash -c "cd /mnt/c/Users/aaron/accessmate && buildozer android debug"
echo APK build complete! Check bin/ folder.
pause
```

## Development Workflow

1. **Edit code on Windows** (VS Code, PyCharm, etc.)
2. **Build APK in WSL** (`buildozer android debug`)
3. **Test APK on device** (transfer from `bin/` folder)
4. **Repeat** (code changes are automatically visible in WSL)

## Performance Tips

- **First build**: 15-30 minutes (downloads Android SDK)
- **Subsequent builds**: 2-5 minutes
- **Use SSD**: WSL performs much better on SSD drives
- **Allocate RAM**: Increase WSL memory limit in `.wslconfig`