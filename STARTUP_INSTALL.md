# Desktop Startup & Hard Install Instructions

## Windows
1. **Startup Shortcut**:
   - Copy a shortcut to your EXE or script into `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`.
   - Example PowerShell:
     ```powershell
     $source = "C:\Users\aaron\Talkback app\dist\TalkbackAssistant.exe"
   $source = "C:\Users\aaron\Talkback app\dist\AccessMate.exe"
     $shortcut = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TalkbackAssistant.lnk"
   $shortcut = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\AccessMate.lnk"
     $ws = New-Object -ComObject WScript.Shell
     $s = $ws.CreateShortcut($shortcut)
     $s.TargetPath = $source
     $s.Save()
     ```
2. **Hard Install**:
   - Use PyInstaller to build an EXE.
   - Copy to `C:\Program Files\TalkbackAssistant`.
      - Copy to `C:\Program Files\AccessMate`.
   - Optionally create an installer (Inno Setup, NSIS).

## macOS
1. **Startup**:
   - Create a `~/Library/LaunchAgents/com.talkbackassistant.plist` file to run your app at login.
      - Create a `~/Library/LaunchAgents/com.accessmate.plist` file to run your app at login.
2. **Hard Install**:
   - Build a `.app` bundle (PyInstaller, py2app).
   - Copy to `/Applications`.

## Linux
1. **Startup**:
   - Add a `.desktop` file to `~/.config/autostart/`.
2. **Hard Install**:
   - Build AppImage or install to `/opt/TalkbackAssistant`.
      - Build AppImage or install to `/opt/AccessMate`.

# Mobile Startup & Hard Install Instructions

## Android (Kivy)
1. **Auto-start**:
   - Use Kivy's `android` module or a plugin to request `RECEIVE_BOOT_COMPLETED` permission and start a background service.
   - Example (add to `buildozer.spec`):
     ```
     android.permissions = RECEIVE_BOOT_COMPLETED
     android.service = myservice.py
     ```
2. **Hard Install**:
   - Build APK and install via Play Store or ADB.

## iOS
- Auto-start is not allowed by Apple. User must launch the app manually.
- Use background modes for limited tasks (audio, location, etc).
- Hard install via App Store.

# Note
- For true background operation, implement a service/daemon for desktop and Android.
- For installers, see your README for PyInstaller and packaging steps.
