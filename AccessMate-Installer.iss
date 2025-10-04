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
InfoAfterFile=SUPPORT.md
OutputDir=dist\installers
OutputBaseFilename=AccessMate-Setup-v1.0.0-Windows
SetupIconFile=src\accessmate_logo_multisize.ico
Compression=lzma2/ultra64
SolidCompression=yes
InternalCompressLevel=ultra64
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
DisableReadyMemo=no
DisableFinishedPage=no
PrivilegesRequired=lowest
ArchitecturesAllowed=x64 arm64
ArchitecturesInstallIn64BitMode=x64 arm64
MinVersion=10.0.17763
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
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "chinese"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startmenuicon"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "associatefile"; Description: "Associate with .accessmate files"; GroupDescription: "File associations"
Name: "autostart"; Description: "Start AccessMate with Windows (accessibility)"; GroupDescription: "Accessibility Options"

[Types]
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "Compact installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "main"; Description: "Core AccessMate Application"; Types: full compact custom; Flags: fixed
Name: "docs"; Description: "Documentation and Help Files"; Types: full
Name: "examples"; Description: "Example configurations"; Types: full
Name: "voice"; Description: "Enhanced Voice Recognition"; Types: full compact
Name: "ocr"; Description: "OCR and Document Reading"; Types: full

[Files]
; Main executable
Source: "dist\AccessMate.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: main

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion; Components: docs
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion; Components: main
Source: "PRIVACY.md"; DestDir: "{app}"; Flags: ignoreversion; Components: docs
Source: "SUPPORT.md"; DestDir: "{app}"; Flags: ignoreversion; Components: docs
Source: "TERMS.md"; DestDir: "{app}"; Flags: ignoreversion; Components: docs
Source: "ACCESSIBILITY.txt"; DestDir: "{app}"; Flags: ignoreversion; Components: docs

; Source code (optional)
Source: "src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: examples

; Configuration files
Source: "user_settings.json"; DestDir: "{app}"; Flags: ignoreversion; Components: main
Source: "support_messages.json"; DestDir: "{app}"; Flags: ignoreversion; Components: main

; Icons and resources
Source: "src\accessmate_logo_multisize.ico"; DestDir: "{app}"; Flags: ignoreversion; Components: main

[Icons]
; Start Menu icons
Name: "{group}\AccessMate"; Filename: "{app}\AccessMate.exe"; WorkingDir: "{app}"; IconFilename: "{app}\accessmate_logo_multisize.ico"; Comment: "Launch AccessMate Accessibility Assistant"; Tasks: startmenuicon
Name: "{group}\AccessMate Documentation"; Filename: "{app}\README.md"; Comment: "View AccessMate Documentation"; Components: docs; Tasks: startmenuicon
Name: "{group}\AccessMate Support"; Filename: "{app}\SUPPORT.md"; Comment: "Get AccessMate Support"; Components: docs; Tasks: startmenuicon
Name: "{group}\{cm:UninstallProgram,AccessMate}"; Filename: "{uninstallexe}"; Comment: "Uninstall AccessMate"; Tasks: startmenuicon

; Desktop icon
Name: "{autodesktop}\AccessMate"; Filename: "{app}\AccessMate.exe"; WorkingDir: "{app}"; IconFilename: "{app}\accessmate_logo_multisize.ico"; Comment: "AccessMate - Accessibility Assistant"; Tasks: desktopicon

; Quick Launch icon (Windows 7 and earlier)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\AccessMate"; Filename: "{app}\AccessMate.exe"; WorkingDir: "{app}"; IconFilename: "{app}\accessmate_logo_multisize.ico"; Comment: "AccessMate Quick Launch"; Tasks: quicklaunchicon

; Taskbar pin (Windows 10+) 
Name: "{userpinned}\AccessMate"; Filename: "{app}\AccessMate.exe"; WorkingDir: "{app}"; IconFilename: "{app}\accessmate_logo_multisize.ico"

[Registry]
; File association
Root: HKCR; Subkey: ".accessmate"; ValueType: string; ValueName: ""; ValueData: "AccessMateFile"; Flags: uninsdeletevalue; Tasks: associatefile
Root: HKCR; Subkey: "AccessMateFile"; ValueType: string; ValueName: ""; ValueData: "AccessMate Configuration File"; Flags: uninsdeletekey; Tasks: associatefile
Root: HKCR; Subkey: "AccessMateFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\accessmate_logo_multisize.ico"; Tasks: associatefile
Root: HKCR; Subkey: "AccessMateFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\AccessMate.exe"" ""%1"""; Tasks: associatefile

; Autostart (accessibility)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "AccessMate"; ValueData: """{app}\AccessMate.exe"" --minimized"; Flags: uninsdeletevalue; Tasks: autostart

; Application registration
Root: HKCU; Subkey: "Software\AccessMate"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\AccessMate"; ValueType: string; ValueName: "Version"; ValueData: "1.0.0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\AccessMate"; ValueType: dword; ValueName: "FirstRun"; ValueData: 1; Flags: uninsdeletekey

[Run]
; Post-install actions
Filename: "{app}\AccessMate.exe"; Parameters: "--setup-wizard"; Description: "{cm:LaunchProgram,AccessMate Setup Wizard}"; Flags: nowait postinstall skipifsilent unchecked
Filename: "{app}\AccessMate.exe"; Description: "{cm:LaunchProgram,AccessMate}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\README.md"; Description: "View README"; Flags: postinstall skipifsilent unchecked shellexec; Components: docs

[UninstallRun]
; Cleanup on uninstall
Filename: "{app}\AccessMate.exe"; Parameters: "--cleanup"; Flags: runhidden

[Code]
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;

function InitializeSetup(): Boolean;
begin
  // Check Windows version
  if not IsWindows10OrLater then
  begin
    MsgBox('AccessMate requires Windows 10 or later.', mbError, MB_OK);
    Result := False;
    Exit;
  end;
  
  Result := True;
end;

procedure InitializeWizard;
begin
  // Add custom wizard pages here if needed
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if CurPageID = wpSelectDir then
  begin
    // Validate installation directory
    if not DirExists(ExpandConstant('{app}')) then
    begin
      if not CreateDir(ExpandConstant('{app}')) then
      begin
        MsgBox('Unable to create installation directory. Please choose a different location.', mbError, MB_OK);
        Result := False;
      end;
    end;
  end;
end;

procedure DeinitializeSetup();
begin
  // Cleanup if needed
end;