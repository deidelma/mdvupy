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
