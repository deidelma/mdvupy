# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for mdvupy macOS application.

Build with: uv run pyinstaller mdvupy-macos.spec
"""

from pathlib import Path
import sys

block_cipher = None

# Use the top-level main.py that imports from the package
main_script = 'main.py'

a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'markdown_it',
        'qdarktheme',
        'loguru',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='mdvupy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,  # Important for macOS file opening
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mdvupy',
)

app = BUNDLE(
    coll,
    name='mdvupy.app',
    icon=None,
    bundle_identifier='com.mdvupy.viewer',
    version='0.1.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Markdown Document',
                'CFBundleTypeRole': 'Viewer',
                'LSItemContentTypes': ['net.daringfireball.markdown'],
                'LSHandlerRank': 'Default',
                'CFBundleTypeExtensions': ['md', 'markdown', 'mdown', 'mkd', 'mkdn'],
            }
        ],
        'UTExportedTypeDeclarations': [
            {
                'UTTypeIdentifier': 'net.daringfireball.markdown',
                'UTTypeReferenceURL': 'http://daringfireball.net/projects/markdown/',
                'UTTypeDescription': 'Markdown',
                'UTTypeConformsTo': ['public.plain-text'],
                'UTTypeTagSpecification': {
                    'public.filename-extension': ['md', 'markdown', 'mdown', 'mkd', 'mkdn'],
                    'public.mime-type': ['text/markdown', 'text/x-markdown'],
                },
            }
        ],
    },
)
