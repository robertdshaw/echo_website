from pathlib import Path

p=Path('assets/site.css')
s=p.read_text(encoding='utf-8').replace('.evidence-verdict p{font-size:13px;', '.evidence-verdict p{color:#554b5d;font-size:13px;')
p.write_text(s,encoding='utf-8')

p=Path('scripts/build.py')
s=p.read_text(encoding='utf-8')
s=s.replace('The foundations collection is evergreen educational material, not a stream of current alerts or investment recommendations.','The foundations collection is evergreen educational material. Programme notes explain work in development. Neither format should be mistaken for current alerts, verified field coverage, or a forecast track record.')
s=s.replace('<section><h2>Assessment and uncertainty</h2>', '<section><h2>Rights, precision, and source protection</h2><p>The intended Venezuela workflow requires review of permitted source use before client publication. A publicly accessible source is not a blanket permission to reproduce its text. Public outputs should use approved summaries and references.</p><p>Source-protecting material must not expose identities, identifying narrative, or unsafe geographic detail. A state-level observation should not appear as a precise facility pin. These are design and editorial requirements; this public website is not a field-report intake or protection system.</p></section><section><h2>Assessment and uncertainty</h2>')
p.write_text(s,encoding='utf-8')
