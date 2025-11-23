from __future__ import annotations

from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt, QUrl
import qdarktheme

from .loader import load_markdown_file
from .view import MarkdownView
from loguru import logger

class MainWindow(QMainWindow):
	def __init__(self, initial_file: Path | None = None, parent=None) -> None:
		super().__init__(parent)
		self.setWindowTitle("mdvupy")

		qdarktheme.setup_theme("dark")

		self._view = MarkdownView(self)
		self.setCentralWidget(self._view)

		self._action_open = self.menuBar().addAction("Open…")
		self._action_open.triggered.connect(self._open_dialog)  # type: ignore[arg-type]

		# Wire link signals from MarkdownView
		self._view.external_link_clicked.connect(self._open_external)
		self._view.local_file_link_clicked.connect(self._open_local_file)

		if initial_file is not None:
			self.open_document(initial_file)

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

		logger.info(f"Setting markdown in view with base_path: {path.parent}")
		self._view.set_markdown(text, base_path=path.parent)
		self.setWindowTitle(f"mdvupy — {path.name}")
		logger.info("Document loaded successfully")

	def _open_external(self, url: str) -> None:
		"""Open external URLs in the default browser."""
		logger.info(f"Opening external URL: {url}")
		QDesktopServices.openUrl(QUrl(url))

	def _open_local_file(self, path: Path) -> None:
		"""Open local file links in the same viewer window."""
		logger.info(f"Opening local file: {path}")
		self.open_document(path)


def main() -> None:
    initial_file: Path | None = None
    if len(sys.argv) > 1:
        initial_file = Path(sys.argv[1])
        logger.info(f"Opening initial file: {initial_file}")
    app = QApplication(sys.argv)
    logger.info("Application initialized")
    window = MainWindow(initial_file=initial_file)
    logger.info("Main window created")
    window.show()   
    logger.info("Main window shown")
    sys.exit(app.exec())
