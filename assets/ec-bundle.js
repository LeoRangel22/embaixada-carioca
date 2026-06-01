/* ec-bundle.js — consolidated site scripts
 * Replaces: bondinho-ticket-notice.js, conversion-tracking.js, r2d2-dynamic-banner.js, internal-page-contrast-rescue.js, dossie-content-enhancer.js, menuitem-schema-enhancer.js
 * geo-proximity.js kept separate (subset of pages). */

/* === bondinho-ticket-notice.js === */
(function(){
  'use strict';
  if (window.ecBondinhoTicketNoticeLoaded) return;
  window.ecBondinhoTicketNoticeLoaded = true;

  function lang(){
    var l = (document.documentElement.lang || 'pt').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  var copy = {
    pt: 'A reserva no restaurante não inclui o ingresso do Parque Bondinho. Para subir de bondinho, compre o ingresso do parque separadamente.',
    en: 'Restaurant reservations do not include the Sugarloaf Cable Car Park ticket. To ride the cable car, buy the park ticket separately.',
    es: 'La reserva del restaurante no incluye la entrada del Parque Bondinho. Para subir en teleférico, compre la entrada del parque por separado.'
  };

  function injectStyle(){
    if (document.getElementById('ec-bondinho-ticket-notice-style')) return;
    var css = '.ec-bondinho-ticket-notice{display:block;margin:.65rem 0 0;padding:.72rem .9rem;border-radius:14px;background:rgba(245,155,30,.13);border:1px solid rgba(245,155,30,.38);color:#00405a!important;-webkit-text-fill-color:#00405a!important;font-family:Catamaran,Verdana,system-ui,sans-serif;font-size:.92rem;line-height:1.38;font-weight:700;max-width:560px}.hero-ctas .ec-bondinho-ticket-notice,.ctas .ec-bondinho-ticket-notice{flex-basis:100%}section[style*="background:#00405a"] .ec-bondinho-ticket-notice,section[style*="background: #00405a"] .ec-bondinho-ticket-notice,section[style*="background:#1a2e24"] .ec-bondinho-ticket-notice,section[style*="background: #1a2e24"] .ec-bondinho-ticket-notice{background:rgba(245,155,30,.16);border-color:rgba(245,155,30,.42);color:#f6efde!important;-webkit-text-fill-color:#f6efde!important}@media(max-width:760px){.ec-bondinho-ticket-notice{font-size:.86rem;max-width:100%}}';
    var style = document.createElement('style');
    style.id = 'ec-bondinho-ticket-notice-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function isReservationLink(a){
    var href = (a.getAttribute('href') || '').toLowerCase();
    var text = (a.textContent || '').toLowerCase();
    return href.indexOf('tagme.com.br') >= 0 || /reserv|reserve|reserva/.test(text);
  }

  function addNotice(link){
    var parent = link.parentElement;
    if (!parent || parent.querySelector('.ec-bondinho-ticket-notice')) return;
    var note = document.createElement('small');
    note.className = 'ec-bondinho-ticket-notice';
    note.textContent = copy[lang()];
    parent.appendChild(note);
  }

  function run(){
    injectStyle();
    Array.prototype.slice.call(document.querySelectorAll('a[href]')).forEach(function(a){
      if (!isReservationLink(a)) return;
      var nearHero = a.closest('.hero-ctas,.ctas,.ec-faq-actions,.seo-conversion-block,.guia-reservation-links,header,main,section');
      if (!nearHero) return;
      addNotice(a);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once:true });
  else run();
  window.addEventListener('load', run, { once:true });
})();

/* === conversion-tracking.js === */
(function(){
  'use strict';
  if (window.ecConversionTrackingLoaded) return;
  window.ecConversionTrackingLoaded = true;

  function pushEvent(name, params){
    params = params || {};
    params.event_category = params.event_category || 'conversion';
    params.transport_type = params.transport_type || 'beacon';
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params));
    if (typeof window.gtag === 'function') {
      try { window.gtag('event', name, params); } catch(e) {}
    }
  }

  function classify(url){
    var u = (url || '').toLowerCase();
    if (u.indexOf('go.tagme.com.br') >= 0 || u.indexOf('tagme.com.br') >= 0) return 'tagme_reservation';
    if (u.indexOf('wa.me') >= 0 || u.indexOf('api.whatsapp.com') >= 0 || u.indexOf('whatsapp') >= 0) return 'whatsapp';
    if (u.indexOf('mailto:') === 0) return 'email';
    if (u.indexOf('tel:') === 0) return 'phone';
    return '';
  }

  document.addEventListener('click', function(evt){
    var link = evt.target && evt.target.closest ? evt.target.closest('a[href]') : null;
    if (!link) return;
    var href = link.getAttribute('href') || '';
    var type = classify(href);
    if (!type) return;

    pushEvent('ec_outbound_conversion_click', {
      conversion_type: type,
      link_url: link.href || href,
      link_text: (link.textContent || '').trim().slice(0, 120),
      page_path: location.pathname,
      page_title: document.title,
      language: document.documentElement.lang || '',
      event_label: type + ' | ' + location.pathname
    });

    if (type === 'tagme_reservation') {
      pushEvent('ec_reservation_click', {
        link_url: link.href || href,
        link_text: (link.textContent || '').trim().slice(0, 120),
        page_path: location.pathname,
        page_title: document.title,
        language: document.documentElement.lang || '',
        event_label: 'TagMe reservation | ' + location.pathname
      });
    }
  }, true);
})();

/* === r2d2-dynamic-banner.js === */
(function(){
  'use strict';
  if (window.ecR2D2BannerLoaded) return;
  window.ecR2D2BannerLoaded = true;

  function currentLang(){
    var l = (document.documentElement.lang || 'pt').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  function browserLang(){
    var l = ((navigator.languages && navigator.languages[0]) || navigator.language || '').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  function rememberInterest(){
    var p = location.pathname.toLowerCase();
    try {
      localStorage.setItem('ec_last_visit_at', String(Date.now()));
      var visits = Number(localStorage.getItem('ec_visit_count') || '0') + 1;
      localStorage.setItem('ec_visit_count', String(visits));
      if (p.indexOf('cafe') >= 0 || p.indexOf('breakfast') >= 0) localStorage.setItem('ec_interest', 'breakfast');
      if (p.indexOf('almoco') >= 0 || p.indexOf('lunch') >= 0) localStorage.setItem('ec_interest', 'lunch');
      if (p.indexOf('evento') >= 0 || p.indexOf('event') >= 0) localStorage.setItem('ec_interest', 'events');
      if (p.indexOf('romant') >= 0) localStorage.setItem('ec_interest', 'romantic');
    } catch(e) {}
  }

  function hasReservationClick(){
    try { return localStorage.getItem('ec_reservation_clicked') === '1'; } catch(e) { return false; }
  }

  document.addEventListener('click', function(evt){
    var a = evt.target && evt.target.closest ? evt.target.closest('a[href]') : null;
    if (!a) return;
    var href = (a.getAttribute('href') || '').toLowerCase();
    var txt = (a.textContent || '').toLowerCase();
    if (href.indexOf('tagme.com.br') >= 0 || /reserv|reserve|reserva/.test(txt)) {
      try { localStorage.setItem('ec_reservation_clicked','1'); } catch(e) {}
    }
  }, true);

  function content(){
    var h = new Date().getHours();
    var l = currentLang();
    var b = browserLang();
    var slot = h < 11 ? 'morning' : h < 15 ? 'lunch' : h < 19 ? 'sunset' : 'evening';
    var interest = '';
    var visits = 1;
    try {
      interest = localStorage.getItem('ec_interest') || '';
      visits = Number(localStorage.getItem('ec_visit_count') || '1');
    } catch(e) {}

    if (b !== l && !sessionStorage.getItem('ec_language_suggestion_seen')) {
      sessionStorage.setItem('ec_language_suggestion_seen','1');
      if (b === 'en') return ['Prefer English?', 'We also have an English version with practical information for international visitors.', 'Open English', '/en/'];
      if (b === 'es') return ['¿Prefiere español?', 'También tenemos una versión en español con información práctica para visitantes.', 'Abrir español', '/es/'];
    }

    if (visits > 1 && !hasReservationClick()) {
      if (interest === 'breakfast') {
        return l === 'en' ? ['Welcome back — still thinking about breakfast?', 'Book your breakfast with a Sugarloaf view before visiting Urca Hill.', 'Reserve breakfast', 'https://go.tagme.com.br/embaixadacarioca'] : l === 'es' ? ['Bienvenido de vuelta — ¿todavía pensando en el desayuno?', 'Reserve su desayuno con vista al Pan de Azúcar antes de visitar el Morro da Urca.', 'Reservar desayuno', 'https://go.tagme.com.br/embaixadacarioca'] : ['Bem-vindo de volta — ainda pensando no café da manhã?', 'Reserve o café com vista para o Pão de Açúcar antes de visitar o Morro da Urca.', 'Reservar café', 'https://go.tagme.com.br/embaixadacarioca'];
      }
      if (interest === 'romantic') {
        return l === 'en' ? ['Welcome back — plan the romantic moment', 'View, caipirinhas and Brazilian food at Urca Hill.', 'Reserve a table', 'https://go.tagme.com.br/embaixadacarioca'] : l === 'es' ? ['Bienvenido de vuelta — planifique el momento romántico', 'Vista, caipirinhas y comida brasileña en el Morro da Urca.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca'] : ['Bem-vindo de volta — planeje o momento especial', 'Vista, caipirinhas e comida brasileira no Morro da Urca.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca'];
      }
    }

    var copy = {
      pt: {
        morning: ['Café da manhã com vista no Morro da Urca', 'Comece o passeio no Parque Bondinho com café, frutas, pães e vista para o Pão de Açúcar.', 'Ver café da manhã', '/cafe-da-manha.html'],
        lunch: ['Almoço carioca no Parque Bondinho', 'Picanha, feijoada premiada, caipirinhas e chope gelado na primeira parada do bondinho.', 'Ver almoço', '/almoco.html'],
        sunset: ['Entardecer no alto do Rio', 'Drinks, caipirinhas e vista para transformar a visita ao Morro da Urca em memória.', 'Ver entardecer', '/entardecer.html'],
        evening: ['Reserve sua experiência no Morro da Urca', 'Planeje café da manhã, almoço ou evento com vista dentro do Parque Bondinho.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca']
      },
      en: {
        morning: ['Breakfast with a Sugarloaf view', 'Start your visit at Urca Hill with coffee, fruit, breads and a direct view of Sugarloaf.', 'See breakfast', '/en/cafe-da-manha.html'],
        lunch: ['Brazilian lunch at Sugarloaf Cable Car Park', 'Picanha, feijoada, caipirinhas and cold draft beer at the first cable car stop.', 'See lunch', '/en/almoco.html'],
        sunset: ['Sunset drinks above Rio', 'Caipirinhas, cocktails and the Urca Hill view before or after your Sugarloaf visit.', 'See sunset', '/en/sunset.html'],
        evening: ['Plan your Urca Hill experience', 'Book breakfast, lunch or a private event inside Sugarloaf Cable Car Park.', 'Reserve a table', 'https://go.tagme.com.br/embaixadacarioca']
      },
      es: {
        morning: ['Desayuno con vista al Pan de Azúcar', 'Empiece su visita en el Morro da Urca con café, frutas, panes y vista directa al Pan de Azúcar.', 'Ver desayuno', '/es/cafe-da-manha.html'],
        lunch: ['Almuerzo brasileño en el Parque Bondinho', 'Picanha, feijoada, caipirinhas y chopp frío en la primera parada del teleférico.', 'Ver almuerzo', '/es/almoco.html'],
        sunset: ['Atardecer en lo alto de Río', 'Caipirinhas, drinks y vista desde el Morro da Urca para completar la visita.', 'Ver atardecer', '/es/sunset.html'],
        evening: ['Planifique su experiencia en el Morro da Urca', 'Reserve desayuno, almuerzo o evento privado dentro del Parque Bondinho.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca']
      }
    };
    return copy[l][slot];
  }

  function injectStyle(){
    if (document.getElementById('ec-r2d2-banner-style')) return;
    var css = '.ec-r2d2-banner{position:relative;z-index:20;background:#00405a;color:#f6efde;border-bottom:1px solid rgba(246,239,222,.18);padding:14px 20px;font-family:Catamaran,Verdana,system-ui,sans-serif}.ec-r2d2-banner__inner{max-width:1180px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:18px}.ec-r2d2-banner strong{display:block;color:#fff;font-size:18px;line-height:1.15}.ec-r2d2-banner span{display:block;color:rgba(246,239,222,.86);font-size:15px;line-height:1.35}.ec-r2d2-banner a{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:0 18px;border-radius:999px;background:#f59b1e;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:12px}.ec-r2d2-banner button{background:transparent;border:0;color:#f6efde;font-size:22px;line-height:1;cursor:pointer;padding:6px}.ec-r2d2-banner__copy{display:flex;align-items:center;gap:14px}.ec-r2d2-banner__dot{width:10px;height:10px;border-radius:99px;background:#f59b1e;box-shadow:0 0 0 6px rgba(245,155,30,.18)}@media(max-width:760px){.ec-r2d2-banner__inner{align-items:flex-start}.ec-r2d2-banner__copy{align-items:flex-start}.ec-r2d2-banner a{display:none}.ec-r2d2-banner strong{font-size:16px}.ec-r2d2-banner span{font-size:14px}}';
    var style = document.createElement('style');
    style.id = 'ec-r2d2-banner-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function render(){
    rememberInterest();
    if (sessionStorage.getItem('ec_r2d2_banner_closed') === '1') return;
    if (document.querySelector('.ec-r2d2-banner')) return;
    injectStyle();
    var c = content();
    var bar = document.createElement('aside');
    bar.className = 'ec-r2d2-banner';
    bar.setAttribute('aria-label', 'Sugestão contextual da Embaixada Carioca');
    bar.innerHTML = '<div class="ec-r2d2-banner__inner"><div class="ec-r2d2-banner__copy"><i class="ec-r2d2-banner__dot" aria-hidden="true"></i><div><strong>'+c[0]+'</strong><span>'+c[1]+'</span></div></div><a href="'+c[3]+'">'+c[2]+'</a><button type="button" aria-label="Fechar">×</button></div>';
    bar.querySelector('button').addEventListener('click', function(){
      sessionStorage.setItem('ec_r2d2_banner_closed','1');
      bar.remove();
    });
    document.body.insertBefore(bar, document.body.firstChild);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, { once:true });
  else render();
})();

/* === internal-page-contrast-rescue.js === */
(function(){
  'use strict';
  if (window.ecInternalPageContrastRescueLoaded) return;
  window.ecInternalPageContrastRescueLoaded = true;

  function markPage(){
    var path = location.pathname.toLowerCase();
    if (path.indexOf('guia-do-rio') >= 0) document.body.classList.add('ec-page-guia-do-rio');
    if (path.indexOf('eventos') >= 0) document.body.classList.add('ec-page-eventos');
    if (path.indexOf('morro-da-urca') >= 0) document.body.classList.add('ec-page-morro-da-urca');
    if (path.indexOf('parque-bondinho') >= 0) document.body.classList.add('ec-page-parque-bondinho');
  }

  function injectStyle(){
    if (document.getElementById('ec-internal-page-contrast-rescue-style')) return;
    var css = `
      :root{
        --ec-rescue-blue:#00405a;
        --ec-rescue-blue-dark:#002f3f;
        --ec-rescue-cream:#f6efde;
        --ec-rescue-paper:#fffaf0;
        --ec-rescue-gray:#485156;
        --ec-rescue-orange:#f59b1e;
        --ec-rescue-green:#335d4a;
      }

      /* Base: remove texto fantasma em páginas internas críticas. */
      body.ec-page-guia-do-rio .article-body *,
      body.ec-page-eventos #faq *,
      body.ec-page-eventos .faq *,
      body.ec-page-eventos .capacity *,
      body.ec-page-eventos #capacity *,
      body.ec-page-morro-da-urca main *,
      body.ec-page-parque-bondinho main *{
        opacity:1!important;
        visibility:visible!important;
        filter:none!important;
        mix-blend-mode:normal!important;
        text-shadow:none!important;
        -webkit-text-stroke:0!important;
        -webkit-background-clip:border-box!important;
        background-clip:border-box!important;
      }

      /* GUIA DO RIO — cards claros dentro do artigo: texto sempre escuro. */
      body.ec-page-guia-do-rio .article-body .guia-card,
      body.ec-page-guia-do-rio .article-body .guia-intro-box,
      body.ec-page-guia-do-rio .article-body .guia-roteiro,
      body.ec-page-guia-do-rio .article-body .guia-reservation-links,
      body.ec-page-guia-do-rio .article-body .tip-box,
      body.ec-page-guia-do-rio .article-body .highlight,
      body.ec-page-guia-do-rio .article-body .info-box,
      body.ec-page-guia-do-rio .article-body .card,
      body.ec-page-guia-do-rio .article-body article,
      body.ec-page-guia-do-rio .article-body table,
      body.ec-page-guia-do-rio .article-body tr,
      body.ec-page-guia-do-rio .article-body td,
      body.ec-page-guia-do-rio .article-body th{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card,
      body.ec-page-guia-do-rio .article-body .guia-intro-box,
      body.ec-page-guia-do-rio .article-body .tip-box,
      body.ec-page-guia-do-rio .article-body .highlight,
      body.ec-page-guia-do-rio .article-body .info-box,
      body.ec-page-guia-do-rio .article-body .card{
        background:var(--ec-rescue-paper)!important;
        border-color:rgba(0,64,90,.16)!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card h1,
      body.ec-page-guia-do-rio .article-body .guia-card h2,
      body.ec-page-guia-do-rio .article-body .guia-card h3,
      body.ec-page-guia-do-rio .article-body .guia-card h4,
      body.ec-page-guia-do-rio .article-body .guia-card h5,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h1,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h2,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h3,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h4,
      body.ec-page-guia-do-rio .article-body .tip-box h3,
      body.ec-page-guia-do-rio .article-body .highlight h3,
      body.ec-page-guia-do-rio .article-body .info-box h3,
      body.ec-page-guia-do-rio .article-body .card h3,
      body.ec-page-guia-do-rio .article-body table th,
      body.ec-page-guia-do-rio .article-body table strong{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
        font-weight:800!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card p,
      body.ec-page-guia-do-rio .article-body .guia-card li,
      body.ec-page-guia-do-rio .article-body .guia-card td,
      body.ec-page-guia-do-rio .article-body .guia-card span,
      body.ec-page-guia-do-rio .article-body .guia-intro-box p,
      body.ec-page-guia-do-rio .article-body .guia-intro-box li,
      body.ec-page-guia-do-rio .article-body .tip-box p,
      body.ec-page-guia-do-rio .article-body .highlight p,
      body.ec-page-guia-do-rio .article-body .info-box p,
      body.ec-page-guia-do-rio .article-body .card p,
      body.ec-page-guia-do-rio .article-body table td{
        color:var(--ec-rescue-gray)!important;
        -webkit-text-fill-color:var(--ec-rescue-gray)!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card strong,
      body.ec-page-guia-do-rio .article-body .guia-intro-box strong,
      body.ec-page-guia-do-rio .article-body .tip-box strong,
      body.ec-page-guia-do-rio .article-body .highlight strong,
      body.ec-page-guia-do-rio .article-body .info-box strong,
      body.ec-page-guia-do-rio .article-body .card strong{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
        font-weight:900!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card a,
      body.ec-page-guia-do-rio .article-body .guia-intro-box a,
      body.ec-page-guia-do-rio .article-body .tip-box a,
      body.ec-page-guia-do-rio .article-body .highlight a,
      body.ec-page-guia-do-rio .article-body .info-box a,
      body.ec-page-guia-do-rio .article-body .card a{
        color:#9a6400!important;
        -webkit-text-fill-color:#9a6400!important;
        font-weight:900!important;
      }

      /* GUIA DO RIO — áreas escuras fora dos cards: texto claro consistente. */
      body.ec-page-guia-do-rio main > section,
      body.ec-page-guia-do-rio .topic-authority,
      body.ec-page-guia-do-rio footer{
        color:var(--ec-rescue-cream)!important;
      }
      body.ec-page-guia-do-rio main > section h1,
      body.ec-page-guia-do-rio main > section h2,
      body.ec-page-guia-do-rio main > section h3,
      body.ec-page-guia-do-rio main > section h4,
      body.ec-page-guia-do-rio .topic-authority h1,
      body.ec-page-guia-do-rio .topic-authority h2,
      body.ec-page-guia-do-rio .topic-authority h3,
      body.ec-page-guia-do-rio footer h1,
      body.ec-page-guia-do-rio footer h2,
      body.ec-page-guia-do-rio footer h3{
        color:var(--ec-rescue-cream)!important;
        -webkit-text-fill-color:var(--ec-rescue-cream)!important;
      }
      body.ec-page-guia-do-rio main > section > .wrap > p,
      body.ec-page-guia-do-rio .topic-authority p,
      body.ec-page-guia-do-rio footer p{
        color:rgba(246,239,222,.92)!important;
        -webkit-text-fill-color:rgba(246,239,222,.92)!important;
      }

      /* EVENTOS — FAQ e capacidade em fundo azul: p/h3/h4 legíveis. */
      body.ec-page-eventos #faq,
      body.ec-page-eventos section#faq,
      body.ec-page-eventos .faq-grid,
      body.ec-page-eventos .capacity,
      body.ec-page-eventos section.capacity,
      body.ec-page-eventos #capacity{
        color:var(--ec-rescue-cream)!important;
      }

      body.ec-page-eventos #faq h1,
      body.ec-page-eventos #faq h2,
      body.ec-page-eventos #faq h3,
      body.ec-page-eventos #faq h4,
      body.ec-page-eventos #faq summary,
      body.ec-page-eventos .faq h1,
      body.ec-page-eventos .faq h2,
      body.ec-page-eventos .faq h3,
      body.ec-page-eventos .faq h4,
      body.ec-page-eventos .capacity h1,
      body.ec-page-eventos .capacity h2,
      body.ec-page-eventos .capacity h3,
      body.ec-page-eventos .capacity h4,
      body.ec-page-eventos #capacity h1,
      body.ec-page-eventos #capacity h2,
      body.ec-page-eventos #capacity h3,
      body.ec-page-eventos #capacity h4{
        color:var(--ec-rescue-cream)!important;
        -webkit-text-fill-color:var(--ec-rescue-cream)!important;
        font-weight:800!important;
      }

      body.ec-page-eventos #faq p,
      body.ec-page-eventos #faq li,
      body.ec-page-eventos #faq td,
      body.ec-page-eventos #faq span,
      body.ec-page-eventos .faq p,
      body.ec-page-eventos .faq li,
      body.ec-page-eventos .capacity p,
      body.ec-page-eventos .capacity li,
      body.ec-page-eventos .capacity td,
      body.ec-page-eventos #capacity p,
      body.ec-page-eventos #capacity li,
      body.ec-page-eventos #capacity td{
        color:rgba(246,239,222,.88)!important;
        -webkit-text-fill-color:rgba(246,239,222,.88)!important;
      }

      body.ec-page-eventos #faq strong,
      body.ec-page-eventos .faq strong,
      body.ec-page-eventos .capacity strong,
      body.ec-page-eventos #capacity strong{
        color:var(--ec-rescue-orange)!important;
        -webkit-text-fill-color:var(--ec-rescue-orange)!important;
        font-weight:900!important;
      }

      body.ec-page-eventos #faq a,
      body.ec-page-eventos .faq a,
      body.ec-page-eventos .capacity a,
      body.ec-page-eventos #capacity a{
        color:var(--ec-rescue-orange)!important;
        -webkit-text-fill-color:var(--ec-rescue-orange)!important;
        font-weight:900!important;
      }

      /* Cards claros genéricos em páginas internas: sempre texto escuro. */
      body.ec-page-eventos .card-light,
      body.ec-page-eventos .white-card,
      body.ec-page-eventos [class*="light-card"],
      body.ec-page-eventos [style*="background:#fff"],
      body.ec-page-eventos [style*="background: #fff"],
      body.ec-page-eventos [style*="background:#f6efde"],
      body.ec-page-eventos [style*="background: #f6efde"],
      body.ec-page-eventos [style*="background:#fffaf0"],
      body.ec-page-eventos [style*="background: #fffaf0"]{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
      }
      body.ec-page-eventos .card-light h3,
      body.ec-page-eventos .white-card h3,
      body.ec-page-eventos [class*="light-card"] h3,
      body.ec-page-eventos [style*="background:#fff"] h3,
      body.ec-page-eventos [style*="background: #fff"] h3,
      body.ec-page-eventos [style*="background:#f6efde"] h3,
      body.ec-page-eventos [style*="background: #f6efde"] h3,
      body.ec-page-eventos [style*="background:#fffaf0"] h3,
      body.ec-page-eventos [style*="background: #fffaf0"] h3{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
      }
      body.ec-page-eventos .card-light p,
      body.ec-page-eventos .white-card p,
      body.ec-page-eventos [class*="light-card"] p,
      body.ec-page-eventos [style*="background:#fff"] p,
      body.ec-page-eventos [style*="background: #fff"] p,
      body.ec-page-eventos [style*="background:#f6efde"] p,
      body.ec-page-eventos [style*="background: #f6efde"] p,
      body.ec-page-eventos [style*="background:#fffaf0"] p,
      body.ec-page-eventos [style*="background: #fffaf0"] p{
        color:var(--ec-rescue-gray)!important;
        -webkit-text-fill-color:var(--ec-rescue-gray)!important;
      }
    `;
    var style = document.createElement('style');
    style.id = 'ec-internal-page-contrast-rescue-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function run(){
    markPage();
    injectStyle();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once:true });
  else run();
  window.addEventListener('load', run, { once:true });
})();

/* === dossie-content-enhancer.js === */
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

/* === menuitem-schema-enhancer.js === */
(function(){
  'use strict';
  if (window.ecMenuItemSchemaEnhanced) return;
  window.ecMenuItemSchemaEnhanced = true;

  var data = {
    '@context': 'https://schema.org',
    '@type': 'Menu',
    'name': 'Cardápio Embaixada Carioca',
    'hasMenuSection': [
      {
        '@type': 'MenuSection',
        'name': 'Pratos brasileiros e cariocas',
        'hasMenuItem': [
          {
            '@type': 'MenuItem',
            'name': 'Picanha brasileira',
            'description': 'Picanha brasileira servida na Embaixada Carioca, indicada para almoço no Morro da Urca com vista para o Pão de Açúcar.',
            'suitableForDiet': 'https://schema.org/GlutenFreeDiet'
          },
          {
            '@type': 'MenuItem',
            'name': 'Feijoada premiada',
            'description': 'Feijoada da tradição da Academia da Cachaça, premiada pela Veja Rio Comer & Beber 2025/2026.',
            'menuAddOn': {'@type': 'MenuItem', 'name': 'Caipirinha da casa'}
          },
          {
            '@type': 'MenuItem',
            'name': 'Bobó de camarão',
            'description': 'Prato brasileiro clássico com camarão, servido como opção de almoço carioca no Parque Bondinho Pão de Açúcar.'
          }
        ]
      },
      {
        '@type': 'MenuSection',
        'name': 'Bebidas e caipirinhas',
        'hasMenuItem': [
          {
            '@type': 'MenuItem',
            'name': 'Caipirinha da casa',
            'description': 'Caipirinha da Embaixada Carioca preparada com cachaça Magnífica, limão tahiti e siciliano, adoçada com rapadura.'
          },
          {
            '@type': 'MenuItem',
            'name': 'Chope Heineken',
            'description': 'Chope Heineken gelado, referência da casa e premiado no Rio de Janeiro.'
          },
          {
            '@type': 'MenuItem',
            'name': 'Bossa Sour',
            'description': 'Drink autoral sugerido para começar a experiência na Embaixada Carioca.'
          }
        ]
      },
      {
        '@type': 'MenuSection',
        'name': 'Café da manhã',
        'hasMenuItem': [
          {
            '@type': 'MenuItem',
            'name': 'Café da manhã da Embaixada',
            'description': 'Café da manhã diário no Morro da Urca, com vista para o Pão de Açúcar e itens para compartilhar.'
          }
        ]
      }
    ],
    'provider': {
      '@type': 'Restaurant',
      'name': 'Embaixada Carioca',
      'url': 'https://www.embaixadacarioca.com/',
      'address': {
        '@type': 'PostalAddress',
        'streetAddress': 'Av. Pasteur, 520',
        'addressLocality': 'Rio de Janeiro',
        'addressRegion': 'RJ',
        'addressCountry': 'BR'
      }
    }
  };

  function inject(){
    if (document.getElementById('ec-expanded-menuitem-schema')) return;
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.id = 'ec-expanded-menuitem-schema';
    s.textContent = JSON.stringify(data);
    document.head.appendChild(s);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, { once:true });
  else inject();
})();

