"""One-off, explicit migration of the 24 audited inner pages. No workflow hook.

Rebuilds the opening component; preserves menu content and schema structure.
Corrects three band-photo thumbnail URLs to a visually verified existing asset.
Run manually; subsequent runs skip pages already carrying the migration marker.
"""
from pathlib import Path
import re, json, html
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
 'pt': ('', ['cardapio','almoco','cafe-da-manha','eventos','como-chegar','guia-do-rio','feijoada','entardecer']),
 'en': ('en/', ['cardapio','almoco','cafe-da-manha','eventos','how-to-get-there','guia-do-rio','feijoada','sunset']),
 'es': ('es/', ['cardapio','almoco','cafe-da-manha','eventos','como-llegar','guia-do-rio','feijoada','atardecer']),
}
COPY = {
 'pt': ['Restaurante no Bondinho · Morro da Urca', 'Cardápio brasileiro com vista', 'Da primeira refeição aos drinks do entardecer, descubra os sabores da Embaixada Carioca com o Pão de Açúcar em primeiro plano.', 'Explorar o cardápio', 'Reservar mesa', 'Café da manhã com vista para o Pão de Açúcar', 'Comece o dia no Morro da Urca com pães, frutas e café, em frente ao Pão de Açúcar. Café da manhã todos os dias, das 8h30 às 11h30.', 'Mesa de café da manhã na Embaixada Carioca', 'Carne grelhada com arroz, farofa e batatas no cardápio da Embaixada Carioca'],
 'en': ['Restaurant at Sugarloaf · Morro da Urca', 'Brazilian flavours with a view', 'From breakfast to sunset drinks, explore the flavours of Embaixada Carioca with Sugarloaf Mountain right in front of you.', 'Explore the menu', 'Book a table', 'Breakfast with a view of Sugarloaf', 'Start your day at Morro da Urca with bread, fruit and coffee overlooking Sugarloaf Mountain. Breakfast is served daily from 8:30 to 11:30 AM.', 'Breakfast table at Embaixada Carioca', 'Grilled beef with rice, farofa and fries on the Embaixada Carioca menu'],
 'es': ['Restaurante en el Bondinho · Morro da Urca', 'Sabores brasileños con vista', 'Desde el desayuno hasta los cócteles al atardecer, descubre los sabores de Embaixada Carioca con el Pan de Azúcar frente a ti.', 'Explorar el menú', 'Reservar mesa', 'Desayuno con vista al Pan de Azúcar', 'Empieza el día en Morro da Urca con panes, frutas y café frente al Pan de Azúcar. Servimos el desayuno todos los días, de 8:30 a 11:30.', 'Mesa de desayuno en Embaixada Carioca', 'Carne a la parrilla con arroz, farofa y patatas del menú de Embaixada Carioca'],
}
def blocks(source):
 return re.findall(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>[\s\S]*?</script>', source, re.I)
def div_span(source, pattern):
 m=re.search(pattern,source,re.I)
 if not m:return None
 depth=0
 for token in re.finditer(r'</?div\b[^>]*>',source[m.start():],re.I):
  depth += -1 if token.group().startswith('</') else 1
  if depth==0:return (m.start(),m.start()+token.end())
 raise ValueError('Unbalanced div')
def migrate(file, lang, kind):
 source=file.read_text(encoding='utf-8')
 if 'data-ec-inner="20260909"' in source:return {'file':str(file.relative_to(ROOT)),'skipped':True}
 before=BeautifulSoup(source,'html.parser')
 menu_before=[str(x) for x in before.select('.menu-item,.cardapio-card,.menu-card')]
 hero=re.search(r'<header\b[^>]*class="(?:page-hero|hero)"[^>]*>[\s\S]*?</header>',source)
 if not hero:raise ValueError(f'Hero not found: {file}')
 soup=BeautifulSoup(hero.group(),'html.parser');h=soup.header;c=COPY[lang]
 h1=h.find('h1');intro=h.select_one('.lede,.hero-sub')
 if intro is None:intro=next((p for p in h.find_all('p') if not p.find_parent(class_='answer-block')),None)
 headline=h1.decode_contents();intro_html=intro.decode_contents() if intro else ''
 image=h.select_one('img.page-hero-photo,.page-hero-photo img')
 src=image.get('src','/assets/hero.webp') if image else '/assets/hero.webp'
 alt=image.get('alt','Embaixada Carioca · Morro da Urca') if image else 'Embaixada Carioca · Morro da Urca'
 srcset=image.get('srcset','') if image else ''
 actions=h.select_one('.ctas,.hero-ctas')
 links=[]
 for i,a in enumerate(actions.find_all('a') if actions else []):
  a['class']=['ec-inner-action']+(['is-primary'] if i==0 else [])
  a.attrs.pop('style',None);links.append(str(a))
 if kind=='cardapio':
  headline=c[1];intro_html=c[2];src='/assets/almoco-picanha-grelhada.webp';alt=c[8];srcset=''
  first=before.select_one('section.menu-section[id]')
  if not first:raise ValueError('Menu category missing')
  links=[f'<a class="ec-inner-action is-primary" href="#{first["id"]}">{c[3]}</a>',f'<a class="ec-inner-action" href="https://go.tagme.com.br/embaixadacarioca">{c[4]}</a>']
 elif kind=='cafe-da-manha':
  headline=c[5];intro_html=c[6];src='/assets/cafe/cafe-da-embaixada-mesa-completa.webp';alt=c[7];srcset=''
 photo=f'<img src="{html.escape(src,quote=True)}" alt="{html.escape(alt,quote=True)}" loading="eager" fetchpriority="high" decoding="async"'+(f' srcset="{html.escape(srcset,quote=True)}" sizes="(max-width: 960px) 100vw, 50vw"' if srcset else '')+'/>'
 hidden=''.join(str(x) for x in h.select('#seo-subtitle'))
 attrs=f' id="{h["id"]}"' if h.get('id') else ''
 fresh=f'''<header class="page-hero ec-inner-hero"{attrs}>
<div class="ec-inner-media">{photo}</div>
<div class="ec-inner-content">
<p class="ec-inner-kicker">{c[0]}</p>
<h1>{headline}</h1>{hidden}
<div class="ec-inner-intro"><p>{intro_html}</p></div>
<div class="ec-inner-actions">{''.join(links)}</div>
</div></header>'''
 # Keep original facts and award attribution outside the photo, not discarded.
 chips=h.select_one('.hero-chips,.chips');fact_text=[]
 if chips:
  for item in chips.find_all(['span','a'],recursive=False):
   fact_text.append('<p>'+html.escape(item.get_text(' ',strip=True).removeprefix('🏆').strip())+'</p>')
 answers=''.join(str(x) for x in h.select('.answer-block'))
 support='<section class="ec-inner-details"><div class="ec-inner-detail-wrap">'+''.join(fact_text)+answers+'</div></section>' if fact_text or answers else ''
 source=source[:hero.start()]+fresh+support+source[hero.end():]
 source=re.sub(r'<body\b', '<body data-ec-inner="20260909"',source,count=1)
 source=re.sub(r'<link\b[^>]*href="/assets/css/ec-design-aaa-fix.css[^\"]*"[^>]*>','',source)
 source=source.replace('</head>','<link rel="stylesheet" href="/assets/css/ec-design-aaa-fix.css?v=20260909-inner"/>\n<link rel="stylesheet" href="/assets/css/ec-inner-pages.css?v=20260909a"/>\n</head>',1)
 span=div_span(source,r'<div\b[^>]*\bid="wa-preview"[^>]*>')
 if span:source=source[:span[0]]+source[span[1]:]
 source=re.sub(r'<script\b[^>]*>[\s\S]*?</script>',lambda m:'' if re.search(r"var preview = document.getElementById\('wa-preview'\)",m.group()) else m.group(),source)
 source=re.sub(r'<span\b[^>]*class="wa-badge"[^>]*>[\s\S]*?</span>','',source)
 assert blocks(source)==blocks(file.read_text(encoding='utf-8')), f'JSON-LD changed: {file}'
 after=BeautifulSoup(source,'html.parser')
 assert menu_before==[str(x) for x in after.select('.menu-item,.cardapio-card,.menu-card')],f'Menu changed: {file}'
 file.write_text(source,encoding='utf-8')
 return {'file':str(file.relative_to(ROOT)), 'schema_unchanged':True,'menu_items_unchanged':len(menu_before),'popup_removed':bool(span)}

if __name__=='__main__':
 result=[]
 for lang,(prefix,names) in GROUPS.items():
  for name in names:result.append(migrate(ROOT/(prefix+name+'.html'),lang,name))
 # Replace only the four decorative bottom-navigation emoji spans; labels/links stay intact.
 icons = {
  '🍽️': '<circle cx="14" cy="12" r="7"/><path d="M3 3v7m3-7v7M3 7h3M4.5 10v11"/>',
  '☀️': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
  '📋': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6m-6 4h6m-6 4h4"/>',
  '📅': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 2v6m10-6v6M3 11h18m-14 5h3m4 0h3"/>',
 }
 for lang,(prefix,names) in GROUPS.items():
  for name in ['index',*names]:
   file=ROOT/(prefix+name+'.html');text=file.read_text(encoding='utf-8')
   if name=='index':
    text=text.replace('ec-design-aaa-fix.css?v=20260909-minimal','ec-design-aaa-fix.css?v=20260909-inner')
   else:
    language_box=div_span(text,r'<div\b[^>]*class="lang-switcher"[^>]*>')
    if language_box:
     fragment=BeautifulSoup(text[language_box[0]:language_box[1]],'html.parser')
     index=names.index(name)
     for a in fragment.select('a[hreflang]'):
      target_lang=a['hreflang'][:2]
      if target_lang in GROUPS:
       target_prefix,target_names=GROUPS[target_lang]
       a['href']='/'+target_prefix+target_names[index]+'.html'
     text=text[:language_box[0]]+str(fragment)+text[language_box[1]:]
   if name!='index' and '/assets/js/ec-inner-navigation.js' not in text:
    text=text.replace('</head>','<script defer src="/assets/js/ec-inner-navigation.js?v=20260909a"></script>\n</head>',1)
   for emoji,paths in icons.items():
    svg=f'<svg aria-hidden="true" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'
    text=text.replace(f'<span class="bnav-icon">{emoji}</span>',f'<span class="bnav-icon">{svg}</span>')
   if name in ('entardecer','sunset','atardecer'):
    old='/assets/'+name+'-banda-opt'
    for match in list(re.finditer(r'<picture\b[^>]*>[\s\S]*?</picture>',text))[::-1]:
     if old in match.group():
      picture=BeautifulSoup(match.group(),'html.parser'); image=picture.find('img')
      if image:
       image['src']='/assets/fotos/banda-pao-de-acucar-01.webp'
       image.attrs.pop('srcset',None)
       text=text[:match.start()]+str(image)+text[match.end():]
    text=text.replace(old+'.webp','/assets/fotos/banda-pao-de-acucar-01.webp')
   file.write_text(text,encoding='utf-8')
 css=ROOT/'assets/css/ec-design-aaa-fix.css'
 text=css.read_text(encoding='utf-8')
 text=text.replace('html body[data-screen-label="Home"] nav','html body:is([data-screen-label="Home"], [data-ec-inner]) nav')
 css.write_text(text,encoding='utf-8')
 sitemap=ROOT/'sitemap.xml'
 content=sitemap.read_text(encoding='utf-8')
 changed={'https://www.embaixadacarioca.com/'+prefix+name+'.html' for prefix,names in GROUPS.values() for name in names}
 content=re.sub(r'<url>[\s\S]*?</url>',lambda m:re.sub(r'<lastmod>[^<]*</lastmod>','<lastmod>2026-09-09</lastmod>',m.group()) if re.search(r'<loc>(.*?)</loc>',m.group()).group(1) in changed else m.group(),content)
 sitemap.write_text(content,encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
