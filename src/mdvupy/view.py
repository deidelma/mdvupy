from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWidgets import QTextBrowser

from .links import LinkType, classify_link
from .loader import render_markdown_to_html


class MarkdownView(QTextBrowser):
	external_link_clicked = Signal(str)
	local_file_link_clicked = Signal(Path)
	internal_anchor_clicked = Signal(str)

	def __init__(self, parent=None) -> None:
		super().__init__(parent)
		self.setOpenExternalLinks(False)
		self.setOpenLinks(False)
		self._base_path: Path | None = None
		
		# Connect the anchorClicked signal to our handler
		self.anchorClicked.connect(self._handle_link_click)

	def set_markdown(self, text: str, base_path: Path | None = None) -> None:
		self._base_path = base_path
		html = render_markdown_to_html(text)
		self.setHtml(html)

	def set_base_path(self, path: Path | None) -> None:
		self._base_path = path

	def _handle_link_click(self, url: QUrl) -> None:
		"""Handle link clicks from the QTextBrowser."""
		href = url.toString()
		link_type, target = classify_link(href, base_path=self._base_path)

		if link_type is LinkType.EXTERNAL:
			self.external_link_clicked.emit(str(target))
		elif link_type is LinkType.LOCAL_FILE:
			self.local_file_link_clicked.emit(target)
		elif link_type is LinkType.INTERNAL:
			self.scrollToAnchor(str(target))
			self.internal_anchor_clicked.emit(str(target))

	def setSource(self, url: QUrl) -> None:  # type: ignore[override]
		"""Override setSource to prevent default navigation behavior."""
		# Delegate to our link handler
		self._handle_link_click(url)
