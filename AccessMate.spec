# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\aaron\\accessmate\\src\\main.py'],
    pathex=['C:\\Users\\aaron\\accessmate\\src'],
    binaries=[],
    datas=[('C:\\Users\\aaron\\accessmate\\src', 'src')],
    hiddenimports=['pyttsx3.drivers', 'pyttsx3.drivers.espeak', 'pygame.mixer', 'tkinter.messagebox', 'tkinter.filedialog', 'PIL.Image', 'PIL.ImageTk', 'requests.adapters', 'urllib3.util.retry', 'gi.repository.Gtk', 'gi.repository.GLib'],
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
    name='accessmate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['linux_icons\\256x256\\accessmate.png'],
)
