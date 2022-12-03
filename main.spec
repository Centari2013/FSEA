# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas += [('authButton.png', '/FSEA/bulk/assets/authButton.png', "DATA")]
a.datas += [('closeButton.png', '/FSEA/bulk/assets/closeButton.png', "DATA")]
a.datas += [('entry_2.png', '/FSEA/bulk/assets/entry_2.png', "DATA")]
a.datas += [('FSEAlogo.png', '/FSEA/bulk/assets/FSEAlogo.png', "DATA")]
a.datas += [('login_entry.png', '/FSEA/bulk/assets/login_entry.png', "DATA")]
a.datas += [('maximize.png', '/FSEA/bulk/assets/maximize.png', "DATA")]
a.datas += [('minimize.png', '/FSEA/bulk/assets/minimize.png', "DATA")]
a.datas += [('restore.png', '/FSEA/bulk/assets/restore.png', "DATA")]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='F-SEA Database',
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
)
