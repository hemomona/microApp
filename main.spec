# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2,glew  # 导入kivy_deps

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['D:\\code\\microAPP'],
    binaries=[],
    datas=[('data', 'data'), ('font', 'font'), ('pics', 'pics'), ('screenkv', 'screenkv'),
           ('log.conf', '.'), ('logging.log', '.'), ('Micro.kv', '.'), ('records.db', '.'), ('sql.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['discard'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='micro-GCFP',  # 主程序名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='pics\\growthcurve.ico',  # icon
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins+glew.dep_bins)],  # exe包含的一些库打包进来
    strip=False,
    upx=True,
    upx_exclude=[],
    name='microApp',  # 文件夹名
)
