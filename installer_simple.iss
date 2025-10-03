[Setup]
AppName=AccessMate
AppVersion=1.0
DefaultDirName={pf}\AccessMate
DefaultGroupName=AccessMate
UninstallDisplayIcon={app}\AccessMate.exe
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
OutputBaseFilename=AccessMateSetup

[Files]
Source: "dist\AccessMate.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "ACCESSIBILITY.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\accessmate_logo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AccessMate"; Filename: "{app}\AccessMate.exe"
Name: "{userdesktop}\AccessMate"; Filename: "{app}\AccessMate.exe"; IconFilename: "{app}\accessmate_logo.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\AccessMate.exe"; Description: "Launch AccessMate"; Flags: nowait postinstall skipifsilent