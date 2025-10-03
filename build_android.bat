@echo off
REM build_android.bat - Windows batch file for Android builds
REM This is a Windows-compatible version of build_android.sh

echo 🤖 AccessMate Android Build Script (Windows)
echo ==============================================

REM Configuration
set APP_NAME=AccessMate
set VERSION=1.0.0
set BUILD_TYPE=debug
if not "%1"=="" set BUILD_TYPE=%1

echo Build Type: %BUILD_TYPE%
echo Version: %VERSION%
echo.

REM Check if buildozer is installed
echo Checking buildozer installation...
python -c "import buildozer" 2>nul
if errorlevel 1 (
    echo Installing buildozer...
    pip install buildozer
    echo Buildozer installed successfully
) else (
    echo ✅ Buildozer is already installed
)

REM Check if buildozer.spec exists
if not exist "buildozer.spec" (
    echo ❌ buildozer.spec not found
    echo Run 'buildozer init' first to create configuration
    pause
    exit /b 1
)

echo ✅ buildozer.spec found

REM Check mobial directory
if not exist "mobial" (
    echo ❌ mobial directory not found
    echo The mobial directory should contain the mobile version
    pause
    exit /b 1
)

echo ✅ mobial directory found

REM Install dependencies
echo.
echo Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
)
if exist "mobial\requirements.txt" (
    pip install -r mobial\requirements.txt
)

REM Install additional buildozer dependencies
pip install cython

REM Create directories
if not exist "bin" mkdir bin
if not exist ".buildozer" mkdir .buildozer

echo.
echo Starting Android build...
echo This may take 15-30 minutes on first build...
echo.

REM Build APK
if "%BUILD_TYPE%"=="release" (
    echo Building release APK...
    python -m buildozer android release
) else (
    echo Building debug APK...
    python -m buildozer android debug
)

REM Check if build was successful
if exist "bin\*.apk" (
    echo.
    echo ✅ Android APK build completed successfully!
    echo.
    echo APK files created in bin\ directory:
    dir bin\*.apk
    echo.
    echo Installation Instructions:
    echo 1. Enable 'Unknown Sources' in Android Settings
    echo 2. Transfer APK to Android device
    echo 3. Install APK by tapping it or using: adb install bin\*.apk
    echo 4. Grant accessibility permissions in Android Settings
    echo.
) else (
    echo.
    echo ❌ Android APK build failed
    echo Check the output above for errors
    echo.
    echo Common issues:
    echo - Java JDK not installed or not in PATH
    echo - Insufficient disk space (need ~10GB)
    echo - Internet connection issues (for downloading Android SDK/NDK)
    echo.
)

echo.
echo Build process completed.
pause