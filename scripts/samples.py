"""Complete fictional research specimens, generated as HTML and downloadable text."""
import json
from pathlib import Path
from html import escape as E
from depth import opening, close
from placeholders import worked_example

ROOT=Path(__file__).resolve().parents[1]
SAMPLES=json.loads((ROOT/'content/samples.json').read_text(encoding='utf-8'))


def sample_library():
    return '<section class="depth-hero"><div class="container"><div class="eyebrow">Inside the research / Complete examples</div><h1>Read the brief.<br/>Follow the reasoning.</h1><p>The blank templates below help define a research question and organise its evidence. The worked briefs are awaiting real, redacted material.</p></div></section><section class="section container worked-example-pending"><h2>Worked example to follow</h2><p>Real, redacted material will be added here when it is ready for publication.</p><p class="review-marker">[[ROB: supply real redacted material for the sample brief collection]]</p></section><section class="depth-wash"><div class="container split-depth"><div><div class="eyebrow">A useful brief has layers</div><h2>Read the conclusion.<br/>Inspect what supports it.</h2><p>A busy reader needs the conclusion quickly. A careful reader needs enough evidence to challenge it. A good brief serves both.</p></div><ol class="delivery-steps"><li><strong>The question</strong><p>Subject, horizon, decision context, and resolution rule.</p></li><li><strong>The assessment</strong><p>What the evidence supports, competing explanations, and remaining gaps.</p></li><li><strong>The record</strong><p>Source references, observation dates, independence checks, and limits.</p></li><li><strong>The next step</strong><p>Review triggers, collection priorities, and questions for the decision-maker.</p></li></ol></div></section><section class="section container"><div class="section-heading"><div><div class="eyebrow">Build your own research brief</div><h2>Templates for a better starting point.</h2></div></div><div class="depth-link-grid"><a download="" href="downloads/research-mandate.md"><span>MARKDOWN / BLANK TEMPLATE</span><h3>Research mandate</h3><p>Frame the question, intended use, delivery format, and handling requirements.</p><b></b></a><a download="" href="downloads/evidence-register.csv"><span>CSV / BLANK TEMPLATE</span><h3>Evidence register</h3><p>Keep provenance, timing, scope, and review status with the record.</p><b></b></a><a download="" href="downloads/question-register.csv"><span>CSV / BLANK TEMPLATE</span><h3>Question register</h3><p>Track the outcome rule, alternative explanations, and revision history.</p><b></b></a></div></section><section class="depth-close container"><div class="eyebrow">A conversation with context</div><h2>Bring us the question<br/>that matters to you.</h2><p>Tell us which decision the research needs to inform and what evidence is missing.</p><a class="button button-coral" href="briefing.html">See how we can help you </a></section>'


def sample_page(s):
    return opening(s['audience'], E(s['title']), s['format']) + worked_example(s['format']) + '<section class="section container"><p>The brief will identify the research question, the evidence supporting the assessment, unresolved issues and the next review. Source-identifying details will be removed before publication.</p><a href="sample-briefs.html">Research templates</a></section>'


def write_sample_downloads():
    return []
