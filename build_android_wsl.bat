@echo off
REM build_android_wsl.bat - Windows batch file for building Android APKs via WSL
REM This script builds Android APKs using Windows Subsystem for Linux

echo 🤖 AccessMate Android Build via WSL
echo =====================================
echo.

REM Check if WSL is available
wsl --status >nul 2>&1
if errorlevel 1 (
    echo ❌ WSL is not installed or not available
    echo.
    echo To install WSL, run as Administrator:
    echo   wsl --install
    echo.
    echo Or install specific Ubuntu version:
    echo   wsl --install -d Ubuntu-22.04
    echo.
    pause
    exit /b 1
)

echo ✅ WSL is available
echo.

REM Check if Ubuntu is installed
wsl -l -q | findstr -i ubuntu >nul
if errorlevel 1 (
    echo ❌ Ubuntu distribution not found in WSL
    echo.
    echo Install Ubuntu with:
    echo   wsl --install -d Ubuntu-22.04
    echo.
    pause
    exit /b 1
)

echo ✅ Ubuntu distribution found
echo.

REM Get build type (default to debug)
set BUILD_TYPE=debug
if not "%1"=="" set BUILD_TYPE=%1

echo Build Type: %BUILD_TYPE%
echo Project Path: %CD%
echo WSL Path: /mnt/c%CD:~1%
echo.

REM Check if buildozer.spec exists
if not exist "buildozer.spec" (
    echo ❌ buildozer.spec not found in current directory
    echo Make sure you're running this from the AccessMate project root
    pause
    exit /b 1
)

echo ✅ buildozer.spec found
echo.

REM Build the APK using WSL
echo 🔨 Starting Android build...
echo This may take 15-30 minutes for the first build (downloads Android SDK)
echo Subsequent builds will be much faster (2-5 minutes)
echo.

REM Convert Windows path to WSL path
set "WSL_PATH=/mnt/c%CD:C:=%"
set "WSL_PATH=%WSL_PATH:\=/%"

REM Execute buildozer in WSL
if "%BUILD_TYPE%"=="release" (
    echo Building release APK...
    wsl bash -c "cd '%WSL_PATH%' && buildozer android release"
) else (
    echo Building debug APK...
    wsl bash -c "cd '%WSL_PATH%' && buildozer android debug"
)

REM Check if build was successful
if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo.
    echo Common solutions:
    echo - Ensure WSL Ubuntu has buildozer installed: pip3 install buildozer
    echo - Check Java is installed: sudo apt install openjdk-11-jdk
    echo - Try clean build: wsl bash -c "cd '%WSL_PATH%' && buildozer android clean"
    echo.
    echo For detailed setup instructions, see WSL_ANDROID_SETUP.md
    pause
    exit /b 1
)

REM Check if APK was created
if exist "bin\*.apk" (
    echo.
    echo ✅ Build successful!
    echo.
    echo APK files created:
    dir /b bin\*.apk
    echo.
    echo APK location: %CD%\bin\
    echo.
    echo You can now:
    echo - Install on Android: adb install bin\accessmate-*.apk
    echo - Transfer to device and install manually
    echo - Upload to Google Play Store (for release builds)
) else (
    echo.
    echo ⚠️ Build completed but no APK found in bin\ folder
    echo Check the build output above for any errors
)

echo.
echo Build process complete.
pause