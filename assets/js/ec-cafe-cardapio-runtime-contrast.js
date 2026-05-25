// Embaixada Carioca — runtime contrast fix for cafe-da-manha cardapio cards
// Applies final DOM styles after legacy/global CSS locks have loaded.
(function () {
  'use strict';

  var AREIA = '#f6efde';
  var AREIA_MUTED = '#dbe7d0';
  var AMARELO = '#ffc62e';
  var AZUL = '#00405a';
  var CINZA = '#485156';
  var DOURADO = '#9a6500';

  function setElementStyles(el, styles) {
    if (!el || !styles) return;
    Object.keys(styles).forEach(function (prop) {
      el.style.setProperty(prop, styles[prop], 'important');
    });
  }

  function parseRGB(value) {
    var match = String(value || '').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([0-9.]+))?\)/i);
    if (!match) return null;
    return {
      r: Number(match[1]),
      g: Number(match[2]),
      b: Number(match[3]),
      a: match[4] == null ? 1 : Number(match[4])
    };
  }

  function isDarkCard(card) {
    var bg = parseRGB(window.getComputedStyle(card).backgroundColor);
    if (!bg || bg.a < 0.35) return false;
    var luma = (0.2126 * bg.r) + (0.7152 * bg.g) + (0.0722 * bg.b);
    return luma < 125;
  }

  function fixDarkCard(card) {
    setElementStyles(card, {
      color: AREIA,
      '-webkit-text-fill-color': AREIA,
      opacity: '1',
      'text-shadow': 'none',
      filter: 'none',
      'mix-blend-mode': 'normal'
    });

    card.querySelectorAll('h1,h2,h3,h4,h5,h6,.cardapio-card-header,.cardapio-card-header *,.item-nome').forEach(function (el) {
      setElementStyles(el, {
        color: AREIA,
        '-webkit-text-fill-color': AREIA,
        opacity: '1',
        'text-shadow': 'none',
        filter: 'none',
        'mix-blend-mode': 'normal'
      });
    });

    card.querySelectorAll('p,li,span,small,.item-sub,.item-desc,.item-add,.cardapio-card-nota').forEach(function (el) {
      setElementStyles(el, {
        color: AREIA_MUTED,
        '-webkit-text-fill-color': AREIA_MUTED,
        opacity: '1',
        'text-shadow': 'none',
        filter: 'none',
        'mix-blend-mode': 'normal'
      });
    });

    card.querySelectorAll('.item-preco,.cardapio-destaque-mini strong,.metodo-icone,strong,b').forEach(function (el) {
      setElementStyles(el, {
        color: AMARELO,
        '-webkit-text-fill-color': AMARELO,
        opacity: '1',
        'text-shadow': 'none',
        filter: 'none',
        'mix-blend-mode': 'normal'
      });
    });

    card.querySelectorAll('.cardapio-lista li').forEach(function (el) {
      setElementStyles(el, {
        'border-bottom-color': 'rgba(246,239,222,.16)'
      });
    });
  }

  function fixLightCard(card) {
    setElementStyles(card, {
      color: AZUL,
      '-webkit-text-fill-color': AZUL,
      opacity: '1',
      'text-shadow': 'none',
      filter: 'none',
      'mix-blend-mode': 'normal'
    });

    card.querySelectorAll('h1,h2,h3,h4,h5,h6,.cardapio-card-header,.cardapio-card-header *,.item-nome').forEach(function (el) {
      setElementStyles(el, {
        color: AZUL,
        '-webkit-text-fill-color': AZUL,
        opacity: '1',
        'text-shadow': 'none'
      });
    });

    card.querySelectorAll('p,li,span,small,.item-sub,.item-desc,.item-add,.cardapio-card-nota').forEach(function (el) {
      setElementStyles(el, {
        color: CINZA,
        '-webkit-text-fill-color': CINZA,
        opacity: '1',
        'text-shadow': 'none'
      });
    });

    card.querySelectorAll('.item-preco').forEach(function (el) {
      setElementStyles(el, {
        color: DOURADO,
        '-webkit-text-fill-color': DOURADO,
        opacity: '1'
      });
    });
  }

  function fixCafeCardapioContrast() {
    var cards = Array.prototype.slice.call(document.querySelectorAll('.cardapio-grid .cardapio-card'));
    var darkCount = 0;
    var lightCount = 0;

    cards.forEach(function (card) {
      if (isDarkCard(card)) {
        darkCount += 1;
        fixDarkCard(card);
      } else {
        lightCount += 1;
        fixLightCard(card);
      }
    });

    window.ecCafeCardapioContrast = {
      success: true,
      totalCards: cards.length,
      darkCards: darkCount,
      lightCards: lightCount,
      sampleDarkSubColor: (document.querySelector('.cardapio-card--cafe .item-sub') && window.getComputedStyle(document.querySelector('.cardapio-card--cafe .item-sub')).color) || null,
      sampleDarkNameColor: (document.querySelector('.cardapio-card--escuro .item-nome') && window.getComputedStyle(document.querySelector('.cardapio-card--escuro .item-nome')).color) || null
    };
  }

  function scheduleFixes() {
    fixCafeCardapioContrast();
    window.setTimeout(fixCafeCardapioContrast, 50);
    window.setTimeout(fixCafeCardapioContrast, 250);
    window.setTimeout(fixCafeCardapioContrast, 900);
    window.setTimeout(fixCafeCardapioContrast, 1600);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scheduleFixes, { once: true });
  } else {
    scheduleFixes();
  }
  window.addEventListener('load', scheduleFixes, { once: true });

  var observer = new MutationObserver(function () {
    window.clearTimeout(observer._ecTimer);
    observer._ecTimer = window.setTimeout(fixCafeCardapioContrast, 80);
  });
  observer.observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style'] });
})();
