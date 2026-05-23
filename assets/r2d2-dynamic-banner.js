(function(){
  'use strict';
  if (window.ecR2D2BannerLoaded) return;
  window.ecR2D2BannerLoaded = true;

  function lang(){
    var l = (document.documentElement.lang || 'pt').toLowerCase();
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('es') === 0) return 'es';
    return 'pt';
  }

  function content(){
    var h = new Date().getHours();
    var l = lang();
    var slot = h < 11 ? 'morning' : h < 15 ? 'lunch' : h < 19 ? 'sunset' : 'evening';
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
    var css = '.ec-r2d2-banner{position:relative;z-index:20;background:#00405a;color:#f6efde;border-bottom:1px solid rgba(246,239,222,.18);padding:14px 20px;font-family:Catamaran,Verdana,system-ui,sans-serif}.ec-r2d2-banner__inner{max-width:1180px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:18px}.ec-r2d2-banner strong{display:block;color:#fff;font-size:18px;line-height:1.15}.ec-r2d2-banner span{display:block;color:rgba(246,239,222,.86);font-size:15px;line-height:1.35}.ec-r2d2-banner a{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:0 18px;border-radius:999px;background:#f59b1e;color:#00405a!important;-webkit-text-fill-color:#00405a!important;text-decoration:none;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:12px}.ec-r2d2-banner button{background:transparent;border:0;color:#f6efde;font-size:22px;line-height:1;cursor:pointer;padding:6px}.ec-r2d2-banner__copy{display:flex;align-items:center;gap:14px}.ec-r2d2-banner__dot{width:10px;height:10px;border-radius:99px;background:#f59b1e;box-shadow:0 0 0 6px rgba(245,155,30,.18)}@media(max-width:760px){.ec-r2d2-banner__inner{align-items:flex-start}.ec-r2d2-banner__copy{align-items:flex-start}.ec-r2d2-banner a{display:none}.ec-r2d2-banner strong{font-size:16px}.ec-r2d2-banner span{font-size:14px}}';
    var style = document.createElement('style');
    style.id = 'ec-r2d2-banner-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function render(){
    if (sessionStorage.getItem('ec_r2d2_banner_closed') === '1') return;
    if (document.querySelector('.ec-r2d2-banner')) return;
    injectStyle();
    var c = content();
    var bar = document.createElement('aside');
    bar.className = 'ec-r2d2-banner';
    bar.setAttribute('aria-label', 'Sugestão contextual da Embaixada Carioca');
    bar.innerHTML = '<div class="ec-r2d2-banner__inner"><div class="ec-r2d2-banner__copy"><i class="ec-r2d2-banner__dot" aria-hidden="true"></i><div><strong>'+c[0]+'</strong><span>'+c[1]+'</span></div></div><a href="'+c[3]+'">'+c[2]+'</a><button type="button" aria-label="Fechar">×</button></div>';
    bar.querySelector('button').addEventListener('click', function(){
      sessionStorage.setItem('ec_r2d2_banner_closed','1');
      bar.remove();
    });
    document.body.insertBefore(bar, document.body.firstChild);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, { once:true });
  else render();
})();
