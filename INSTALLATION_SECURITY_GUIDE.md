# AccessMate Installation & Security Guide

## 🛡️ Smart App Control Blocking AccessMate? Here Are Your Solutions!

Windows Smart App Control is blocking AccessMate because it's not yet digitally signed. **This is normal for new applications.** AccessMate is completely safe - here are multiple ways to install and run it:

---

## 🚀 Quick Solutions (Choose Any One)

### Option 1: Portable Version (Recommended - Easiest)
✅ **No installation required**  
✅ **Less likely to be blocked**  
✅ **Run from anywhere (USB drive, folder, etc.)**

1. Download `AccessMate_Portable.zip`
2. Extract to any folder
3. Run `AccessMate_Portable.bat` 
4. Or double-click `AccessMate.exe` directly

### Option 2: Bypass Smart App Control (Standard Version)
✅ **Full Windows integration**  
✅ **One-time setup**

**Method A: Run Anyway**
1. When Windows blocks AccessMate, click **"More info"**
2. Click **"Run anyway"** 
3. AccessMate launches and is remembered as safe

**Method B: Unblock File**
1. Right-click `AccessMate.exe` → **Properties**
2. Go to **Security** tab
3. Check **"Unblock"** if available → **OK**

**Method C: Temporary Disable (Advanced)**
1. Press `Win + I` → **Privacy & Security** → **Windows Security**
2. **App & browser control** → **Smart App Control** → **Settings**
3. Select **"Off"** → Restart computer

### Option 3: Microsoft Store Version (Coming Soon)
✅ **Automatically trusted**  
✅ **Automatic updates**  
✅ **Zero security warnings**

We're preparing AccessMate for Microsoft Store submission.

---

## 🔒 Is AccessMate Safe? (Yes!)

**AccessMate is 100% safe and legitimate:**

| ✅ **Safe** | ❌ **Why Blocked?** |
|-------------|-------------------|
| Open source code on GitHub | No digital signature yet |
| No malware, viruses, or threats | Smart App Control doesn't recognize it |
| Privacy-focused (no data collection) | New application (not in Microsoft's database) |
| Accessibility-focused features | Security precaution by Windows |
| Offline operation | We're working on code signing certificate |

---

## 📁 Available Downloads

### Regular Version
- **AccessMate.exe** - Standard Windows executable
- **AccessMate-Setup.exe** - Inno Setup installer with shortcuts
- **AccessMate.msi** - Windows Installer package

### Portable Version  
- **AccessMate_Portable.zip** - No installation required
  - Contains: `AccessMate.exe`, launcher batch file, README
  - Perfect for USB drives or temporary usage
  - Less likely to trigger security warnings

### Store Version (Future)
- **AccessMate.msix** - Microsoft Store package
- Will be automatically trusted by Windows
- One-click install from Store

---

## 🛠️ Troubleshooting

### "This app can't run on your PC"
- Try the portable version instead
- Or follow "Unblock File" steps above

### "Windows protected your PC"
- Click **"More info"** → **"Run anyway"**
- This is Smart App Control, not a virus warning

### Still having issues?
1. **Disable antivirus temporarily** and try again
2. **Run as Administrator**: Right-click → "Run as administrator"
3. **Check Windows version**: Requires Windows 10/11
4. **Download fresh copy** from official GitHub releases

---

## 🔮 Future Plans

We're working on eliminating these security warnings:

- **✅ Enhanced metadata** - Added version info and descriptions
- **🔄 Code signing certificate** - Currently being obtained
- **🔄 Microsoft Store approval** - Application in progress
- **🔄 Enterprise certificates** - For business/organization use

---

## 💡 For Advanced Users

### Verify File Integrity
```powershell
# Check file hash in PowerShell
Get-FileHash -Path "AccessMate.exe" -Algorithm SHA256
```
Hashes are provided with each GitHub release.

### Test in Windows Sandbox
1. Enable Windows Sandbox in Windows Features
2. Copy AccessMate to sandbox
3. Test safely in isolated environment

### Build from Source
```bash
git clone https://github.com/aarondhurst2016-ship-it/accessmate.git
cd accessmate
pip install -r requirements.txt
python build_windows.py
```

---

## 📞 Still Need Help?

- **📖 Documentation**: Check README.md for detailed setup
- **🐛 Report Issues**: GitHub Issues for bugs/problems  
- **📧 Contact**: Enterprise support available
- **💬 Community**: GitHub Discussions for questions

---

## 🎯 Summary

**Smart App Control is just doing its job** - protecting you from unknown software. AccessMate is completely safe, but Windows doesn't know that yet. 

**Choose your preferred solution:**
- **Quick & Easy**: Portable version (`AccessMate_Portable.zip`)
- **Standard**: Regular version + "Run anyway" when prompted
- **Future**: Microsoft Store version (automatically trusted)

**Remember**: Once you run AccessMate successfully once, Windows will remember it's safe and won't block it again!

---
*AccessMate Team - Making technology accessible for everyone* 🌟