# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainmain.py'],
    pathex=[],
    binaries=[('FlightDetails.dll', '.'), ('insert_and_delete.dll', '.'), ('manager.dll', '.'), ('manager_order.dll', '.'), ('manager_order_delete.dll', '.'), ('orderchange.dll', '.'), ('passenger.dll', '.'), ('RSA.dll', '.'), ('search_flights.dll', '.'), ('eluosi.exe', '.'), ('snake.exe', '.')],
    datas=[('../data/*', 'data'), ('../assets/*', 'assets'), ('company.csv', '.'), ('price.csv', '.'), ('..\\\\assets\\\\D315856FD459A2B52B8D781C3CFCC3D2.png', 'assets')],
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
    name='TicketManager',
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
    icon=['..\\assets\\NaiLong.ico'],
)
