from pathlib import Path
import json

# Edit complete phrases, not class names or research-data identifiers.
revisions={
    'From scattered information<br>to a connected perspective.':'The story is bigger<br>than the headline.',
    'Explore how sources, events, actors, and assets can be organised around a decision. Inspect the proposed workflow and the research outputs it is designed to support.':'A policy announcement is only the beginning. The people who carry it out, the assets it affects, and the evidence from the ground determine what happens next. Explore how we bring those pieces together.',
    'Go deeper into<br>the question on your desk.':'Follow the story.<br>Test what it means.',
    'Each capability has its own evidence requirements, analytical limits, and output format.':'Start with the people involved, examine the evidence, then ask what could change the outlook.',
    'A workflow with<br>clear hand-offs.':'From the first question<br>to the finished brief.',
    'Collection supports a question. The analyst reviews the evidence. The briefing explains the reasoning and the next observation to seek.':'Good research starts with a clear question. It gathers the evidence, weighs competing explanations, and gives the reader a judgment they can examine.',
    'One question.<br>An inspectable answer.':'One clear question.<br>The evidence behind it.',
    'What changed? Why does it matter? What would change our assessment?':'What has changed? Why does it matter? What should you watch next?',
    'See the relationships<br>behind the decision.':'Who has the power<br>to change the outcome?',
    'A useful actor map explains the relationship, its source, and its limits. Explore a fictional operating-asset example, then see how it becomes a stakeholder brief.':'An organisation chart tells you who holds a title. A useful stakeholder map goes further: who makes the decision, who carries it out, and who may be affected. This fictional example shows how we examine those relationships.',
    'A map that explains itself':'Every connection needs a source',
    'From a network<br>to a useful conversation.':'Know who matters.<br>Know what to ask.',
    'The accompanying note explains which relationships matter to the specific question.':'The accompanying note explains why a relationship matters and what remains uncertain.',
    'An evidence record should let another reader retrace the analysis. Explore how four reports about a fictional terminal can contain fewer independent observations than the headline count suggests.':'Four reports can tell one story without providing four independent accounts. In this fictional example, we follow the original claims, identify repetition, and keep the disagreement in view.',
    'Are the sources<br>answering the same question?':'An open terminal.<br>A closed gate. Both can be true.',
    'A wider-area physical observation may add context without resolving the gate-level claim. The useful next step is a discriminating observation, not another copy of the initial statement.':'An image of activity around a terminal cannot tell you whether a particular contractor got through a particular gate. The next piece of evidence needs to answer that narrower question.',
    'Keep the source.<br>Keep the disagreement.':'When accounts differ,<br>follow the evidence.',
    'A useful scenario has an observable trigger, a decision horizon, and a rule for review. Explore a fictional access question without turning uncertainty into an unsupported probability.':'What would make you change your view? A useful scenario names the event, the date, and the evidence that would matter. This fictional example shows how to make that question concrete.',
    'A disciplined alternative<br>to a broad country score.':'A better question<br>than “How risky is the country?”',
    'Challenge a thesis<br>one assumption at a time.':'Test the assumptions<br>behind the investment.',
    'Work backwards from the assumption that matters to committee. Name the political milestone, the counterparty dependency, and the evidence that could change the view.':'Start with the part of the investment case that depends on politics or operations. Name the decision that must happen, the party responsible, and the evidence that would make you reconsider.',
    'Research you can inspect.<br>Boundaries you can understand.':'Trust begins with<br>showing the work.',
    'Trust starts with an accurate account of the evidence and the service. Here is how this public website works, the editorial rules we use, and the controls to agree before any private research engagement.':'Readers should be able to see where a claim comes from and where its limits lie. Here we explain our editorial standards, how this website handles information, and what we agree before private research begins.',
    'A focused mandate.<br>A clear research process.':'Start with the decision.<br>Agree the work it needs.',
    'Start with a decision and build the scope around it. These engagement formats describe possible research structures; availability, source access, delivery, and fees are agreed directly.':'Tell us the decision you face and the time you have. We can then discuss the research, sources, and format that would help. Scope, timing, and fees are agreed before work begins.',
    'Bring the question.<br>Build the research mandate.':'Bring us the question<br>that matters to you.',
    'Define the subject, the evidence you need, and the date that matters.':'Tell us what you need to understand and when you need an answer.',
    'Inspect the output.<br>Follow the reasoning.':'Read the brief.<br>Follow the reasoning.',
    'Two complete fictional briefs show how a research question becomes an evidence record, an assessment, and a set of next steps. Read them in full or download a copy.':'These two fictional briefs show the whole argument: the question, the evidence, the judgment, and what to watch next. Read them in full or download a copy.',
    'The executive assessment should be concise. The supporting record should let a demanding reader test how it was reached.':'A busy reader needs the conclusion quickly. A careful reader needs enough evidence to challenge it. A good brief serves both.',
    'Start with the record.<br>Know what it can tell you.':'Go to the source.<br>Read it in context.',
    'A curated directory for policy, energy, and counterparty research. Each entry explains where to start, what to record, and what the source cannot establish on its own.':'Official records are a starting point, not the whole story. This directory explains where to find them, what to look for, and what each source can—and cannot—tell you.',
    'A source-linked stakeholder view, questions for engagement, and a review horizon.':'A sourced view of the key people, questions for your next meeting, and a date to revisit the findings.',
    'Pressure-test the political and operational assumptions in a distressed-debt thesis.':'Examine the political and operational assumptions behind a distressed-debt investment.',
    'A set of bounded, dated research questions with evidence rules and explicit unresolved assumptions.':'Clear questions, deadlines, and the evidence needed to answer them—with unresolved assumptions kept in view.',
    'Bring a more demanding question to committee.':'Bring a clearer argument to committee.',
    'Your mandate. Your perspective.':'The decision on your desk',
    'Start with the question on your desk. See how political context becomes a focused research brief.':'A government affairs team and an investment manager may follow the same event for different reasons. Start with the decision you face.',
    'Depth you can bring<br>to the next conversation.':'Research that earns<br>its place in the conversation.',
    'Six ways to structure a research mandate. Agree the scope and source access in a briefing conversation.':'Six ways to turn a broad concern into useful research. We agree the question, sources, and scope with you.',
}
for name in ['scripts/depth.py','scripts/audiences.py','scripts/experience.py','scripts/samples.py','scripts/site_navigation.py']:
    p=Path(name); s=p.read_text(encoding='utf-8')
    for before,after in revisions.items(): s=s.replace(before,after)
    p.write_text(s,encoding='utf-8')

p=Path('content/articles.json'); articles=json.loads(p.read_text(encoding='utf-8'))
essay=next(a for a in articles if a['slug']=='from-signal-to-significance')
essay['dek']='A burst of headlines can draw attention to an asset. It takes a closer reading of the evidence to understand what has actually changed.'
essay['takeaway']='More reporting does not always mean more evidence. The useful question is what happened, whose account supports it, and what it means for the decision you face.'
essay['sections']=[
 {'heading':'The story at the gate','paragraphs':['Consider a fictional energy terminal. Its operator says business continues as usual. A local report says contractors have been turned away at a gate. Within hours, several other publications repeat the operator’s statement. A dashboard shows a surge in mentions.','What has changed? The number of articles cannot answer that question. The operator may be describing the terminal as a whole, while the local account concerns one entrance, one shift, or one group of workers. Both accounts could be accurate. Neither, on its own, tells a company whether its contractors can get in.']},
 {'heading':'Attention is a starting point','paragraphs':['Search tools and topic scores help an analyst find material worth reading. A rise in mentions can draw attention to a place or an issue that would otherwise be missed. That is useful. But a measure of attention is not a measure of whether an event occurred, or how likely another event is to follow.','The distinction matters when a report is repeated. Five publications may rely on the same statement. Counting them as five confirmations would make the evidence look stronger without adding a single new observation. The analyst needs to follow each account back to its origin.']},
 {'heading':'Read the claims closely','paragraphs':['Return to the terminal. The first task is to establish what each source actually says: the activity, the location, and the period it describes. “Open” may mean that cargo is moving. It may say nothing about contractor access. “Turned away” may describe a brief interruption rather than a lasting restriction.','The next useful source would distinguish between those possibilities. It might be a dated access procedure or an independent observation of the relevant gate. Another broad statement would add little. An image showing activity across the wider site could provide context while leaving the access question unanswered.']},
 {'heading':'Bring the evidence back to the decision','paragraphs':['For a government affairs team, the practical questions are who sets the access rules, who applies them, and which office can explain the discrepancy. For an investor, the issue may be whether a service interruption challenges an assumption about the asset. The same evidence can matter in different ways.','That is the approach behind EchoFrame’s Venezuela programme: start with a specific asset, contract, or local question, then gather the evidence needed to answer it. The connected event and forecasting workflow is still being developed. The aim is a clearer account of what is known, what remains uncertain, and what would change the view.']}
]
# Simplify recurrent phrases in prose fields across the remaining articles.
phrases={'a bounded question':'a clearly defined question','an inspectable record':'a record the reader can examine','a discriminating observation':'an observation that distinguishes between the competing accounts','a decision horizon':'a deadline for the decision','the decision horizon':'the deadline for the decision','source-linked':'linked to its sources','a resolvable question':'a question with a clear answer and deadline'}
def simplify(value):
    if isinstance(value,str):
        for a,b in phrases.items(): value=value.replace(a,b)
        return value
    if isinstance(value,list): return [simplify(x) for x in value]
    if isinstance(value,dict): return {k:(v if k in ('slug','url','art','category','date','status') else simplify(v)) for k,v in value.items()}
    return value
p.write_text(json.dumps(simplify(articles),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
