"""Read-only safeguards for the 24-page responsive design migration."""
import unittest, re, subprocess, json
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
GROUPS=[('', ['cardapio','almoco','cafe-da-manha','eventos','como-chegar','guia-do-rio','feijoada','entardecer']),('en/', ['cardapio','almoco','cafe-da-manha','eventos','how-to-get-there','guia-do-rio','feijoada','sunset']),('es/', ['cardapio','almoco','cafe-da-manha','eventos','como-llegar','guia-do-rio','feijoada','atardecer'])]

class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

class InnerDesignTests(unittest.TestCase):
 def test_pages(self):
  for prefix,names in GROUPS:
   for i,name in enumerate(names):
    file=prefix+name+'.html'
    with self.subTest(file=file):
     source=(ROOT/file).read_text(encoding='utf-8'); tags=Tags();tags.feed(source)
     self.assertEqual(source.count('class="page-hero ec-inner-hero"'),1)
     self.assertIn('data-ec-inner="20260909"',source)
     self.assertNotRegex(source,r'<div[^>]+id="wa-preview"')
     self.assertNotRegex(source,r'<span[^>]+class="bnav-icon">[^<]')
     self.assertNotIn('class="ec-page-hero-side-frame"',source)
     hero=re.search(r'<header class="page-hero ec-inner-hero"[\s\S]*?</header>',source).group()
     self.assertNotIn('17h44',hero)
     self.assertIn('class="ec-inner-actions"',hero)
     if name=='cardapio':self.assertIn('href="#cafe-da-manha"',hero)
     for langprefix,langnames in GROUPS:
      self.assertIn('href="/'+langprefix+langnames[i]+'.html"',source)
     for tag,attrs in tags.tags:
      if tag=='img' and attrs.get('src','').startswith('/assets/'):
       self.assertTrue((ROOT/attrs['src'].lstrip('/')).is_file(),attrs['src'])
     ld=re.findall(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>([\s\S]*?)</script>',source,re.I)
     for block in ld:json.loads(block)
     # Compare against the current checked-in baseline before committing.
     baseline=subprocess.check_output(['git','show','HEAD:'+file],cwd=ROOT).decode('utf-8')
     if name in ('entardecer','sunset','atardecer'):
      baseline=baseline.replace('/assets/'+name+'-banda-opt.webp','/assets/fotos/banda-pao-de-acucar-01.webp')
     old_ld=re.findall(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>([\s\S]*?)</script>',baseline,re.I)
     self.assertEqual(ld,old_ld,'JSON-LD changed')
     before=Tags();before.feed(baseline)
     seo=lambda p:[a for t,a in p.tags if t=='link' and (a.get('rel')=='canonical' or 'hreflang' in a)]
     self.assertEqual(seo(tags),seo(before),'Canonical/hreflang changed')
     prices=lambda s:set(re.findall(r'R\$\s*[\d.,]+',s))
     self.assertEqual(prices(source),prices(baseline),'Price changed')

if __name__=='__main__':unittest.main()
