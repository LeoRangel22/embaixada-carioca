"""Manual, start-tag-only layout annotation; preserves all text, images and schema."""
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
FILES=[prefix+name+'.html' for prefix in ('','en/','es/') for name in ('almoco','feijoada','eventos')]
for name in FILES:
 path=ROOT/name;source=path.read_text(encoding='utf-8')
 if 'data-ec-editorial="20260909"' in source:
  if name.endswith('eventos.html'):
   source=source.replace('/assets/musicos-ao-vivo-opt.webp','/assets/fotos/banda-pao-de-acucar-01.webp')
   path.write_text(source,encoding='utf-8')
  continue
 soup=BeautifulSoup(source,'html.parser');changes={}
 def mark(node,cls):
  if not node or node.sourceline is None:return
  offset=sum(len(x) for x in source.splitlines(keepends=True)[:node.sourceline-1])+node.sourcepos
  changes.setdefault(offset,set()).add(cls)
 for section in soup.find_all('section'):
  if 'ec-inner-details' not in section.get('class',[]):mark(section,'ec-editorial-section')
 for figure in soup.find_all('figure'):
  if len(figure.parent.find_all('figure',recursive=False))>=2:mark(figure.parent,'ec-photo-grid')
 for node in soup.select('.dishes-grid,.cards,.formats,.process,.facts,.feature-grid,.feijoada-info'):
  mark(node,'ec-layout-grid')
 for node in soup.select('section div[style]'):
  if 'display: grid' in node.get('style','') or 'display:grid' in node.get('style',''):mark(node,'ec-layout-grid')
 for offset,classes in sorted(changes.items(),reverse=True):
  end=source.index('>',offset)+1;tag=source[offset:end]
  if re.search(r'\bclass="',tag):tag=re.sub(r'\bclass="', 'class="'+' '.join(sorted(classes))+' ',tag,count=1)
  else:tag=tag[:-1]+' class="'+' '.join(sorted(classes))+'">'
  source=source[:offset]+tag+source[end:]
 source=source.replace('<body ', '<body data-ec-editorial="20260909" ',1)
 source=source.replace('</head>','<link rel="stylesheet" href="/assets/css/ec-editorial-sections.css?v=20260909a"/>\n</head>',1)
 # Structural annotations must never rewrite business content or structured data.
 after=BeautifulSoup(source,'html.parser')
 assert soup.get_text(' ',strip=True)==after.get_text(' ',strip=True)
 for selector,attr in [('a','href'),('img','src'),('script','src')]:
  assert [x.get(attr) for x in soup.select(selector)]==[x.get(attr) for x in after.select(selector)]
 assert [x.string for x in soup.select('script[type="application/ld+json"]')]==[x.string for x in after.select('script[type="application/ld+json"]')]
 if name.endswith('eventos.html'):source=source.replace('/assets/musicos-ao-vivo-opt.webp','/assets/fotos/banda-pao-de-acucar-01.webp')
 path.write_text(source,encoding='utf-8');print(name,len(changes))
