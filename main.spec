# -*- mode: python -*-

block_cipher = None

# 路径修改成自己的路径
# 执行 pyinstaller -D main.spec
a = Analysis(['main.py',
  'E:\\python\\Gps\\Gui\\GpsDataModel.py',
  'E:\\python\\Gps\\Gui\\GpsDataView.py',
  'E:\\python\\Gps\\Gui\\mainWindow.py',
  'E:\\python\\Gps\\Gui\\MessageBox.py',
  'E:\\python\\Gps\\pipe\\argument.py',
  'E:\\python\\Gps\\pipe\\Setting.py',
  'E:\\python\\Gps\\Plot\\DataView.py',
  'E:\\python\\Gps\\Src\\Algorithm\\AbstractHeightFitting.py',
  'E:\\python\\Gps\\Src\\Algorithm\\accuracy_evaluation.py',
  'E:\\python\\Gps\\Src\\Algorithm\\AccuracySubStance.py',
  'E:\\python\\Gps\\Src\\Algorithm\\PolyhedralFunctions.py',
  'E:\\python\\Gps\\Src\\Algorithm\\polynomial.py',
  'E:\\python\\Gps\\Src\\Algorithm\\polynomial_line.py',
  'E:\\python\\Gps\\Src\\Algorithm\\SurfaceFitting.py',
  'E:\\python\\Gps\\Src\\DataProcess\\DataExport.py',
  'E:\\python\\Gps\\Src\\DataProcess\\DataProcessingAnalysis.py',
  'E:\\python\\Gps\\Src\\Style\\StyleSheet.py'
  ],
             pathex=['E:\\python\\Gps'],
             binaries=[],
             datas=[('E:\\python\\Gps\\Img','Img'),('E:\\python\\Gps\\resource','resource')],
             hiddenimports=[],
             hookspath=[],
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
          name='GPS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
