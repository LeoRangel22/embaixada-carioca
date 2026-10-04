/* Event-system handoff only. A click is not a submitted or confirmed lead. */
(function () {
  'use strict';
  if (window.ecEventSystemLinksReady) return;
  window.ecEventSystemLinksReady = true;
  document.addEventListener('click', function (event) {
    var link = event.target && event.target.closest
      ? event.target.closest('a[data-event-system-link]') : null;
    if (!link) return;
    var target;
    try { target = new URL(link.href); } catch (_) { return; }
    if (target.origin !== 'https://leorangel22.github.io' ||
        target.pathname !== '/main/formulario.html') return;
    var position = link.closest('nav') ? 'top_navigation'
      : link.closest('header, .hero') ? 'hero'
      : link.closest('footer') ? 'footer'
      : link.closest('.contact, .ec-event-system-card, #cotacao') ? 'form_section'
      : 'page_content';
    var details = {
      form_id: 'event_system_public_form',
      page_path: location.pathname,
      page_language: document.documentElement.lang || 'pt-BR',
      cta_destination: 'event_system',
      cta_location: position,
      event_variant: 'events_system_handoff_v2',
      transport_type: 'beacon'
    };
    // Never include query strings, contact details, or user-entered text.
    // Do not prevent navigation: static links also work without JavaScript.
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'ec_event_form_cta_click', details);
    } else {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: 'ec_event_form_cta_click' }, details));
    }
  });
})();
