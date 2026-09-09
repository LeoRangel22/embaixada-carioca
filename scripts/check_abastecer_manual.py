#!/usr/bin/env python3
"""Reject a site build when its operational code no longer matches its manual."""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'manual'))
from release import ROOT,digest,operation_hash

def check():
 folder=ROOT/'abastecer/manual';current=json.loads((folder/'current.json').read_text());version=current['version'];d=folder/version;release=json.loads((d/'release.json').read_text());content=json.loads((d/'conteudo.json').read_text())
 assert version==release['version']==release['appVersion']==content['version'],'Versão do manual divergente'
 assert len(content['slides'])==5,'O manual deve ter cinco slides'
 assert release['operationalDigest']==operation_hash()==current['operationalDigest'],'App mudou: atualize o conteúdo e crie uma nova versão do manual antes de publicar'
 assert release['contentDigest']==digest(d/'conteudo.json'),'Conteúdo alterado sem gerar apresentação'
 for f,h in release['files'].items():assert digest(d/f)==h,'Arquivo do manual alterado: '+f
 for f in ['abastecer/index.html','scripts/abastecer-apps-script/Index.html']:
  source=(ROOT/f).read_text();assert f'data-app-version="{version}"' in source and f'/manual/{version}/' in source,'O app deve ligar ao manual da mesma versão'
 print('Manual e app sincronizados: '+version)
if __name__=='__main__':check()
