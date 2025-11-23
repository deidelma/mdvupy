from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


class SearchWidget(QWidget):
    """Search bar with find next/previous functionality."""
    
    close_requested = Signal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.returnPressed.connect(self._on_find_next)
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self._on_find_prev)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._on_find_next)
        
        self.match_label = QLabel("")
        
        self.close_button = QPushButton("✕")
        self.close_button.setMaximumWidth(30)
        self.close_button.clicked.connect(self.close_requested.emit)
        
        layout.addWidget(QLabel("Find:"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)
        layout.addWidget(self.match_label)
        layout.addWidget(self.close_button)
        
        # Escape to close
        esc_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        esc_shortcut.activated.connect(self.close_requested.emit)
        
    def _on_find_next(self) -> None:
        """Signal handled by parent to find next match."""
        pass  # Parent will connect to this via search_input.returnPressed
        
    def _on_find_prev(self) -> None:
        """Signal handled by parent to find previous match."""
        pass  # Parent will connect to this via prev_button.clicked
        
    def get_search_text(self) -> str:
        return self.search_input.text()
        
    def update_match_count(self, current: int, total: int) -> None:
        if total > 0:
            self.match_label.setText(f"{current}/{total}")
        else:
            self.match_label.setText("No matches")
            
    def focus_search(self) -> None:
        self.search_input.setFocus()
        self.search_input.selectAll()
