# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('static/assets/icons/config_icon.png', 'assets/icons'),
        ('static/assets/icons/home_icon.png', 'assets/icons'),
        ('static/assets/icons/rma_mode.png', 'assets/icons'),
        ('static/assets/data/errors.json', 'assets/data'),
        ('static/assets/commands/help.txt', 'assets/commands')
    ],
    hiddenimports=[],
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
    name='JocelineFB',
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
    icon=['static\\ico\\app.ico'],
)
