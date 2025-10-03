; Inno Setup Script for AccessMate Support Admin Tool

[Setup]
AppName=AccessMate Support Admin Tool
AppVersion=1.0
DefaultDirName={commonpf}\AccessMate\admin
DefaultGroupName=AccessMate Admin
OutputDir=dist
OutputBaseFilename=AccessMateAdminSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\support_admin-tool.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AccessMate Support Admin Tool"; Filename: "{app}\support_admin-tool.exe"

[Run]
Filename: "{app}\support_admin-tool.exe"; Description: "Launch AccessMate Support Admin Tool"; Flags: nowait postinstall skipifsilent