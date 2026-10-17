#!/usr/bin/env python3
"""Check the built airfoil page, its registration and curated scientific assets.

Uses only Python's standard library. Run after mkdocs build --strict.
"""
import csv
import hashlib
import json
import struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
ROUTE='projects/passive-airfoil-aeroelasticity/'


class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.tags=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if 'id' in a:self.ids.add(a['id'])


def main():
    page=SITE/ROUTE/'index.html';text=page.read_text();p=Page();p.feed(text)
    assert 'PROJECT_REVISION' not in text,'Unresolved scientific source revision'
    assert '69 controles' in text,'Verification count missing'
    assert text.count('<h1')==1,'Expected one primary heading'
    for f in ('docs/index.md','docs/projects.md','mkdocs.yml'):
        assert 'projects/passive-airfoil-aeroelasticity.md' in (ROOT/f).read_text(),f
    failures=[];checked=0
    for tag,a in p.tags:
        for key in ('src','poster','href'):
            value=a.get(key,'');u=urlsplit(value)
            if not value or u.scheme or u.netloc:continue
            target=(SITE/u.path.lstrip('/')) if u.path.startswith('/') else page.parent/unquote(u.path)
            if not u.path:target=page
            if target.is_dir():target=target/'index.html'
            if not target.is_file():failures.append(value);continue
            if u.fragment and target.suffix=='.html':
                q=Page();q.feed(target.read_text())
                if unquote(u.fragment) not in q.ids:failures.append(value)
            checked+=1
        if tag=='img':
            assert len(a.get('alt',''))>=15,'Missing descriptive image alternative'
            path=(page.parent/a['src']).resolve()
            if 'assets/airfoil/' in str(path):
                raw=path.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'
                width,height=struct.unpack('>II',raw[16:24]);assert width>=900
                assert (int(a['width']),int(a['height']))==(width,height),'Wrong intrinsic image dimensions'
        if tag=='video':
            assert 'controls' in a and 'muted' in a and 'playsinline' in a
            assert 'autoplay' not in a and a.get('poster') and a.get('aria-label')
    assert not failures,failures
    meta={a.get('property',a.get('name')):a.get('content') for tag,a in p.tags if tag=='meta'}
    assert meta.get('description') and meta.get('og:description')
    assert meta['og:url']=='https://mc-andes.github.io/'+ROUTE
    assert meta['og:image']=='https://mc-andes.github.io/assets/airfoil/geometry.png'
    assets=ROOT/'docs/assets/airfoil';hashes=json.loads((assets/'asset-hashes.json').read_text())
    for name,digest in hashes.items():assert hashlib.sha256((assets/name).read_bytes()).hexdigest()==digest,name
    assert set(hashes)=={f.name for f in assets.iterdir() if f.is_file() and f.name!='asset-hashes.json'}
    evidence=json.loads((assets/'evidence.json').read_text());assert evidence['verification_checks']==69
    assert evidence['video']['states']==241 and not evidence['video']['interpolated_states']
    for state in evidence['speed_map']:assert state['growth_per_s']<0
    assert (assets/'posterior-motion.mp4').stat().st_size<2_000_000
    rows=list(csv.reader((assets/'posterior-motion.csv').open()))
    assert len(rows)==241 and abs(float(rows[-1][0])-1.2)<1e-12
    print(f'PASS: registered page, metadata, {checked} local references, {len(hashes)} hashed assets, 241 computed video states.')


if __name__=='__main__':main()
