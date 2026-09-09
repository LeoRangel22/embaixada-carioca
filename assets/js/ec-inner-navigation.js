/* Supply a drawer only on migrated pages that never had one. */
(function () {
  'use strict';
  function init() {
    if (!document.body.hasAttribute('data-ec-inner')) return;
    var existing = document.getElementById('nav-drawer');
    if (existing && !/\/feijoada(?:\.html)?\/?$/.test(location.pathname)) return;
    if (existing) {
      existing.remove();
      var oldOverlay = document.getElementById('nav-drawer-overlay');
      if (oldOverlay) oldOverlay.remove();
      var oldButton = document.getElementById('nav-hamburger');
      if (oldButton) oldButton.replaceWith(oldButton.cloneNode(true));
    }
    var button = document.getElementById('nav-hamburger');
    var links = document.querySelector('#topnav .nav-links');
    if (!button || !links) return;
    var lang = document.documentElement.lang.slice(0, 2);
    var closeLabel = lang === 'en' ? 'Close menu' : lang === 'es' ? 'Cerrar menú' : 'Fechar menu';
    var drawer = document.createElement('nav');
    drawer.id = 'nav-drawer'; drawer.className = 'ec-inner-drawer';
    drawer.setAttribute('aria-label', button.getAttribute('aria-label') || 'Menu');
    drawer.setAttribute('aria-hidden', 'true');
    var close = document.createElement('button'); close.type = 'button'; close.textContent = closeLabel;
    close.className = 'ec-inner-menu-close'; drawer.appendChild(close);
    var list = links.cloneNode(true); list.className = 'ec-inner-menu-links'; list.removeAttribute('id'); drawer.appendChild(list);
    var reservation = document.querySelector('#topnav .nav-inner > a.btn');
    if (reservation) { var cta = reservation.cloneNode(true); cta.className = 'ec-inner-menu-reserve'; drawer.appendChild(cta); }
    var overlay = document.createElement('div'); overlay.className = 'ec-inner-menu-overlay'; overlay.hidden = true;
    document.body.append(overlay, drawer);
    var previousOverflow = '';
    function shut() { drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); button.setAttribute('aria-expanded','false'); overlay.hidden=true; document.body.style.overflow=previousOverflow; button.focus(); }
    function open() { previousOverflow=document.body.style.overflow; drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); button.setAttribute('aria-expanded','true'); overlay.hidden=false; document.body.style.overflow='hidden'; close.focus(); }
    button.addEventListener('click', function(){ drawer.classList.contains('open') ? shut() : open(); });
    close.addEventListener('click',shut); overlay.addEventListener('click',shut);
    drawer.addEventListener('click', function(e){ if(e.target.closest('a')) shut(); });
    document.addEventListener('keydown',function(e){
      if (!drawer.classList.contains('open')) return;
      if(e.key==='Escape'){e.preventDefault();shut();}
      if(e.key==='Tab'){
        var items=drawer.querySelectorAll('a[href],button');var first=items[0],last=items[items.length-1];
        if(e.shiftKey && document.activeElement===first){e.preventDefault();last.focus();}
        else if(!e.shiftKey && document.activeElement===last){e.preventDefault();first.focus();}
      }
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init,{once:true}); else init();
})();
