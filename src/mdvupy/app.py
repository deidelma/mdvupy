from __future__ import annotations

from pathlib import Path
import sys

from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QAction, QDesktopServices, QKeySequence, QTextDocument
from PySide6.QtCore import Qt, QUrl, QEvent
import qdarktheme

from .history import FileHistory
from .loader import load_markdown_file
from .search import SearchWidget
from .toc import extract_toc
from .view import MarkdownView
from loguru import logger

class MainWindow(QMainWindow):
	def __init__(self, initial_file: Path | None = None, parent=None) -> None:
		super().__init__(parent)
		self.setWindowTitle("mdvupy")
		self.resize(1000, 700)

		qdarktheme.setup_theme("light")

		self._current_text = ""  # Store current markdown text for search/TOC
		self._history = FileHistory(max_size=20)
		self._loading_from_history = False  # Flag to prevent adding to history during navigation
		
		self._setup_ui()
		self._create_actions()
		self._create_menus()
		self._create_toolbar()
		self._create_shortcuts()

		if initial_file is not None:
			self.open_document(initial_file)

	def _setup_ui(self) -> None:
		"""Set up the main UI components."""
		# Main view
		self._view = MarkdownView(self)
		self.setCentralWidget(self._view)

		# Wire link signals from MarkdownView
		self._view.external_link_clicked.connect(self._open_external)
		self._view.local_file_link_clicked.connect(self._open_local_file)

		# Search widget (hidden by default)
		self._search_widget = SearchWidget(self)
		self._search_widget.hide()
		self._search_widget.close_requested.connect(self._hide_search)
		self._search_widget.search_input.textChanged.connect(self._on_search_text_changed)
		self._search_widget.next_button.clicked.connect(self._find_next)
		self._search_widget.prev_button.clicked.connect(self._find_prev)

		# Add search widget to a container above the view
		container = QWidget()
		layout = QVBoxLayout(container)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self._search_widget)
		layout.addWidget(self._view)
		self.setCentralWidget(container)

		# TOC dock widget
		self._toc_dock = QDockWidget("Table of Contents", self)
		self._toc_list = QListWidget()
		self._toc_list.itemClicked.connect(self._on_toc_item_clicked)
		self._toc_dock.setWidget(self._toc_list)
		self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._toc_dock)
		self._toc_dock.hide()  # Hidden by default

	def _create_actions(self) -> None:
		"""Create actions for menus and shortcuts."""
		# Navigation actions
		self._action_back = QAction("◀ Back", self)
		self._action_back.setShortcut(QKeySequence("Alt+Left"))
		self._action_back.triggered.connect(self._navigate_back)
		self._action_back.setEnabled(False)

		self._action_forward = QAction("Forward ▶", self)
		self._action_forward.setShortcut(QKeySequence("Alt+Right"))
		self._action_forward.triggered.connect(self._navigate_forward)
		self._action_forward.setEnabled(False)

		# File actions
		self._action_open = QAction("Open…", self)
		self._action_open.setShortcut(QKeySequence.StandardKey.Open)
		self._action_open.triggered.connect(self._open_dialog)

		self._action_quit = QAction("Quit", self)
		self._action_quit.setShortcut(QKeySequence.StandardKey.Quit)
		self._action_quit.triggered.connect(self.close)

		# View actions
		self._action_toggle_toc = QAction("Toggle TOC", self)
		self._action_toggle_toc.setShortcut(QKeySequence("Ctrl+T"))
		self._action_toggle_toc.setCheckable(True)
		self._action_toggle_toc.triggered.connect(self._toggle_toc)

		self._action_search = QAction("Search…", self)
		self._action_search.setShortcut(QKeySequence.StandardKey.Find)
		self._action_search.triggered.connect(self._show_search)

		# Zoom actions
		self._action_zoom_in = QAction("Zoom In", self)
		self._action_zoom_in.setShortcut(QKeySequence.StandardKey.ZoomIn)
		self._action_zoom_in.triggered.connect(self._zoom_in)

		self._action_zoom_out = QAction("Zoom Out", self)
		self._action_zoom_out.setShortcut(QKeySequence.StandardKey.ZoomOut)
		self._action_zoom_out.triggered.connect(self._zoom_out)

		self._action_zoom_reset = QAction("Reset Zoom", self)
		self._action_zoom_reset.setShortcut(QKeySequence("Ctrl+0"))
		self._action_zoom_reset.triggered.connect(self._zoom_reset)

	def _create_menus(self) -> None:
		"""Create the menu bar."""
		# File menu
		file_menu = self.menuBar().addMenu("File")
		file_menu.addAction(self._action_back)
		file_menu.addAction(self._action_forward)
		file_menu.addSeparator()
		file_menu.addAction(self._action_open)
		file_menu.addSeparator()
		file_menu.addAction(self._action_quit)

		# View menu
		view_menu = self.menuBar().addMenu("View")
		view_menu.addAction(self._action_toggle_toc)
		view_menu.addAction(self._action_search)
		view_menu.addSeparator()
		view_menu.addAction(self._action_zoom_in)
		view_menu.addAction(self._action_zoom_out)
		view_menu.addAction(self._action_zoom_reset)

	def _create_toolbar(self) -> None:
		"""Create the navigation toolbar."""
		toolbar = QToolBar("Navigation")
		toolbar.setMovable(False)
		self.addToolBar(toolbar)
		
		toolbar.addAction(self._action_back)
		toolbar.addAction(self._action_forward)

	def _create_shortcuts(self) -> None:
		"""Create additional keyboard shortcuts."""
		# All shortcuts are handled via QAction.setShortcut in _create_actions
		pass

	def _open_dialog(self) -> None:
		path_str, _ = QFileDialog.getOpenFileName(
			self,
			"Open Markdown File",
			"",
			"Markdown Files (*.md *.markdown);;All Files (*)",
		)
		if path_str:
			self.open_document(Path(path_str))

	def open_document(self, path: Path) -> None:
		logger.info(f"open_document called with path: {path}")
		logger.info(f"Path exists: {path.exists()}, is_file: {path.is_file()}")
		try:
			text = load_markdown_file(path)
			logger.info(f"Loaded {len(text)} characters from file")
		except Exception as exc:  # noqa: BLE001
			logger.error(f"Failed to load file: {exc}")
			QMessageBox.critical(self, "Error", f"Failed to load file:\n{exc}")
			return

		self._current_text = text
		logger.info(f"Setting markdown in view with base_path: {path.parent}")
		self._view.set_markdown(text, base_path=path.parent)
		self.setWindowTitle(f"mdvupy — {path.name}")
		
		# Add to history (unless we're navigating through history)
		if not self._loading_from_history:
			self._history.add_file(path)
		
		# Update navigation buttons
		self._update_navigation_state()
		
		# Update TOC
		self._update_toc()
		
		logger.info("Document loaded successfully")

	def _update_navigation_state(self) -> None:
		"""Update the enabled state of navigation buttons."""
		self._action_back.setEnabled(self._history.can_go_back())
		self._action_forward.setEnabled(self._history.can_go_forward())

	def _navigate_back(self) -> None:
		"""Navigate to previous file in history."""
		prev_file = self._history.go_back()
		if prev_file and prev_file.exists():
			self._loading_from_history = True
			self.open_document(prev_file)
			self._loading_from_history = False

	def _navigate_forward(self) -> None:
		"""Navigate to next file in history."""
		next_file = self._history.go_forward()
		if next_file and next_file.exists():
			self._loading_from_history = True
			self.open_document(next_file)
			self._loading_from_history = False

	def _update_toc(self) -> None:
		"""Update the table of contents from current markdown text."""
		self._toc_list.clear()
		toc_items = extract_toc(self._current_text)
		
		for item in toc_items:
			indent = "  " * (item.level - 1)
			list_item = QListWidgetItem(f"{indent}{item.text}")
			list_item.setData(Qt.ItemDataRole.UserRole, item.anchor)
			self._toc_list.addItem(list_item)
		
		# Show TOC if there are items
		if toc_items:
			self._toc_dock.show()
			self._action_toggle_toc.setChecked(True)

	def _on_toc_item_clicked(self, item: QListWidgetItem) -> None:
		"""Handle TOC item click to scroll to section."""
		anchor = item.data(Qt.ItemDataRole.UserRole)
		if anchor:
			self._view.scrollToAnchor(anchor)

	def _toggle_toc(self) -> None:
		"""Toggle TOC visibility."""
		if self._toc_dock.isVisible():
			self._toc_dock.hide()
		else:
			self._toc_dock.show()

	def _show_search(self) -> None:
		"""Show search widget and focus input."""
		self._search_widget.show()
		self._search_widget.focus_search()

	def _hide_search(self) -> None:
		"""Hide search widget."""
		self._search_widget.hide()
		self._view.setFocus()

	def _on_search_text_changed(self) -> None:
		"""Handle search text changes."""
		search_text = self._search_widget.get_search_text()
		if search_text:
			self._find_next()

	def _find_next(self) -> None:
		"""Find next occurrence of search text."""
		search_text = self._search_widget.get_search_text()
		if search_text:
			found = self._view.find(search_text)
			if not found:
				# Wrap around to beginning
				cursor = self._view.textCursor()
				cursor.movePosition(cursor.MoveOperation.Start)
				self._view.setTextCursor(cursor)
				self._view.find(search_text)

	def _find_prev(self) -> None:
		"""Find previous occurrence of search text."""
		search_text = self._search_widget.get_search_text()
		if search_text:
			found = self._view.find(search_text, QTextDocument.FindFlag.FindBackward)
			if not found:
				# Wrap around to end
				cursor = self._view.textCursor()
				cursor.movePosition(cursor.MoveOperation.End)
				self._view.setTextCursor(cursor)
				self._view.find(search_text, QTextDocument.FindFlag.FindBackward)

	def _zoom_in(self) -> None:
		"""Increase text size."""
		self._view.zoomIn(1)

	def _zoom_out(self) -> None:
		"""Decrease text size."""
		self._view.zoomOut(1)

	def _zoom_reset(self) -> None:
		"""Reset zoom to default."""
		self._view.zoomIn(0)  # Reset to base font size
		# Alternative: store original font size and restore it
		font = self._view.font()
		font.setPointSize(12)  # Default size
		self._view.setFont(font)

	def _open_external(self, url: str) -> None:
		"""Open external URLs in the default browser."""
		logger.info(f"Opening external URL: {url}")
		QDesktopServices.openUrl(QUrl(url))

	def _open_local_file(self, path: Path) -> None:
		"""Open local file links in the same viewer window."""
		logger.info(f"Opening local file: {path}")
		self.open_document(path)

	def event(self, event: QEvent) -> bool:
		"""Handle Qt events, including macOS file open events."""
		if event.type() == QEvent.Type.FileOpen:
			# macOS file open event (from double-click or "Open With")
			file_path = Path(event.file())
			logger.info(f"Received FileOpen event for: {file_path}")
			self.open_document(file_path)
			return True
		return super().event(event)


def main() -> None:
    initial_file: Path | None = None
    if len(sys.argv) > 1:
        initial_file = Path(sys.argv[1])
    app = QApplication(sys.argv)
    window = MainWindow(initial_file=initial_file)
    window.show()   
    sys.exit(app.exec())
