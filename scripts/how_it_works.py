"""How it works. The six-step loop, and the five operations inside the fifth step."""
from figures import figure

STEPS = [
    ('1. Collect', 'Human judgement, then tools at scale',
     'Human judgement sets the collection. We decide what we want to collect and why, and the tools then do the '
     'collecting and the first pass of processing at scale.'),
    ('2. Verify', 'Investigative journalism',
     'Reporters check what has arrived before it is allowed to count. Who says this, how would they know, and who '
     'else confirms it independently. Four outlets running the same unnamed official is one piece of unconfirmed '
     'information, not four.'),
    ('3. Structure', 'Data science',
     'What survives becomes a dated event with named actors, typed against the taxonomy, so a year of reporting can '
     'be counted rather than remembered.'),
    ('4. Weigh', 'Political risk analysis',
     'Political risk analysis and the model work out what is happening. The readings move separately rather than '
     'collapsing into one number, so pressure from outside stays visible next to whether the people in power are '
     'holding together.'),
    ('5. Decide', 'Structured judgement',
     'The five operations run here. The output is not a summary. It is cover or ignore, alert or hold, task a '
     'correspondent or wait.'),
    ('6. Check', 'Structured judgement, with a person',
     'The loop closes with review by an expert we employ. Some calls will always come in with the probabilities off. '
     'Someone goes back over those, works out how and why, and what they find changes the criteria for the next round.'),
]

OPERATIONS = [
    ('Comparison against a baseline',
     'Is this new or normal. You can only answer that if you are holding a model of normal. An editor has it in their '
     'head after twenty years on a patch. We have it in the archive and in actor histories. A ministry statement means '
     'little if they make one every month and means a great deal if it breaks the pattern.'),
    ('Source weighting',
     'Who is telling me this, and why now. The same sentence carries different value from a ministry press office, a '
     'Maracaibo correspondent and an anonymous messaging channel. Every input is weighted for credibility and motive '
     'before it is allowed to move anything. The words are identical. The judgement is the weight.'),
    ('A significance function',
     'Does it change anyone’s position, can it be reversed, how close does it sit to the exposure the client actually '
     'holds. That is an editor’s instinct written down as weighted criteria. Domain experts own it, not engineers.'),
    ('Inference of implication',
     'Given this, what becomes more likely. This is the step that separates knowing from judging. The item is '
     'connected to a model of how the situation develops, and the probabilities move.'),
    ('An allocation decision',
     'The output of judgement is never a summary. It is a decision about scarce resources. Cover or ignore. Alert or '
     'hold. Task a correspondent or wait. This step spends the client’s attention for them.'),
]


def page(intro):
    steps = ''.join(
        f'<div><span class="eyebrow">{title}</span><h3>{pillar}</h3><p>{body}</p></div>'
        for title, pillar, body in STEPS)
    operations = ''.join(
        f'<div><span class="eyebrow">{i:02d}</span><h3>{title}</h3><p>{body}</p></div>'
        for i, (title, body) in enumerate(OPERATIONS, 1))
    return intro(
        'How it works',
        'Six steps, run as a loop',
        'Structured judgement runs from collecting the material through to deciding what it means. It is built as a '
        'loop rather than a pipeline, because a person reviews the calls that missed and changes the criteria.'
    ) + f'''<section class="section container" id="the-loop"><div class="section-heading"><div><div class="eyebrow">The loop</div><h2>Collect, verify, structure, weigh, decide, check</h2></div><p>The first three steps are the evidence. The last three are the judgement. The loop closes because someone goes back over the calls that came in wrong.</p></div>{figure("loop-diagram")}<div class="standards-grid">{steps}</div></section>
<section class="section container" id="five-operations"><div class="section-heading"><div><div class="eyebrow">Inside the fifth step</div><h2>Five operations</h2></div><p>These take the decisions a good editor or intelligence analyst makes by instinct and make each one explicit, so they can run continuously, at scale, on live material, with people owning the criteria.</p></div><div class="standards-grid">{operations}</div>{figure("machine-diagram")}</section>
'''
