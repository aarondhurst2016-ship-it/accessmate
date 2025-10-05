[Setup]
AppName=AccessMate
AppVersion=1.0.0
AppVerName=AccessMate 1.0.0
AppPublisher=AccessMate Team
AppPublisherURL=https://accessmate.app
AppSupportURL=https://accessmate.app/support
AppUpdatesURL=https://accessmate.app/updates
AppComments=Comprehensive Accessibility Assistant
AppCopyright=Copyright (C) 2025 AccessMate Team
DefaultDirName={autopf}\AccessMate
DefaultGroupName=AccessMate
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.md
OutputDir=dist\installers
OutputBaseFilename=AccessMate-Setup-v1.0.0-Windows
SetupIconFile=src\accessmate_logo.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DisableReadyMemo=no
DisableFinishedPage=no
PrivilegesRequired=lowest
ArchitecturesAllowed=x64 arm64
ArchitecturesInstallIn64BitMode=x64 arm64
UninstallDisplayIcon={app}\AccessMate.exe
UninstallDisplayName=AccessMate - Accessibility Assistant
VersionInfoVersion=1.0.0.0
VersionInfoProductName=AccessMate
VersionInfoProductTextVersion=1.0.0
VersionInfoDescription=Comprehensive Accessibility Assistant
VersionInfoCopyright=Copyright (C) 2025 AccessMate Team
VersionInfoCompany=AccessMate Team

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl" 
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startmenuicon"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "autostart"; Description: "Start AccessMate with Windows (accessibility)"; GroupDescription: "Accessibility Options"

[Files]
; Main executable
Source: "dist\AccessMate.exe"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

; Icons and resources
Source: "src\accessmate_logo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu icons
Name: "{group}\AccessMate"; Filename: "{app}\AccessMate.exe"; WorkingDir: "{app}"; IconFilename: "{app}\accessmate_logo.ico"; Comment: "Launch AccessMate Accessibility Assistant"; Tasks: startmenuicon
Name: "{group}\{cm:UninstallProgram,AccessMate}"; Filename: "{uninstallexe}"; Comment: "Uninstall AccessMate"; Tasks: startmenuicon

; Desktop icon
Name: "{autodesktop}\AccessMate"; Filename: "{app}\AccessMate.exe"; WorkingDir: "{app}"; IconFilename: "{app}\accessmate_logo.ico"; Comment: "AccessMate - Accessibility Assistant"; Tasks: desktopicon

; Quick Launch icon (Windows 7 and earlier)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\AccessMate"; Filename: "{app}\AccessMate.exe"; WorkingDir: "{app}"; IconFilename: "{app}\accessmate_logo.ico"; Comment: "AccessMate Quick Launch"; Tasks: quicklaunchicon

[Registry]
; Add to Windows startup (optional)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "AccessMate"; ValueData: "{app}\AccessMate.exe"; Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\AccessMate.exe"; Description: "{cm:LaunchProgram,AccessMate}"; Flags: nowait postinstall skipifsilent