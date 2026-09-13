"""Create a draft in the editorial collection. Drafts are not published by build.py."""
import argparse
import datetime
import json
import re
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('slug',help='Lowercase words separated by hyphens')
parser.add_argument('--title',required=True)
parser.add_argument('--category',default='Methods',choices=['Methods','Venezuela','Europe','Latin America'])
args=parser.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.slug):
    parser.error('Use a lowercase hyphenated slug.')
path=Path(__file__).resolve().parents[1]/'content/articles.json'
articles=json.loads(path.read_text(encoding='utf-8'))
if any(a['slug']==args.slug for a in articles):
    parser.error('That slug already exists.')
articles.append({
    'slug':args.slug,'status':'draft','title':args.title,'dek':'',
    'category':args.category,'format':'Research note','art':'signals',
    'date':datetime.date.today().isoformat(),'author':'','takeaway':'',
    'sections':[{'heading':'','paragraphs':['']}], 'watch':[],
    'sources':[],'sourceNote':''
})
path.write_text(json.dumps(articles,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Created draft: {args.slug}. Complete the content and review before setting status to published.')
