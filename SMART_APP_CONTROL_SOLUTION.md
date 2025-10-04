# Windows Smart App Control Solution Guide

## 🛡️ Why is AccessMate Being Blocked?

Windows Smart App Control is a security feature that blocks applications that aren't digitally signed or recognized by Microsoft. AccessMate is currently blocked because:

1. **No Code Signing Certificate**: The executable isn't digitally signed with a trusted certificate
2. **New Application**: Smart App Control doesn't recognize AccessMate as a known safe application
3. **Security Precaution**: Windows is protecting you from potentially unsafe downloads

## ✅ Solutions (Choose One)

### Option 1: Bypass Smart App Control (Recommended)

#### Method A: Run Anyway (Easiest)
1. When Smart App Control blocks AccessMate, look for **"More info"** or **"Run anyway"** link
2. Click **"More info"** 
3. Click **"Run anyway"** button
4. AccessMate will launch and be remembered as safe

#### Method B: Temporarily Disable Smart App Control
1. Press `Win + I` to open Windows Settings
2. Go to **Privacy & Security** → **Windows Security**
3. Click **App & browser control**
4. Under **Smart App Control**, click **Settings**
5. Select **"Off"** (requires restart)
6. Restart your computer
7. Run AccessMate normally

#### Method C: Add File Exception
1. Right-click on `AccessMate.exe`
2. Select **Properties**
3. Go to **Security** tab
4. Click **"Unblock"** if available
5. Click **OK**

### Option 2: Use Microsoft Store Version (Coming Soon)

We're working on getting AccessMate approved for the Microsoft Store, which will bypass Smart App Control entirely.

### Option 3: Use Portable Version

Download the portable version that doesn't require installation and is less likely to be blocked.

## 🔒 Is AccessMate Safe?

**YES!** AccessMate is completely safe:

- ✅ **Open Source**: All code is publicly available on GitHub
- ✅ **No Malware**: Clean code focused on accessibility features
- ✅ **No Data Collection**: Doesn't send your data anywhere
- ✅ **Privacy Focused**: Works entirely offline
- ✅ **Accessibility Tool**: Designed to help users with disabilities

## 🛠️ For Advanced Users

### Verify File Integrity
You can verify the AccessMate executable hasn't been tampered with:

```powershell
# Check file hash (run in PowerShell)
Get-FileHash -Path "AccessMate.exe" -Algorithm SHA256
```

Expected hash will be provided with each release.

### Run in Sandbox Mode
Test AccessMate in Windows Sandbox first:
1. Enable Windows Sandbox in Windows Features
2. Copy AccessMate.exe to sandbox
3. Test functionality safely

## 📞 Need Help?

If you're still having issues:

1. **Check Our Documentation**: See README.md for detailed setup
2. **GitHub Issues**: Report problems at https://github.com/aarondhurst2016-ship-it/accessmate/issues
3. **Contact Support**: Email support for enterprise/commercial licenses

## 🔮 Future Plans

We're working on:
- **Code Signing Certificate**: Will eliminate Smart App Control blocks
- **Microsoft Store Version**: Automatic trust through Store
- **Enterprise Distribution**: For organizations needing signed applications
- **Portable Versions**: No-install options that bypass some restrictions

---

**Remember**: Smart App Control is trying to protect you. AccessMate is safe, but always be cautious with downloaded software from unknown sources!