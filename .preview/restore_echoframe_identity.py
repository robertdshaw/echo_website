from pathlib import Path
import colorsys
import re

def brand_color(match):
    value=match.group(0)
    if len(value) not in (7,9):
        return value
    rgb=[int(value[i:i+2],16)/255 for i in (1,3,5)]
    hue,light,saturation=colorsys.rgb_to_hls(*rgb)
    if 0.025 < hue < 0.18 and saturation > 0.045:
        rgb=colorsys.hls_to_rgb(0.755,light,saturation)
        return '#'+''.join(f'{round(c*255):02x}' for c in rgb)+value[7:]
    return value

p=Path('assets/presence.css')
s=p.read_text(encoding='utf-8')
s=re.sub(r'#[0-9a-fA-F]{3,8}\b',brand_color,s)
s=s.replace('/* Spacious editorial design inspired by Zite. Original EchoFrame content and assets. */','/* Reference-inspired layout with EchoFrame violet, coral, and original editorial content. */')
s=s.replace('--ink:#242424','--ink:#25212a').replace('--purple:#6b4087','--purple:#5a3878')
s=s.replace('background:#292929','background:#33213f').replace('background:#2c2c2c','background:#5a3878').replace('border-color:#2c2c2c','border-color:#5a3878').replace('color:#242424','color:#33213f')
s=s.replace('.power-copy h1 em{font-style:normal;font-family:var(--serif);color:#33213f}', '.power-copy h1 em{font-style:normal;font-family:var(--serif);color:#5a3878}')
# Explicit brand accents: coral is a highlight, violet carries navigation and text.
s += '\n/* EchoFrame signature accents. */\n.brand{color:#33213f}.brand svg path:first-child{stroke:#ed704b}.topline{background:#33213f}.topline a{color:#ffb598}.button-coral{background:#ed704b;border-color:#ed704b;color:#30213e}.button-coral:hover{background:#f58d6e;border-color:#f58d6e;color:#30213e}.console-symbol,.statement-mark,.format-icon{color:#ac482e}.signal-light{background:#ed704b}.perspective-tabs>button[aria-selected=true]{border-color:#9e80b4;box-shadow:inset 0 -2px #ed704b;background:#eee7f4}.preview-topics button[aria-pressed=true]{background:#5a3878;border-color:#5a3878}.frame-statement p span{color:#5a3878}.nav-shell nav .nav-contact{border-color:#9e80b4}\n'
p.write_text(s,encoding='utf-8')

p=Path('scripts/experience.py')
s=p.read_text(encoding='utf-8').replace('A clearer view of power.<br><em>A stronger basis for decisions.</em>', 'Power shifts.<br><em>Exposure follows.</em>').replace('When the world changes,<br><span>understand what it means for your exposure.</span>', 'National policy. Local actors. Operating assets.<br><span>Understand the connections behind your exposure.</span>')
p.write_text(s,encoding='utf-8')
p=Path('scripts/build.py')
s=p.read_text(encoding='utf-8').replace('Every decision deserves<br>a clearer perspective.', 'Your exposure.<br>A sharper perspective.')
p.write_text(s,encoding='utf-8')
p=Path('assets/social-card.svg')
s=p.read_text(encoding='utf-8').replace('#292929','#33213f').replace('#e5ca9f','#ffb598').replace('#796342','#5a3878').replace('A clearer view of power.', 'Power shifts.').replace('A stronger basis for decisions.', 'Exposure follows.')
p.write_text(s,encoding='utf-8')
p=Path('README.md')
s=p.read_text(encoding='utf-8').replace('Zite-inspired white, charcoal, and gold theme', 'EchoFrame violet and coral palette with reference-inspired spacing and layout')
p.write_text(s,encoding='utf-8')
p=Path('docs/AUDIENCE-CONTENT-PLAN.md')
s=p.read_text(encoding='utf-8').replace('Zite-inspired white space, charcoal serif headlines, warm gold accents, pill-shaped calls to action, and subtle lavender section backgrounds.', 'Reference-inspired white space, serif headlines, and pill-shaped calls to action, using EchoFrame violet, coral accents, and pale lavender backgrounds. Content is original to EchoFrame; the reference informs layout and presentation only.')
p.write_text(s,encoding='utf-8')
