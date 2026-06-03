(function(){
  'use strict';
  if (window.ecR2D2BannerLoaded) return;
  window.ecR2D2BannerLoaded = true;

  function currentLang(){
    var l = (document.documentElement.lang || 'pt').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  function browserLang(){
    var l = ((navigator.languages && navigator.languages[0]) || navigator.language || '').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  function rememberInterest(){
    var p = location.pathname.toLowerCase();
    try {
      localStorage.setItem('ec_last_visit_at', String(Date.now()));
      var visits = Number(localStorage.getItem('ec_visit_count') || '0') + 1;
      localStorage.setItem('ec_visit_count', String(visits));
      if (p.indexOf('cafe') >= 0 || p.indexOf('breakfast') >= 0) localStorage.setItem('ec_interest', 'breakfast');
      if (p.indexOf('almoco') >= 0 || p.indexOf('lunch') >= 0) localStorage.setItem('ec_interest', 'lunch');
      if (p.indexOf('evento') >= 0 || p.indexOf('event') >= 0) localStorage.setItem('ec_interest', 'events');
      if (p.indexOf('romant') >= 0) localStorage.setItem('ec_interest', 'romantic');
    } catch(e) {}
  }

  function hasReservationClick(){
    try { return localStorage.getItem('ec_reservation_clicked') === '1'; } catch(e) { return false; }
  }

  document.addEventListener('click', function(evt){
    var a = evt.target && evt.target.closest ? evt.target.closest('a[href]') : null;
    if (!a) return;
    var href = (a.getAttribute('href') || '').toLowerCase();
    var txt = (a.textContent || '').toLowerCase();
    if (href.indexOf('tagme.com.br') >= 0 || /reserv|reserve|reserva/.test(txt)) {
      try { localStorage.setItem('ec_reservation_clicked','1'); } catch(e) {}
    }
  }, true);

  function content(){
    var h = new Date().getHours();
    var l = currentLang();
    var b = browserLang();
    var slot = h < 11 ? 'morning' : h < 15 ? 'lunch' : h < 19 ? 'sunset' : 'evening';
    var interest = '';
    var visits = 1;
    try {
      interest = localStorage.getItem('ec_interest') || '';
      visits = Number(localStorage.getItem('ec_visit_count') || '1');
    } catch(e) {}

    if (b !== l && !sessionStorage.getItem('ec_language_suggestion_seen')) {
      sessionStorage.setItem('ec_language_suggestion_seen','1');
      if (b === 'en') return ['Prefer English?', 'We also have an English version with practical information for international visitors.', 'Open English', '/en/'];
      if (b === 'es') return ['¿Prefiere español?', 'También tenemos una versión en español con información práctica para visitantes.', 'Abrir español', '/es/'];
    }

    if (visits > 1 && !hasReservationClick()) {
      if (interest === 'breakfast') {
        return l === 'en' ? ['Welcome back — still thinking about breakfast?', 'Book your breakfast with a Sugarloaf view before visiting Urca Hill.', 'Reserve breakfast', 'https://go.tagme.com.br/embaixadacarioca'] : l === 'es' ? ['Bienvenido de vuelta — ¿todavía pensando en el desayuno?', 'Reserve su desayuno con vista al Pan de Azúcar antes de visitar el Morro da Urca.', 'Reservar desayuno', 'https://go.tagme.com.br/embaixadacarioca'] : ['Bem-vindo de volta — ainda pensando no café da manhã?', 'Reserve o café com vista para o Pão de Açúcar antes de visitar o Morro da Urca.', 'Reservar café', 'https://go.tagme.com.br/embaixadacarioca'];
      }
      if (interest === 'romantic') {
        return l === 'en' ? ['Welcome back — plan the romantic moment', 'View, caipirinhas and Brazilian food at Urca Hill.', 'Reserve a table', 'https://go.tagme.com.br/embaixadacarioca'] : l === 'es' ? ['Bienvenido de vuelta — planifique el momento romántico', 'Vista, caipirinhas y comida brasileña en el Morro da Urca.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca'] : ['Bem-vindo de volta — planeje o momento especial', 'Vista, caipirinhas e comida brasileira no Morro da Urca.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca'];
      }
    }

    var copy = {
      pt: {
        morning: ['Café da manhã com vista no Morro da Urca', 'Comece o passeio no Parque Bondinho com café, frutas, pães e vista para o Pão de Açúcar.', 'Ver café da manhã', '/cafe-da-manha.html'],
        lunch: ['Almoço carioca no Parque Bondinho', 'Picanha, feijoada premiada, caipirinhas e chope gelado na primeira parada do bondinho.', 'Ver almoço', '/almoco.html'],
        sunset: ['Entardecer no alto do Rio', 'Drinks, caipirinhas e vista para transformar a visita ao Morro da Urca em memória.', 'Ver entardecer', '/entardecer.html'],
        evening: ['Reserve sua experiência no Morro da Urca', 'Planeje café da manhã, almoço ou evento com vista dentro do Parque Bondinho.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca']
      },
      en: {
        morning: ['Breakfast with a Sugarloaf view', 'Start your visit at Urca Hill with coffee, fruit, breads and a direct view of Sugarloaf.', 'See breakfast', '/en/cafe-da-manha.html'],
        lunch: ['Brazilian lunch at Sugarloaf Cable Car Park', 'Picanha, feijoada, caipirinhas and cold draft beer at the first cable car stop.', 'See lunch', '/en/almoco.html'],
        sunset: ['Sunset drinks above Rio', 'Caipirinhas, cocktails and the Urca Hill view before or after your Sugarloaf visit.', 'See sunset', '/en/sunset.html'],
        evening: ['Plan your Urca Hill experience', 'Book breakfast, lunch or a private event inside Sugarloaf Cable Car Park.', 'Reserve a table', 'https://go.tagme.com.br/embaixadacarioca']
      },
      es: {
        morning: ['Desayuno con vista al Pan de Azúcar', 'Empiece su visita en el Morro da Urca con café, frutas, panes y vista directa al Pan de Azúcar.', 'Ver desayuno', '/es/cafe-da-manha.html'],
        lunch: ['Almuerzo brasileño en el Parque Bondinho', 'Picanha, feijoada, caipirinhas y chopp frío en la primera parada del teleférico.', 'Ver almuerzo', '/es/almoco.html'],
        sunset: ['Atardecer en lo alto de Río', 'Caipirinhas, drinks y vista desde el Morro da Urca para completar la visita.', 'Ver atardecer', '/es/sunset.html'],
        evening: ['Planifique su experiencia en el Morro da Urca', 'Reserve desayuno, almuerzo o evento privado dentro del Parque Bondinho.', 'Reservar mesa', 'https://go.tagme.com.br/embaixadacarioca']
      }
    };
    return copy[l][slot];
  }

  function injectStyle(){
    if (document.getElementById('ec-r2d2-banner-style')) return;
    var css = '.ec-r2d2-banner{position:sticky;top:0;z-index:1000;background:#00405a;color:#f6efde;border-bottom:1px solid rgba(246,239,222,.18);padding:14px 20px;font-family:Catamaran,Verdana,system-ui,sans-serif}.ec-r2d2-banner__inner{max-width:1180px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:18px}.ec-r2d2-banner strong{display:block;color:#fff;font-size:18px;line-height:1.15}.ec-r2d2-banner span{display:block;color:rgba(246,239,222,.86);font-size:15px;line-height:1.35}.ec-r2d2-banner a{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:0 18px;border-radius:999px;background:#f59b1e;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:12px}.ec-r2d2-banner button{background:transparent;border:0;color:#f6efde;font-size:22px;line-height:1;cursor:pointer;padding:6px}.ec-r2d2-banner__copy{display:flex;align-items:center;gap:14px}.ec-r2d2-banner__dot{width:10px;height:10px;border-radius:99px;background:#f59b1e;box-shadow:0 0 0 6px rgba(245,155,30,.18)}@media(max-width:760px){.ec-r2d2-banner__inner{align-items:flex-start}.ec-r2d2-banner__copy{align-items:flex-start}.ec-r2d2-banner a{display:none}.ec-r2d2-banner strong{font-size:16px}.ec-r2d2-banner span{font-size:14px}}';
    var style = document.createElement('style');
    style.id = 'ec-r2d2-banner-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function render(){
    rememberInterest();
    if (sessionStorage.getItem('ec_r2d2_banner_closed') === '1') return;
    if (document.querySelector('.ec-r2d2-banner')) return;
    injectStyle();
    var c = content();
    var bar = document.createElement('aside');
    bar.className = 'ec-r2d2-banner';
    bar.setAttribute('aria-label', 'Sugestão contextual da Embaixada Carioca');
    bar.innerHTML = '<div class="ec-r2d2-banner__inner"><div class="ec-r2d2-banner__copy"><i class="ec-r2d2-banner__dot" aria-hidden="true"></i><div><strong>'+c[0]+'</strong><span>'+c[1]+'</span></div></div><a href="'+c[3]+'">'+c[2]+'</a><button type="button" aria-label="Fechar">×</button></div>';
    document.body.insertBefore(bar, document.body.firstChild);
    /* Ajustar o top do nav fixo para não sobrepor o banner */
    function adjustNavTop(){
      var nav = document.getElementById('topnav') || document.querySelector('nav.top');
      if (!nav) return;
      var bh = document.body.contains(bar) ? bar.offsetHeight : 0;
      if (bh > 0) {
        nav.style.setProperty('top', bh + 'px', 'important');
      } else {
        nav.style.removeProperty('top');
      }
    }
    adjustNavTop();
    window.addEventListener('resize', adjustNavTop, { passive: true });
    /* Ao fechar o banner, resetar o top do nav */
    bar.querySelector('button').addEventListener('click', function(){
      sessionStorage.setItem('ec_r2d2_banner_closed','1');
      bar.remove();
      var nav = document.getElementById('topnav') || document.querySelector('nav.top');
      if (nav) nav.style.removeProperty('top');
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, { once:true });
  else render();
})();
