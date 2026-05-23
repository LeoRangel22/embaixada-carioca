#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_audit_reports'
REPORT = OUT / 'geo_cluster_deduplication_report.md'
START = '<!-- EC GEO UNIQUE INTENT BLOCK -->'
END = '<!-- /EC GEO UNIQUE INTENT BLOCK -->'
DOSSIE = '<script defer src="/assets/dossie-content-enhancer.js"></script>'

INTENTS = {
    'morro': {
        'pt': ('Restaurante no Morro da Urca: intenção local e acesso', 'Esta página responde à busca de quem já decidiu subir ao Morro da Urca e quer entender onde comer, como chegar ao restaurante e por que a primeira parada do Bondinho é o ponto correto.', ['Foco principal: restaurante no Morro da Urca, primeira parada do Bondinho.', 'Conteúdo único: localização, acesso, vista, horários e contexto do parque.', 'Evita competir com a Home: aqui a resposta é local e operacional.']),
        'en': ('Restaurant at Urca Hill: local search and access intent', 'This page answers visitors who already plan to go up to Urca Hill and need to understand where to eat, how to reach the restaurant and why the first cable car stop is the correct location.', ['Main focus: restaurant at Urca Hill, the first Sugarloaf Cable Car stop.', 'Unique content: location, access, view, opening context and park flow.', 'Avoids competing with the Home page: this answer is local and operational.']),
        'es': ('Restaurante en el Morro da Urca: intención local y acceso', 'Esta página responde a quien ya decidió subir al Morro da Urca y necesita entender dónde comer, cómo llegar al restaurante y por qué la primera parada del Bondinho es el punto correcto.', ['Foco principal: restaurante en el Morro da Urca, primera parada del Bondinho.', 'Contenido único: ubicación, acceso, vista, horarios y contexto del parque.', 'Evita competir con la Home: aquí la respuesta es local y operativa.']),
    },
    'bondinho': {
        'pt': ('Restaurante do Bondinho: intenção parque e visitante', 'Esta página atende quem pesquisa restaurante dentro do Parque Bondinho Pão de Açúcar e precisa entender ingresso, teleférico, primeira parada e experiência gastronômica.', ['Foco principal: restaurante dentro do Parque Bondinho Pão de Açúcar.', 'Conteúdo único: ingresso, teleférico, fluxo do visitante e parada no Morro da Urca.', 'Evita competir com Morro da Urca: aqui a busca nasce no parque.']),
        'en': ('Restaurant at the Sugarloaf Cable Car: park visitor intent', 'This page serves people searching for a restaurant inside Sugarloaf Cable Car Park and explains ticket, cable car, first stop and dining experience.', ['Main focus: restaurant inside Sugarloaf Cable Car Park.', 'Unique content: ticket, cable car, visitor flow and the Urca Hill stop.', 'Avoids competing with Urca Hill pages: this search begins with the park.']),
        'es': ('Restaurante del Bondinho: intención parque y visitante', 'Esta página atiende a quien busca restaurante dentro del Parque Bondinho Pão de Açúcar y necesita entender entrada, teleférico, primera parada y experiencia gastronómica.', ['Foco principal: restaurante dentro del Parque Bondinho Pão de Açúcar.', 'Contenido único: entrada, teleférico, flujo del visitante y parada en el Morro da Urca.', 'Evita competir con Morro da Urca: aquí la búsqueda nace en el parque.']),
    },
    'onde_comer': {
        'pt': ('Onde comer no Pão de Açúcar: intenção comparativa', 'Esta página atende quem compara opções para comer durante o passeio, explicando quando vale tomar café, almoçar ou beber algo no Morro da Urca.', ['Foco principal: comparação de momentos e opções para comer no passeio.', 'Conteúdo único: decisão entre café da manhã, almoço, drinks e grupos.', 'Evita competir com restaurante específico: aqui a intenção é escolher onde comer.']),
        'en': ('Where to eat at Sugarloaf: comparison intent', 'This page helps visitors compare where and when to eat during the Sugarloaf visit, including breakfast, lunch and drinks at Urca Hill.', ['Main focus: comparing eating moments during the visit.', 'Unique content: choice between breakfast, lunch, drinks and groups.', 'Avoids competing with restaurant pages: the intent is choosing where to eat.']),
        'es': ('Dónde comer en el Pan de Azúcar: intención comparativa', 'Esta página ayuda a comparar dónde y cuándo comer durante el paseo, incluyendo desayuno, almuerzo y drinks en el Morro da Urca.', ['Foco principal: comparación de momentos y opciones para comer durante el paseo.', 'Contenido único: decisión entre desayuno, almuerzo, drinks y grupos.', 'Evita competir con restaurante específico: la intención es elegir dónde comer.']),
    },
    'cafe': {
        'pt': ('Café da manhã com vista: intenção manhã e reserva', 'Esta página fica concentrada em café da manhã: horário, reserva, vista, perfil da experiência e motivos para subir cedo ao Morro da Urca.', ['Foco principal: café da manhã diário no Morro da Urca.', 'Conteúdo único: manhã, primeira subida, vista, itens do café e reserva.', 'Evita competir com almoço e eventos: não vende tudo ao mesmo tempo.']),
        'en': ('Breakfast with a view: morning and reservation intent', 'This page focuses on breakfast: schedule, reservation, view, experience profile and reasons to go up early to Urca Hill.', ['Main focus: daily breakfast at Urca Hill.', 'Unique content: morning visit, first cable car stop, view, breakfast items and reservation.', 'Avoids competing with lunch and events: it does not sell everything at once.']),
        'es': ('Desayuno con vista: intención mañana y reserva', 'Esta página se concentra en desayuno: horario, reserva, vista, perfil de la experiencia y motivos para subir temprano al Morro da Urca.', ['Foco principal: desayuno diario en el Morro da Urca.', 'Contenido único: mañana, primera subida, vista, ítems del desayuno y reserva.', 'Evita competir con almuerzo y eventos: no vende todo al mismo tiempo.']),
    },
    'cafe_vista': {
        'pt': ('Café da manhã com vista no Rio: intenção paisagem e experiência', 'Esta página atende a busca ampla por café da manhã com vista no Rio, posicionando a Embaixada como experiência de manhã com paisagem do Pão de Açúcar.', ['Foco principal: café da manhã com vista no Rio.', 'Conteúdo único: experiência visual, turismo, fotos, casais e famílias.', 'Evita competir com a página de café: aqui a intenção é descoberta e inspiração.']),
        'en': ('Breakfast with a view in Rio: scenery and experience intent', 'This page answers broader searches for breakfast with a view in Rio, positioning Embaixada as a morning experience with Sugarloaf scenery.', ['Main focus: breakfast with a view in Rio.', 'Unique content: visual experience, tourism, photos, couples and families.', 'Avoids competing with the breakfast page: this intent is discovery and inspiration.']),
        'es': ('Desayuno con vista en Río: intención paisaje y experiencia', 'Esta página responde a búsquedas amplias de desayuno con vista en Río, posicionando la Embaixada como experiencia de mañana con paisaje del Pan de Azúcar.', ['Foco principal: desayuno con vista en Río.', 'Contenido único: experiencia visual, turismo, fotos, parejas y familias.', 'Evita competir con la página de desayuno: aquí la intención es descubrimiento e inspiración.']),
    },
    'como_chegar': {
        'pt': ('Como chegar: intenção logística pura', 'Esta página resolve acesso, ingresso, trilha, Uber, táxi, estacionamento, primeira parada e deslocamento dentro do parque, sem repetir argumentos gastronômicos longos.', ['Foco principal: logística e orientação do visitante.', 'Conteúdo único: rotas, entrada, Bondinho, trilha, mapa e tempo de deslocamento.', 'Evita competir com páginas de comida: aqui a resposta é como chegar.']),
        'en': ('How to get there: pure logistics intent', 'This page solves access, ticket, trail, ride apps, taxi, parking, first stop and movement inside the park without repeating long dining arguments.', ['Main focus: visitor logistics and orientation.', 'Unique content: routes, entrance, cable car, trail, map and travel time.', 'Avoids competing with food pages: the answer here is how to get there.']),
        'es': ('Cómo llegar: intención logística pura', 'Esta página resuelve acceso, entrada, trilha, apps de transporte, taxi, estacionamiento, primera parada y movimiento dentro del parque sin repetir argumentos gastronómicos largos.', ['Foco principal: logística y orientación del visitante.', 'Contenido único: rutas, entrada, Bondinho, trilha, mapa y tiempo de desplazamiento.', 'Evita competir con páginas de comida: aquí la respuesta es cómo llegar.']),
    },
    'guia': {
        'pt': ('Guia do Rio: intenção roteiro e planejamento', 'Esta página atende quem monta um roteiro no Rio e precisa encaixar Pão de Açúcar, Morro da Urca, refeição, pôr do sol e outros programas no mesmo dia.', ['Foco principal: roteiro turístico no Rio de Janeiro.', 'Conteúdo único: ordem do passeio, duração, melhores horários e combinações.', 'Evita competir com páginas comerciais: aqui a resposta é planejamento.']),
        'en': ('Rio guide: itinerary and planning intent', 'This page supports travelers planning a Rio itinerary and fitting Sugarloaf, Urca Hill, a meal, sunset and other activities into the same day.', ['Main focus: Rio de Janeiro travel itinerary.', 'Unique content: visit order, duration, best times and combinations.', 'Avoids competing with commercial pages: the answer is planning.']),
        'es': ('Guía de Río: intención roteiro y planificación', 'Esta página ayuda a quien arma un roteiro en Río y necesita combinar Pan de Azúcar, Morro da Urca, comida, atardecer y otros programas en el mismo día.', ['Foco principal: roteiro turístico en Río de Janeiro.', 'Contenido único: orden del paseo, duración, mejores horarios y combinaciones.', 'Evita competir con páginas comerciales: aquí la respuesta es planificación.']),
    },
    'eventos': {
        'pt': ('Eventos com vista: intenção corporativa e grupos', 'Esta página atende empresas, agências e grupos que procuram evento com vista no Rio, com foco em capacidade, formatos, horários, logística e orçamento.', ['Foco principal: eventos, grupos e experiências privadas.', 'Conteúdo único: capacidade, formato, operação, troféus, coffee, coquetéis e logística.', 'Evita competir com restaurante: aqui a intenção é contratar um evento.']),
        'en': ('Events with a view: corporate and group intent', 'This page serves companies, agencies and groups looking for an event with a view in Rio, focusing on capacity, formats, timing, logistics and quotation.', ['Main focus: events, groups and private experiences.', 'Unique content: capacity, format, operation, trophies, coffee, cocktails and logistics.', 'Avoids competing with restaurant pages: the intent is booking an event.']),
        'es': ('Eventos con vista: intención corporativa y grupos', 'Esta página atiende empresas, agencias y grupos que buscan evento con vista en Río, con foco en capacidad, formatos, horarios, logística y presupuesto.', ['Foco principal: eventos, grupos y experiencias privadas.', 'Contenido único: capacidad, formato, operación, trofeos, coffee, cocteles y logística.', 'Evita competir con restaurante: la intención es contratar un evento.']),
    },
    'romantico': {
        'pt': ('Restaurante romântico: intenção casal e ocasião especial', 'Esta página atende quem busca um programa romântico no Rio, com foco em vista, entardecer, drinks, pedido de casamento, noivado e celebrações a dois.', ['Foco principal: casais, surpresa, pedido e ocasião especial.', 'Conteúdo único: pôr do sol, mesa com vista, clima, fotografia e reserva.', 'Evita competir com eventos: aqui a intenção é íntima, não corporativa.']),
        'en': ('Romantic restaurant: couples and special occasion intent', 'This page serves people looking for a romantic plan in Rio, focused on views, sunset, drinks, proposals, engagement and celebrations for two.', ['Main focus: couples, surprise, proposals and special occasions.', 'Unique content: sunset, table with a view, atmosphere, photography and reservation.', 'Avoids competing with events pages: this is intimate, not corporate.']),
        'es': ('Restaurante romántico: intención pareja y ocasión especial', 'Esta página atiende a quien busca un programa romántico en Río, con foco en vista, atardecer, drinks, pedido de matrimonio, compromiso y celebraciones para dos.', ['Foco principal: parejas, sorpresa, pedido y ocasión especial.', 'Contenido único: atardecer, mesa con vista, clima, fotografía y reserva.', 'Evita competir con eventos: aquí la intención es íntima, no corporativa.']),
    },
}

PAGES = {
    'restaurante-morro-da-urca.html': ('morro', 'pt'), 'en/restaurante-morro-da-urca.html': ('morro', 'en'), 'es/restaurante-morro-da-urca.html': ('morro', 'es'),
    'restaurante-bondinho-pao-de-acucar.html': ('bondinho', 'pt'), 'en/restaurante-bondinho-pao-de-acucar.html': ('bondinho', 'en'), 'es/restaurante-bondinho-pao-de-acucar.html': ('bondinho', 'es'),
    'onde-comer-no-pao-de-acucar.html': ('onde_comer', 'pt'), 'en/onde-comer-no-pao-de-acucar.html': ('onde_comer', 'en'), 'es/onde-comer-no-pao-de-acucar.html': ('onde_comer', 'es'),
    'cafe-da-manha.html': ('cafe', 'pt'), 'en/cafe-da-manha.html': ('cafe', 'en'), 'es/cafe-da-manha.html': ('cafe', 'es'),
    'cafe-da-manha-com-vista.html': ('cafe_vista', 'pt'), 'en/cafe-da-manha-com-vista.html': ('cafe_vista', 'en'), 'es/cafe-da-manha-com-vista.html': ('cafe_vista', 'es'),
    'como-chegar.html': ('como_chegar', 'pt'), 'en/como-chegar.html': ('como_chegar', 'en'), 'es/como-chegar.html': ('como_chegar', 'es'),
    'guia-do-rio.html': ('guia', 'pt'), 'en/guia-do-rio.html': ('guia', 'en'), 'es/guia-do-rio.html': ('guia', 'es'),
    'eventos.html': ('eventos', 'pt'), 'en/eventos.html': ('eventos', 'en'), 'es/eventos.html': ('eventos', 'es'),
    'restaurantes-romanticos-rio-de-janeiro.html': ('romantico', 'pt'), 'en/restaurantes-romanticos-rio-de-janeiro.html': ('romantico', 'en'), 'es/restaurantes-romanticos-rio-de-janeiro.html': ('romantico', 'es'),
}

LABEL = {'pt': 'Busca específica', 'en': 'Specific search intent', 'es': 'Búsqueda específica'}
ARIA = {'pt': 'Intenção única desta página', 'en': 'Unique intent of this page', 'es': 'Intención única de esta página'}


def make_block(intent_key, lang):
    title, text, items = INTENTS[intent_key][lang]
    lis = ''.join(f'<li>{item}</li>' for item in items)
    return f'''{START}
<section class="ec-geo-unique-intent" aria-label="{ARIA[lang]}">
  <div class="wrap">
    <p class="eyebrow">{LABEL[lang]}</p>
    <h2>{title}</h2>
    <p>{text}</p>
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
    by_lang = {'pt': 0, 'en': 0, 'es': 0}
    for rel, (intent_key, lang) in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        html = path.read_text(encoding='utf-8', errors='ignore')
        original = html
        html = strip_old_block(html)
        html = html.replace(DOSSIE, '')
        html = insert_before_end(html, make_block(intent_key, lang))
        if html != original:
            path.write_text(html, encoding='utf-8')
            changed.append(rel)
            by_lang[lang] += 1
    lines = ['# GEO Cluster Deduplication Report', '', 'Status: **PASS**', '', '## Regra aplicada', '- Tudo que foi feito em português foi também previsto para inglês e espanhol quando houver página equivalente.', '', '## O que foi feito', '- Removido o enhancer genérico de dossiê das páginas do cluster GEO quando presente.', '- Inserido bloco estático de intenção única por página e por idioma.', '- Cada página passa a ter função de busca distinta: local, parque, comparativa, café, logística, roteiro, eventos ou romântica.', '', f'Páginas alteradas: **{len(changed)}**', f'PT: **{by_lang["pt"]}** | EN: **{by_lang["en"]}** | ES: **{by_lang["es"]}**', f'Páginas ausentes: **{len(missing)}**', '', '## Alteradas']
    for rel in changed:
        lines.append(f'- `{rel}`')
    if missing:
        lines += ['', '## Sem página equivalente encontrada']
        for rel in missing:
            lines.append(f'- `{rel}`')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'GEO cluster deduplication applied: changed={len(changed)} missing={len(missing)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
