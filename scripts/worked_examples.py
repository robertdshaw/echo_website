"""Worked examples. The page supplied in docs/worked_examples_page.html.

The markup is held in content/worked-examples.html exactly as delivered, with
three changes made when it was brought in. The embedded photographs are served
from assets/ rather than as data URIs, the credit elements are removed because
no credit was supplied, and the style block now lives in assets/refinements.css.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content' / 'worked-examples.html'


def page(intro):
    body = CONTENT.read_text(encoding='utf-8').strip()
    return intro(
        'Worked examples', 'Three pieces of work, and what each one changed',
        'Every one of these is real. No client is named and no figure from a client document appears. Where a '
        'number carried the argument it has been replaced by the proportion or the direction.'
    ) + f'<section class="section container">{body}</section>'
