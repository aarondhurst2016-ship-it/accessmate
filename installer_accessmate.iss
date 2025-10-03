; Inno Setup Script for AccessMate

[Setup]
AppName=AccessMate
AppVersion=1.0
DefaultDirName={commonpf}\AccessMate
DefaultGroupName=AccessMate
OutputDir=dist
OutputBaseFilename=AccessMateSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\AccessMate.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*.*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "ACCESSIBILITY.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AccessMate"; Filename: "{app}\AccessMate.exe"
Name: "{userdesktop}\AccessMate"; Filename: "{app}\AccessMate.exe"; IconFilename: "{app}\..\src\accessmate_logo.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\AccessMate.exe"; Description: "Launch AccessMate"; Flags: nowait postinstall skipifsilent

; You must build your app with PyInstaller first:
; pyinstaller --onefile --windowed src/main.py
; Then run this script with Inno Setup Compiler.
