from pathlib import Path
p=Path('scripts/build.py'); s=p.read_text(encoding='utf-8')
s=s.replace('from site_navigation import navigation, home_directory','from site_navigation import navigation, home_directory\nfrom visuals import charts, video_section\nfrom contact import contact_page')
start=s.index("MARK = '"); end=s.index('\n',start)
s=s[:start]+'''MARK = '<svg class="echoframe-mark" viewBox="0 0 48 48" fill="none" aria-hidden="true"><g stroke-width="3.8" stroke-linecap="round"><path d="M7 7L29 41M13 7L35 41M19 7L41 41" stroke="#ed704b"/><path d="M41 7L19 41M35 7L13 41M29 7L7 41" stroke="currentColor"/></g></svg>' '''.rstrip()+s[end:]
s=s.replace('h1>Power shifts.', 'h1>Power shifts.')
s=s.replace("home_directory()+'''<section", "home_directory()+video_section()+charts()+'''<section")
start=s.index('def briefing():'); end=s.index('\n\ndef standards():',start)
s=s[:start]+'def briefing():\n    return contact_page()'+s[end:]
s=s.replace('<link rel="stylesheet" href="{prefix}assets/depth.css">','<link rel="stylesheet" href="{prefix}assets/depth.css"><link rel="stylesheet" href="{prefix}assets/refinements.css">')
s=s.replace('Book a briefing {ARROW}</a></nav>', 'Request a demo {ARROW}</a></nav>')
s=s.replace("'assets/depth.css', 'assets/site.js'", "'assets/depth.css', 'assets/refinements.css', 'assets/site.js'")
s=s.replace("files += downloads", "files += downloads + ['images/EchoFramev3.mp4']")
p.write_text(s,encoding='utf-8')

p=Path('scripts/experience.py'); s=p.read_text(encoding='utf-8')
s=s.replace('Connect politics, people, and assets with research shaped for <strong>oil &amp; gas government affairs</strong> and <strong>distressed-debt investors.</strong>', 'Political decisions change the outlook for companies, assets, and investments. Follow the people and events behind them—with research for <strong>energy-sector government affairs</strong> and <strong>distressed-debt investors.</strong>')
start=s.index('<div class="research-console">'); end=s.index('<p class="image-disclosure">',start)
console=s[start:end]
# Existing suffix closes console, landscape, then starts image disclosure.
assert console.endswith('</div></div></div>')
console=console[:-6]
story='<div class="landscape-story"><p><span class="story-line">The policy changes.</span><span class="story-line">The local picture shifts.</span><span class="story-line">Your exposure follows.</span></p><a href="venezuela.html">Look closer at Venezuela <span aria-hidden="true">↗</span></a></div></div>'
s=s[:start]+story+console+s[end:]
p.write_text(s,encoding='utf-8')
