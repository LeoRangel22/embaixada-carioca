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
  function run(){
    injectStyle();
    /* Remover qualquer aviso inserido dentro de header (regressão de versão anterior) */
    document.querySelectorAll('header .ec-bondinho-ticket-notice').forEach(function(el){ el.remove(); });
    /* Inserir aviso APENAS em containers de conteúdo dentro de main/section/article.
       NUNCA inserir dentro de: header, nav, .mobile-bottom-nav */
    Array.prototype.slice.call(document.querySelectorAll('a[href]')).forEach(function(a){
      if (!isReservationLink(a)) return;
      /* Excluir links dentro de qualquer header, nav ou mobile-bottom-nav */
      if (a.closest('header') || a.closest('nav') || a.closest('.mobile-bottom-nav')) return;
      /* Restringir apenas a containers de conteúdo dentro de main/section/article */
      var nearContent = a.closest('main, section, article, .ec-faq-actions, .seo-conversion-block, .guia-reservation-links');
      if (!nearContent) return;
      var parent = a.parentElement;
      if (!parent || parent.querySelector('.ec-bondinho-ticket-notice')) return;
      var note = document.createElement('small');
      note.className = 'ec-bondinho-ticket-notice';
      note.textContent = copy[lang()];
      parent.appendChild(note);
    });
  }
  /* Executar UMA ÚNICA VEZ */
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once:true });
  else run();
})();
