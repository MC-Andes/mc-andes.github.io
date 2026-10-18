"""Check generated local links and external references on the Delaunay page."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import json
root=Path('site').resolve()
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for key in ('href','src'):
   if key in a and not (tag == 'link' and a.get('rel') in ('canonical','preconnect')):self.links.append(a[key])
errors=[]; external=set()
for page in root.rglob('*.html'):
 p=Links();p.feed(page.read_text())
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:
   if page==root/'projects/delaunay-mesher/index.html' and u.scheme in ('https','http'):external.add(link)
   continue
  target=(root/u.path.lstrip('/') if u.path.startswith('/') else page.parent/unquote(u.path)).resolve() if u.path else page
  if target.is_dir():target=target/'index.html'
  if not target.exists(): errors.append({'page':str(page.relative_to(root)),'link':link,'error':'missing'})
  elif u.fragment and target.suffix=='.html':
   q=Links();q.feed(target.read_text())
   if unquote(u.fragment) not in q.ids:errors.append({'page':str(page.relative_to(root)),'link':link,'error':'fragment'})
def check(url):
 try:
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as r:return {'url':url,'status':r.status,'final':r.url}
 except Exception as e:return {'url':url,'error':str(e)}
result={'local_errors':errors,'external':list(ThreadPoolExecutor(8).map(check,sorted(external)))}
Path('review/delaunay/links.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors or any('error' in r for r in result['external'])))
