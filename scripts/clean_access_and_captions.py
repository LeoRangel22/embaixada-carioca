"""Bounded readability, repeated-access-content and visually verified caption fixes."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
for prefix,name,extra in [('', 'como-chegar','Para fins de semana, feriados ou visitas em grupo, consulte a equipe e planeje sua reserva com antecedência.'),('en/','how-to-get-there','For weekends, holidays or group visits, contact our team and plan your reservation in advance.'),('es/','como-llegar','Para fines de semana, festivos o visitas en grupo, consulta con nuestro equipo y planifica tu reserva con antelación.')]:
 file=ROOT/(prefix+name+'.html');text=file.read_text(encoding='utf-8');before=re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',text)
 if 'data-ec-access-clean' not in text:
  for cls in ('ec-featured-snippet-ol','ec-sprint5-quality'):
   text,count=re.subn(r'<section\b[^>]*class="'+cls+r'"[^>]*>[\s\S]*?</section>','',text)
   print(file.name,cls,count)
  text=re.sub(r'(<section class="ec-sprint4-steps">[\s\S]*?)(</div></section>)',lambda m:m.group(1)+'<p>'+extra+'</p>'+m.group(2),text,count=1)
  text=text.replace('<body ','<body data-ec-access-clean="20260909" ',1).replace('<main>','<main id="ec-access-main">',1)
  # Explicit light-section semantics prevent legacy dark-theme rules from matching.
  start=text.index('<main');end=text.index('</main>',start)
  chunk=text[start:end]
  chunk=re.sub(r'(<section\b[^>]*class=")([^"]*)(")',lambda m:m.group(1)+m.group(2)+' light-section'+m.group(3),chunk)
  text=text[:start]+chunk+text[end:]
  text=text.replace('</head>','<link rel="stylesheet" href="/assets/css/ec-access-clean.css?v=20260909a"/>\n</head>',1)
 text=re.sub(r'<script id="ec-como-chegar-runtime-visible-lock">[\s\S]*?</script>','',text)
 text=re.sub(r'(<section\b[^>]*class="ec-priority-query-fix[^>]*>)([\s\S]*?)(</section>)',lambda m:m.group(1)+re.sub(r'<ol\b[^>]*>[\s\S]*?</ol>','',m.group(2))+m.group(3),text)
 assert before==re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>',text)
 file.write_text(text,encoding='utf-8')
COPIES={
'': [('Visitante com xícara e o Pão de Açúcar ao fundo','Uma pausa com vista para o Pão de Açúcar.'),('Visitante com taça e o Pão de Açúcar ao fundo','Um brinde à paisagem do Rio.')],
'en/':[('Visitor holding a cup with Sugarloaf Mountain in the background','A break with a view of Sugarloaf Mountain.'),('Visitor holding a glass with Sugarloaf Mountain in the background','A toast to the Rio landscape.')],
'es/':[('Visitante con una taza y el Pan de Azúcar al fondo','Una pausa con vista al Pan de Azúcar.'),('Visitante con una copa y el Pan de Azúcar al fondo','Un brindis por el paisaje de Río.')]
}
for prefix,copy in COPIES.items():
 file=ROOT/(prefix+'eventos.html');text=file.read_text(encoding='utf-8')
 def figure(m):
  result=m.group()
  for asset,(alt,caption) in zip(('evento-chandon-opt','grupo-amigos-opt'),copy):
   if asset in result:
    result=re.sub(r'(<img\b[^>]*\balt=")[^"]*(")',lambda x:x.group(1)+alt+x.group(2),result)
    result=re.sub(r'(<figcaption\b[^>]*>)[\s\S]*?(</figcaption>)',lambda x:x.group(1)+caption+x.group(2),result)
  return result
 text=re.sub(r'<figure\b[^>]*>[\s\S]*?</figure>',figure,text)
 file.write_text(text,encoding='utf-8')
