"""Keep products on nine editorial pages; direct prices to the online menu."""
from pathlib import Path
import re,json,html
ROOT=Path(__file__).resolve().parents[1]
MENU='https://livemenu.app/menu/61cb5857aa455a0012ebbdcf'
COPY={
 '':('Cardápio completo e preços','Explore todos os produtos e consulte os preços no cardápio online, com opções em diversos idiomas.','Abrir cardápio online'),
 'en/':('Full menu and prices','Explore all products and view prices in our online menu, available in multiple languages.','Open online menu'),
 'es/':('Menú completo y precios','Descubre todos los productos y consulta los precios en nuestro menú online, disponible en varios idiomas.','Abrir menú online')}
def clean(node):
 if isinstance(node,list):return [clean(x) for x in node]
 if not isinstance(node,dict):return node
 return {k:clean(v) for k,v in node.items() if k not in {'offers','price','priceCurrency','priceRange','priceSpecification','lowPrice','highPrice'}}
for prefix,(title,description,label) in COPY.items():
 for name in ('almoco','feijoada','eventos'):
  file=ROOT/(prefix+name+'.html');text=file.read_text(encoding='utf-8')
  def light(m):
   classes=m.group(1).split()
   if 'ec-editorial-section' in classes and not set(classes)&{'dark','feijoada-feature','hero-internal','contact','light-section'}:classes.append('light-section')
   return '<section class="'+' '.join(classes)+'"'
  text=re.sub(r'<section class="([^"]*)"',light,text)
  # Also handle sections whose id/other attributes precede class.
  text=re.sub(r'(<section\b[^>]*\bclass=")([^"]*)(")',lambda m:m.group(1)+m.group(2)+(' light-section' if 'ec-editorial-section' in m.group(2).split() and not set(m.group(2).split())&{'dark','feijoada-feature','hero-internal','contact','light-section'} else '')+m.group(3),text)
  def serving(m):
   notes=re.findall(r'<small>(.*?)</small>',m.group(),re.S)
   return '<div class="ec-serving-notes">'+' · '.join(x.strip() for x in notes)+'</div>' if notes else ''
  text=re.sub(r'<div class="price">[\s\S]*?</div>',serving,text)
  text=re.sub(r'<span class="big">R\$\s*[\d.,]+</span>\s*<br\s*/?>','',text)
  def ld(m):
   data=json.loads(m.group(2));new=clean(data)
   return m.group() if new==data else m.group(1)+json.dumps(new,ensure_ascii=False,indent=2)+m.group(3)
  text=re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)',ld,text)
  if 'class="ec-online-menu"' not in text:
   block=f'<aside class="ec-online-menu" aria-label="{html.escape(title)}"><div><h2>{title}</h2><p>{description}</p></div><a href="{MENU}">{label} <span aria-hidden="true">→</span></a></aside>'
   text=re.sub(r'(<section class="ec-inner-details">[\s\S]*?</section>)',lambda m:m.group()+block,text,count=1)
  assert not re.search(r'R\$\s*[\d.,]+',text),file
  file.write_text(text,encoding='utf-8');print(file.name,prefix or 'PT')
