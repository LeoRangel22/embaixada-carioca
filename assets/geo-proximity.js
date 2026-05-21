(function(){
  'use strict';

  function injectStyle(){
    if(document.getElementById('ec-breakfast-gallery-visual-fix')) return;
    var css = `
      .cafe-galeria{
        display:grid!important;
        grid-template-columns:2fr 1fr 1fr!important;
        grid-template-rows:280px 280px!important;
        gap:12px!important;
        margin-bottom:3rem!important;
        border-radius:16px!important;
        overflow:hidden!important;
      }
      .cafe-galeria-item{position:relative!important;overflow:hidden!important;background:#00405a!important;}
      .cafe-galeria-item--tall{grid-row:span 2!important;}
      .cafe-galeria-item img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;}
      .cafe-galeria-item--focus-arms img{object-position:center center!important;}
      .cafe-galeria-caption{position:absolute!important;left:0!important;right:0!important;bottom:0!important;padding:1.6rem .9rem .7rem!important;background:linear-gradient(transparent,rgba(0,0,0,.68))!important;color:#fff!important;font-size:.8rem!important;}
      .photo-ph.cafe-photo.tall[data-label*='Café'],
      .photo-ph.cafe-photo.tall[data-label*='café'],
      .photo-ph.cafe-photo.tall[data-label*='Foto']{
        background-image:url('/assets/cafe/cafe-casal-mesa-cima.webp')!important;
        background-size:cover!important;
        background-position:center center!important;
        border-radius:18px!important;
        overflow:hidden!important;
        box-shadow:0 18px 48px rgba(0,0,0,.18)!important;
      }
      .photo-ph.cafe-photo.tall[data-label*='Café']::before,
      .photo-ph.cafe-photo.tall[data-label*='café']::before,
      .photo-ph.cafe-photo.tall[data-label*='Foto']::before{display:none!important;content:none!important;}
      .photo-ph.cafe-photo.tall[data-label*='Café']::after,
      .photo-ph.cafe-photo.tall[data-label*='café']::after,
      .photo-ph.cafe-photo.tall[data-label*='Foto']::after{content:''!important;position:absolute!important;inset:0!important;background:linear-gradient(180deg,rgba(0,64,90,0) 55%,rgba(0,64,90,.24) 100%)!important;}
      .btn, a.btn, .ctas a, .hero-ctas a{color:#00405a!important;-webkit-text-fill-color:#00405a!important;font-weight:900!important;}
      .ctas a[href*='almoco'], .hero-ctas a[href*='almoco'], a[href*='almoco'].btn{color:#fff!important;-webkit-text-fill-color:#fff!important;font-weight:900!important;letter-spacing:.12em!important;}
      @media(max-width:900px){
        .cafe-galeria{grid-template-columns:1fr 1fr!important;grid-template-rows:220px 220px 220px!important;}
        .cafe-galeria-item--tall{grid-row:span 1!important;grid-column:span 2!important;}
      }
      @media(max-width:600px){
        .cafe-galeria{grid-template-columns:1fr!important;grid-template-rows:none!important;}
        .cafe-galeria-item,.cafe-galeria-item--tall{grid-column:auto!important;grid-row:auto!important;height:260px!important;}
        .cafe-galeria-item--tall{height:320px!important;}
      }
    `;
    var style=document.createElement('style');
    style.id='ec-breakfast-gallery-visual-fix';
    style.textContent=css;
    document.head.appendChild(style);
  }

  function item(src, alt, caption, extraClass){
    var div=document.createElement('div');
    div.className='cafe-galeria-item '+(extraClass||'');
    div.innerHTML='<img src="'+src+'" alt="'+alt+'" loading="lazy" decoding="async"><div class="cafe-galeria-caption">'+caption+'</div>';
    return div;
  }

  function fixBreakfastGallery(){
    if(!/cafe-da-manha/i.test(location.pathname)) return;
    injectStyle();

    var gallery=document.querySelector('.cafe-galeria');
    if(gallery && !gallery.dataset.ecFixed){
      gallery.dataset.ecFixed='1';
      gallery.innerHTML='';
      gallery.appendChild(item('/assets/cafe/cafe-casal-mesa-cima.webp','Mesa de café da manhã vista de cima, com duas pessoas compartilhando o Café da Embaixada','Café da manhã para compartilhar, com experiência real à mesa','cafe-galeria-item--tall cafe-galeria-item--focus-arms'));
      gallery.appendChild(item('/assets/cafe/cafe-mesa-iogurte-acai.webp','Detalhe do iogurte natural, açaí, frutas e frios do café da manhã','Iogurte, açaí, frutas e frios'));
      gallery.appendChild(item('/assets/cafe/cafe-da-embaixada-mesa-completa.webp','Mesa completa do Café da Embaixada com pães, frutas, frios e bebidas quentes','Mesa completa do Café da Embaixada'));
      gallery.appendChild(item('/assets/cafe/cafe-da-embaixada-vista-lateral.webp','Vista lateral da mesa do Café da Embaixada com acompanhamentos','Mesa farta com acompanhamentos'));
      gallery.appendChild(item('/assets/cafe/cafe-mesa-cima-spread.webp','Vista superior do café da manhã completo da Embaixada Carioca','Spread completo do Café da Embaixada'));
    }

    var ph=document.querySelector('.photo-ph.cafe-photo.tall');
    if(ph && !ph.dataset.ecFixed){
      ph.dataset.ecFixed='1';
      ph.setAttribute('role','img');
      ph.setAttribute('aria-label','Mesa de café da manhã da Embaixada Carioca com duas pessoas compartilhando pães, frios, café, açaí e acompanhamentos.');
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',fixBreakfastGallery,{once:true});
  else fixBreakfastGallery();
  window.addEventListener('load',fixBreakfastGallery,{once:true});
})();
