from pathlib import Path
import re, json, shutil, sys, ast

ROOT = Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding='utf-8')
def write(p, s):
    (ROOT/p).parent.mkdir(parents=True, exist_ok=True)
    (ROOT/p).write_text(s, encoding='utf-8')
def replace(p, old, new):
    s=read(p)
    assert old in s, (p, old[:100])
    write(p,s.replace(old,new))
def function(p, name, new):
    s=read(p); tree=ast.parse(s)
    node=next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name==name)
    lines=s.splitlines(keepends=True)
    write(p,''.join(lines[:node.lineno-1])+new.rstrip()+'\n'+''.join(lines[node.end_lineno:]))
def archive(p):
    src=(ROOT/p).resolve(); dst=(ROOT/'_unpublished'/p).resolve()
    assert src.is_relative_to(ROOT) and dst.is_relative_to(ROOT/'_unpublished')
    assert not dst.exists(), dst
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.move(str(src),str(dst))

def item1():
    replace('scripts/experience.py', 'For oil and gas teams and distressed-debt investors, EchoFrame turns political reporting into judgments you can inspect, scenarios you can challenge, and decisions measured against your own criteria.', 'EchoFrame serves oil and gas government affairs teams and distressed-debt and special-situations investors. Venezuela is our lead programme. Our second area is European energy policy.')
    replace('scripts/build.py', 'EchoFrame desarrolla plataformas de análisis de riesgo político para el sector energético, investigadores de materias primas y organizaciones que necesitan comprender los cambios geopolíticos.', 'EchoFrame trabaja para equipos de asuntos gubernamentales del sector del petróleo y el gas e inversores en deuda en dificultades y situaciones especiales.')
    replace('scripts/build.py', 'Nuestra cobertura incluye Oriente Medio, la política energética europea, América Latina y el sector energético de México.', 'Venezuela es nuestro programa principal. Nuestra segunda área es la política energética europea.')
    replace('scripts/build.py', '        result += f\'\'\'<section id=', '        if r["id"] == "europe":\n            link = "<p>The European energy policy tracker is available to clients on request.</p>"\n        result += f\'\'\'<section id=')
    replace('scripts/build.py', '    old_figure =', '    result = re.sub(r\'<figure class="coverage-figure"><img src="images/eu-regulatory-map.png".*?</figure>\', "", result)\n    old_figure =')
    replace('scripts/build.py', "    files += ['images/'+r['image'] for r in REGIONS if r['id'] != 'latin-america']", '    # Archive interface screenshots are not part of the publication output.')

def item2():
    archive('frame-bureau.html'); archive('scripts/bureau.py')
    s=read('scripts/build.py')
    s=s.replace('from bureau import bureau_page\n','')
    s=re.sub(r'    write\(\'frame-bureau.html\'.*\n','',s)
    s=re.sub(r'<p><a href="frame-bureau.html">.*?</p>','',s)
    s=s.replace("'''+video_section()+testimonials()+faq()+cta()", "'''+frame_bureau_summary()+video_section()+testimonials()+faq()+cta()")
    s=re.sub(r'<a href="\{prefix\}frame-bureau.html">.*?</a>','',s)
    write('scripts/build.py',s)
    write('scripts/build.py',read('scripts/build.py').replace('def about():', '''def frame_bureau_summary():
    return '<section class="section container" id="frame-bureau"><h2>The Frame Bureau</h2><p>The Frame Bureau is EchoFrame’s training division. It brings investigative journalism, data science and political risk analysis into practical work on research questions. Participants check sources, distinguish evidence from assumptions, write assessments and review them when the evidence changes.</p><p>Training is available on request through <a href="mailto:contact@echoframe.co">contact@echoframe.co</a>.</p></section>'


def about():'''))
    s=read('scripts/site_navigation.py')
    s=re.sub(r"        \('frame-bureau.html'.*\n",'',s)
    write('scripts/site_navigation.py',s)
    write('_unpublished/README.md', '# Unpublished website material\n\nThese files are retained for editorial review and excluded from the public build.\n\nThe standalone Frame Bureau page has been replaced by a short section on About.\n')

def item3():
    articles=json.loads(read('content/articles.json'))
    rewrites=json.loads(read('.preview/article_rewrites.json'))
    removed=[a for a in articles if a['slug'] not in rewrites]
    write('_unpublished/content/articles.json',json.dumps(removed,ensure_ascii=False,indent=2)+'\n')
    write('_unpublished/content/retained-articles-before-edit.json',json.dumps([a for a in articles if a['slug'] in rewrites],ensure_ascii=False,indent=2)+'\n')
    for a in removed:
        p='research/'+a['slug']+'.html'
        if (ROOT/p).exists(): archive(p)
    kept=[]
    for a in articles:
        if a['slug'] not in rewrites: continue
        r=rewrites[a['slug']]
        a.update({k:r[k] for k in ('dek','takeaway','watch')})
        for section, paragraphs in zip(a['sections'],r['paragraphs']): section['paragraphs']=paragraphs
        a['author']='Robert Shaw'
        a['date_confirmed']=False
        a['date_marker']='[[ROB: confirm dates]]'
        a['sourceNote']=('This article explains a research method. It does not assess a current asset or establish operating coverage.' if a['slug']!='following-european-energy-policy' else 'This article explains how to follow a policy. It does not determine a particular legal obligation. Consult the current official document for a specific policy question.')
        kept.append(a)
    write('content/articles.json',json.dumps(kept,ensure_ascii=False,indent=2)+'\n')
    s=read('scripts/build.py')
    s=s.replace('<span>{minutes(a)} min read</span>','')
    s=s.replace("['All intelligence','Venezuela','Europe','Latin America','Methods']", "['All intelligence'] + sorted({a['category'] for a in ARTICLES})")
    s=s.replace("date_label = datetime.date.fromisoformat(a['date']).strftime('%d %B %Y').lstrip('0')", "date_label = datetime.date.fromisoformat(a['date']).strftime('%d %B %Y').lstrip('0') if a.get('date_confirmed', True) else a['date_marker']")
    s=s.replace('<time datetime="{a[\'date\']}">{date_label}</time> · {minutes(a)} min read', '<span class="article-date">{E(date_label)}</span>')
    s=s.replace('Prepared {date_label}.', 'Publication date {E(date_label)}.')
    write('scripts/build.py',s)
    redirects={
      'from-signal-to-significance':'when-sources-disagree',
      'mapping-power-without-false-precision':'venezuela-from-country-to-asset',
      'sanctions-and-operational-reality':'questions-that-can-resolve',
      'scenarios-that-can-be-tested':'questions-that-can-resolve'}
    titles={a['slug']:a['title'] for a in articles}
    for path in list((ROOT/'scripts').glob('*.py'))+list((ROOT/'assets').glob('*.js')):
        s=path.read_text(encoding='utf-8')
        for old,new in redirects.items():
            s=s.replace(old,new).replace(titles[old],titles[new])
        path.write_text(s,encoding='utf-8')
    write('docs/CONTENT-FIX-REVIEW.md', '# September content revision review\n\nLocal work only on content-fix-sept. No push or deployment.\n\n## Pending owner confirmations\n\n- Four retained research articles, publication dates. [[ROB: confirm dates]]\n- About, anonymised traction and channel naming. [[ROB: confirm wording and whether the channel partner may be named]]\n- About, unchanged testimonials. [[ROB: confirm written permission on file for Luis Matos Azócar and Jean-Christophe Loubier quotes]]\n\nHeadlines are retained under revised item 9, including existing paired headings. The existing LinkedIn URL is retained.\n')

def item4():
    s=read('scripts/build.py')
    start=s.index('<div class="standards-grid">',s.index('def about():'))
    end=s.index('</div></div></section>',start)+len('</div></div></section>')
    s=s[:start]+'''<div class="standards-grid"><div><span class="eyebrow">01</span><h3>Government affairs</h3><p>Research for oil and gas government affairs teams examining policy decisions, the institutions responsible and the evidence around an operating asset. The work helps prepare questions for stakeholder meetings and internal briefings.</p></div><div><span class="eyebrow">02</span><h3>Distressed debt and special situations</h3><p>Research for investors examining the political, counterparty and operating assumptions behind an investment. The work identifies which developments would support a view, challenge it or leave it unresolved.</p></div><div><span class="eyebrow">03</span><h3>Venezuela</h3><p>Our lead programme connects national decisions with local evidence around assets and contracts. Collection follows the question being investigated and the evidence needed to answer it.</p></div></div></section><section class="section container"><div class="eyebrow">Where the programme stands</div><p>Three organisations are using work built on this method, two of them paying, delivered through a channel partner. <span class="review-marker">[[ROB: confirm wording and whether the channel partner may be named]]</span></p></section>'''+s[end:]
    s=s.replace('EchoFrame develops political risk research around specific assets, contracts, and local actors. Our Venezuela programme is being shaped around the decisions operators, entrants, creditors, and suppliers need to make.', 'EchoFrame serves oil and gas government affairs teams and distressed-debt and special-situations investors. Venezuela is our lead programme. Our second area is European energy policy.')
    write('scripts/build.py',s)

def item5():
    from bs4 import BeautifulSoup
    sys.path.insert(0,str(ROOT/'scripts'))
    import depth, samples
    from placeholders import worked_example
    # Preserve useful explanatory sections while withdrawing the invented workbenches.
    for name,context in [('actor_mapping','actor and asset mapping'),('evidence_workspace','evidence review'),('pathways','decision pathways')]:
        soup=BeautifulSoup(getattr(depth,name)(),'html.parser')
        for n in soup.select('.product-overview'): n.replace_with(BeautifulSoup(worked_example(context),'html.parser'))
        if name=='evidence_workspace':
            note=soup.select_one('.assessment-note')
            if note: note.find_parent('section').decompose()
            lead=soup.select_one('.depth-hero p')
            lead.string='Each source needs to be read for what it establishes. Compare the activity, location and observation period before deciding whether accounts agree or conflict. Keep the original source and the reason for your assessment together.'
            for p in soup.find_all('p'):
                if 'This public example shows' in p.get_text(): p.string='The connected event and corroboration workflow remains in development. A useful research record preserves the source, its limits and the review history. The fields below describe the information needed for that record.'
        elif name=='actor_mapping':
            soup.select_one('.depth-hero p').string='An organisation chart identifies formal positions. A stakeholder assessment examines who makes a decision, who carries it out and who is affected. Each relationship needs evidence of the role it describes, together with its date and any uncertainty.'
        else:
            soup.select_one('.depth-hero p').string='An assessment becomes easier to review when the question names an outcome, a deadline and the evidence needed to establish it. Record the observation that would change your view and explain why it matters to the decision.'
        html=str(soup)
        if name=='pathways':
            tests=str(soup.select_one('#entry-tests'))
            before,after=html.split(tests)
            function('scripts/depth.py',name,f'def {name}():\n    return {before!r} + entry_tests() + {after!r}')
        else: function('scripts/depth.py',name,f'def {name}():\n    return {html!r}')
    # Keep the audience-specific problems and fit criteria, removing the fictional deliverable.
    variants={}
    for key in ['government','credit']:
        soup=BeautifulSoup(depth.audience_depth(key),'html.parser')
        sheet=soup.select_one('.deliverable-sheet')
        sheet.replace_with(BeautifulSoup(worked_example(key+' affairs' if key=='government' else 'distressed-debt research'),'html.parser'))
        variants[key]=str(soup)
    function('scripts/depth.py','audience_depth',f'def audience_depth(key):\n    return {variants!r}[key]')
    # Retain sample page titles, formats and blank templates. Archive every invented record.
    archive('content/samples.json')
    for p in ['downloads/sample-asset-access.md','downloads/sample-thesis-review.md']: archive(p)
    metadata=[{k:s[k] for k in ['slug','title','code','audience','format']} for s in samples.SAMPLES]
    write('content/samples.json',json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    soup=BeautifulSoup(samples.sample_library(),'html.parser')
    soup.select_one('.depth-hero p').string='The blank templates below help define a research question and organise its evidence. The worked briefs are awaiting real, redacted material.'
    grid=soup.select_one('.sample-grid')
    grid.parent.replace_with(BeautifulSoup(worked_example('the sample brief collection'),'html.parser'))
    function('scripts/samples.py','sample_library',f'def sample_library():\n    return {str(soup)!r}')
    s=read('scripts/samples.py').replace('from depth import opening, close','from depth import opening, close\nfrom placeholders import worked_example')
    write('scripts/samples.py',s)
    function('scripts/samples.py','sample_page', '''def sample_page(s):
    return opening(s['audience'], E(s['title']), s['format']) + worked_example(s['format']) + '<section class="section container"><p>The brief will identify the research question, the evidence supporting the assessment, unresolved issues and the next review. Source-identifying details will be removed before publication.</p><a href="sample-briefs.html">Research templates</a></section>' ''')
    function('scripts/samples.py','write_sample_downloads','def write_sample_downloads():\n    return []')
    s=read('scripts/programme.py')
    start=s.index('<section class="section container"><div class="section-heading"><div><div class="eyebrow">01 / The unit')
    end=s.index('<section class="section container"><div class="section-heading"><div><div class="eyebrow">03 / Proposed',start)
    s=s[:start]+worked_example('the Venezuela asset case')+'\n'+s[end:]
    s=s.replace('The asset-level examples below are fictional walkthroughs of the evidence process, not current findings or a live forecast feed.', 'Real, redacted asset material is being prepared for this page.')
    s=s.replace('These examples explain the brief structure.', 'The sections above explain the intended brief structure.')
    write('scripts/programme.py',s)
    function('scripts/programme.py','question_preview',f'def question_preview():\n    return {worked_example("the coverage overview")!r}')
    # No hypothetical examples in the analytical layer panels.
    replace('scripts/intelligence.py','<details><summary>See how to use it</summary><p>{E(example)}</p></details>','')
    replace('scripts/build.py', 'from map_page import map_page', 'from map_page import map_page\nfrom placeholders import worked_example')
    replace('scripts/build.py', '+six_layers()+evidence_flow()', '+six_layers()+worked_example("the analytical method")+evidence_flow()')
    # The retained articles no longer contain case retellings, but explicitly show what is pending.
    replace('scripts/build.py', '    sources = \'\'.join', '    sections += worked_example(a["slug"])\n    sources = \'\'.join')
    # Remove obsolete interactive fictional records from the shipped JavaScript.
    js=read('assets/site.js')
    start=js.index('// The interactive workbenches use fictional')
    end=js.index("document.querySelectorAll('.print-sample')",start)
    archive_copy=js[start:end]
    write('_unpublished/assets/fictional-workbenches.js',archive_copy)
    write('assets/site.js',js[:start]+js[end:])
    replacements={
      'Explore the five risk dimensions, scenario framework, and six decision tests alongside an anonymised historical assessment and fictional asset-level examples.':'Explore the risk dimensions and decision criteria alongside the historical assessment. Real, redacted asset material will be added when it is ready.',
      'Inspect the fictional asset-access brief':'Asset brief awaiting redacted material',
      'Inspect the fictional thesis-review brief':'Investment brief awaiting redacted material',
      'Inspect the fictional asset-access example':'Asset research material to follow',
      'Inspect complete fictional examples':'Research templates and forthcoming briefs',
      'Inspect a fictional relationship map and its evidence requirements.':'Read how relationships are documented and checked.',
      'Complete fictional examples and downloads.':'Research templates and forthcoming briefs.',
      'Public examples explain the intended approach and are labeled as illustrative.':'Real, redacted material will be added when it is ready for publication.',
      'Two fictional research examples with downloadable copies and blank templates.':'Blank templates and space for real, redacted research material.',
      'AN ILLUSTRATIVE RESEARCH MANDATE':'RESEARCH QUESTION',
      'Inspect a sample brief':'Research brief formats',
      'Inspect the complete sample':'Worked material to follow',
      'Inspect the asset-access brief':'Asset brief material to follow',
      'Read the thesis-review sample':'Investment brief material to follow',
    }
    for p in list((ROOT/'scripts').glob('*.py')):
        if p.name in ['map_page.py','map_data.py']: continue
        s=p.read_text(encoding='utf-8')
        for old,new in replacements.items(): s=s.replace(old,new)
        p.write_text(s,encoding='utf-8')

def item6():
    function('scripts/depth.py','trust', '''def trust():
    return opening('Trust / Evidence, access & privacy','Trust begins with<br>showing the work.','Before private research begins, we agree how the material will be used, who can receive it and how sensitive information will be handled.') + '<section class="section container"><div class="section-heading"><div><div class="eyebrow">Before a private engagement</div><h2>Agree the handling<br>before sharing the material.</h2></div><p>These requirements form part of the discussion before work begins. They need to reflect the sources, intended recipients and sensitivity of the particular engagement.</p></div>' + cards([
        ('Access and permitted use','Agree who can access the output, whether redistribution is allowed, and which source licences constrain publication.'),
        ('Sensitive material','Agree a suitable exchange channel and source-protection arrangements before sending confidential or identifying information.'),
        ('Retention and deletion','Document the retention period, storage arrangements, responsibilities, and process for correction or deletion requests.')]) + '<p>The agreed scope should identify the material covered by these arrangements and who is responsible for applying them. Resolve questions about access and permitted use before sensitive material is shared.</p></section><section class="depth-wash"><div class="container split-depth"><div><h2>What happens<br>to your information.</h2><p>The <a href="privacy.html">privacy notice</a> explains how this website handles enquiries, saved reading lists and service records.</p></div><div><h2>Show uncertainty.<br>Make corrections possible.</h2><p>The <a href="editorial-standards.html">editorial standards</a> explain attribution, uncertainty, source protection and corrections.</p></div></div></section>'
''')

def item7():
    write('scripts/contact.py',read('.preview/contact_page.py'))
    js=read('assets/site.js')
    start=js.index("const briefingForm ="); end=js.index('// The image opens',start)
    write('assets/site.js',js[:start]+read('.preview/contact_handler.js')+'\n\n'+js[end:])
    s=read('server.py')
    start=s.index('FIELDS={'); end=s.index('\n\n\ndef valid_email',start)
    s=s[:start]+'''FIELDS={
    'name':('Full name',120,True), 'email':('Work email',200,True),
    'organization':('Organisation',160,True), 'role':('Role / team',160,False),
    'sector':('Sector',100,True), 'question':('Decision or question',3000,True),
    'details':('Additional details',3000,False), 'referral':('How they found EchoFrame',80,False),
}'''+s[end:]
    s=s.replace('subject=f"EchoFrame {values[\'request_type\'].lower()} — {values[\'organization\']}"', 'subject=f"EchoFrame conversation request from {values[\'organization\']}"')
    s=s.replace("CONTACT_TO=os.getenv('CONTACT_TO','contact@echoframe.co')", "CONTACT_TO='contact@echoframe.co'")
    s=s.replace("key not in ('question','proof')", "key not in ('question','details')")
    s=re.sub(r"        if values.get\('request_type'\).*?        if errors:", '        if errors:', s, flags=re.S)
    s=s.replace('Direct sending is not connected yet. Your details are still here; please use the email link below to contact us.', 'Sending is temporarily unavailable. Your request has not been sent. Please try again later.')
    write('server.py',s)
    s=read('scripts/build.py')
    s=s.replace('These details include your name, work email, organisation, role, location, message, and any optional phone or research information you supply.', 'These details include your name, work email, organisation, sector and decision or question, together with any role, additional details and referral information you provide.')
    s=s.replace('We use this information to respond to your demo or contact request.', 'We use this information to respond to your conversation request.')
    s=s.replace('Your details remain in the page so you can use the direct email link. They are not saved in your browser when you leave.', 'Your details remain in the form so you can review them. They are not saved in your browser when you leave.')
    s=s.replace('The fallback email link opens your chosen email application.', 'Email links elsewhere on the website open your chosen email application.')
    write('scripts/build.py',s)
    s=read('scripts/test_contact.py')
    start=s.index('        self.payload='); end=s.index('\n',start)
    s=s[:start]+'''        self.payload={'request_id':str(uuid.uuid4()),'token':self.token,'name':'Test Reader','email':'reader@example.com','organization':'Example Company','role':'Research director','sector':'Distressed debt & special situations','question':'Please discuss our research question.\\nSecond paragraph.','details':'Our deadline is approaching.\\nPlease explain the available scope.','referral':'Search','website':''}'''+s[end:]
    s=re.sub(r"        for key in \['name'.*?:", "        for key in ['name','email','organization','role','question','sector','details','referral']:",s)
    start=s.index('    def test_contact_type_is_also_supported'); end=s.index('    def test_duplicate',start)
    s=s[:start]+'''    def test_optional_details_can_be_empty(self):
        for key in ('role','details','referral'): self.payload.pop(key)
        self.assertEqual(self.post().status_code,200)
        self.assertEqual(self.sent[0][0]['details'],'')

'''+s[end:]
    s=s.replace("self.payload['role']=''", "self.payload['name']=''")
    s=s.replace("'role',result.json['fields']", "'name',result.json['fields']")
    s=s.replace("'proof'", "'details'")
    write('scripts/test_contact.py',s)

def item8():
    s=read('scripts/build.py').replace('from placeholders import worked_example', 'from placeholders import worked_example\nfrom page_presentation import enquiry_policy')
    s=s.replace('layout(title,body,page,prefix,description,lang)', 'layout(title,enquiry_policy(body,path),page,prefix,description,lang)')
    s=re.sub(r'<a class="nav-contact".*?</a>','',s)
    s=s.replace('<a href="{prefix}briefing.html?kind=contact">Contact us</a>','')
    s=s.replace('<a href="mailto:contact@echoframe.co">contact@echoframe.co</a>', '<span>contact@echoframe.co</span>')
    s=s.replace('Request a demo or send us a question', 'Send us a question')
    write('scripts/build.py',s)
    replace('scripts/experience.py','Request a demo or send us a question through the contact form.', 'Send us a question through the contact form.')
    # Until the map archive step, keep its temporary navigation free of extra invitations.
    p='scripts/map_page.py'; s=read(p)
    s=re.sub(r'<a class="nav-contact".*?</a>','',s)
    write(p,s)

def item10():
    import hashlib
    items=['map.html','es/map.html','assets/gis-demo','assets/map.js','assets/map.css','scripts/map_data.py','scripts/map_page.py','scripts/check_map.py']
    hashes={}
    for item in items:
        p=ROOT/item
        for f in (p.rglob('*') if p.is_dir() else [p]):
            if f.is_file(): hashes[f.relative_to(ROOT).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    for item in items: archive(item)
    for rel,digest in hashes.items():
        assert hashlib.sha256((ROOT/'_unpublished'/rel).read_bytes()).hexdigest()==digest
    write('_unpublished/map-archive-sha256.json',json.dumps(hashes,indent=2)+'\n')
    s=read('scripts/build.py')
    s=s.replace('from map_data import build_map_data\n','').replace('from map_page import map_page\n','')
    start=s.index('    map_files = build_map_data()'); end=s.index('    for path, title, render, key in PAGES:',start)
    s=s[:start]+s[end:]
    s=s.replace("    files += map_files + ['assets/map.css', 'assets/map.js']\n",'')
    write('scripts/build.py',s)
    s=read('scripts/programme.py')
    start=s.index('<section class="programme-note container"><div class="eyebrow">PRISMA')
    end=s.index('</section>',start)+len('</section>')
    s=s[:start]+'''<section class="programme-note container"><p>The eastern Venezuela asset record is being rebuilt around a three-class corroboration rule and an asset-first view. A public demonstration will return when the first asset case is complete.</p></section><section class="section container" id="visualisations"><h2>Visualisations</h2><div class="depth-cards"><article><h3>Asset map</h3><p>To follow</p><p class="review-marker">[[ROB: supply the completed José asset map for public review]]</p></article><article><h3>Question probability chart</h3><p>To follow</p><p class="review-marker">[[ROB: supply a dated question probability chart for public review]]</p></article></div></section>'''+s[end:]
    write('scripts/programme.py',s)
    write('_unpublished/README.md',read('_unpublished/README.md')+'\nThe public map, its question catalogue, interface code and assets are retained intact here. They return when the José asset case ships. There is no announced return date. Map asset integrity is recorded in map-archive-sha256.json.\n\nThe research and downloads folders retain withdrawn editorial material for internal review. They are not part of the publication allowlist.\n')

def item11():
    s=read('scripts/intelligence.py')
    start=s.index("    ('Prospect theory'"); end=s.index("    ('Bayesian inference'",start)
    s=s[:start]+s[end:]
    start=s.index('RISKS = ['); end=s.index('\n\nTESTS = [',start)
    s=s[:start]+'''RISKS = [
    ('Elite Cohesion', 'Changes in alignment among decision-makers, and what those changes could mean for authority and implementation.'),
    ('Political Order', 'The institutions, rules and policy decisions that shape the operating and contractual environment.'),
    ('Security and Military', 'The use or threat of force, security constraints and their implications for people, access and continuity.'),
    ('Economic and Fiscal Stability', 'Pressure on public finances, payment capacity and the services or infrastructure an asset depends on.'),
    ('Geopolitical and External Pressure', 'External alignments, sanctions decisions and international actions that could change the available options.'),
    ('Social', '[[ROB: confirm the definition and evidence covered by the Social dimension]]'),
]
'''+s[end:]
    s=s.replace('Six analytical layers','Five analytical layers').replace('Five dimensions','Six dimensions').replace('these five dimensions','these six dimensions')
    s=s.replace('Let evidence change the scenario assessment','Let evidence change the probability assessment')
    s=s.replace('Start with explicit alternatives and prior judgments. Ask how much more likely a new observation would be under one scenario than another, then record the reason for any revision.', 'Start with a clearly defined question and an initial probability. Assess how the new evidence changes the likelihood of its outcome, then record the reason for any revision.')
    s=s.replace('a scenario probability','a question probability')
    s=s.replace('Scenarios meet<br>the client’s criteria','Assessments are compared<br>with the client’s criteria')
    s=s.replace('the relevant scenario','the relevant question')
    write('scripts/intelligence.py',s)
    function('scripts/intelligence.py','scenario_framework', '''def scenario_framework():
    return '<section class="section container" id="tracked-questions"><p>The scenario layer has been replaced by dated questions with tracked probabilities.</p></section>'
''')
    s=read('scripts/intelligence.py')
    s=s.replace('<strong>05</strong><h3>Risk dimensions</h3>','<strong>06</strong><h3>Risk dimensions</h3>')
    s=re.sub(r'<a href="capabilities.html#five-scenarios">.*?</a>','',s)
    write('scripts/intelligence.py',s)
    replacements={
      'Six analytical layers':'Five analytical layers',
      'six-layers':'analytical-layers',
      'six_layers':'analytical_layers',
      'five-scenarios':'tracked-questions',
      'connect events, relationships, and behaviour to competing scenarios':'connect events, relationships and behaviour to dated research questions',
      'Each judgment should show its evidence—and what would change it.':'Each judgment should show its evidence and explain what would change it.',
      'Where a country is heading is one question. Whether the terms hold under different scenarios—and meet your own requirements—is another.':'The country outlook does not establish whether a particular opportunity meets your requirements. Examine the terms and the evidence for the conditions you need.',
      'Which statements are supported by documents and independent observations—and where do accounts diverge?':'Which statements are supported by documents and independent observations? Where do accounts diverge?',
      'Clear questions, deadlines, and the evidence needed to answer them—with unresolved assumptions kept in view.':'Clear questions, deadlines and the evidence needed to answer them, with unresolved assumptions kept in view.',
      'Political reporting becomes useful when you can explain what it changes. Examine five dimensions of risk, the people behind the decisions, and the evidence behind the assessment.':'Political reporting becomes useful when you can explain what it changes. Examine the six risk dimensions, the people behind the decisions and the evidence behind the assessment.',
      'competing scenarios, and the conditions an opportunity must meet':'dated questions and the conditions an opportunity must meet',
      'risk dimensions, scenarios, and commercial criteria':'risk dimensions, dated questions and commercial criteria',
      'client-specific scenario odds':'client-specific probabilities',
      'Our Venezuela programme brings that question into focus: how can national context, local reporting, official records, and physical observations inform a decision about a particular asset?':'Our Venezuela programme examines how national context, local reporting, official records and physical observations inform decisions about particular assets.',
      'Turn a stream of reporting into a structured answer: where the country is heading, how the outlook could change, and whether the opportunity meets your requirements.':'A structured assessment examines where the country is heading, what could change and whether an opportunity meets your requirements.',
      'Take one expectation from the investment case: access will improve, a counterparty will perform, or a political decision will arrive on time. Define the observable event behind it, then seek evidence that could challenge it as well as support it.':'Identify a political or operating assumption in the investment case. Define the event that would establish whether it holds, then seek evidence that could challenge it as well as support it.',
      'Our public editorial standard: a reader should be able to identify the evidence, understand the interpretation, and see where uncertainty remains.':'Our public editorial standard requires a reader to be able to identify the evidence, understand the interpretation and see where uncertainty remains.',
      'We can scope a first briefing around the decision that matters most: who holds authority, what still has to happen, and which local evidence would establish a change.':'We can scope a first briefing around the decision that matters most. The research establishes who holds authority, what still has to happen and which local evidence would demonstrate a change.',
      'Examine the positions in a confrontation: what each actor wants, what they threaten, and what would make another actor comply.':'Examine what each actor wants, what they threaten and what would make another actor comply.',
      'These contain a random request reference, a keyed digest of the request, its delivery state, and a timestamp—not the text of your message.':'These contain a random request reference, a keyed digest of the request, its delivery state and a timestamp. They do not contain the text of your message.',
      'Official records are a starting point, not the whole story. This directory explains where to find them, what to look for, and what each source can—and cannot—tell you.':'These sources provide official records relevant to the research. Each entry explains where to find the material, what to look for and the limits of what it establishes.',
      'Our inference from this historical contrast is a research priority: a large resource base does not answer a question about present operating access, deliverability, or a particular commercial position.':'This historical contrast points to a research need. A large resource base does not establish present operating access, deliverability or a particular commercial position.',
      'Who has authority—and what happens next?':'Who has authority and what happens next?',
      'A useful starting point:':'A useful starting point is',
      'Tell us your sector, the decision you face, and what you would need to see in a first briefing.':'Tell us which decision the research needs to inform and what evidence is missing.',
      'A clearer view of a complex world.':'Research on political decisions and their consequences.',
      'Evidence. Context. Judgment.':'Venezuela and European energy policy',
      'Intelligence with perspective.':'EchoFrame research',
      'THE BIG PICTURE / THE LOCAL DETAIL':'POLITICAL AND OPERATING CONDITIONS',
      'THE WIDER FRAME':'ECHOFRAME',
      'Evidence  Context  Perspective':'Research and assessment',
      'Put intelligence in context':'Research enquiries',
      'The hard ask':'Reviewing an assessment',
      'Set the bar from decisions, not slogans':'Identify the criteria behind previous decisions',
      'Reports become<br>reviewable events':'Reports are organised<br>into event records',
      'One happening. Competing accounts.':'Accounts of the same event.',
      'From source to judgment':'The assessment process',
      'Read a complete brief.':'Forthcoming research briefs',
      'This library contains evergreen research guides and programme-design notes. Venezuela collection priorities and sample briefs describe work in development, not live coverage or current forecasts.':'These articles explain research methods and plans for collection. They do not report current asset conditions or present a forecast performance record.',
      'Yes. The intelligence library includes complete research essays, field guides, and programme notes. These explain our reasoning and methods. They are not a live feed or a record of validated forecasts.':'Yes. The four library articles explain source comparison, question design, Venezuela collection priorities and European energy policy research. They do not present a live feed or a validated forecast record.',
    }
    for p in list((ROOT/'scripts').glob('*.py'))+list((ROOT/'assets').glob('*.js')):
        s=p.read_text(encoding='utf-8')
        for old,new in replacements.items(): s=s.replace(old,new)
        p.write_text(s,encoding='utf-8')
    # Never manufacture dates for the retained articles.
    articles=json.loads(read('content/articles.json'))
    for a in articles:
        for sec in a['sections']:
            sec['paragraphs']=[re.sub(r'(^|(?<=[.!?])\s+)Also\s+',r'\1',p) for p in sec['paragraphs']]
    write('content/articles.json',json.dumps(articles,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__': globals()['item'+sys.argv[1]]()
