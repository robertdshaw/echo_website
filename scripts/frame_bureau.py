"""The Frame Bureau. EchoFrame's training division, rebuilt from the reference page."""
from figures import figure

MODULES = [
    ('Module 1 · Finding and checking', 'Investigative journalism',
     [('masterclass', 'An investigative editor on how to find people who know things, and how to tell when you are '
                      'the one being used.'),
      ('desk practice', 'The group builds the evidence file behind one live question on the desk.'),
      ('you hand in', 'An evidence file where every claim names its source and the second source that stands it up.')]),
    ('Module 2 · Who holds power', 'Political risk analysis',
     [('masterclass', 'A former finance minister and central bank director on how decisions are really taken '
                      'inside a state.'),
      ('desk practice', 'Map the people around one decision. What each wants, what each fears, and what each can '
                        'actually do.'),
      ('you hand in', 'An actor map naming the three relationships most likely to break first, and what would break '
                      'them.')]),
    ('Module 3 · Turning it into data', 'Data science',
     [('masterclass', 'How a year of reporting becomes dated, counted events, and what the counting cannot tell you.'),
      ('desk practice', 'Classify a week of live material against the desk’s own rules, and argue the ones you '
                        'think are wrong.'),
      ('you hand in', 'A coded set of events, plus a written note on where the rules failed and why.')]),
    ('Module 4 · The live desk', 'All of it at once',
     [('masterclass', 'Running all six steps at the pace real events arrive.'),
      ('desk practice', 'The group holds the desk for a fortnight. Read, classify and re-weigh the desk’s own '
                        'questions every day.'),
      ('you hand in', 'The desk’s odds at the end of the fortnight, with the reasoning behind every change.')]),
    ('Module 5 · Writing the call', 'Structured judgement',
     [('masterclass', 'Briefing a minister or a board. What belongs in the first paragraph, and what has to be left '
                      'out.'),
      ('desk practice', 'Write the call with a probability and a date, and state in advance what would prove it '
                        'wrong.'),
      ('you hand in', 'A brief that reality settles a few weeks later. That verdict is your mark.')]),
]

BENCH = [
    ('Luis Raul Matos Azocar', 'Chief Intelligence Architect',
     'Former Minister of Finance, Central Bank Director and Minister of Planning in Venezuela, where he built the '
     'government situation room in the 1990s. Two decades directing a master’s programme in political '
     'communication and governance at George Washington University. He teaches how decisions are actually taken '
     'inside a state.'),
    ('Robert Shaw', 'Managing Partner and Lead Mission Architect',
     'Twenty years across investigative journalism, risk intelligence and emerging markets, and the founder of '
     'EchoFrame. He teaches sourcing and verification, including how to reach the hyperlocal and paywalled reporting '
     'that standard monitoring never sees.'),
    ('Dr Juan Manuel Trak', 'Head of Intelligence Design',
     'PhD in political processes with a master’s in business analytics, and Chief Product Officer at EchoFrame. '
     'Advisory work for UNDP, International IDEA and NDI. He teaches how social theory becomes indicators a system '
     'can score.'),
    ('Dr Jean-Christophe Loubier', 'Director of Decision Analytics',
     'Twenty years in decision support and scenario modelling for complex systems, with a standing insistence that '
     'an output has to be explainable. He teaches why a model nobody can explain will not survive its first serious '
     'challenge.'),
    ('Adam Dempsey', 'Director of Strategic Communications',
     'Two decades in strategic communications and geopolitical risk across the Gulf and Europe, and Director of '
     'Business Development at EchoFrame. He teaches how an assessment survives contact with the people who act on '
     'it.'),
    ('Dr Simon King', 'Director of Strategic Intelligence',
     'Twenty years of operational political risk across the Middle East, Africa and Asia, integrating open sources '
     'with human networks. He teaches how to read the way the people involved behave before it becomes an event.'),
]

STEPS_OF_ENGAGEMENT = [
    ('1. Scoping', 'We work together to identify the desk the group would run, who the trainees are, and the problem '
                   'that needs solving. Out of that we choose the country desk and the questions it should answer.'),
    ('2. Design', 'Four to six weeks working with you and your faculty to write the pilot syllabus together, so the '
                  'case material fits your trainees, your priorities and the way we work.'),
    ('3. Pilot group', 'We start with modules one to three, with clear markers, deliverables and measures for every '
                       'trainee, so we can see that the process is working for them rather than assume it.'),
    ('4. Full programme', 'All five modules. The written procedures and the desk itself are built over the course of '
                          'it, because the whole thing is designed to be handed over.'),
]

EXAMPLE = [
    ('The situation', 'The institute trains senior officials and wanted analytical capability held internally rather '
                      'than bought in from consultants each time a question arose.'),
    ('The question', 'Can our own people run a live intelligence desk, and what would it take?'),
    ('What the evidence showed', 'The gap was not analytical talent. It was that the judgements a good analyst makes '
                                 'by instinct were nowhere written down, so they could not be taught, checked or run '
                                 'at scale. The trainees build the desk and the written procedures as they go.'),
    ('What it changed', 'The institute keeps the desk, the procedures and the training process. The measure of '
                        'success is that a group can staff its own analytical desk within two to four weeks of '
                        'finishing, without us in the room.'),
]


def page(intro, withhold=()):
    """The Bureau page. `withhold` drops a teacher's card until they have seen
    their own entry and agreed to it; the section stands without them."""
    modules = ''
    for title, pillar, rows in MODULES:
        body = ''.join(f'<p><span class="eyebrow">{key}</span> {value}</p>' for key, value in rows)
        modules += f'<div><span class="eyebrow">{pillar}</span><h3>{title}</h3>{body}</div>'
    bench = ''.join(
        f'<div><h3>{name}</h3><span class="eyebrow">{role}</span><p>{body}</p></div>'
        for name, role, body in BENCH if name not in withhold)
    steps = ''.join(f'<div><h3>{title}</h3><p>{body}</p></div>' for title, body in STEPS_OF_ENGAGEMENT)
    example = ''.join(f'<div><span class="eyebrow">{heading}</span><p>{text}</p></div>' for heading, text in EXAMPLE)
    return intro(
        'The training division',
        'The Frame Bureau',
        'The Frame Bureau brings an organisation’s own people into the way EchoFrame works, until they can run a '
        'live desk without us. It is built for institutions that want the capability held internally, and for '
        'companies that want their own analysts trained on it.'
    ) + f'''<section class="section container" id="how-it-starts"><div class="section-heading"><div><div class="eyebrow">How an engagement starts</div><h2>Four steps, designed with you</h2></div></div><div class="standards-grid">{steps}</div><div class="prose-page"><p>What the institution keeps is a programme where the trainees do the work, and are able to staff their own analytical desk within two to four weeks of finishing the five modules. The desk, the written procedures and the training process stay with them.</p></div></section>
<section class="section container" id="the-programme"><div class="section-heading"><div><div class="eyebrow">The programme</div><h2>Five modules</h2></div></div>{figure("modules-diagram")}<div class="standards-grid">{modules}</div></section>
<section class="section container" id="who-teaches"><div class="section-heading"><div><div class="eyebrow">Who teaches it</div><h2>Taught by the people who do it</h2></div></div><div class="prose-page"><p>The Bureau teaches from a working consortium rather than a faculty list. People who have sat in the room where the decision was taken, editors who have run the investigation, and the data scientists who built the desks.</p><p>The teaching team for a programme is agreed with the institution during the design stage, and is drawn from that group.</p></div><div class="standards-grid">{bench}</div></section>
<section class="section container" id="worked-example"><div class="section-heading"><div><div class="eyebrow">Worked example</div><h2>A leadership institute that wanted the desk, not the reports</h2></div><p><em>A national leadership institute in the Gulf. Programme design, 2026.</em></p></div><div class="standards-grid">{example}</div></section>
'''
