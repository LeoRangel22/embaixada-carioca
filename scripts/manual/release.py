#!/usr/bin/env python3
"""Package the reviewed 5-slide manual and bind its release to operational sources."""
from pathlib import Path
import json,hashlib,html,sys,shutil
ROOT=Path(__file__).resolve().parents[2]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def sources():
 return sorted(set([p for pat in ['abastecer/*.js','abastecer/*.css','abastecer/*.html','functions/abastecer/*.js','scripts/abastecer-apps-script/*'] for p in ROOT.glob(pat)]))
def operation_hash():return hashlib.sha256(json.dumps({str(p.relative_to(ROOT)):digest(p) for p in sources()},sort_keys=True).encode()).hexdigest()
def main():
 v=sys.argv[1];build=Path(sys.argv[2]);d=ROOT/'abastecer/manual'/v
 if (d/'release.json').exists():raise SystemExit('Versão já fechada. Crie outra versão, preservando o histórico.')
 data=json.loads((d/'conteudo.json').read_text());assert data['version']==v and len(data['slides'])==5
 for i in range(1,6):shutil.copy(build/'build'/f'slide-{i}.png',d/f'slide-{i}.png')
 for ext in ['pptx','pdf']:shutil.copy(build/'output'/f'Manual-Embaixada-Carioca-{v}.{ext}',d/f'Manual-Embaixada-Carioca-{v}.{ext}')
 sections=[]
 for i,s in enumerate(data['slides'],1):
  details='<h2>'+html.escape(s['title'])+'</h2><p>'+html.escape(s['subtitle'])+'</p>'
  if 'table' in s:details+='<table>'+''.join('<tr>'+''.join('<td>'+html.escape(c)+'</td>' for c in row)+'</tr>' for row in s['table'])+'</table>'
  if 'formula' in s:details+='<p>'+html.escape(s['formula'])+'</p>'
  details+='<ol>'+''.join('<li>'+html.escape(x)+'</li>' for x in s['steps'])+'</ol><p>'+html.escape(s['note'])+'</p>'
  sections.append(f'<section id="passo-{i}" aria-label="Passo {i}: {html.escape(s["title"])}"><img src="slide-{i}.png" width="720" height="1280" alt="Passo {i}: {html.escape(s["title"])}. Instruções na versão em texto logo abaixo." loading="{ "eager" if i==1 else "lazy"}"><details><summary>Ler passo {i} em texto</summary>{details}</details></section>')
 page='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#00405a"><title>Como usar • Embaixada Carioca</title><link rel="stylesheet" href="../manual.css"></head><body><header><a href="/abastecer/">Voltar ao app</a><span>Manual '''+v+'''</span></header><main>'''+''.join(sections)+'''<footer><h2>Manual no seu celular</h2><p>Guarde o PDF para consultar durante o turno.</p><a href="Manual-Embaixada-Carioca-'''+v+'''.pdf">Baixar PDF vertical</a><a href="Manual-Embaixada-Carioca-'''+v+'''.pptx">Baixar apresentação editável</a><a href="../">Consultar versão atual</a></footer></main></body></html>'''
 from build_online import build_online
 build_online(d)
 files={p.name:digest(p) for p in d.iterdir() if p.is_file() and p.name!='release.json'}
 release={'version':v,'appVersion':v,'operationalDigest':operation_hash(),'contentDigest':digest(d/'conteudo.json'),'files':files}
 (d/'release.json').write_text(json.dumps(release,indent=2));(d.parent/'current.json').write_text(json.dumps({'version':v,'path':v+'/','operationalDigest':release['operationalDigest']},indent=2))
 (d.parent/'index.html').write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url='+v+'/"><title>Manual da Embaixada Carioca</title></head><body><a href="'+v+'/">Abrir manual atual '+v+'</a></body></html>')
 print('Manual fechado: '+v)
if __name__=='__main__':main()
