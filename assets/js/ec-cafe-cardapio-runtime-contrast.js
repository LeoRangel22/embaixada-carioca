// Embaixada Carioca — runtime contrast fix for cafe-da-manha cardapio cards
// Purpose: apply final computed styles after legacy/global CSS locks have loaded.
(function () {
  'use strict';

  var DARK_CARD_SELECTOR = [
    '.cardapio-grid .cardapio-card--escuro',
    '.cardapio-grid .cardapio-card--verde-escuro',
    '.cardapio-grid .cardapio-card--roxo',
    '.cardapio-grid .cardapio-card--amarelo-escuro',
    '.cardapio-grid .cardapio-card--cafe'
  ].join(',');

  var LIGHT_CARD_SELECTOR = [
    '.cardapio-grid .cardapio-card--amarelo',
    '.cardapio-grid .cardapio-card--verde',
    '.cardapio-grid .cardapio-card--verde-agua'
  ].join(',');

  function setElementStyles(el, styles) {
    if (!el || !styles) return;
    Object.keys(styles).forEach(function (prop) {
      el.style.setProperty(prop, styles[prop], 'important');
    });
  }

  function applyToAll(selector, styles) {
    document.querySelectorAll(selector).forEach(function (el) {
      setElementStyles(el, styles);
    });
  }

  function fixCafeCardapioContrast() {
    var darkCards = document.querySelectorAll(DARK_CARD_SELECTOR);
    var lightCards = document.querySelectorAll(LIGHT_CARD_SELECTOR);

    darkCards.forEach(function (card) {
      setElementStyles(card, {
        color: '#f6efde',
        '-webkit-text-fill-color': '#f6efde',
        opacity: '1',
        'text-shadow': 'none',
        filter: 'none',
        'mix-blend-mode': 'normal'
      });

      card.querySelectorAll('h3, .cardapio-card-header h3, .item-nome').forEach(function (el) {
        setElementStyles(el, {
          color: '#f6efde',
          '-webkit-text-fill-color': '#f6efde',
          opacity: '1',
          'text-shadow': 'none',
          filter: 'none',
          'mix-blend-mode': 'normal'
        });
      });

      card.querySelectorAll('.item-sub, .item-desc, .item-add, .cardapio-card-nota').forEach(function (el) {
        setElementStyles(el, {
          color: '#dbe7d0',
          '-webkit-text-fill-color': '#dbe7d0',
          opacity: '1',
          'text-shadow': 'none',
          filter: 'none',
          'mix-blend-mode': 'normal'
        });
      });

      card.querySelectorAll('.item-preco, .cardapio-destaque-mini strong, .metodo-icone').forEach(function (el) {
        setElementStyles(el, {
          color: '#ffc62e',
          '-webkit-text-fill-color': '#ffc62e',
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
    });

    lightCards.forEach(function (card) {
      setElementStyles(card, {
        color: '#00405a',
        '-webkit-text-fill-color': '#00405a',
        opacity: '1',
        'text-shadow': 'none',
        filter: 'none',
        'mix-blend-mode': 'normal'
      });

      card.querySelectorAll('h3, .cardapio-card-header h3, .item-nome').forEach(function (el) {
        setElementStyles(el, {
          color: '#00405a',
          '-webkit-text-fill-color': '#00405a',
          opacity: '1',
          'text-shadow': 'none'
        });
      });

      card.querySelectorAll('.item-sub, .item-desc, .item-add, .cardapio-card-nota').forEach(function (el) {
        setElementStyles(el, {
          color: '#485156',
          '-webkit-text-fill-color': '#485156',
          opacity: '1',
          'text-shadow': 'none'
        });
      });

      card.querySelectorAll('.item-preco').forEach(function (el) {
        setElementStyles(el, {
          color: '#9a6500',
          '-webkit-text-fill-color': '#9a6500',
          opacity: '1'
        });
      });
    });

    // Expose minimal debug info for DevTools.
    window.ecCafeCardapioContrast = {
      success: true,
      darkCards: darkCards.length,
      lightCards: lightCards.length,
      sampleSubColor: (document.querySelector('.cardapio-card--cafe .item-sub') && window.getComputedStyle(document.querySelector('.cardapio-card--cafe .item-sub')).color) || null,
      sampleNameColor: (document.querySelector('.cardapio-card--escuro .item-nome') && window.getComputedStyle(document.querySelector('.cardapio-card--escuro .item-nome')).color) || null
    };
  }

  function scheduleFixes() {
    fixCafeCardapioContrast();
    window.setTimeout(fixCafeCardapioContrast, 50);
    window.setTimeout(fixCafeCardapioContrast, 250);
    window.setTimeout(fixCafeCardapioContrast, 900);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scheduleFixes, { once: true });
  } else {
    scheduleFixes();
  }
  window.addEventListener('load', scheduleFixes, { once: true });

  // Guard against late scripts/classes changing the DOM after load.
  var observer = new MutationObserver(function () {
    window.clearTimeout(observer._ecTimer);
    observer._ecTimer = window.setTimeout(fixCafeCardapioContrast, 60);
  });
  observer.observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style'] });
})();
