"""Apply the site's single enquiry invitation policy to generated page bodies."""
import html
import re

INVITATIONS = {
    'index.html': 'Start a conversation',
    'about.html': 'Ask us about the company',
    'actor-mapping.html': 'Discuss the relationships your decision depends on',
    'capabilities.html': 'Outline the research you need',
    'case-study-venezuela.html': 'Bring us a question with a date on it',
    'worked-examples.html': 'Put a question to the desk',
    'frame-bureau.html': 'Talk to us about training a desk',
    'services.html': 'Tell us what you need covered',
    'asset-watch.html': 'Tell us which assets to watch',
    'question-book.html': 'Bring us a decision to turn into questions',
    'ground-truth.html': 'Ask where we have people on the ground',
    'projects.html': 'Scope a piece of work with us',
    'coverage.html': 'Enquire about research coverage',
    'decision-pathways.html': 'Discuss your decision criteria',
    'distressed-debt.html': 'Examine an investment assumption with us',
    'engagement.html': 'Arrange a scoping conversation',
    'evidence-workspace.html': 'Discuss the evidence your team needs',
    'government-affairs.html': 'Prepare a government affairs enquiry',
    'how-it-works.html': 'Ask how this would run on your question',
    'sample-asset-access.html': 'Discuss an asset access research brief',
    'sample-briefs.html': 'Discuss a brief for your team',
    'sample-thesis-review.html': 'Discuss a thesis review brief',
    'trust.html': 'Discuss handling arrangements for an engagement',
    'venezuela-context.html': 'Discuss the context around your asset',
    'venezuela.html': 'Discuss a Venezuela research mandate',
}
REFERENCE_PAGES = {'sources.html', 'privacy.html', 'editorial-standards.html'}
REFERENCE_LABELS = {
    'Watch the film': 'EchoFrame presentation video',
    'Explore the research approach': 'Research approach',
    'Explore the source directory': 'Primary-source directory',
    'Read our privacy notice': 'Privacy notice',
    'Download a question register': 'Question register template',
    'Explore the full methodology': 'How it works',
    'Download a mandate template': 'Research mandate template',
    'Download a blank evidence register': 'Evidence register template',
    'Download the evidence register': 'Evidence register template',
    'Read the evidence guide': 'Evidence guide',
    'Explore counterparty research sources': 'Counterparty research sources',
    'Conozca el programa de Venezuela (en inglés)': 'Programa de Venezuela (en inglés)',
}


def enquiry_policy(body, path):
    # Remove whole existing promotional closing sections, including their repeated copy.
    body = re.sub(r'<section\b[^>]*class="[^"]*\b(?:depth-close|briefing-banner|audience-close)\b[^"]*"[^>]*>.*?</section>', '', body, flags=re.S)
    def contact_anchor(match):
        attrs, label = match.group(1), match.group(2)
        href = re.search(r'href=[\"\']([^\"\']+)', attrs)
        if not href:
            return match.group(0)
        target = html.unescape(href.group(1))
        plain_label = re.sub(r'<[^>]+>', '', label).strip()
        label = REFERENCE_LABELS.get(plain_label, label)
        if 'briefing.html' in target or target.startswith('https://cal.eu/'):
            return ''
        if target.startswith('mailto:') and path not in REFERENCE_PAGES:
            return 'contact@echoframe.co'
        classes = re.search(r'class=[\"\']([^\"\']+)', attrs)
        if classes and {'button', 'text-link'} & set(classes.group(1).split()) and path != '404.html':
            # Keep document references as ordinary links; remove secondary invitations.
            if '/downloads/' in '/' + target or target.startswith('https://') and path in REFERENCE_PAGES:
                attrs = attrs.replace(classes.group(0), 'class="document-reference"')
                label = re.sub(r'^Open the primary source', 'Source document', label.strip())
                return '<a' + attrs + '>' + label + '</a>'
            return ''
        return '<a' + attrs + '>' + label + '</a>'
    body = re.sub(r'<a\b([^>]*)>(.*?)</a>', contact_anchor, body, flags=re.S)
    if path in INVITATIONS:
        prefix = '../' if '/' in path else ''
        body += ('<section class="section container page-enquiry"><a class="button button-coral" href="'
                 + prefix + 'briefing.html">' + html.escape(INVITATIONS[path]) + '</a></section>')
    return body
