# mdvupy Development Plan

A comprehensive plan for building a Python + Qt markdown viewer with full macOS and Windows support for double-click / "Open With" file associations.

---

## Step 0 – Technology & Project Skeleton (with `uv`)

### 0.1. Install `uv` (macOS & Windows)

If you don't already have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows (PowerShell):
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```bash
uv --version
```

### 0.2. Create project with `uv init`

In the parent directory where you want `mdvupy`:

```bash
uv init --package mdvupy
cd mdvupy
```

This will create:

- `pyproject.toml`
- `src/mdvupy/__init__.py`
- `tests/` etc.

We'll customize `pyproject.toml` next.

### 0.3. Adjust layout

Ensure:

```text
mdvupy/
  src/
    mdvupy/
      __init__.py
      main.py
      app.py
      view.py
      loader.py
      links.py
      # later: toc.py, search.py, settings.py, resources/...
  tests/
    unit/
    integration/
  docs/
  README.md
  LICENSE
  pyproject.toml
```

You can create empty files now; we'll fill them in per later steps.

---

## Step 1 – Dependency & Tooling Setup with `uv`

### 1.1. Define dependencies in `pyproject.toml`

Open `pyproject.toml` and update it along these lines:

```toml
[project]
name = "mdvupy"
version = "0.1.0"
description = "Cross-platform Markdown viewer in Python + Qt"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }

dependencies = [
  "pyside6>=6.7",
  "markdown-it-py>=3.0.0",
  "pyqtdarktheme>=2.1.0",
]

[project.optional-dependencies]
dev = [
  "pytest",
  "pytest-qt",
  "ruff",
  "black",
  "mkdocs",
]

[build-system]
requires = ["hatchling>=1.22"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mdvupy"]
```

### 1.2. Create and use `uv` environment

Instead of `venv` + `pip`, we use `uv` fully:

```bash
# Create a Python 3.11 environment
uv venv --python 3.11

# Activate (macOS / bash):
source .venv/bin/activate
# On Windows PowerShell:
# .venv\Scripts\Activate.ps1
```

Or let `uv` manage it implicitly by prefixing commands with `uv run` (no manual activation needed).

### 1.3. Install dependencies with `uv`

```bash
# Install runtime + dev dependencies
uv pip install -e ".[dev]"
```

From now on, use `uv run` to execute tools:

```bash
uv run python -m mdvupy.main
uv run pytest
uv run ruff check .
uv run black src tests
```

---

## Step 2 – Minimal Qt App + Markdown View

### 2.1. Entry point

Create `src/mdvupy/main.py`:

```python
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from .app import MainWindow

def main():
    initial_file: Path | None = None
    if len(sys.argv) > 1:
        initial_file = Path(sys.argv[1])

    app = QApplication(sys.argv)
    window = MainWindow(initial_file=initial_file)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

Run (during dev):

```bash
uv run python -m mdvupy.main
# or, with a file:
uv run python -m mdvupy.main /path/to/test.md
```

### 2.2. MainWindow + pyqtdarktheme

Create `src/mdvupy/app.py`:

```python
from __future__ import annotations
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import qdarktheme

from .view import MarkdownView
from .loader import load_markdown_file

class MainWindow(QMainWindow):
    def __init__(self, initial_file: Path | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mdvupy")

        # Dark theme
        qdarktheme.setup_theme("dark")

        self._view = MarkdownView(self)
        self.setCentralWidget(self._view)

        self._create_actions()
        self._create_menus()

        if initial_file:
            self.open_document(initial_file)

    def _create_actions(self):
        self._action_open = self.menuBar().addAction("Open…")
        self._action_open.triggered.connect(self._open_dialog)

    def _create_menus(self):
        # Extend later (File/Edit/View/etc.)
        pass

    def _open_dialog(self):
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown);;All Files (*)",
        )
        if path_str:
            self.open_document(Path(path_str))

    def open_document(self, path: Path):
        try:
            text = load_markdown_file(path)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{exc}")
            return
        self._view.set_markdown(text, base_path=path.parent)
        self.setWindowTitle(f"mdvupy — {path.name}")
```

### 2.3. MarkdownView widget

Create `src/mdvupy/view.py`:

```python
from __future__ import annotations
from pathlib import Path
from PySide6.QtWidgets import QTextBrowser
from PySide6.QtCore import QUrl, Signal

from .links import classify_link, LinkType
from .loader import render_markdown_to_html

class MarkdownView(QTextBrowser):
    external_link_clicked = Signal(str)
    local_file_link_clicked = Signal(Path)
    internal_anchor_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)
        self._base_path: Path | None = None

    def set_markdown(self, text: str, base_path: Path | None = None):
        self._base_path = base_path
        html = render_markdown_to_html(text)
        self.setHtml(html)

    def set_base_path(self, path: Path | None):
        self._base_path = path

    def setSource(self, url: QUrl):  # invoked when user clicks a link
        href = url.toString()
        link_type, target = classify_link(href, base_path=self._base_path)

        if link_type is LinkType.EXTERNAL:
            self.external_link_clicked.emit(str(target))
        elif link_type is LinkType.LOCAL_FILE:
            self.local_file_link_clicked.emit(target)
        elif link_type is LinkType.INTERNAL:
            self.scrollToAnchor(str(target))
            self.internal_anchor_clicked.emit(str(target))
        else:
            super().setSource(url)
```

---

## Step 3 – Markdown Loader (Google‑style) with `markdown-it-py`

Create `src/mdvupy/loader.py`:

```python
from __future__ import annotations
from pathlib import Path
from markdown_it import MarkdownIt

md = (
    MarkdownIt("commonmark", {"html": False})
    .enable("table")
    .enable("strikethrough")
)

def load_markdown_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def render_markdown_to_html(text: str) -> str:
    body = md.render(text)
    return f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body {{
        font-family: -apple-system, system-ui, sans-serif;
        line-height: 1.5;
        padding: 1.5rem;
      }}
      h1, h2, h3, h4, h5, h6 {{
        font-weight: 600;
        margin-top: 1.5em;
      }}
      code {{
        font-family: "SF Mono", "Consolas", monospace;
      }}
      pre code {{
        display: block;
        padding: 0.75rem;
        border-radius: 4px;
      }}
      a {{
        color: #4f8cff;
        text-decoration: none;
      }}
      a:hover {{
        text-decoration: underline;
      }}
    </style>
  </head>
  <body>
    {body}
  </body>
</html>
"""
```

---

## Step 4 – Link Handling

### 4.1. Link classifier

Create `src/mdvupy/links.py`:

```python
from __future__ import annotations
from enum import Enum, auto
from pathlib import Path
from urllib.parse import urlparse

class LinkType(Enum):
    EXTERNAL = auto()
    LOCAL_FILE = auto()
    INTERNAL = auto()
    UNKNOWN = auto()

def classify_link(href: str, base_path: Path | None):
    if href.startswith("#"):
        return (LinkType.INTERNAL, href[1:])

    parsed = urlparse(href)
    if parsed.scheme in ("http", "https"):
        return (LinkType.EXTERNAL, href)

    if href.startswith("www."):
        return (LinkType.EXTERNAL, "https://" + href)

    if base_path is not None:
        return (LinkType.LOCAL_FILE, (base_path / href).resolve())

    return (LinkType.UNKNOWN, href)
```

### 4.2. Wire signals in MainWindow

Update `src/mdvupy/app.py`:

```python
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

# Add to MainWindow.__init__:
    def __init__(self, initial_file: Path | None = None, parent=None):
        # ... existing code ...
        self._view.external_link_clicked.connect(self._open_external)
        self._view.local_file_link_clicked.connect(self._open_local_file)

    def _open_external(self, url: str):
        QDesktopServices.openUrl(QUrl(url))

    def _open_local_file(self, path: Path):
        self.open_document(path)
```

---

## Step 5 – TOC, Search, Zoom, Shortcuts

### 5.1. TOC generation

- Create `toc.py` with:
  - Function `extract_toc(text: str) -> List[TOCItem]`
  - Use markdown-it-py to parse headings
  - Display in `QTreeView` or `QListWidget`
- Wire clicking TOC entries to `MarkdownView.scrollToAnchor(section_id)`

### 5.2. Search

- Use `QTextDocument::find` via `QTextBrowser.find()` methods
- Add search bar (QLineEdit + next/prev buttons)
- Highlight matches and count

### 5.3. Zoom

- Implement actions: Zoom In (Ctrl/Cmd `+`), Zoom Out (Ctrl/Cmd `-`), Reset (Ctrl/Cmd `0`)
- Use `QTextBrowser.zoomIn()` / `zoomOut()` or adjust font size

### 5.4. Keyboard shortcuts

- Open: Ctrl/Cmd+O  
- Quit: Ctrl/Cmd+Q  
- Search: Ctrl/Cmd+F  
- Zoom in/out/reset as above

Use `QAction` with `setShortcut`.

---

## Step 6 – File Association & "Open With" / Double‑click

### 6.1. Windows

- Build `.exe` with PyInstaller:

  ```bash
  uv pip install pyinstaller
  uv run pyinstaller --noconfirm --windowed --name mdvupy src/mdvupy/main.py
  ```

- Use installer (Inno Setup/NSIS) to register file associations:
  - ProgID `mdvupy.md`  
  - `HKEY_CLASSES_ROOT\.md` → `mdvupy.md`  
  - Shell open command pointing to installed exe with `"%1"`

At runtime, `sys.argv[1]` will contain the file path.

### 6.2. macOS

- Build `.app` with PyInstaller:

  ```bash
  uv pip install pyinstaller
  uv run pyinstaller --noconfirm --windowed --name mdvupy src/mdvupy/main.py
  ```

- Edit generated `Info.plist` to include `CFBundleDocumentTypes`:

  ```xml
  <key>CFBundleDocumentTypes</key>
  <array>
    <dict>
      <key>CFBundleTypeName</key>
      <string>Markdown Document</string>
      <key>CFBundleTypeRole</key>
      <string>Viewer</string>
      <key>LSItemContentTypes</key>
      <array>
        <string>net.daringfireball.markdown</string>
      </array>
      <key>LSHandlerRank</key>
      <string>Default</string>
    </dict>
  </array>
  ```

Qt on macOS translates document open events into `sys.argv` for bundled apps launched via double-click / Open With.

---

## Step 7 – Testing with `uv`

### 7.1. Unit tests

Create `tests/unit/test_links.py`:

```python
from pathlib import Path
from mdvupy.links import classify_link, LinkType

def test_internal_link():
    t, target = classify_link("#section-1", base_path=None)
    assert t is LinkType.INTERNAL
    assert target == "section-1"

def test_external_http():
    t, target = classify_link("https://example.com", base_path=None)
    assert t is LinkType.EXTERNAL

def test_external_www():
    t, target = classify_link("www.example.com", base_path=None)
    assert t is LinkType.EXTERNAL
    assert target == "https://www.example.com"

def test_local_file():
    base = Path("/docs")
    t, target = classify_link("README.md", base)
    assert t is LinkType.LOCAL_FILE
    assert target == (base / "README.md").resolve()
```

Create `tests/unit/test_loader.py`:

```python
from mdvupy.loader import render_markdown_to_html

def test_render_disables_html():
    md = "# Title\n\n<script>alert('x')</script>"
    html = render_markdown_to_html(md)
    assert "<script" not in html.lower()
```

Run:

```bash
uv run pytest
```

### 7.2. Integration tests (with pytest-qt)

Create `tests/integration/test_markdown_view.py`:

```python
from pathlib import Path
from mdvupy.view import MarkdownView

def test_internal_link_scrolls_anchor(qtbot, tmp_path):
    view = MarkdownView()
    qtbot.addWidget(view)

    md = "# Title\n\n[Go](#title)"
    view.set_markdown(md, base_path=tmp_path)

    view.setSource("title")
    # Verify no crash; advanced: check scroll position
```

---

## Step 8 – Documentation

### 8.1. README.md

Cover:

- What mdvupy is  
- Supported platforms (macOS, Windows)  
- Features (TOC, search, zoom, open external links, local files, internal anchors)  
- Install from source with `uv`  
- How to run (CLI + GUI)  
- Known limitations  

### 8.2. BUILDING.md

Explain:

- Prerequisites: Python 3.11+, uv installed  
- `uv venv --python 3.11`  
- `uv pip install -e ".[dev]"`  
- `uv run python -m mdvupy.main`  
- Running tests: `uv run pytest`

### 8.3. PACKAGING.md

- **macOS:**
  - Using `uv run pyinstaller --windowed --name mdvupy src/mdvupy/main.py`
  - Editing `Info.plist` for document types
  - Notarization / code signing

- **Windows:**
  - Using `uv run pyinstaller --windowed --name mdvupy src/mdvupy/main.py`
  - Creating installer (Inno Setup or NSIS) with `.md` file associations

### 8.4. Architecture & design docs

- `docs/architecture.md`: Component overview (app, view, loader, links, TOC, search)  
- `docs/design-decisions.md`: Why Python+Qt, markdown-it-py, QTextBrowser, etc.

### 8.5. THIRD_PARTY_LICENSES.md

List all dependencies with:

- PySide6 (LGPL 3 / Qt license)  
- markdown-it-py (MIT)  
- pyqtdarktheme (MIT)  
- pytest, pytest-qt, etc.

Include name, version, license, URL, and license texts as necessary.

---

## Step 9 – Polishing & Parity with mdview

Match mdview feature set:

- Remember last opened file / recent files (use `QSettings`)
- Optional: sidebar TOC with resizable splitter
- Zoom and search behavior aligned with mdview
- External links use default browser
- Local file links open in same window
- Support `.md` and `.markdown` extensions
- Command line help: `uv run python -m mdvupy.main --help` (use `argparse`)

---

## Step 10 – Release

- Tag version (e.g., `v0.1.0`)  
- Build macOS `.app` + `.dmg` (PyInstaller + create-dmg)  
- Build Windows `.exe` + installer  
- Publish releases on GitHub with checksums and changelog

---

## Technology Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.11+ | Cross-platform development |
| GUI Framework | PySide6 | Qt bindings (LGPL-friendly) |
| Package Manager | uv | Fast Python package management |
| Markdown Parser | markdown-it-py | CommonMark-compliant, Google-style |
| Theming | pyqtdarktheme | Dark/light theme support |
| Testing | pytest + pytest-qt | Unit and integration tests |
| Linting | ruff + black | Code quality and formatting |
| Packaging | PyInstaller | Standalone executables |
| Docs | mkdocs | Documentation generation |

---

## Key Advantages Over Tauri (mdview)

1. **File associations work natively** on both macOS and Windows
2. **Double-click / "Open With" fully supported** via standard Qt mechanisms
3. **No OS-level event handling gaps** - Qt exposes file open events properly
4. **Simpler packaging** - single PyInstaller command per platform
5. **Easier debugging** - Python stack traces vs Rust compilation errors
6. **Faster iteration** - no Rust compilation time during development

---

## Next Steps

To begin implementation:

1. Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Initialize project: `uv init --package mdvupy`
3. Set up dependencies in `pyproject.toml`
4. Create minimal working app (Steps 1-4)
5. Add features incrementally (Steps 5-9)
6. Package and test file associations (Step 6)
7. Polish and release (Step 10)
