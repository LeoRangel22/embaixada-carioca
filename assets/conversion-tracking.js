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

  function injectCtrMetadata(){
    var path = String(location.pathname || '/').toLowerCase();
    var rules = {
      '/morro-da-urca.html': {
        title: 'Morro da Urca: Onde Comer, O Que Fazer e Como Chegar | Embaixada Carioca',
        description: 'Guia do Morro da Urca: onde comer na 1ª parada do Bondinho, o que fazer, como chegar, vista para o Pão de Açúcar, café da manhã e almoço brasileiro.'
      },
      '/en/morro-da-urca.html': {
        title: 'Urca Hill: Where to Eat, What to Do and How to Get There | Embaixada Carioca',
        description: 'Guide to Urca Hill in Rio: where to eat at the first Sugarloaf Cable Car stop, what to do, how to get there, breakfast, Brazilian lunch and views.'
      },
      '/es/morro-da-urca.html': {
        title: 'Morro da Urca: Dónde Comer, Qué Hacer y Cómo Llegar | Embaixada Carioca',
        description: 'Guía del Morro da Urca: dónde comer en la primera parada del Bondinho, qué hacer, cómo llegar, desayuno, almuerzo brasileño y vista al Pan de Azúcar.'
      },
      '/parque-bondinho.html': {
        title: 'Onde Comer no Parque Bondinho Pão de Açúcar | Morro da Urca',
        description: 'Onde comer no Parque Bondinho Pão de Açúcar: Embaixada Carioca no Morro da Urca, 1ª parada do bondinho, com café da manhã, almoço, caipirinha e vista.'
      },
      '/en/parque-bondinho.html': {
        title: 'Where to Eat at Sugarloaf Cable Car Park | Urca Hill',
        description: 'Where to eat at Sugarloaf Cable Car Park: Embaixada Carioca at Urca Hill, first cable car stop, with breakfast, Brazilian lunch, caipirinhas and views.'
      },
      '/es/parque-bondinho.html': {
        title: 'Dónde Comer en el Parque Bondinho Pan de Azúcar | Morro da Urca',
        description: 'Dónde comer en el Parque Bondinho Pan de Azúcar: Embaixada Carioca en el Morro da Urca, primera parada del teleférico, con desayuno, almuerzo y vista.'
      },
      '/como-chegar.html': {
        title: 'Como Chegar à Embaixada Carioca | Av. Pasteur 520, Urca',
        description: 'Como chegar à Embaixada Carioca: use Av. Pasteur 520, Praia Vermelha, Urca. Restaurante na 1ª parada do Bondinho, no Morro da Urca.'
      },
      '/en/how-to-get-there.html': {
        title: 'How to Get to Embaixada Carioca | Av. Pasteur 520, Urca',
        description: 'How to get to Embaixada Carioca: use Av. Pasteur 520, Praia Vermelha, Urca. Restaurant at the first Sugarloaf Cable Car stop on Urca Hill.'
      },
      '/es/como-llegar.html': {
        title: 'Cómo Llegar a Embaixada Carioca | Av. Pasteur 520, Urca',
        description: 'Cómo llegar a Embaixada Carioca: use Av. Pasteur 520, Praia Vermelha, Urca. Restaurante en la primera parada del Bondinho, Morro da Urca.'
      }
    };
    var data = rules[path];
    if (!data) return;

    function setMeta(selector, attr, value){
      var el = document.querySelector(selector);
      if (el) el.setAttribute(attr, value);
    }

    document.title = data.title;
    setMeta('meta[name="description"]', 'content', data.description);
    setMeta('meta[property="og:title"]', 'content', data.title);
    setMeta('meta[property="og:description"]', 'content', data.description);
    window.ecCtrMetadataOverride = { success: true, path: path, title: data.title };
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

  function runVisualSafety(){
    translateNavLabels();
    injectCtrMetadata();
    injectScrolledNavContrastLock();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runVisualSafety, { once: true });
  } else {
    runVisualSafety();
  }
  window.addEventListener('load', runVisualSafety, { once: true });
})();
