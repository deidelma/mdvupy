from __future__ import annotations

from pathlib import Path

from markdown_it import MarkdownIt

md = MarkdownIt("commonmark", {"html": False}).enable("table").enable("strikethrough")


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
