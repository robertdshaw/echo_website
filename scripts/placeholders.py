"""Visible editorial placeholders for real, redacted worked material."""
from html import escape


def worked_example(context='this research method'):
    return ('<section class="section container worked-example-pending">'
            '<h2>Worked example to follow</h2>'
            '<p>Real, redacted material will be added here when it is ready for publication.</p>'
            '<p class="review-marker">[[ROB: supply real redacted material for '
            + escape(context) + ']]</p></section>')
