"""A short front door: one claim, one explanation, one next step."""


def claims():
    sections = [
        ('01 / Government affairs', 'Judgment you can defend to a board',
         'Political reporting becomes useful when you can explain what it changes. Examine the six risk dimensions, the people behind the decisions and the evidence behind the assessment.',
         'government-affairs.html', 'Learn how we build the brief'),
        ('02 / Distressed debt', 'The opportunity has to clear your bar',
         'The country outlook does not establish whether a particular opportunity meets your requirements. Examine the terms and the evidence for the conditions you need.',
         'distressed-debt.html', 'Learn how we test the opportunity'),
        ('03 / Our method', 'Political science, run as data science',
         'Five analytical layers connect events, relationships and behaviour to dated research questions. Each judgment should show its evidence and explain what would change it.',
         'methodology.html', 'Learn how it works'),
    ]
    return '<div class="home-claims container">'+''.join(
        f'<section class="home-claim" aria-labelledby="claim-{i}"><div class="eyebrow">{kicker}</div>'
        f'<div><h2 id="claim-{i}">{title}</h2><p>{copy}</p>'
        f'<a class="text-link" href="{url}">{label} </a></div></section>'
        for i, (kicker, title, copy, url, label) in enumerate(sections, 1)
    )+'</div>'
