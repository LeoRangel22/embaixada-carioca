"""Repair audited footer links and provide localized visitor-assistance guidance."""
from pathlib import Path
import re
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
DATA={
'':('como-chegar','Acessibilidade','Planeje uma visita com mais conforto','Se você ou alguém do seu grupo tem necessidades específicas de mobilidade ou atendimento, converse com nossa equipe antes de reservar. Confirme também com o Parque Bondinho as condições de acesso ao Morro da Urca.','Informe a data prevista, o número de pessoas e o apoio necessário. Assim, a equipe pode orientar sua visita sem depender de informações genéricas.','Consultar a equipe','Olá! Gostaria de confirmar as condições de acessibilidade para minha visita à Embaixada Carioca.'),
'en/':('how-to-get-there','Accessibility','Plan a more comfortable visit','If you or someone in your group has specific mobility or assistance needs, contact our team before booking. Please also confirm access arrangements for Urca Hill with Sugarloaf Cable Car Park.','Share your planned date, group size and the assistance you need so our team can provide guidance for your visit.','Contact our team','Hello! I would like to confirm accessibility arrangements for my visit to Embaixada Carioca.'),
'es/':('como-llegar','Accesibilidad','Planifica una visita más cómoda','Si tú o alguien de tu grupo tiene necesidades específicas de movilidad o asistencia, consulta con nuestro equipo antes de reservar. Confirma también con el Parque Bondinho las condiciones de acceso al Morro da Urca.','Indica la fecha prevista, el número de personas y el apoyo necesario para que nuestro equipo pueda orientarte.','Consultar al equipo','¡Hola! Quisiera confirmar las condiciones de accesibilidad para mi visita a Embaixada Carioca.')}
for prefix,(name,label,title,p1,p2,cta,message) in DATA.items():
 files=[ROOT/(prefix+n+'.html') for n in ('cardapio','almoco','cafe-da-manha','eventos',name,'guia-do-rio','feijoada', 'entardecer' if not prefix else 'sunset' if prefix=='en/' else 'atardecer')]
 for file in files:
  text=file.read_text(encoding='utf-8')
  text=text.replace(f'<a href="#">{label}</a>',f'<a href="/{prefix}{name}.html#visit-accessibility">{label}</a>')
  if file.name==name+'.html':
   if 'id="visit-accessibility"' not in text:
    block=f'<section id="visit-accessibility" aria-labelledby="visit-accessibility-title"><div><h2 id="visit-accessibility-title">{title}</h2><p>{p1}</p><p>{p2}</p><a href="https://wa.me/5521966837556?text={quote(message)}">{cta}</a></div></section>'
    text=text.replace('</main>',block+'</main>',1)
   if prefix:
    text=text.replace('<main>','<main id="conteudo-principal" tabindex="-1">',1)
    text=text.replace('>Pular para o conteúdo principal</a>','>'+('Skip to main content' if prefix=='en/' else 'Saltar al contenido principal')+'</a>')
  text=text.replace('ec-inner-pages.css?v=20260909a','ec-inner-pages.css?v=20260909b')
  file.write_text(text,encoding='utf-8')
