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
    var css = '.ec-bondinho-ticket-notice{display:block;margin:.65rem 0 0;padding:.72rem .9rem;border-radius:14px;background:rgba(245,155,30,.13);border:1px solid rgba(245,155,30,.38);color:#00405a!important;-webkit-text-fill-color:#00405a!important;font-family:Catamaran,Verdana,system-ui,sans-serif;font-size:.92rem;line-height:1.38;font-weight:700;max-width:560px}section[style*="background:#00405a"] .ec-bondinho-ticket-notice,section[style*="background: #00405a"] .ec-bondinho-ticket-notice,section[style*="background:#1a2e24"] .ec-bondinho-ticket-notice,section[style*="background: #1a2e24"] .ec-bondinho-ticket-notice{background:rgba(245,155,30,.16);border-color:rgba(245,155,30,.42);color:#f6efde!important;-webkit-text-fill-color:#f6efde!important}@media(max-width:760px){.ec-bondinho-ticket-notice{font-size:.86rem;max-width:100%}}';
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
  function insertAfter(note, refNode){
    if (refNode.parentNode) refNode.parentNode.insertBefore(note, refNode.nextSibling);
  }
  function run(){
    injectStyle();
    /* Seletores de containers CTA do hero — tanto .hero-ctas (index) quanto .ctas (subpáginas) */
    var heroCtas = document.querySelector('.hero-ctas') || document.querySelector('header .ctas');
    if (heroCtas) {
      var hasRes = false;
      var links = heroCtas.querySelectorAll('a[href]');
      for (var i = 0; i < links.length; i++) {
        if (isReservationLink(links[i])) { hasRes = true; break; }
      }
      if (hasRes) {
        /* Remover aviso antigo dentro do heroCtas (se existir de versão anterior) */
        var oldInside = heroCtas.querySelector('.ec-bondinho-ticket-notice');
        if (oldInside) oldInside.remove();
        /* Inserir APÓS o heroCtas como irmão — não dentro dele.
           Isso evita que o container (position:absolute ou overflow:hidden) quebre o layout. */
        var nextSib = heroCtas.nextElementSibling;
        if (!nextSib || !nextSib.classList.contains('ec-bondinho-ticket-notice')) {
          var note = document.createElement('small');
          note.className = 'ec-bondinho-ticket-notice';
          note.textContent = copy[lang()];
          insertAfter(note, heroCtas);
        }
      }
    }
    /* Para outros containers de CTAs dentro de main/section/article:
       inserir o aviso no parentElement do link.
       NUNCA inserir dentro de: nav.top, .mobile-bottom-nav, qualquer header. */
    Array.prototype.slice.call(document.querySelectorAll('a[href]')).forEach(function(a){
      if (!isReservationLink(a)) return;
      /* Pular links dentro do heroCtas (já tratado acima) */
      if (heroCtas && heroCtas.contains(a)) return;
      /* Pular links dentro do nav.top, mobile-bottom-nav e qualquer header */
      if (a.closest('nav.top') || a.closest('.mobile-bottom-nav') || a.closest('header')) return;
      var parent = a.parentElement;
      if (!parent || parent.querySelector('.ec-bondinho-ticket-notice')) return;
      /* Restringir apenas a containers de conteúdo dentro de main/section/article */
      var nearContent = a.closest('main, section, article, .ec-faq-actions, .seo-conversion-block, .guia-reservation-links');
      if (!nearContent) return;
      var note2 = document.createElement('small');
      note2.className = 'ec-bondinho-ticket-notice';
      note2.textContent = copy[lang()];
      parent.appendChild(note2);
    });
  }
  /* Executar UMA ÚNICA VEZ — sem window.load para evitar dupla execução */
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once:true });
  else run();
})();
