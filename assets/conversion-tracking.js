(function(){
  'use strict';
  if (window.ecConversionTrackingLoaded) return;
  window.ecConversionTrackingLoaded = true;

  function pushEvent(name, params){
    params = params || {};
    params.event_category = params.event_category || 'conversion';
    params.transport_type = params.transport_type || 'beacon';
    window.dataLayer = window.dataLayer || [];
    if (typeof window.gtag === 'function') {
      try { window.gtag('event', name, params); } catch(e) {}
    } else {
      window.dataLayer.push(Object.assign({ event: name }, params));
    }
  }

  function classify(url){
    var u = (url || '').toLowerCase();
    if (u.indexOf('go.tagme.com.br') >= 0 || u.indexOf('tagme.com.br') >= 0) return 'tagme_reservation';
    if (u.indexOf('wa.me') >= 0 || u.indexOf('api.whatsapp.com') >= 0 || u.indexOf('whatsapp') >= 0) return 'whatsapp';
    if ((u.indexOf('g.page') >= 0 && u.indexOf('review') >= 0) || u.indexOf('google.com/maps/place') >= 0 && u.indexOf('review') >= 0) return 'google_reviews';
    if (u.indexOf('google.com/maps') >= 0 || u.indexOf('maps.google.') >= 0 || u.indexOf('maps.app.goo') >= 0) return 'google_maps';
    if (u.indexOf('mailto:') === 0) return 'email';
    if (u.indexOf('tel:') === 0) return 'phone';
    return '';
  }

  function eventNameFor(el, url){
    var label = normalizeLabel(
      (el && (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || el.getAttribute('data-analytics-label'))) || ''
    );
    var classes = String((el && el.className) || '');
    var haystack = (String(url || '') + ' ' + label + ' ' + classes).toLowerCase();

    if (haystack.indexOf('go.tagme.com.br') >= 0 || haystack.indexOf('reservar') >= 0 || haystack.indexOf('reserva') >= 0) return 'click_reservar';
    if (haystack.indexOf('wa.me') >= 0 || haystack.indexOf('whatsapp') >= 0) return 'whatsapp_click';
    if ((haystack.indexOf('g.page') >= 0 && haystack.indexOf('review') >= 0) || haystack.indexOf('google reviews') >= 0 || haystack.indexOf('avaliações no google') >= 0 || haystack.indexOf('avaliacoes no google') >= 0) return 'click_google_reviews';
    if (haystack.indexOf('google.com/maps') >= 0 || haystack.indexOf('maps.google.') >= 0 || haystack.indexOf('maps.app.goo') >= 0) return 'click_google_maps';
    if (haystack.indexOf('como-chegar') >= 0 || haystack.indexOf('como chegar') >= 0 || haystack.indexOf('how-to-get-there') >= 0 || haystack.indexOf('how to get') >= 0 || haystack.indexOf('como-llegar') >= 0 || haystack.indexOf('cómo llegar') >= 0 || haystack.indexOf('directions') >= 0) return 'click_como_chegar';
    if (haystack.indexOf('cardapio') >= 0 || haystack.indexOf('cardápio') >= 0 || haystack.indexOf('/menu') >= 0) return 'click_cardapio';
    if (haystack.indexOf('eventos') >= 0 || haystack.indexOf('events') >= 0) return 'click_eventos';
    if (haystack.indexOf('cafe-da-manha') >= 0 || haystack.indexOf('café da manhã') >= 0 || haystack.indexOf('breakfast') >= 0 || haystack.indexOf('desayuno') >= 0) return 'click_cafe_da_manha';
    if (haystack.indexOf('almoco') >= 0 || haystack.indexOf('almoço') >= 0 || haystack.indexOf('lunch') >= 0 || haystack.indexOf('almuerzo') >= 0) return 'click_almoco';
    if (haystack.indexOf('lang-') >= 0 || haystack.indexOf('hreflang') >= 0 || (el && el.closest && el.closest('.lang-switcher'))) return 'click_idioma';
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

  function injectScrolledNavContrastLock(){
    if (document.getElementById('ec-scrolled-nav-contrast-lock')) return;
    var style = document.createElement('style');
    style.id = 'ec-scrolled-nav-contrast-lock';
    style.textContent = `
      @media (min-width: 901px) {
        html body nav.top.scrolled,
        html body #topnav.top.scrolled {
          background: rgba(0, 32, 46, .88) !important;
          border-bottom-color: rgba(246, 239, 222, .18) !important;
          box-shadow: 0 12px 34px rgba(0, 0, 0, .24) !important;
          -webkit-backdrop-filter: blur(14px) !important;
          backdrop-filter: blur(14px) !important;
        }

        html body nav.top.scrolled .nav-inner,
        html body nav.top.scrolled .brand-mark,
        html body nav.top.scrolled .brand-word,
        html body nav.top.scrolled .nav-links a,
        html body #topnav.top.scrolled .nav-inner,
        html body #topnav.top.scrolled .brand-mark,
        html body #topnav.top.scrolled .brand-word,
        html body #topnav.top.scrolled .nav-links a {
          color: #f6efde !important;
          -webkit-text-fill-color: #f6efde !important;
          opacity: 1 !important;
          text-shadow: none !important;
        }

        html body nav.top.scrolled .nav-links a::after,
        html body #topnav.top.scrolled .nav-links a::after {
          background: #f59b1e !important;
        }

        html body nav.top.scrolled .brand-logo.light,
        html body #topnav.top.scrolled .brand-logo.light {
          display: block !important;
        }

        html body nav.top.scrolled .brand-logo.dark,
        html body #topnav.top.scrolled .brand-logo.dark {
          display: none !important;
        }

        html body nav.top.scrolled .nav-rating-badge,
        html body #topnav.top.scrolled .nav-rating-badge {
          background: rgba(246, 239, 222, .12) !important;
          border-color: rgba(246, 239, 222, .30) !important;
          color: #f6efde !important;
          -webkit-text-fill-color: #f6efde !important;
          opacity: 1 !important;
        }

        html body nav.top.scrolled .nav-rating-badge *,
        html body #topnav.top.scrolled .nav-rating-badge * {
          color: #f6efde !important;
          -webkit-text-fill-color: #f6efde !important;
          opacity: 1 !important;
          text-shadow: none !important;
        }

        html body nav.top.scrolled .nav-rating-badge .stars,
        html body nav.top.scrolled .nav-rating-badge .star,
        html body nav.top.scrolled .nav-rating-badge [class*="star"],
        html body #topnav.top.scrolled .nav-rating-badge .stars,
        html body #topnav.top.scrolled .nav-rating-badge .star,
        html body #topnav.top.scrolled .nav-rating-badge [class*="star"] {
          color: #f59b1e !important;
          -webkit-text-fill-color: #f59b1e !important;
        }

        html body nav.top.scrolled .lang-current,
        html body nav.top.scrolled .lang-switcher button,
        html body nav.top.scrolled .lang-switcher > a,
        html body #topnav.top.scrolled .lang-current,
        html body #topnav.top.scrolled .lang-switcher button,
        html body #topnav.top.scrolled .lang-switcher > a {
          color: #f6efde !important;
          -webkit-text-fill-color: #f6efde !important;
          border-color: rgba(246, 239, 222, .32) !important;
          background: rgba(246, 239, 222, .08) !important;
        }

        html body nav.top.scrolled a.btn[href*="tagme"],
        html body nav.top.scrolled a.btn[href*="reserv"],
        html body #topnav.top.scrolled a.btn[href*="tagme"],
        html body #topnav.top.scrolled a.btn[href*="reserv"] {
          background: #f59b1e !important;
          border-color: #f59b1e !important;
          color: #00405a !important;
          -webkit-text-fill-color: #00405a !important;
          text-shadow: none !important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  document.addEventListener('click', function(evt){
    var link = evt.target && evt.target.closest ? evt.target.closest('a[href], button, [role="button"]') : null;
    if (!link) return;
    var href = link.getAttribute('href') || '';
    var type = classify(href);
    var eventName = eventNameFor(link, href);
    if (!type && !eventName) return;

    if (type) {
      pushEvent('ec_outbound_conversion_click', {
        conversion_type: type,
        link_url: link.href || href,
        link_text: (link.textContent || '').trim().slice(0, 120),
        page_path: location.pathname,
        page_title: document.title,
        language: document.documentElement.lang || '',
        event_label: type + ' | ' + location.pathname
      });
    }

    if (eventName) {
      pushEvent(eventName, {
        link_url: link.href || href,
        link_text: (link.textContent || '').trim().slice(0, 120),
        page_path: location.pathname,
        page_title: document.title,
        language: document.documentElement.lang || '',
        event_label: (type || eventName) + ' | ' + location.pathname,
        analytics_version: '2026-08-24.1'
      });
    }

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

  function runVisualSafety(){
    translateNavLabels();
    injectScrolledNavContrastLock();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runVisualSafety, { once: true });
  } else {
    runVisualSafety();
  }
  window.addEventListener('load', runVisualSafety, { once: true });
})();
