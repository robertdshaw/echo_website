"""Apply the site's single enquiry invitation policy to generated page bodies."""
import html
import re

INVITATIONS = {
    'index.html': 'Discuss your research priorities',
    'about.html': 'Ask about EchoFrame and training',
    'actor-mapping.html': 'Discuss the relationships your decision depends on',
    'capabilities.html': 'Outline the research you need',
    'coverage.html': 'Enquire about research coverage',
    'decision-pathways.html': 'Discuss your decision criteria',
    'distressed-debt.html': 'Examine an investment assumption with us',
    'engagement.html': 'Arrange a scoping conversation',
    'es/index.html': 'Comente sus necesidades de investigación',
    'evidence-workspace.html': 'Discuss the evidence your team needs',
    'government-affairs.html': 'Prepare a government affairs enquiry',
    'methodology.html': 'Ask about the analytical method',
    'research.html': 'Suggest a research question for discussion',
    'research/following-european-energy-policy.html': 'Discuss a European energy policy question',
    'research/questions-that-can-resolve.html': 'Develop a dated research question with us',
    'research/venezuela-from-country-to-asset.html': 'Discuss a Venezuela collection requirement',
    'research/when-sources-disagree.html': 'Ask about reviewing conflicting evidence',
    'sample-asset-access.html': 'Discuss an asset access research brief',
    'sample-briefs.html': 'Discuss a brief for your team',
    'sample-thesis-review.html': 'Discuss a thesis review brief',
    'trust.html': 'Discuss handling arrangements for an engagement',
    'venezuela-context.html': 'Discuss the context around your asset',
    'venezuela.html': 'Discuss a Venezuela research mandate',
}
REFERENCE_PAGES = {'sources.html', 'privacy.html', 'editorial-standards.html'}


def enquiry_policy(body, path):
    # Remove whole existing promotional closing sections, including their repeated copy.
    body = re.sub(r'<section\b[^>]*class="[^"]*\b(?:depth-close|briefing-banner|audience-close)\b[^"]*"[^>]*>.*?</section>', '', body, flags=re.S)
    def contact_anchor(match):
        attrs, label = match.group(1), match.group(2)
        href = re.search(r'href=[\"\']([^\"\']+)', attrs)
        if not href:
            return match.group(0)
        target = html.unescape(href.group(1))
        if 'briefing.html' in target or target.startswith('https://cal.eu/'):
            return ''
        if target.startswith('mailto:') and path not in REFERENCE_PAGES:
            return 'contact@echoframe.co'
        return match.group(0)
    body = re.sub(r'<a\b([^>]*)>(.*?)</a>', contact_anchor, body, flags=re.S)
    if path in INVITATIONS:
        prefix = '../' if '/' in path else ''
        body += ('<section class="section container page-enquiry"><a class="button button-coral" href="'
                 + prefix + 'briefing.html">' + html.escape(INVITATIONS[path]) + '</a></section>')
    return body
