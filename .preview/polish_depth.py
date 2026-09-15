from pathlib import Path
for name in ['scripts/depth.py','scripts/samples.py']:
    p=Path(name); s=p.read_text(encoding='utf-8').replace('<div class="table-scroll">','<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable research table">'); p.write_text(s,encoding='utf-8')
p=Path('assets/depth.css'); s=p.read_text(encoding='utf-8').replace('color:#766680;line-height:1.6','color:#6b5875;line-height:1.6'); s+='\n.table-scroll:focus-visible{outline:2px solid #a15439;outline-offset:4px}.section.container>h2{font-size:38px;line-height:1.2}.expanded-enquiry .briefing-form{background:#f7f3fa;border:1px solid #e3d8eb;border-radius:5px}@media(max-width:680px){.section.container>h2{font-size:31px}}\n'; p.write_text(s,encoding='utf-8')
PYTHON_MARKER=''
