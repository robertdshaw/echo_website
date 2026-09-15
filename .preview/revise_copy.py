import json
from pathlib import Path

p=Path('content/articles.json')
s=p.read_text(encoding='utf-8')
for old,new in {'operator?s':'operator’s','analyst?s':'analyst’s','actor?s':'actor’s','client?s':'client’s','asset?s':'asset’s','Bol?var':'Bolívar','Anzo?tegui':'Anzoátegui','Falc?n':'Falcón','ECMWF ? Verification':'ECMWF · Verification'}.items():
    s=s.replace(old,new)
p.write_text(s,encoding='utf-8')

p=Path('scripts/build.py')
s=p.read_text(encoding='utf-8')
s=s.replace('© 2026 EchoFrame Ltd · Ireland · CRO 803377',"© 2026 {E(SITE['legal_name'])}{' · '+E(SITE['registration_line']) if SITE['registration_line'] else ''}")
s=s.replace('programme?s','programme’s').replace('Optional ? the subject','Optional — the subject')
s=s.replace('Archive platform screenshot ? Illustrates','Archive platform screenshot · Illustrates')
s=s.replace('href="coverage.html#latin-america"><span class="status-dot"></span> LATIN AMERICA','href="venezuela.html"><span class="status-dot"></span> VENEZUELA')
s=s.replace('<a href="coverage.html#latin-america">Political transitions ↗</a>','<a href="venezuela.html">Asset-level questions ↗</a>')
s=s.replace('· Foundations collection</small>',"· {E(a.get('collection','Foundations collection'))}</small>")
s=s.replace('EchoFrame brings those layers together through regional research and analytical platforms. Our focus spans the Middle East, European energy policy, Latin America, and Mexico’s energy sector.','Our Venezuela programme brings that question into focus: how can national context, local reporting, official records, and physical observations inform a decision about a particular asset? The connected event and forecasting workflow remains in development. Our wider research frame also includes the Middle East, European energy policy, Latin America, and Mexico.')
s=s.replace('Combinamos investigación de fuentes abiertas, conocimiento regional y escenarios con supuestos explícitos.','El programa de Venezuela se está desarrollando en torno a activos concretos, hechos locales, fuentes que discrepan y preguntas con una fecha y una regla de resolución. La integración de eventos y pronósticos sigue en desarrollo.')
s=s.replace('<h2>Explore nuestra investigación.</h2>','<p><a href="../venezuela.html">Conozca el programa de Venezuela (en inglés) ↗</a></p><h2>Explore nuestra investigación.</h2>')
s=s.replace("'Record missing evidence'", "'Record missing evidence'")
p.write_text(s,encoding='utf-8')
