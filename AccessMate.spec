# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\aaron\\accessmate\\src\\main_desktop.py'],
    pathex=['C:\\Users\\aaron\\accessmate\\src'],
    binaries=[],
    datas=[('C:\\Users\\aaron\\accessmate\\src', 'src')],
    hiddenimports=['pyttsx3.drivers', 'pyttsx3.drivers.sapi5', 'pygame.mixer', 'tkinter.messagebox', 'tkinter.filedialog', 'PIL.Image', 'PIL.ImageTk', 'requests.adapters', 'urllib3.util.retry', 'googletrans', 'googletrans.client', 'googletrans.constants', 'googletrans.models', 'gtts', 'gtts.tts', 'gtts.lang', 'httpx', 'httpcore', 'h11', 'sniffio', 'certifi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AccessMate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='C:\\Users\\aaron\\AppData\\Local\\Temp\\tmpf7szejo9.txt',
    uac_admin=True,
    icon=['C:\\Users\\aaron\\accessmate\\src\\accessmate_logo.ico'],
)
