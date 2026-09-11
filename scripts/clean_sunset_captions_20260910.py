"""Visually checked photo descriptions; no guessed recipes, brands or schedules."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
COPY={
 '': [('Duas taças erguidas em um brinde, com a paisagem do Rio ao fundo','Um brinde com vista para o Rio.'),('Duas taças de coquetel com o Pão de Açúcar ao fundo','Coquetéis com o Pão de Açúcar em primeiro plano.'),('Músicos se apresentando na Embaixada Carioca, com o Pão de Açúcar ao fundo','Música na Embaixada Carioca. Consulte a programação.'),('Risoto de camarão finalizado com ervas','Risoto de camarão.')],
 'en/':[('Two glasses raised in a toast with the Rio landscape in the background','A toast with a view of Rio.'),('Two cocktail glasses with Sugarloaf Mountain in the background','Cocktails with Sugarloaf Mountain in full view.'),('Musicians performing at Embaixada Carioca with Sugarloaf Mountain in the background','Music at Embaixada Carioca. Check the schedule.'),('Shrimp risotto garnished with herbs','Shrimp risotto.')],
 'es/':[('Dos copas brindando con el paisaje de Río al fondo','Un brindis con vista a Río.'),('Dos copas de cóctel con el Pan de Azúcar al fondo','Cócteles con el Pan de Azúcar en primer plano.'),('Músicos actuando en Embaixada Carioca con el Pan de Azúcar al fondo','Música en Embaixada Carioca. Consulta la programación.'),('Risotto de camarones con hierbas','Risotto de camarones.')]
}
for prefix,names in [('', ['entardecer','feijoada']),('en/', ['sunset','entardecer','feijoada']),('es/', ['atardecer','entardecer','feijoada'])]:
 for name in names:
  path=ROOT/(prefix+name+'.html');text=path.read_text(encoding='utf-8')
  before=re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',text)
  count=[0]
  def figure(m):
   block=m.group()
   if re.search(r'/assets/(?:sunset|atardecer)-banda-opt',block):
    # These legacy translated asset paths do not exist. Replace all picture sources.
    block=re.sub(r'<picture>[\s\S]*?</picture>', '<img src="/assets/fotos/banda-pao-de-acucar-01.webp" alt="" width="1200" height="675" loading="lazy" decoding="async" style="width:100%;height:320px;object-fit:cover;display:block;"/>',block)
   for asset,(alt,caption) in zip(['gin-tonic-vista','cocktails-vista','banda-pao-de-acucar-01','bobo-camarao-real'],COPY[prefix]):
    if asset in block:
     block=re.sub(r'(<img\b[^>]*\balt=")[^"]*(")',lambda x:x[1]+alt+x[2],block)
     block=re.sub(r'(<figcaption\b[^>]*>)[\s\S]*?(</figcaption>)',lambda x:x[1]+caption+x[2],block)
     count[0]+=1
   return block
  text=re.sub(r'<figure\b[^>]*>[\s\S]*?</figure>',figure,text)
  # Only canonical sunset pages have the current shared inner-page layout.
  if name in ('entardecer','sunset','atardecer') and 'data-ec-inner="20260909"' in text:
   def section(m):
    block=m.group();tag=re.match(r'<section\b[^>]*>',block).group()
    if 'class="gallery-section' in tag:
     block=block.replace('class="gallery-section"','class="gallery-section light-section ec-reading-section"',1)
    return block
   text=re.sub(r'<section\b[^>]*>[\s\S]*?</section>',section,text)
   if 'id="ec-editorial-page"' not in text:
    text=text.replace('<body ','<body id="ec-editorial-page" data-ec-legacy-clean="20260910" ',1)
   if '/assets/css/ec-legacy-reading.css?' not in text:
    text=text.replace('</head>','<link rel="stylesheet" href="/assets/css/ec-legacy-reading.css?v=20260910b"/>\n</head>',1)
  text=text.replace('/assets/css/ec-legacy-reading.css?v=20260910a','/assets/css/ec-legacy-reading.css?v=20260910b')
  assert before==re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',text)
  path.write_text(text,encoding='utf-8');print(prefix+name,count[0])
