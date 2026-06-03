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
    var css = [
      '.ec-bondinho-ticket-notice{',
        'display:block;',
        'margin:0;',
        'padding:.8rem 1.2rem;',
        'background:rgba(245,155,30,.13);',
        'border-top:2px solid rgba(245,155,30,.45);',
        'border-bottom:2px solid rgba(245,155,30,.45);',
        'color:#00405a!important;',
        '-webkit-text-fill-color:#00405a!important;',
        'font-family:Catamaran,Verdana,system-ui,sans-serif;',
        'font-size:.92rem;',
        'line-height:1.4;',
        'font-weight:700;',
        'text-align:center;',
        'width:100%;',
        'box-sizing:border-box',
      '}',
      '@media(max-width:760px){',
        '.ec-bondinho-ticket-notice{font-size:.84rem;padding:.7rem .9rem}',
      '}'
    ].join('');
    var style = document.createElement('style');
    style.id = 'ec-bondinho-ticket-notice-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function run(){
    injectStyle();

    /* Remover qualquer aviso anterior em qualquer lugar da pagina */
    document.querySelectorAll('.ec-bondinho-ticket-notice').forEach(function(el){
      el.remove();
    });

    /* Inserir o aviso logo APOS o header.page-hero, no fluxo normal do documento.
       Assim fica visivel abaixo do hero, sem conflito com position:absolute ou overflow:hidden. */
    var hero = document.querySelector('header.page-hero');
    if (!hero) return;

    var note = document.createElement('small');
    note.className = 'ec-bondinho-ticket-notice';
    note.textContent = copy[lang()];

    /* insertBefore(note, hero.nextSibling) insere logo apos o header no body */
    if (hero.parentNode) {
      hero.parentNode.insertBefore(note, hero.nextSibling);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once: true });
  } else {
    run();
  }
})();
