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
