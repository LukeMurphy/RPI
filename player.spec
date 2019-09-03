# -*- mode: python -*-

block_cipher = None


a = Analysis(['player.py'],
	         pathex=['/Users/lamshell/Documents/Dev/RPI'],
	         binaries=[],
	         datas=[('./assets', 'assets'), ('./configs', 'configs'), ('./cntrlscripts', 'cntrlscripts')],
	         hiddenimports=['numpy', 'noise'],
	         hookspath=['./pieces/workmodules/particleobjects/'],
	         runtime_hooks=['./pieces/workmodules/particleobjects/particle.py'],
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
	      name='player',
	      debug=False,
	      bootloader_ignore_signals=False,
	      strip=False,
	      upx=True,
	      console=True )
coll = COLLECT(exe,
	           a.binaries,
	           a.zipfiles,
	           a.datas,
	           strip=False,
	           upx=True,
	           name='player')
