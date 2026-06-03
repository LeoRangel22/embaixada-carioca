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
    var css = '.ec-bondinho-ticket-notice{display:block;margin:.65rem 0 0;padding:.72rem .9rem;border-radius:14px;background:rgba(245,155,30,.13);border:1px solid rgba(245,155,30,.38);color:#00405a!important;-webkit-text-fill-color:#00405a!important;font-family:Catamaran,Verdana,system-ui,sans-serif;font-size:.92rem;line-height:1.38;font-weight:700;max-width:560px}@media(max-width:760px){.ec-bondinho-ticket-notice{font-size:.86rem;max-width:100%}}';
    var style = document.createElement('style');
    style.id = 'ec-bondinho-ticket-notice-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function run(){
    injectStyle();

    /* 1. Remover TODOS os avisos existentes em qualquer lugar da pagina */
    document.querySelectorAll('.ec-bondinho-ticket-notice').forEach(function(el){
      el.remove();
    });

    /* 2. Inserir o aviso UMA UNICA VEZ — logo apos o bloco de CTAs do hero.
          O hero usa .hero-ctas (index.html) ou header.page-hero .ctas (subpaginas). */
    var heroCtas = (
      document.querySelector('header.page-hero .hero-ctas') ||
      document.querySelector('header.page-hero .ctas') ||
      document.querySelector('.hero-ctas') ||
      document.querySelector('header .ctas')
    );

    if (!heroCtas) return;

    var note = document.createElement('small');
    note.className = 'ec-bondinho-ticket-notice';
    note.textContent = copy[lang()];

    if (heroCtas.parentNode) {
      heroCtas.parentNode.insertBefore(note, heroCtas.nextSibling);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once: true });
  } else {
    run();
  }
})();
