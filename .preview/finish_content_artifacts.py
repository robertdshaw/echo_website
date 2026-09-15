from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
# Preserve the previous text snapshot outside the publication build.
archive=ROOT/'_unpublished'/'EchoFrame-Website-Content-before-revision.md'
if not archive.exists(): archive.write_bytes((ROOT/'EchoFrame-Website-Content.md').read_bytes())
s=(ROOT/'.preview/extract_website_content.py').read_text(encoding='utf-8')
s=s.replace("parts = ['# EchoFrame website content', 'Content snapshot from the published-site files, 13 September 2026. Includes all 35 HTML pages in English and Spanish, interactive explanatory copy and downloadable text templates. Shared navigation and footer content appear once per variant. Original wording is preserved. Images and video are linked; no video transcript is available. Map geometry and individual event-data rows are linked rather than expanded into prose.']", "parts = ['# EchoFrame website content', f'Local review build, 13 September 2026. Includes all {len(pages)} retained HTML pages, the active interactive explanations and blank templates. These changes have not been pushed or deployed. Web addresses identify the page destinations and do not imply that this draft is live. Shared navigation and footer content appear once per variant. Images and video are linked.']")
start=s.index('objects = '); end=s.index('\nfor name, label in objects:',start)
s=s[:start]+"objects = [('evidenceStates', 'Evidence status')]"+s[end:]
s=s.replace('These alternatives appear when a visitor changes a selector or opens a tailored briefing form.', 'These explanations appear when the visitor changes the evidence-status selector on the methodology page.')
start=s.index("parts.append('### Historical exports chart')"); end=s.index("parts.append('## Downloadable text and templates')",start)
s=s[:start]+s[end:]
s=s.replace(", 'questions': len(seen)", '')
# Improve spacing and Markdown links without changing the wording.
s=s.replace("label = clean(text) or node.get('aria-label', '')", "label = re.sub(r'#{1,6} ', '', clean(text)) or node.get('aria-label', '')")
s=s.replace("return text + ' ' if text else ''", "return ' ' + text + ' ' if text else ''")
s=s.replace("label + '](' + urljoin(url, node.get('href', '')) + ') '", "label + '](' + urljoin(url, node.get('href', '')).replace(' ', '%20') + ') '")
s=s.replace("text = re.sub(r'(?m)^(#{1,6}) '", "text = re.sub(r'(?m)^(#{1,6}) '")
s=s.replace("parts.append(text.strip())", "parts.append(re.sub(r'(?m)^(#{1,6} .+)\\n(?=[-*] )', r'\\1\\n\\n', text.strip()))")
(ROOT/'scripts/export_content.py').write_text(s,encoding='utf-8')
# Keep the current browser checks reproducible as a repository script.
browser=(ROOT/'.preview/browser_revision_check.py').read_text(encoding='utf-8')
(ROOT/'scripts/preview_check.py').write_text(browser,encoding='utf-8')
