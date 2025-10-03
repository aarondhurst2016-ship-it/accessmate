# Talkback Assistant

A modular Python project for accessibility, speech, and integrations.

## Legal & Support

- [Privacy Policy](PRIVACY.md)
- [Terms of Use](TERMS.md)
- [Support](SUPPORT.md)


## Project Structure

- All main modules are in `src/`
- Dependencies are listed in `requirements.txt`
- Copilot instructions are in `.github/copilot-instructions.md`

## Requirements

See `requirements.txt` for all dependencies.  
Install them with:

```sh
pip install -r requirements.txt
```

## Build Instructions (Windows)

1. Install all dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Build the executable with PyInstaller:
    ```sh
    pyinstaller --onefile --windowed src/main.py
    ```

3. Build the Windows installer with Inno Setup:
    ```powershell
    & "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Users\aaron\Talkback app\installer.iss"
    ```

## Cross-Platform Build Instructions

### Desktop (Windows/macOS/Linux)
- Use `build_desktop.sh` to build executables for each platform with PyInstaller:
    ```sh
    bash build_desktop.sh
    ```
- For Windows, you can package the executable with Inno Setup using `installer.iss`.

### Android
- Use Buildozer to package the Kivy app as an APK:
    ```sh
    buildozer -v android debug
    ```
- See `buildozer.spec` for configuration.

### iOS
- See `kivy-ios-instructions.txt` for step-by-step instructions to build and deploy on iOS devices.

## Usage

Run the app:
```sh
python src/main.py
```

Or launch the built executable from the `dist` folder.

## Updating

- Update `.github/copilot-instructions.md` as you add new features or modules.
- Add new dependencies to `requirements.txt`.

## Accessibility

- Accessibility features are implemented in `src/accessibility.py`.
- Speech features use `gtts`, `pyttsx3`, and `speechrecognition`.

## Integrations

- Integrations for email, smart home, calendar, and more are scaffolded in `src/`.

## Notes
- Some features may require platform-specific permissions or setup (e.g., microphone, internet).
- For mobile builds, test on real devices for best results.
