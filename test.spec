# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import copy_metadata

datas = []
hiddenimports = ['qt5_tools']
datas += copy_metadata('pyqt5_plugins')
datas += copy_metadata('qt5_tools')
datas += copy_metadata('qt5_applications')
hiddenimports += collect_submodules('qt5_applications')
hiddenimports += collect_submodules('pyqt5_plugins')


block_cipher = None


a = Analysis(['test.py'],
             pathex=['C:\\Users\\achraf\\Documents\\gestion_absences'],
             binaries=[],
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='test')
