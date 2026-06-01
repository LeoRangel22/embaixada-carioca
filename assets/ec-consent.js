(function () {
  'use strict';
  var CONSENT_KEY = 'ec_analytics_consent';
  var CONSENT_VERSION = '1';

  function getConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }
  function setConsent(val) {
    try { localStorage.setItem(CONSENT_KEY, val); } catch (e) {}
  }

  var consent = getConsent();

  // Already decided — load GA4 if accepted
  if (consent === 'y') {
    if (typeof window.ecLoadGA4 === 'function') window.ecLoadGA4();
    return;
  }
  if (consent === 'n') return;

  // First visit — show banner
  function buildBanner() {
    var lang = (document.documentElement.lang || 'pt').toLowerCase();
    var texts = {
      pt: {
        msg: 'Usamos cookies de análise para entender como os visitantes usam o site. Você pode recusar sem prejuízo.',
        accept: 'Aceitar',
        decline: 'Recusar',
      },
      en: {
        msg: 'We use analytics cookies to understand how visitors use the site. You can decline without any impact.',
        accept: 'Accept',
        decline: 'Decline',
      },
      es: {
        msg: 'Usamos cookies de análisis para entender cómo los visitantes usan el sitio. Puede rechazarlos sin ningún impacto.',
        accept: 'Aceptar',
        decline: 'Rechazar',
      },
    };
    var t = lang.indexOf('en') === 0 ? texts.en : lang.indexOf('es') === 0 ? texts.es : texts.pt;

    var banner = document.createElement('div');
    banner.id = 'ec-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Aviso de cookies');

    var p = document.createElement('p');
    p.textContent = t.msg;

    var btns = document.createElement('div');
    btns.className = 'ec-consent-btns';

    var accept = document.createElement('button');
    accept.id = 'ec-consent-accept';
    accept.textContent = t.accept;
    accept.addEventListener('click', function () {
      setConsent('y');
      banner.remove();
      if (typeof window.ecLoadGA4 === 'function') window.ecLoadGA4();
    });

    var decline = document.createElement('button');
    decline.id = 'ec-consent-decline';
    decline.textContent = t.decline;
    decline.addEventListener('click', function () {
      setConsent('n');
      banner.remove();
    });

    btns.appendChild(accept);
    btns.appendChild(decline);
    banner.appendChild(p);
    banner.appendChild(btns);
    document.body.appendChild(banner);

    // Animate in after paint
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { banner.classList.add('visible'); });
    });
  }

  // Show after 1.5s so it doesn't block first impressions
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(buildBanner, 1500); });
  } else {
    setTimeout(buildBanner, 1500);
  }
})();
