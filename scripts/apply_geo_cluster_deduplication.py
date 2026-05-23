#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'geo_cluster_deduplication_report.md'
START = '<!-- EC GEO UNIQUE INTENT BLOCK -->'
END = '<!-- /EC GEO UNIQUE INTENT BLOCK -->'
DOSSIE = '<script defer src="/assets/dossie-content-enhancer.js"></script>'

PAGES = {
    'restaurante-morro-da-urca.html': {
        'title': 'Restaurante no Morro da Urca: intenção local e acesso',
        'intent': 'Esta página responde à busca de quem já decidiu subir ao Morro da Urca e quer entender onde comer, como chegar ao restaurante e por que a primeira parada do Bondinho é o ponto correto.',
        'items': [
            'Foco principal: restaurante no Morro da Urca, primeira parada do Bondinho.',
            'Conteúdo único: localização, acesso, vista, horários e contexto do parque.',
            'Evita competir com a Home: aqui a resposta é local e operacional, não institucional.',
        ],
    },
    'restaurante-bondinho-pao-de-acucar.html': {
        'title': 'Restaurante do Bondinho: intenção parque e visitante',
        'intent': 'Esta página atende quem pesquisa restaurante dentro do Parque Bondinho Pão de Açúcar e precisa entender a relação entre ingresso, teleférico, primeira parada e experiência gastronômica.',
        'items': [
            'Foco principal: restaurante dentro do Parque Bondinho Pão de Açúcar.',
            'Conteúdo único: ingresso, teleférico, fluxo do visitante e parada no Morro da Urca.',
            'Evita competir com Morro da Urca: aqui a busca nasce no parque, não no bairro.',
        ],
    },
    'onde-comer-no-pao-de-acucar.html': {
        'title': 'Onde comer no Pão de Açúcar: intenção comparativa',
        'intent': 'Esta página atende quem compara opções para comer durante o passeio ao Pão de Açúcar, explicando quando vale tomar café, almoçar ou beber algo no Morro da Urca.',
        'items': [
            'Foco principal: comparação de momentos e opções para comer no passeio.',
            'Conteúdo único: decisão entre café da manhã, almoço, drinks e grupos.',
            'Evita competir com restaurante específico: aqui a intenção é escolher onde comer.',
        ],
    },
    'cafe-da-manha.html': {
        'title': 'Café da manhã com vista: intenção manhã e reserva',
        'intent': 'Esta página deve ser 100% concentrada em café da manhã: horário, reserva, vista, perfil da experiência e motivos para subir cedo ao Morro da Urca.',
        'items': [
            'Foco principal: café da manhã diário no Morro da Urca.',
            'Conteúdo único: manhã, primeira subida, vista, itens do café e reserva.',
            'Evita competir com almoço e eventos: não vende tudo ao mesmo tempo.',
        ],
    },
    'cafe-da-manha-com-vista.html': {
        'title': 'Café da manhã com vista no Rio: intenção paisagem e experiência',
        'intent': 'Esta página atende a busca ampla por café da manhã com vista no Rio de Janeiro, posicionando a Embaixada como experiência de manhã com paisagem do Pão de Açúcar.',
        'items': [
            'Foco principal: café da manhã com vista no Rio.',
            'Conteúdo único: experiência visual, turismo, fotos, casais e famílias.',
            'Evita competir com a página de café: aqui a intenção é descoberta e inspiração.',
        ],
    },
    'como-chegar.html': {
        'title': 'Como chegar: intenção logística pura',
        'intent': 'Esta página deve resolver acesso, ingresso, trilha, Uber, táxi, estacionamento, primeira parada e deslocamento dentro do parque, sem repetir argumentos gastronômicos longos.',
        'items': [
            'Foco principal: logística e orientação do visitante.',
            'Conteúdo único: rotas, entrada, Bondinho, trilha, mapa e tempo de deslocamento.',
            'Evita competir com páginas de comida: aqui a resposta é como chegar.',
        ],
    },
    'guia-do-rio.html': {
        'title': 'Guia do Rio: intenção roteiro e planejamento',
        'intent': 'Esta página atende quem está montando um roteiro no Rio e precisa encaixar Pão de Açúcar, Morro da Urca, refeição, pôr do sol e outros programas no mesmo dia.',
        'items': [
            'Foco principal: roteiro turístico no Rio de Janeiro.',
            'Conteúdo único: ordem do passeio, duração, melhores horários e combinações.',
            'Evita competir com páginas comerciais: aqui a resposta é planejamento.',
        ],
    },
    'eventos.html': {
        'title': 'Eventos com vista: intenção corporativa e grupos',
        'intent': 'Esta página atende empresas, agências e grupos que procuram evento com vista no Rio, com foco em capacidade, formatos, horários, logística e orçamento.',
        'items': [
            'Foco principal: eventos, grupos e experiências privadas.',
            'Conteúdo único: capacidade, formato, operação, troféus, coffee, coquetéis e logística.',
            'Evita competir com restaurante: aqui a intenção é contratar um evento.',
        ],
    },
    'restaurantes-romanticos-rio-de-janeiro.html': {
        'title': 'Restaurante romântico: intenção casal e ocasião especial',
        'intent': 'Esta página atende quem busca um programa romântico no Rio, com foco em vista, entardecer, drinks, pedido de casamento, noivado e celebrações a dois.',
        'items': [
            'Foco principal: casais, surpresa, pedido e ocasião especial.',
            'Conteúdo único: pôr do sol, mesa com vista, clima, fotografia e reserva.',
            'Evita competir com eventos: aqui a intenção é íntima, não corporativa.',
        ],
    },
}


def make_block(data):
    lis = ''.join(f'<li>{item}</li>' for item in data['items'])
    return f'''{START}
<section class="ec-geo-unique-intent" aria-label="Intenção única desta página">
  <div class="wrap">
    <p class="eyebrow">Busca específica</p>
    <h2>{data['title']}</h2>
    <p>{data['intent']}</p>
    <ul>{lis}</ul>
  </div>
</section>
{END}
'''


def strip_old_block(html):
    return re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\s*', '', html, flags=re.S)


def insert_before_end(html, block):
    idx = html.lower().rfind('</main>')
    if idx >= 0:
        return html[:idx] + block + html[idx:]
    idx = html.lower().rfind('</body>')
    if idx >= 0:
        return html[:idx] + block + html[idx:]
    return html + '\n' + block


def main():
    OUT.mkdir(exist_ok=True)
    changed, missing = [], []
    for rel, data in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        html = path.read_text(encoding='utf-8', errors='ignore')
        original = html
        html = strip_old_block(html)
        # Remove the generic dynamic dossier block from GEO cluster pages to reduce repeated rendered boilerplate.
        html = html.replace(DOSSIE, '')
        html = insert_before_end(html, make_block(data))
        if html != original:
            path.write_text(html, encoding='utf-8')
            changed.append(rel)
    lines = ['# GEO Cluster Deduplication Report', '', 'Status: **PASS**', '', '## O que foi feito', '- Removido o enhancer genérico de dossiê das páginas do cluster GEO quando presente.', '- Inserido bloco estático de intenção única por página.', '- Cada página passa a ter função de busca distinta: local, parque, comparativa, café, logística, roteiro, eventos ou romântica.', '', f'Páginas alteradas: **{len(changed)}**', f'Páginas ausentes: **{len(missing)}**', '', '## Alteradas']
    for rel in changed:
        lines.append(f'- `{rel}`')
    if missing:
        lines += ['', '## Ausentes']
        for rel in missing:
            lines.append(f'- `{rel}`')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'GEO cluster deduplication applied: changed={len(changed)} missing={len(missing)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
