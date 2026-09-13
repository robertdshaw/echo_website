"""Complete fictional research specimens, generated as HTML and downloadable text."""
import json
from pathlib import Path
from html import escape as E
from depth import opening, close

ROOT=Path(__file__).resolve().parents[1]
SAMPLES=json.loads((ROOT/'content/samples.json').read_text(encoding='utf-8'))


def sample_library():
    result=opening('Inside the research / Complete examples','Read the brief.<br>Follow the reasoning.','These two fictional briefs show the whole argument: the question, the evidence, the judgment, and what to watch next. Read them in full or download a copy.')
    result+='<section class="section container"><div class="sample-grid">'
    for s in SAMPLES:
        result+=f'<article><a class="sample-cover" href="{s["slug"]}.html"><span>{s["code"]} / FICTIONAL EXAMPLE</span><h2>{E(s["title"])}</h2><div><span>{E(s["format"])}</span><b></b></div></a><div class="sample-card-copy"><div class="eyebrow">{E(s["audience"])}</div><p>{E(s["question"])}</p><div><a class="text-link" href="{s["slug"]}.html">Read the complete brief </a><a class="text-link" href="downloads/{s["slug"]}.md" download>Download </a></div></div></article>'
    return result+'''</div><p class="visual-caption">The examples demonstrate a proposed analytical format. They are not client work, verified field reports, or evidence of platform performance.</p></section><section class="depth-wash"><div class="container split-depth"><div><div class="eyebrow">A useful brief has layers</div><h2>Read the conclusion.<br>Inspect what supports it.</h2><p>A busy reader needs the conclusion quickly. A careful reader needs enough evidence to challenge it. A good brief serves both.</p></div><ol class="delivery-steps"><li><strong>The question</strong><p>Subject, horizon, decision context, and resolution rule.</p></li><li><strong>The assessment</strong><p>What the evidence supports, competing explanations, and remaining gaps.</p></li><li><strong>The record</strong><p>Source references, observation dates, independence checks, and limits.</p></li><li><strong>The next step</strong><p>Review triggers, collection priorities, and questions for the decision-maker.</p></li></ol></div></section><section class="section container"><div class="section-heading"><div><div class="eyebrow">Build your own research brief</div><h2>Templates for a better starting point.</h2></div></div><div class="depth-link-grid"><a href="downloads/research-mandate.md" download><span>MARKDOWN / BLANK TEMPLATE</span><h3>Research mandate</h3><p>Frame the question, intended use, delivery format, and handling requirements.</p><b></b></a><a href="downloads/evidence-register.csv" download><span>CSV / BLANK TEMPLATE</span><h3>Evidence register</h3><p>Keep provenance, timing, scope, and review status with the record.</p><b></b></a><a href="downloads/question-register.csv" download><span>CSV / BLANK TEMPLATE</span><h3>Question register</h3><p>Track the outcome rule, alternative explanations, and revision history.</p><b></b></a></div></section>'''+close()


def sample_page(s):
    toc=''.join(f'<a href="#brief-section-{i}"><span>{i:02}</span>{E(sec["heading"])}</a>' for i,sec in enumerate(s['sections'],1))
    sections=''.join(f'<section id="brief-section-{i}"><h2>{E(sec["heading"])}</h2>'+''.join(f'<p>{E(p)}</p>' for p in sec['paragraphs'])+'</section>' for i,sec in enumerate(s['sections'],1))
    ledger='<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable research table"><table class="depth-table"><caption>Fictional evidence register · Invented documents for this exercise</caption><thead><tr><th scope="col">ID</th><th scope="col">Record</th><th scope="col">Time</th><th scope="col">What it establishes</th></tr></thead><tbody>'+''.join('<tr>'+''.join(f'<{ "th scope=row" if i==0 else "td"}>{E(value)}</{ "th" if i==0 else "td"}>' for i,value in enumerate(row))+'</tr>' for row in s['evidence'])+'</tbody></table></div>'
    return f'''<article class="sample-document"><header class="container sample-document-header"><a class="back-link" href="sample-briefs.html"> All sample briefs</a><div class="eyebrow">{s['code']} / {E(s['audience'])}</div><h1>{E(s['title'])}</h1><p>{E(s['format'])}</p><div class="sample-toolbar"><span class="fiction-label">FICTIONAL RESEARCH EXERCISE</span><a href="downloads/{s['slug']}.md" download>Download the brief </a><button class="print-sample">Print / Save PDF </button></div><p class="sample-disclosure">All entities, source records, observations, and timelines below are invented. This is a complete format example, not a current assessment or a client case study.</p></header><div class="container sample-document-layout"><aside class="sample-toc"><span class="eyebrow">Inside this brief</span><a href="#brief-assessment">Executive assessment</a>{toc}<a href="#brief-ledger">Evidence register</a></aside><div class="sample-body"><section id="brief-assessment" class="sample-assessment"><div class="eyebrow">Executive assessment</div><h2>{E(s['assessment'])}</h2><dl><dt>Research question</dt><dd>{E(s['question'])}</dd><dt>Subject</dt><dd>{E(s['subject'])}</dd><dt>Resolution horizon</dt><dd>{E(s['horizon'])}</dd><dt>Resolution rule</dt><dd>{E(s['resolution'])}</dd></dl></section>{sections}<section id="brief-ledger"><h2>Evidence register</h2>{ledger}<p class="source-citation">Source IDs refer only to the fictional exercise. For real research starting points, use the <a href="sources.html">primary-source directory</a>.</p></section></div></div></article><section class="section container"><div class="eyebrow">Continue into the method</div><div class="depth-related">{''.join(f'<a href="{url}">{E(label)} </a>' for url,label in s['related'])}</div></section>'''+close()


def write_sample_downloads():
    folder=ROOT/'downloads'; folder.mkdir(exist_ok=True)
    files=[]
    for s in SAMPLES:
        text=f'# {s["title"]}\n\nEchoFrame | {s["code"]} | {s["format"]}\n\nFICTIONAL RESEARCH EXERCISE: All entities, records, observations, and timelines are invented. Not a current assessment or a client case study.\n\n## Executive assessment\n\n{s["assessment"]}\n\nQuestion: {s["question"]}\n\nSubject: {s["subject"]}\n\nHorizon: {s["horizon"]}\n\nResolution rule: {s["resolution"]}\n'
        for sec in s['sections']:
            text+='\n## '+sec['heading']+'\n\n'+'\n\n'.join(sec['paragraphs'])+'\n'
        text+='\n## Fictional evidence register\n\n'
        text+='\n'.join(' | '.join(row) for row in s['evidence'])+'\n\nPrepared as an illustrative EchoFrame research format. Contact contact@echoframe.co to discuss a research mandate.\n'
        path=f'downloads/{s["slug"]}.md'; (ROOT/path).write_text(text,encoding='utf-8'); files.append(path)
    return files
