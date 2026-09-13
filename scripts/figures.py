"""Static figures supplied as drop-in files, held in content/figures/.

The SVG in each file is used exactly as delivered. Only the shared .ef-fig
styles were lifted out, into assets/refinements.css, so they appear once.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / 'content' / 'figures'


def figure(name):
    """Return the figure block for the given id, wrapped in its placeholder div."""
    path = FIGURES / f'{name}.html'
    if not path.is_file():
        raise FileNotFoundError(f'Missing figure: {path}')
    return f'<div id="{name}">{path.read_text(encoding="utf-8").strip()}</div>'
