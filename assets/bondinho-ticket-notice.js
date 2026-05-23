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
