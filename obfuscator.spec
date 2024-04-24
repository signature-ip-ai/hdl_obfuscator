#!/bin/env python3
# -*- mode: python ; coding: utf-8 -*-
import os
import subprocess

def _generateGrammarFiles(grammarFilePath:str) -> None:
    targetPath = os.path.join('src','systemverilog')
    command = {f'antlr4 -Dlanguage=Python3 {os.path.abspath(grammarFilePath)} -o {targetPath}'}
    print(f'Generating ANTLR4.13.1 grammar files for: {grammarFilePath} at {targetPath}')
    subprocess.run(command, shell = True, check = True)

def _getInternalResourcePaths(dirPath:str) -> list:
    filePaths = list()
    for root, _, files in os.walk(dirPath):
        for file in files:
            if os.path.splitext(file)[1] == '.g4':
                newPath = os.path.relpath(os.path.join(root, os.path.dirname(file), file), os.getcwd())
                if newPath not in filePaths:
                    filePaths.append(newPath)
                    print(f'Adding {newPath} to grammar list')

    return filePaths

def _processGrammarDir(internalDirList:list) -> None:
    for dir in internalDirList:
        for path in _getInternalResourcePaths(dir):
            _generateGrammarFiles(path)


block_cipher = None

internal_resources = [
    'grammar'
]

_processGrammarDir(internal_resources)

a = Analysis(['src/obfuscator.py'],
             pathex=['src'],
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
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='obfuscator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
