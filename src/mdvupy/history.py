from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QStandardPaths


class FileHistory:
    """Manages recently opened file history with navigation support."""
    
    def __init__(self, max_size: int = 20) -> None:
        self.max_size = max_size
        self._history: list[Path] = []
        self._current_index: int = -1
        self._config_file = self._get_config_file()
        self._load_history()
    
    def _get_config_file(self) -> Path:
        """Get the path to the config file for storing history."""
        config_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        config_path = Path(config_dir) / "mdvupy"
        config_path.mkdir(parents=True, exist_ok=True)
        return config_path / "history.json"
    
    def _load_history(self) -> None:
        """Load history from disk."""
        if self._config_file.exists():
            try:
                data = json.loads(self._config_file.read_text(encoding="utf-8"))
                self._history = [Path(p) for p in data.get("history", [])]
                self._current_index = data.get("current_index", -1)
                # Clamp current_index to valid range
                if self._history:
                    self._current_index = max(0, min(self._current_index, len(self._history) - 1))
            except Exception:
                self._history = []
                self._current_index = -1
    
    def _save_history(self) -> None:
        """Save history to disk."""
        try:
            data = {
                "history": [str(p) for p in self._history],
                "current_index": self._current_index,
            }
            self._config_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass  # Silently fail if we can't save
    
    def add_file(self, path: Path) -> None:
        """Add a file to history. If navigating in history, truncate forward history."""
        path = path.resolve()
        
        # If we're in the middle of history, remove everything after current position
        if self._current_index < len(self._history) - 1:
            self._history = self._history[: self._current_index + 1]
        
        # Remove duplicate if it exists
        if path in self._history:
            self._history.remove(path)
        
        # Add to end
        self._history.append(path)
        
        # Trim to max size
        if len(self._history) > self.max_size:
            self._history = self._history[-self.max_size :]
        
        # Update current index
        self._current_index = len(self._history) - 1
        self._save_history()
    
    def can_go_back(self) -> bool:
        """Check if we can navigate backward."""
        return self._current_index > 0
    
    def can_go_forward(self) -> bool:
        """Check if we can navigate forward."""
        return 0 <= self._current_index < len(self._history) - 1
    
    def go_back(self) -> Optional[Path]:
        """Navigate to previous file. Returns the file path or None."""
        if self.can_go_back():
            self._current_index -= 1
            self._save_history()
            return self._history[self._current_index]
        return None
    
    def go_forward(self) -> Optional[Path]:
        """Navigate to next file. Returns the file path or None."""
        if self.can_go_forward():
            self._current_index += 1
            self._save_history()
            return self._history[self._current_index]
        return None
    
    def current_file(self) -> Optional[Path]:
        """Get the current file in history."""
        if 0 <= self._current_index < len(self._history):
            return self._history[self._current_index]
        return None
    
    def get_recent_files(self, limit: int = 10) -> list[Path]:
        """Get the most recent files."""
        return list(reversed(self._history[-limit:]))
