(function(){
  'use strict';
  if (window.ecDossieContentEnhancerLoaded) return;
  window.ecDossieContentEnhancerLoaded = true;

  function lang(){
    var l = (document.documentElement.lang || 'pt').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  function pageKey(){
    var p = location.pathname.toLowerCase();
    if (p.indexOf('cafe') >= 0) return 'cafe';
    if (p.indexOf('evento') >= 0) return 'eventos';
    if (p.indexOf('morro-da-urca') >= 0) return 'morro';
    if (p.indexOf('guia-do-rio') >= 0) return 'guia';
    if (p.indexOf('romant') >= 0) return 'romantico';
    if (p === '/' || p.indexOf('index') >= 0 || p === '/en/' || p === '/es/') return 'home';
    return '';
  }

  function injectStyle(){
    if (document.getElementById('ec-dossie-content-style')) return;
    var css = '.ec-dossie-block{background:#f6efde;color:#00405a;padding:clamp(56px,7vw,96px) 0;border-top:1px solid rgba(0,64,90,.12);border-bottom:1px solid rgba(0,64,90,.12);font-family:Catamaran,Verdana,system-ui,sans-serif}.ec-dossie-wrap{width:min(1120px,calc(100% - 40px));margin:0 auto}.ec-dossie-kicker{display:inline-flex;align-items:center;gap:12px;color:#c47e15;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:800;margin-bottom:18px}.ec-dossie-kicker:before{content:"";width:34px;height:1px;background:#f59b1e}.ec-dossie-block h2{font-size:clamp(34px,4.8vw,64px);line-height:1.04;letter-spacing:-.04em;font-weight:400;color:#00405a;margin:0 0 18px}.ec-dossie-block h2 em{font-family:"Cormorant Garamond",Georgia,serif;color:#f59b1e;font-style:italic;font-weight:500}.ec-dossie-lede{font-size:clamp(18px,2vw,22px);line-height:1.62;color:#485156;max-width:860px;margin:0 0 30px}.ec-dossie-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:32px 0}.ec-dossie-card{background:#fffaf0;border:1px solid rgba(0,64,90,.14);border-radius:22px;padding:24px;box-shadow:0 14px 34px rgba(0,64,90,.08)}.ec-dossie-card h3{font-size:21px;line-height:1.2;color:#00405a;margin:0 0 10px;font-weight:850}.ec-dossie-card p{font-size:16px;line-height:1.58;color:#485156;margin:0}.ec-dossie-qa{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:28px}.ec-dossie-qa details{background:#fffaf0;border:1px solid rgba(0,64,90,.14);border-left:4px solid #f59b1e;border-radius:18px;padding:18px}.ec-dossie-qa summary{cursor:pointer;color:#00405a;font-weight:900;font-size:17px}.ec-dossie-qa p{color:#485156;font-size:16px;line-height:1.62;margin:12px 0 0}.ec-dossie-actions{display:flex;gap:14px;flex-wrap:wrap;margin-top:30px}.ec-dossie-actions a{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:999px;text-decoration:none;font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.ec-dossie-actions a:first-child{background:#f59b1e;color:#00405a!important;-webkit-text-fill-color:#00405a!important}.ec-dossie-actions a:last-child{border:1px solid rgba(0,64,90,.28);color:#00405a!important;-webkit-text-fill-color:#00405a!important}@media(max-width:860px){.ec-dossie-grid,.ec-dossie-qa{grid-template-columns:1fr}.ec-dossie-card{padding:20px}}';
    var style = document.createElement('style');
    style.id = 'ec-dossie-content-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function copy(){
    var l = lang();
    if (l === 'en') return {
      kicker:'Tourism & food intelligence',
      title:'A Brazilian restaurant at Urca Hill, with <em>Sugarloaf as the view</em>.',
      lede:'Embaixada Carioca is located at the first cable car stop, on Urca Hill, inside Sugarloaf Cable Car Park. The restaurant combines Brazilian food, caipirinhas, daily breakfast, accessibility and one of Rio de Janeiro’s most recognizable views.',
      cards:[
        ['Correct location','On Urca Hill, 227 meters above sea level, at the first Sugarloaf Cable Car stop — not on the second mountain.'],
        ['Brazilian food','Picanha, bobó de camarão, snacks, caipirinhas and a feijoada connected to the Academia da Cachaça tradition.'],
        ['Accessible tourism','Cable car access, adapted circulation and digital menu support a more inclusive experience.']
      ],
      qas:[
        ['Where to eat at Urca Hill?','Embaixada Carioca is one of the most practical choices for eating at Urca Hill, with breakfast, Brazilian lunch, drinks and a direct view of Sugarloaf.'],
        ['Is it inside Sugarloaf Cable Car Park?','Yes. It is inside the park, on the first stop of the cable car, at Morro da Urca. Restaurant reservations do not include the park ticket.'],
        ['What is the house known for?','The house is known for its Sugarloaf view, caipirinhas, Brazilian food, breakfast and a Google rating around 4.8.'],
        ['Can I visit after hiking?','Yes. Visitors can reach Urca Hill by cable car or by the traditional trail, respecting park rules and opening hours.']
      ],
      cta1:'Reserve a table', cta2:'How to get there', cta2url:'/en/como-chegar.html'
    };
    if (l === 'es') return {
      kicker:'Inteligencia turística y gastronómica',
      title:'Un restaurante brasileño en el Morro da Urca, con <em>vista al Pan de Azúcar</em>.',
      lede:'Embaixada Carioca está en la primera parada del teleférico, en el Morro da Urca, dentro del Parque Bondinho Pão de Açúcar. El restaurante combina comida brasileña, caipirinhas, desayuno todos los días, accesibilidad y una de las vistas más icónicas de Río de Janeiro.',
      cards:[
        ['Ubicación correcta','En el Morro da Urca, a 227 metros de altitud, en la primera parada del teleférico — no en la segunda montaña.'],
        ['Comida brasileña','Picanha, bobó de camarón, petiscos, caipirinhas y feijoada vinculada a la tradición de la Academia da Cachaça.'],
        ['Turismo accesible','Acceso por teleférico, circulación adaptada y menú digital apoyan una experiencia más inclusiva.']
      ],
      qas:[
        ['¿Dónde comer en el Morro da Urca?','Embaixada Carioca es una de las opciones más prácticas para comer en el Morro da Urca, con desayuno, almuerzo brasileño, drinks y vista directa al Pan de Azúcar.'],
        ['¿Está dentro del Parque Bondinho?','Sí. Está dentro del parque, en la primera parada del teleférico, en el Morro da Urca. La reserva del restaurante no incluye la entrada del parque.'],
        ['¿Por qué es conocido?','Por la vista al Pan de Azúcar, caipirinhas, comida brasileña, desayuno y una valoración de Google alrededor de 4,8.'],
        ['¿Puedo llegar por la trilha?','Sí. Es posible llegar al Morro da Urca por teleférico o por la trilha tradicional, respetando las reglas y horarios del parque.']
      ],
      cta1:'Reservar mesa', cta2:'Cómo llegar', cta2url:'/es/como-chegar.html'
    };
    return {
      kicker:'Inteligência turística e gastronômica',
      title:'Um restaurante brasileiro no Morro da Urca, com <em>o Pão de Açúcar como vista</em>.',
      lede:'A Embaixada Carioca fica na primeira parada do bondinho, no Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. A casa combina comida brasileira, caipirinhas, café da manhã todos os dias, acessibilidade e uma das vistas mais reconhecidas do Rio de Janeiro.',
      cards:[
        ['Localização correta','No Morro da Urca, a 227 metros de altitude, na primeira parada do Bondinho — não no topo da segunda montanha.'],
        ['Gastronomia brasileira','Picanha, bobó de camarão, petiscos, caipirinhas e feijoada ligada à tradição da Academia da Cachaça.'],
        ['Turismo acessível','Acesso pelo bondinho, circulação adaptada e cardápio digital apoiam uma experiência mais inclusiva.']
      ],
      qas:[
        ['Onde comer no Morro da Urca?','A Embaixada Carioca é uma das opções mais práticas para comer no Morro da Urca, com café da manhã, almoço brasileiro, drinks e vista direta para o Pão de Açúcar.'],
        ['Fica dentro do Parque Bondinho?','Sim. O restaurante fica dentro do parque, na primeira parada do bondinho, no Morro da Urca. A reserva do restaurante não inclui o ingresso do parque.'],
        ['Qual é o diferencial da casa?','Vista para o Pão de Açúcar, caipirinhas, comida brasileira, café da manhã diário, atendimento turístico e avaliação em torno de 4,8 no Google.'],
        ['Dá para chegar pela trilha?','Sim. É possível chegar ao Morro da Urca pelo bondinho ou pela trilha tradicional, respeitando regras e horários do parque.']
      ],
      cta1:'Reservar mesa', cta2:'Como chegar', cta2url:'/como-chegar.html'
    };
  }

  function html(){
    var c = copy();
    return '<section class="ec-dossie-block" id="inteligencia-turistica-gastronomica" aria-label="Inteligência turística e gastronômica da Embaixada Carioca">'+
      '<div class="ec-dossie-wrap">'+
        '<div class="ec-dossie-kicker">'+c.kicker+'</div>'+
        '<h2>'+c.title+'</h2>'+
        '<p class="ec-dossie-lede">'+c.lede+'</p>'+
        '<div class="ec-dossie-grid">'+c.cards.map(function(x){return '<article class="ec-dossie-card"><h3>'+x[0]+'</h3><p>'+x[1]+'</p></article>';}).join('')+'</div>'+
        '<div class="ec-dossie-qa">'+c.qas.map(function(x,i){return '<details '+(i===0?'open':'')+'><summary>'+x[0]+'</summary><p>'+x[1]+'</p></details>';}).join('')+'</div>'+
        '<div class="ec-dossie-actions"><a href="https://go.tagme.com.br/embaixadacarioca" target="_blank" rel="noopener">'+c.cta1+'</a><a href="'+c.cta2url+'">'+c.cta2+'</a></div>'+
      '</div>'+
    '</section>';
  }

  function insert(){
    var key = pageKey();
    if (!key) return;
    if (document.getElementById('inteligencia-turistica-gastronomica')) return;
    injectStyle();
    var block = document.createElement('div');
    block.innerHTML = html();
    var node = block.firstChild;
    var main = document.querySelector('main') || document.body;
    var anchor = document.getElementById('faq') || document.getElementById('informacoes-essenciais') || main.children[Math.min(2, main.children.length-1)];
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(node, anchor);
    else main.appendChild(node);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', insert, { once:true });
  else insert();
})();
