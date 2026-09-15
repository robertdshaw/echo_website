from pathlib import Path

p=Path('scripts/build.py')
s=p.read_text(encoding='utf-8')
start=s.index('    return \'\'\'<section class="hero container"')
end=s.index('<section class="section container" id="intelligence">',start)
s=s[:start]+"    return cinematic_hero()+perspectives()+programme_teaser()+'''"+s[end:]
s=s.replace('<section class="coverage-section" id="coverage">',"'''+consequence_section()+'''<section class=\"coverage-section\" id=\"coverage\">")
start=s.index('<section class="section container"><div class="section-heading"><div><div class="eyebrow">03 / How we think')
end=s.index('<section class="library-preview section container">',start)
s=s[:start]+s[end:]
start=s.index('<section class="manifesto container">')
end=s.index("'''+cta()",start)
s=s[:start]+s[end:]
s=s.replace('04 / A closer look','Research for the next conversation')
s=s.replace('aria-label="Read The gap between a signal and a decision"','aria-label="Read Attention is not evidence"')
s=s.replace('Asset-level political risk research. Explore the Venezuela development programme, regional context, and evidence behind specific client questions.','Political intelligence for oil and gas government affairs teams and distressed-debt investors. Explore asset-level questions, policy context, and the Venezuela programme.')
s=s.replace('<div><h2>Explore</h2><a href="{prefix}venezuela.html">','<div><h2>Explore</h2><a href="{prefix}government-affairs.html">Government affairs</a><a href="{prefix}distressed-debt.html">Distressed debt</a><a href="{prefix}venezuela.html">')
s=s.replace('<option>Not specified</option><option>Operator</option>','<option>Not specified</option><option>Oil &amp; gas government affairs</option><option>Distressed debt / hedge fund</option><option>Operator</option>')
s=s.replace('<div class="eyebrow">Send a briefing request</div><h2>Give us a little context.</h2>','<div class="eyebrow">Send a briefing request</div><h2 id="briefing-form-title">Give us a little context.</h2><p id="audience-context" class="briefing-audience-context" hidden></p>')
p.write_text(s,encoding='utf-8')
