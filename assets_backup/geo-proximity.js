/**
 * Embaixada Carioca — Geo Proximity Banner
 * Detecta quando o visitante está próximo ao Morro da Urca e exibe
 * um banner de CTA para visita imediata.
 *
 * Coordenadas exatas: -22.9511223, -43.1642121
 * Raios de detecção:
 *   - VERY_CLOSE  ≤ 300m  → "Você está aqui! Suba agora."
 *   - CLOSE       ≤ 1km   → "Você está a X minutos a pé."
 *   - NEARBY      ≤ 3km   → "Você está a X minutos de carro."
 *   - URCA_ZONE   ≤ 5km   → "Você está no bairro da Urca."
 */
(function () {
  'use strict';

  // ── Configuração ──────────────────────────────────────────────
  var EC = {
    lat: -22.9511223,
    lng: -43.1642121,
    VERY_CLOSE: 300,    // metros
    CLOSE:     1000,
    NEARBY:    3000,
    URCA_ZONE: 5000,
    WALK_SPEED: 80,     // m/min caminhando
    DRIVE_SPEED: 400,   // m/min de carro (tráfego urbano)
    STORAGE_KEY: 'ec_geo_dismissed',
    STORAGE_TTL: 30 * 60 * 1000, // 30 min — não mostrar de novo
  };

  // ── Textos multilíngues ───────────────────────────────────────
  var TEXTS = {
    'pt-BR': {
      very_close: '📍 Você está a poucos passos da Embaixada Carioca!',
      close: function(min) { return '📍 Você está a ~' + min + ' min a pé da Embaixada Carioca!'; },
      nearby: function(min) { return '📍 Você está a ~' + min + ' min de carro da Embaixada Carioca!'; },
      urca: '📍 Você está na Urca — a Embaixada Carioca está pertinho!',
      sub_very_close: 'A melhor vista do Rio te espera. Suba agora pelo Bondinho.',
      sub_close: 'Feijoada premiada, picanha e chope Heineken com vista para o Pão de Açúcar.',
      sub_nearby: 'Melhor feijoada do Brasil, todos os dias, com vista para o Pão de Açúcar.',
      sub_urca: 'Restaurante no Morro da Urca — vista panorâmica a 227m de altitude.',
      cta_directions: '🗺 Como chegar',
      cta_reserve: 'Reservar mesa →',
      cta_wa: 'WhatsApp',
      dismiss: '✕',
    },
    'en': {
      very_close: '📍 You are steps away from Embaixada Carioca!',
      close: function(min) { return '📍 You are ~' + min + ' min walk from Embaixada Carioca!'; },
      nearby: function(min) { return '📍 You are ~' + min + ' min drive from Embaixada Carioca!'; },
      urca: '📍 You are in Urca — Embaixada Carioca is nearby!',
      sub_very_close: 'The best view in Rio awaits. Take the cable car up now.',
      sub_close: 'Award-winning feijoada, picanha and Heineken with a view of Sugarloaf.',
      sub_nearby: 'Best feijoada in Brazil, every day, with a view of Sugarloaf Mountain.',
      sub_urca: 'Restaurant at Morro da Urca — panoramic view at 227m altitude.',
      cta_directions: '🗺 Directions',
      cta_reserve: 'Reserve a table →',
      cta_wa: 'WhatsApp',
      dismiss: '✕',
    },
    'es': {
      very_close: '📍 ¡Estás a pocos pasos de Embaixada Carioca!',
      close: function(min) { return '📍 ¡Estás a ~' + min + ' min caminando de Embaixada Carioca!'; },
      nearby: function(min) { return '📍 ¡Estás a ~' + min + ' min en auto de Embaixada Carioca!'; },
      urca: '📍 ¡Estás en Urca — Embaixada Carioca está muy cerca!',
      sub_very_close: 'La mejor vista de Río te espera. Sube ahora por el teleférico.',
      sub_close: 'Feijoada premiada, picanha y Heineken con vista al Pan de Azúcar.',
      sub_nearby: 'La mejor feijoada de Brasil, todos los días, con vista al Pan de Azúcar.',
      sub_urca: 'Restaurante en el Morro da Urca — vista panorámica a 227m de altitud.',
      cta_directions: '🗺 Cómo llegar',
      cta_reserve: 'Reservar mesa →',
      cta_wa: 'WhatsApp',
      dismiss: '✕',
    }
  };

  // ── Detectar idioma ───────────────────────────────────────────
  function getLang() {
    var path = window.location.pathname;
    if (path.indexOf('/en/') === 0 || path.indexOf('/en') === 0) return 'en';
    if (path.indexOf('/es/') === 0 || path.indexOf('/es') === 0) return 'es';
    return 'pt-BR';
  }

  // ── Calcular distância (Haversine) ────────────────────────────
  function haversine(lat1, lng1, lat2, lng2) {
    var R = 6371000; // raio da Terra em metros
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLng = (lng2 - lng1) * Math.PI / 180;
    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLng/2) * Math.sin(dLng/2);
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  // ── Verificar se foi dispensado recentemente ──────────────────
  function wasDismissed() {
    try {
      var data = JSON.parse(localStorage.getItem(EC.STORAGE_KEY) || 'null');
      if (!data) return false;
      return (Date.now() - data.ts) < EC.STORAGE_TTL;
    } catch(e) { return false; }
  }

  function markDismissed() {
    try { localStorage.setItem(EC.STORAGE_KEY, JSON.stringify({ ts: Date.now() })); } catch(e) {}
  }

  // ── Criar e exibir o banner ───────────────────────────────────
  function showBanner(dist, lang) {
    var t = TEXTS[lang] || TEXTS['pt-BR'];
    var title, subtitle;
    var urgency = 'nearby'; // classe de cor

    if (dist <= EC.VERY_CLOSE) {
      title = t.very_close;
      subtitle = t.sub_very_close;
      urgency = 'very-close';
    } else if (dist <= EC.CLOSE) {
      var walkMin = Math.ceil(dist / EC.WALK_SPEED);
      title = typeof t.close === 'function' ? t.close(walkMin) : t.close;
      subtitle = t.sub_close;
      urgency = 'close';
    } else if (dist <= EC.NEARBY) {
      var driveMin = Math.ceil(dist / EC.DRIVE_SPEED);
      title = typeof t.nearby === 'function' ? t.nearby(driveMin) : t.nearby;
      subtitle = t.sub_nearby;
      urgency = 'nearby';
    } else {
      title = t.urca;
      subtitle = t.sub_urca;
      urgency = 'urca';
    }

    // Deep link para Google Maps com navegação até a Embaixada
    var mapsUrl = 'https://www.google.com/maps/dir/?api=1&destination=' +
      EC.lat + ',' + EC.lng +
      '&destination_place_id=ChIJy7c9M82XmQARTa0mIkiMFRw' +
      '&travelmode=walking';

    var banner = document.createElement('div');
    banner.id = 'ec-geo-banner';
    banner.setAttribute('role', 'complementary');
    banner.setAttribute('aria-label', 'Você está perto da Embaixada Carioca');
    banner.innerHTML =
      '<div class="ec-geo-inner">' +
        '<div class="ec-geo-pulse"></div>' +
        '<div class="ec-geo-content">' +
          '<p class="ec-geo-title">' + title + '</p>' +
          '<p class="ec-geo-sub">' + subtitle + '</p>' +
          '<div class="ec-geo-ctas">' +
            '<a href="' + mapsUrl + '" target="_blank" rel="noopener" class="ec-geo-btn ec-geo-btn-dir">' + t.cta_directions + '</a>' +
            '<a href="https://go.tagme.com.br/embaixadacarioca" target="_blank" rel="noopener" class="ec-geo-btn ec-geo-btn-res">' + t.cta_reserve + '</a>' +
            '<a href="https://wa.me/5521966837556?text=Ol%C3%A1%21+Estou+perto+e+quero+saber+mais+sobre+a+Embaixada+Carioca." target="_blank" rel="noopener" class="ec-geo-btn ec-geo-btn-wa">' +
              '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>' +
              ' ' + t.cta_wa +
            '</a>' +
          '</div>' +
        '</div>' +
        '<button class="ec-geo-dismiss" aria-label="Fechar">' + t.dismiss + '</button>' +
      '</div>';

    // Injetar estilos inline (sem dependência de CSS externo)
    if (!document.getElementById('ec-geo-styles')) {
      var style = document.createElement('style');
      style.id = 'ec-geo-styles';
      style.textContent = [
        '#ec-geo-banner{',
          'position:fixed;bottom:0;left:0;right:0;z-index:9999;',
          'background:linear-gradient(135deg,#00405a 0%,#00587a 100%);',
          'color:#fff;padding:0;',
          'box-shadow:0 -4px 24px rgba(0,0,0,0.35);',
          'transform:translateY(100%);',
          'transition:transform 0.4s cubic-bezier(0.34,1.56,0.64,1);',
          'border-top:3px solid #f59b1e;',
          'font-family:"Catamaran",system-ui,sans-serif;',
        '}',
        '#ec-geo-banner.ec-visible{transform:translateY(0);}',
        '.ec-geo-inner{',
          'display:flex;align-items:flex-start;gap:12px;',
          'padding:16px 16px 16px 20px;',
          'max-width:600px;margin:0 auto;position:relative;',
        '}',
        '.ec-geo-pulse{',
          'width:12px;height:12px;border-radius:50%;',
          'background:#f59b1e;flex-shrink:0;margin-top:5px;',
          'box-shadow:0 0 0 0 rgba(245,155,30,0.7);',
          'animation:ec-pulse 1.8s infinite;',
        '}',
        '@keyframes ec-pulse{',
          '0%{box-shadow:0 0 0 0 rgba(245,155,30,0.7);}',
          '70%{box-shadow:0 0 0 10px rgba(245,155,30,0);}',
          '100%{box-shadow:0 0 0 0 rgba(245,155,30,0);}',
        '}',
        '.ec-geo-content{flex:1;min-width:0;}',
        '.ec-geo-title{',
          'margin:0 0 4px;font-size:14px;font-weight:700;',
          'line-height:1.3;color:#fff;',
        '}',
        '.ec-geo-sub{',
          'margin:0 0 12px;font-size:12px;',
          'color:rgba(255,255,255,0.75);line-height:1.4;',
        '}',
        '.ec-geo-ctas{display:flex;gap:8px;flex-wrap:wrap;}',
        '.ec-geo-btn{',
          'display:inline-flex;align-items:center;gap:5px;',
          'padding:7px 12px;border-radius:4px;',
          'font-size:12px;font-weight:700;text-decoration:none;',
          'letter-spacing:0.04em;white-space:nowrap;',
          'transition:opacity .2s;',
        '}',
        '.ec-geo-btn:hover{opacity:0.85;}',
        '.ec-geo-btn-dir{background:rgba(255,255,255,0.15);color:#fff;border:1px solid rgba(255,255,255,0.3);}',
        '.ec-geo-btn-res{background:#f59b1e;color:#00405a;}',
        '.ec-geo-btn-wa{background:#25d366;color:#fff;}',
        '.ec-geo-dismiss{',
          'position:absolute;top:12px;right:12px;',
          'background:transparent;border:none;',
          'color:rgba(255,255,255,0.5);font-size:16px;',
          'cursor:pointer;padding:4px 8px;line-height:1;',
          'transition:color .2s;',
        '}',
        '.ec-geo-dismiss:hover{color:#fff;}',
        /* Acima do mobile bottom nav */
        '@media(max-width:720px){',
          '#ec-geo-banner{bottom:56px;}',
        '}',
      ].join('');
      document.head.appendChild(style);
    }

    document.body.appendChild(banner);

    // Animar entrada
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        banner.classList.add('ec-visible');
      });
    });

    // Botão fechar
    banner.querySelector('.ec-geo-dismiss').addEventListener('click', function() {
      banner.classList.remove('ec-visible');
      markDismissed();
      setTimeout(function() { banner.remove(); }, 400);
    });

    // Auto-fechar após 30 segundos
    setTimeout(function() {
      if (document.getElementById('ec-geo-banner')) {
        banner.classList.remove('ec-visible');
        setTimeout(function() { if (banner.parentNode) banner.remove(); }, 400);
      }
    }, 30000);
  }

  // ── Lógica principal ──────────────────────────────────────────
  function init() {
    // Só roda em mobile (largura ≤ 960px) ou se forçado via ?geo=1
    var isMobile = window.innerWidth <= 960;
    var forceGeo = window.location.search.indexOf('geo=1') !== -1;
    if (!isMobile && !forceGeo) return;

    // Verificar se foi dispensado recentemente
    if (wasDismissed()) return;

    // Verificar suporte à Geolocation API
    if (!navigator.geolocation) return;

    var lang = getLang();

    navigator.geolocation.getCurrentPosition(
      function(pos) {
        var dist = haversine(
          pos.coords.latitude, pos.coords.longitude,
          EC.lat, EC.lng
        );
        // Só exibir se estiver dentro do raio de 5km
        if (dist <= EC.URCA_ZONE) {
          showBanner(dist, lang);
        }
      },
      function(err) {
        // Silenciosamente ignorar erros de permissão
      },
      {
        enableHighAccuracy: true,
        timeout: 8000,
        maximumAge: 300000 // cache de 5 min
      }
    );
  }

  // Iniciar após carregamento da página
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
