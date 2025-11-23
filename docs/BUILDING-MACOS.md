# Building mdvupy for macOS

This guide covers building a standalone macOS `.app` bundle with file association support for Markdown files.

## Prerequisites

- macOS 10.14 or later
- Python 3.13+
- `uv` package manager installed
- Project dependencies installed (`uv pip install -e ".[dev]"`)

## Quick Build

```bash
./build-macos.sh
```

This will:
1. Install PyInstaller
2. Clean previous builds
3. Build `mdvupy.app` in the `dist/` directory

## Manual Build

If you prefer to build manually:

```bash
# Install PyInstaller
uv pip install pyinstaller

# Build the app
uv run pyinstaller mdvupy-macos.spec

# The app will be in dist/mdvupy.app
```

## Testing the Build

### Test the app directly

```bash
open dist/mdvupy.app
```

### Test with a markdown file

```bash
open -a dist/mdvupy.app test.md
```

### Test file association

1. Copy the app to Applications:
   ```bash
   cp -r dist/mdvupy.app /Applications/
   ```

2. Right-click any `.md` file in Finder
3. Select "Get Info"
4. Under "Open with:", select `mdvupy.app`
5. Click "Change All..." to set as default for all `.md` files

### Test double-click

After setting the file association, double-clicking any `.md` file should open it in mdvupy.

## File Associations

The `mdvupy-macos.spec` configures the following file associations:

- **Extensions**: `.md`, `.markdown`, `.mdown`, `.mkd`, `.mkdn`
- **UTI**: `net.daringfireball.markdown`
- **MIME types**: `text/markdown`, `text/x-markdown`

These are registered in the app's `Info.plist` via the spec file's `info_plist` dictionary.

## How It Works

### macOS File Open Events

When a user double-clicks a `.md` file or uses "Open With":

1. macOS launches the app (or brings it to front if already running)
2. macOS sends a `QEvent.Type.FileOpen` event to the application
3. Our `MainWindow.event()` handler catches this event
4. The file path is extracted and opened via `open_document()`

This is handled by:

```python
def event(self, event: QEvent) -> bool:
    if event.type() == QEvent.Type.FileOpen:
        file_path = Path(event.file())
        self.open_document(file_path)
        return True
    return super().event(event)
```

### PyInstaller Configuration

The `mdvupy-macos.spec` file includes:

- **argv_emulation=True**: Enables macOS-style argument handling for file opening
- **CFBundleDocumentTypes**: Declares supported document types
- **UTExportedTypeDeclarations**: Defines the markdown UTI
- **bundle_identifier**: Unique app identifier (`com.mdvupy.viewer`)

## Code Signing (Optional)

For distribution outside the Mac App Store:

```bash
# Sign the app
codesign --deep --force --sign "Developer ID Application: Your Name" dist/mdvupy.app

# Verify signature
codesign --verify --verbose dist/mdvupy.app
spctl --assess --verbose dist/mdvupy.app
```

## Notarization (Optional)

For Gatekeeper approval:

```bash
# Create a zip for notarization
ditto -c -k --keepParent dist/mdvupy.app mdvupy.zip

# Submit for notarization
xcrun notarytool submit mdvupy.zip \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID" \
  --wait

# Staple the notarization ticket
xcrun stapler staple dist/mdvupy.app
```

## Creating a DMG (Optional)

For easier distribution:

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "mdvupy" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "mdvupy.app" 200 190 \
  --hide-extension "mdvupy.app" \
  --app-drop-link 600 185 \
  "mdvupy-0.1.0.dmg" \
  "dist/mdvupy.app"
```

## Troubleshooting

### App won't open

- Check console logs: `Console.app` → search for "mdvupy"
- Verify Python dependencies are bundled: `ls dist/mdvupy.app/Contents/MacOS/`

### File associations not working

- Ensure the app is in `/Applications/`
- Reset Launch Services database:
  ```bash
  /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
  ```
- Restart Finder: `killall Finder`

### Qt platform plugin error

- Ensure PySide6 and its dependencies are properly bundled
- Check that `argv_emulation=True` is set in the spec file

## Distribution Checklist

- [ ] Build app with `./build-macos.sh`
- [ ] Test opening app directly
- [ ] Test opening files via command line
- [ ] Test file association (right-click → Open With)
- [ ] Test double-click on `.md` files
- [ ] Code sign the app (if distributing)
- [ ] Notarize the app (if distributing)
- [ ] Create DMG (optional)
- [ ] Test on a clean macOS system
