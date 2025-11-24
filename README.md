# mdvupy

A lightweight cross-platform Markdown viewer built with Python and Qt.

## Overview

**mdvupy** is a fast, native Markdown viewer that provides:
- Clean, distraction-free reading experience
- Table of Contents (TOC) navigation
- Full-text search with highlighting
- Zoom controls
- File history with back/forward navigation
- External link handling
- Support for tables and strikethrough

This project was developed as an experiment in LLM-assisted coding. The code, tests, and documentation were implemented using LLMs. The plan was created using GPT-4 from OpenAI. The code was primarily generated using Claude Sonnet 4.5 from Anthropic.

## Features

- **Cross-Platform**: Although intended for macOS, also runs on Windows and Linux
- **Python + Qt**: Built with PySide6 for native look and feel
- **TOC Navigation**: Automatically generated table of contents from Markdown headings
- **Search**: Find text within documents with next/previous navigation
- **Zoom**: Adjust text size for comfortable reading
- **File History**: Navigate between recently opened files with back/forward buttons (up to 20 files)
- **Persistent History**: File history saved across sessions
- **Link Handling**: External links open in browser, local file links open in viewer

## Installation

**macOS**: Download `mdvupy.app`, copy to `/Applications/`, then right-click any `.md` file → Get Info → Open with: mdvupy.app → Change All

### From Source

Requirements:
- Python 3.13+
- `uv` package manager (install via [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv))

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/deidelma/mdvupy.git
cd mdvupy

# Create virtual environment and install dependencies
uv venv --python 3.13
uv pip install -e ".[dev]"

# Run the application
uv run main.py
```

For detailed build instructions, see [docs/BUILDING-MACOS.md](docs/BUILDING-MACOS.md).

## Usage

```bash
# Open a Markdown file
uv run main.py path/to/document.md

# Or launch and use File → Open from the menu
uv run main.py
```

After installing the `.app` bundle on macOS:
```bash
open /Applications/mdvupy.app
open -a mdvupy document.md
```

### Keyboard Shortcuts

- **Cmd/Ctrl+O**: Open file
- **Cmd/Ctrl+F**: Search
- **Cmd/Ctrl+T**: Toggle Table of Contents
- **Cmd/Ctrl++**: Zoom in
- **Cmd/Ctrl+-**: Zoom out
- **Cmd/Ctrl+0**: Reset zoom
- **Alt+Left**: Navigate back in history
- **Alt+Right**: Navigate forward in history
- **Cmd/Ctrl+Q**: Quit
- **Esc**: Close search

### Features

- Click any heading in the Table of Contents to jump to that section
- Use the search bar to find text (supports next/previous navigation)
- External links (http://, https://, www.) open in your system browser
- Internal links (#anchors) scroll smoothly to the target section
- Local file links open in the same viewer window
- Navigate between recently opened files using back/forward buttons
- File history persists across application restarts

## Building for macOS

```bash
# Build the .app bundle
./build-macos.sh

# Test the app
open dist/mdvupy.app

# Install to Applications
cp -r dist/mdvupy.app /Applications/
```

See [docs/BUILDING-MACOS.md](docs/BUILDING-MACOS.md) for detailed instructions including code signing and notarization.

## Development

Development follows the plan outlined in [plans/mdvupy-development-plan.md](plans/mdvupy-development-plan.md).

### Project Structure

```
mdvupy/
  src/mdvupy/         # Main package
    app.py            # Main window and application logic
    view.py           # Markdown rendering view
    loader.py         # Markdown parsing and HTML generation
    links.py          # Link classification and handling
    toc.py            # Table of contents extraction
    search.py         # Search widget
    history.py        # File history management
  tests/              # Unit and integration tests
  docs/               # Documentation
  main.py             # Entry point
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Check code
uv run ruff check .

# Format code
uv run ruff format .
```

## Technology Stack

- **Python 3.13+**: Modern Python with type hints
- **PySide6**: Qt bindings for Python
- **markdown-it-py**: CommonMark-compliant Markdown parser
- **pyqtdarktheme**: Dark theme support
- **uv**: Fast Python package manager
- **PyInstaller**: Application bundling for distribution

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Third-Party Licenses

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for licenses of dependencies.
