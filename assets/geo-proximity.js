(function(){
  'use strict';

  var AREIA = '#f6efde';
  var AZUL = '#00405a';
  var CINZA = '#485156';
  var DOURADO = '#9a6500';

  function setElementStyles(el, styles){
    if(!el || !styles) return;
    Object.keys(styles).forEach(function(prop){
      el.style.setProperty(prop, styles[prop], 'important');
    });
  }

  function parseRGB(value){
    var m = String(value || '').match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([0-9.]+))?\)/i);
    if(!m) return null;
    return {r:+m[1], g:+m[2], b:+m[3], a:m[4] == null ? 1 : +m[4]};
  }

  function isDark(el){
    var bg = parseRGB(window.getComputedStyle(el).backgroundColor);
    if(!bg || bg.a < .35) return false;
    var luma = (0.2126 * bg.r) + (0.7152 * bg.g) + (0.0722 * bg.b);
    return luma < 125;
  }

  function fixCafeCardapioContrast(){
    if(!/cafe-da-manha/i.test(location.pathname)) return;
    var cards = Array.prototype.slice.call(document.querySelectorAll('.cardapio-grid .cardapio-card'));
    var darkCount = 0;
    var lightCount = 0;

    cards.forEach(function(card){
      if(isDark(card)){
        darkCount += 1;
        setElementStyles(card, {
          color: AREIA,
          '-webkit-text-fill-color': AREIA,
          opacity: '1',
          'text-shadow': 'none',
          filter: 'none',
          'mix-blend-mode': 'normal'
        });
        card.querySelectorAll('*').forEach(function(el){
          setElementStyles(el, {
            color: AREIA,
            '-webkit-text-fill-color': AREIA,
            opacity: '1',
            'text-shadow': 'none',
            filter: 'none',
            'mix-blend-mode': 'normal'
          });
        });
        card.querySelectorAll('.cardapio-lista li').forEach(function(el){
          setElementStyles(el, {'border-bottom-color':'rgba(246,239,222,.18)'});
        });
      } else {
        lightCount += 1;
        setElementStyles(card, {
          color: AZUL,
          '-webkit-text-fill-color': AZUL,
          opacity: '1',
          'text-shadow': 'none',
          filter: 'none',
          'mix-blend-mode': 'normal'
        });
        card.querySelectorAll('h1,h2,h3,h4,h5,h6,.item-nome,.cardapio-card-header,.cardapio-card-header *').forEach(function(el){
          setElementStyles(el, {color: AZUL, '-webkit-text-fill-color': AZUL, opacity:'1', 'text-shadow':'none'});
        });
        card.querySelectorAll('p,li,span,small,.item-sub,.item-desc,.item-add,.cardapio-card-nota').forEach(function(el){
          setElementStyles(el, {color: CINZA, '-webkit-text-fill-color': CINZA, opacity:'1', 'text-shadow':'none'});
        });
        card.querySelectorAll('.item-preco').forEach(function(el){
          setElementStyles(el, {color: DOURADO, '-webkit-text-fill-color': DOURADO, opacity:'1'});
        });
      }
    });

    window.ecCafeCardapioContrast = {
      success: true,
      strategy: 'runtime-background-aware-via-geo-proximity',
      totalCards: cards.length,
      darkCards: darkCount,
      lightCards: lightCount,
      sampleDarkColor: (document.querySelector('.cardapio-grid .cardapio-card--escuro .item-nome') && window.getComputedStyle(document.querySelector('.cardapio-grid .cardapio-card--escuro .item-nome')).color) || null
    };
  }

  function fixBondinhoCopy(){
    var replacements = [
      [/Restaurante do Bondinho/g, 'Restaurante no Bondinho'],
      [/restaurante do Bondinho/g, 'restaurante no Bondinho'],
      [/restaurante do bondinho/g, 'restaurante no bondinho'],
      [/RESTAURANTE DO BONDINHO/g, 'RESTAURANTE NO BONDINHO']
    ];
    var walker = document.createTreeWalker(document.body || document.documentElement, NodeFilter.SHOW_TEXT, {
      acceptNode: function(node){
        if(!node.nodeValue || !/Restaurante do Bondinho|restaurante do Bondinho|restaurante do bondinho|RESTAURANTE DO BONDINHO/.test(node.nodeValue)) return NodeFilter.FILTER_REJECT;
        var p = node.parentElement;
        if(p && /SCRIPT|STYLE|NOSCRIPT|TEXTAREA|INPUT/.test(p.tagName)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var changed = 0;
    var nodes = [];
    while(walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function(node){
      var next = node.nodeValue;
      replacements.forEach(function(pair){ next = next.replace(pair[0], pair[1]); });
      if(next !== node.nodeValue){ node.nodeValue = next; changed += 1; }
    });
    document.querySelectorAll('[title],[aria-label],[alt]').forEach(function(el){
      ['title','aria-label','alt'].forEach(function(attr){
        var value = el.getAttribute(attr);
        if(!value) return;
        var next = value;
        replacements.forEach(function(pair){ next = next.replace(pair[0], pair[1]); });
        if(next !== value){ el.setAttribute(attr, next); changed += 1; }
      });
    });
    window.ecBondinhoCopyFix = {success:true, changedNodes: changed};
  }

  function injectBreakfastGalleryStyle(){
    if(document.getElementById('ec-breakfast-gallery-visual-fix')) return;
    var css = `
      .cafe-galeria{display:grid!important;grid-template-columns:2fr 1fr 1fr!important;grid-template-rows:280px 280px!important;gap:12px!important;margin-bottom:3rem!important;border-radius:16px!important;overflow:hidden!important;}
      .cafe-galeria-item{position:relative!important;overflow:hidden!important;background:#00405a!important;}
      .cafe-galeria-item--tall{grid-row:span 2!important;}
      .cafe-galeria-item img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;}
      .cafe-galeria-item--focus-arms img{object-position:center center!important;}
      .cafe-galeria-caption{position:absolute!important;left:0!important;right:0!important;bottom:0!important;padding:1.6rem .9rem .7rem!important;background:linear-gradient(transparent,rgba(0,0,0,.68))!important;color:#fff!important;font-size:.8rem!important;}
      .btn,a.btn,.ctas a,.hero-ctas a{font-weight:900!important;}
      @media(max-width:900px){.cafe-galeria{grid-template-columns:1fr 1fr!important;grid-template-rows:220px 220px 220px!important}.cafe-galeria-item--tall{grid-row:span 1!important;grid-column:span 2!important}}
      @media(max-width:600px){.cafe-galeria{grid-template-columns:1fr!important;grid-template-rows:none!important}.cafe-galeria-item,.cafe-galeria-item--tall{grid-column:auto!important;grid-row:auto!important;height:260px!important}.cafe-galeria-item--tall{height:320px!important}}
    `;
    var style=document.createElement('style');
    style.id='ec-breakfast-gallery-visual-fix';
    style.textContent=css;
    document.head.appendChild(style);
  }

  function galleryItem(src, alt, caption, extraClass){
    var div=document.createElement('div');
    div.className='cafe-galeria-item '+(extraClass||'');
    div.innerHTML='<img src="'+src+'" alt="'+alt+'" loading="lazy" decoding="async"><div class="cafe-galeria-caption">'+caption+'</div>';
    return div;
  }

  function fixBreakfastGallery(){
    if(!/cafe-da-manha/i.test(location.pathname)) return;
    injectBreakfastGalleryStyle();
    var gallery=document.querySelector('.cafe-galeria');
    if(gallery && !gallery.dataset.ecFixed){
      gallery.dataset.ecFixed='1';
      gallery.innerHTML='';
      gallery.appendChild(galleryItem('/assets/cafe/cafe-casal-mesa-cima.webp','Mesa de café da manhã vista de cima, com duas pessoas compartilhando o Café da Embaixada','Café da manhã para compartilhar, com experiência real à mesa','cafe-galeria-item--tall cafe-galeria-item--focus-arms'));
      gallery.appendChild(galleryItem('/assets/cafe/cafe-mesa-iogurte-acai.webp','Detalhe do iogurte natural, açaí, frutas e frios do café da manhã','Iogurte, açaí, frutas e frios'));
      gallery.appendChild(galleryItem('/assets/cafe/cafe-da-embaixada-mesa-completa.webp','Mesa completa do Café da Embaixada com pães, frutas, frios e bebidas quentes','Mesa completa do Café da Embaixada'));
      gallery.appendChild(galleryItem('/assets/cafe/cafe-da-embaixada-vista-lateral.webp','Vista lateral da mesa do Café da Embaixada com acompanhamentos','Mesa farta com acompanhamentos'));
      gallery.appendChild(galleryItem('/assets/cafe/cafe-mesa-cima-spread.webp','Vista superior do café da manhã completo da Embaixada Carioca','Spread completo do Café da Embaixada'));
    }
  }

  function runP0(){
    fixBondinhoCopy();
    fixBreakfastGallery();
    fixCafeCardapioContrast();
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', runP0, {once:true});
  } else {
    runP0();
  }
  window.addEventListener('load', runP0, {once:true});
  [60,250,900,1600,3000].forEach(function(ms){window.setTimeout(runP0, ms);});

  var observer = new MutationObserver(function(){
    window.clearTimeout(observer._ecP0Timer);
    observer._ecP0Timer = window.setTimeout(runP0, 100);
  });
  observer.observe(document.documentElement, {childList:true, subtree:true, attributes:true, attributeFilter:['class','style','title','aria-label','alt']});
})();
