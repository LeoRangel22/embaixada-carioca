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

  function normalizeLabel(text){
    return String(text || '').replace(/\s+/g, ' ').trim();
  }

  function currentLanguage(){
    var path = String(location.pathname || '').toLowerCase();
    var htmlLang = String(document.documentElement.lang || '').toLowerCase();
    if (path === '/en/' || path.indexOf('/en/') === 0 || htmlLang.indexOf('en') === 0) return 'en';
    if (path === '/es/' || path.indexOf('/es/') === 0 || htmlLang.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  function translateNavLabels(){
    var lang = currentLanguage();
    if (lang !== 'en' && lang !== 'es') return;

    var dictionaries = {
      en: {
        'Café da Manhã': 'Breakfast',
        'Cafe da Manha': 'Breakfast',
        'Almoço': 'Lunch',
        'Almoco': 'Lunch',
        'Como Chegar': 'How to Get There',
        'Eventos': 'Events',
        'Cardápio': 'Menu',
        'Cardapio': 'Menu',
        'Guia do Rio': 'Rio Guide',
        'Reservar': 'Reserve'
      },
      es: {
        'Café da Manhã': 'Desayuno',
        'Cafe da Manha': 'Desayuno',
        'Almoço': 'Almuerzo',
        'Almoco': 'Almuerzo',
        'Como Chegar': 'Cómo llegar',
        'Eventos': 'Eventos',
        'Cardápio': 'Menú',
        'Cardapio': 'Menú',
        'Guia do Rio': 'Guía de Río',
        'Reservar': 'Reservar'
      }
    };

    var dict = dictionaries[lang];
    var selector = 'nav.top a, .nav-links a, .nav-drawer a, .nav-drawer-links a, .mobile-bottom-nav a';
    document.querySelectorAll(selector).forEach(function(el){
      var label = normalizeLabel(el.textContent);
      if (dict[label]) {
        el.textContent = dict[label];
      }
      var aria = normalizeLabel(el.getAttribute('aria-label'));
      if (dict[aria]) {
        el.setAttribute('aria-label', dict[aria]);
      }
      var title = normalizeLabel(el.getAttribute('title'));
      if (dict[title]) {
        el.setAttribute('title', dict[title]);
      }
    });
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', translateNavLabels, { once: true });
  } else {
    translateNavLabels();
  }
  window.addEventListener('load', translateNavLabels, { once: true });
})();
