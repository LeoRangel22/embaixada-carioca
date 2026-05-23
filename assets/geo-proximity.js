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

  function injectFaqStyle(){
    if(document.getElementById('ec-home-faq-professional-fix')) return;
    var css = `
      body[data-screen-label="Home"] .ec-professional-faq{
        background:#f6efde!important;
        color:#00405a!important;
        padding:clamp(64px,7vw,112px) 0!important;
        border-top:1px solid rgba(0,64,90,.10)!important;
        border-bottom:1px solid rgba(0,64,90,.10)!important;
        position:relative!important;
        overflow:hidden!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq *{
        opacity:1!important;
        filter:none!important;
        text-shadow:none!important;
        mix-blend-mode:normal!important;
        -webkit-text-fill-color:currentColor!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-wrap{
        width:min(1120px,calc(100% - 48px))!important;
        margin:0 auto!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-head{
        max-width:760px!important;
        margin:0 auto 42px!important;
        text-align:center!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-kicker{
        display:inline-flex!important;
        align-items:center!important;
        gap:12px!important;
        font-family:"JetBrains Mono",ui-monospace,monospace!important;
        font-size:11px!important;
        letter-spacing:.26em!important;
        text-transform:uppercase!important;
        color:#c47e15!important;
        margin-bottom:16px!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-kicker::before{
        content:""!important;
        width:34px!important;
        height:1px!important;
        background:#f59b1e!important;
        display:inline-block!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq h2{
        font-family:Catamaran,Verdana,system-ui,sans-serif!important;
        font-size:clamp(36px,4vw,64px)!important;
        line-height:1.02!important;
        font-weight:500!important;
        letter-spacing:-.035em!important;
        color:#00405a!important;
        margin:0 0 18px!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq h2 em{
        color:#f59b1e!important;
        font-style:italic!important;
        font-weight:400!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-lede{
        font-size:18px!important;
        line-height:1.62!important;
        color:#485156!important;
        margin:0 auto!important;
        max-width:680px!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-grid{
        display:grid!important;
        grid-template-columns:repeat(2,minmax(0,1fr))!important;
        gap:16px!important;
        align-items:start!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq details{
        background:#fffaf0!important;
        border:1px solid rgba(0,64,90,.14)!important;
        border-left:4px solid #f59b1e!important;
        border-radius:18px!important;
        padding:0!important;
        overflow:hidden!important;
        box-shadow:0 12px 34px rgba(0,64,90,.08)!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq details[open]{
        box-shadow:0 18px 44px rgba(0,64,90,.12)!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq summary{
        cursor:pointer!important;
        list-style:none!important;
        padding:20px 22px!important;
        color:#00405a!important;
        font-weight:800!important;
        font-size:17px!important;
        line-height:1.28!important;
        display:flex!important;
        justify-content:space-between!important;
        gap:16px!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq summary::-webkit-details-marker{display:none!important;}
      body[data-screen-label="Home"] .ec-professional-faq summary::after{
        content:"+"!important;
        flex:0 0 28px!important;
        width:28px!important;
        height:28px!important;
        border-radius:999px!important;
        display:inline-flex!important;
        align-items:center!important;
        justify-content:center!important;
        background:#00405a!important;
        color:#f6efde!important;
        font-weight:900!important;
        line-height:1!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq details[open] summary::after{content:"–"!important;}
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-answer{
        padding:0 22px 22px!important;
        color:#485156!important;
        font-size:16px!important;
        line-height:1.66!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-answer strong{
        color:#00405a!important;
        font-weight:800!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-actions{
        display:flex!important;
        justify-content:center!important;
        flex-wrap:wrap!important;
        gap:14px!important;
        margin-top:34px!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-actions a{
        display:inline-flex!important;
        align-items:center!important;
        justify-content:center!important;
        min-height:52px!important;
        padding:0 24px!important;
        border-radius:999px!important;
        font-family:"JetBrains Mono",ui-monospace,monospace!important;
        font-size:12px!important;
        font-weight:900!important;
        letter-spacing:.14em!important;
        text-transform:uppercase!important;
        text-decoration:none!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-actions a:first-child{
        background:#f59b1e!important;
        color:#00405a!important;
      }
      body[data-screen-label="Home"] .ec-professional-faq .ec-faq-actions a:last-child{
        background:transparent!important;
        border:1px solid rgba(0,64,90,.28)!important;
        color:#00405a!important;
      }
      body[data-screen-label="Home"] .ec-faq-orphan-hidden{display:none!important;}
      @media(max-width:860px){
        body[data-screen-label="Home"] .ec-professional-faq .ec-faq-grid{grid-template-columns:1fr!important;}
        body[data-screen-label="Home"] .ec-professional-faq .ec-faq-wrap{width:min(100% - 32px,1120px)!important;}
        body[data-screen-label="Home"] .ec-professional-faq summary{font-size:16px!important;padding:18px!important;}
        body[data-screen-label="Home"] .ec-professional-faq .ec-faq-answer{padding:0 18px 18px!important;}
      }
    `;
    var style=document.createElement('style');
    style.id='ec-home-faq-professional-fix';
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

  function faqHtml(){
    var faqs = [
      ['Tem restaurante no Bondinho do Pão de Açúcar?', 'Sim. A <strong>Embaixada Carioca</strong> fica dentro do Parque Bondinho Pão de Açúcar, no Morro da Urca, na primeira parada do teleférico. É o restaurante para quem quer comer bem durante a visita, com vista direta para o Pão de Açúcar.'],
      ['Onde fica a Embaixada Carioca?', 'A Embaixada Carioca fica no <strong>Morro da Urca</strong>, dentro do Parque Bondinho Pão de Açúcar, com acesso pela Av. Pasteur, 520, Urca, Rio de Janeiro. O restaurante está na primeira parada do bondinho.'],
      ['Qual o horário de funcionamento?', 'A casa abre todos os dias a partir das <strong>8h30</strong>. O café da manhã é servido pela manhã e o almoço funciona no período de maior movimento do parque. Em dias de programação especial, os horários podem acompanhar o funcionamento do Parque Bondinho.'],
      ['Tem café da manhã todos os dias?', 'Sim. A Embaixada Carioca serve <strong>café da manhã todos os dias</strong>, em um formato pensado para quem quer começar o passeio no Morro da Urca com vista, pães, frutas, bebidas quentes e itens especiais da casa.'],
      ['Precisa pagar o bondinho para ir ao restaurante?', 'O acesso principal ao restaurante é pelo Parque Bondinho. Para subir de bondinho, é necessário ter ingresso do parque. Também existe acesso por trilha pela Praia Vermelha, respeitando as regras e horários do parque.'],
      ['Quem sobe pela trilha pode usar o bondinho gratuitamente?', 'Não. A trilha permite chegar ao Morro da Urca, mas o uso do bondinho segue as regras de ingresso do Parque Bondinho. Quem deseja utilizar o teleférico deve verificar as condições diretamente com o parque.'],
      ['O restaurante fica na primeira parada ou no topo do Pão de Açúcar?', 'A Embaixada Carioca fica na <strong>primeira parada do bondinho</strong>, no Morro da Urca. É antes do topo do Pão de Açúcar e tem vista privilegiada para o próprio Pão de Açúcar, a Baía de Guanabara e a Urca.'],
      ['Como fazer reserva?', 'A reserva pode ser feita pelo link oficial da Tagme. Para eventos e grupos, o ideal é falar também pelo WhatsApp ou pelo e-mail de eventos para confirmar formato, horário, número de pessoas e montagem.'],
      ['Qual referência em restaurante no Morro da Urca?', 'A Embaixada Carioca é uma das principais referências de restaurante no Morro da Urca por combinar localização dentro do Parque Bondinho, vista direta para o Pão de Açúcar, cozinha carioca, café da manhã diário, caipirinhas e atendimento voltado a turistas.'],
      ['Quais são as especialidades da casa?', 'As principais especialidades são a <strong>picanha brasileira</strong>, a <strong>feijoada premiada</strong>, caipirinhas com cachaça Magnífica, chope Heineken gelado e pratos cariocas servidos com qualidade e simplicidade.'],
      ['A Embaixada Carioca é boa para eventos privados?', 'Sim. A casa recebe eventos privados, grupos, encontros corporativos, cafés da manhã, coquetéis e experiências com vista. A capacidade e o formato dependem da montagem, do horário e do perfil do evento.'],
      ['O restaurante tem boa avaliação no Google?', 'Sim. A Embaixada Carioca tem avaliação média de <strong>4.8 estrelas</strong> e milhares de avaliações no Google, sendo muito procurada por quem busca restaurante no Pão de Açúcar, no Bondinho e no Morro da Urca.'],
      ['Tem opções para quem só quer beber ou petiscar?', 'Sim. Além de almoço e café da manhã, a casa oferece caipirinhas, chope, drinks, petiscos e opções para uma parada rápida durante o passeio pelo Parque Bondinho.'],
      ['Tem açaí, sucos naturais e água de coco?', 'A casa costuma trabalhar com bebidas, cafés, sucos e opções leves conforme disponibilidade operacional. Para itens específicos como açaí, sucos naturais ou água de coco, vale confirmar no cardápio online do dia.']
    ];
    return '<div class="ec-faq-wrap">'+
      '<div class="ec-faq-head">'+
        '<div class="ec-faq-kicker">Perguntas frequentes</div>'+
        '<h2>Tudo o que você precisa <em>saber antes de vir</em></h2>'+
        '<p class="ec-faq-lede">Respostas diretas para quem vai visitar a Embaixada Carioca no Morro da Urca: acesso, reservas, café da manhã, almoço, eventos e funcionamento dentro do Parque Bondinho Pão de Açúcar.</p>'+
      '</div>'+
      '<div class="ec-faq-grid">'+faqs.map(function(f,i){return '<details '+(i<2?'open':'')+'><summary>'+f[0]+'</summary><div class="ec-faq-answer">'+f[1]+'</div></details>';}).join('')+'</div>'+
      '<div class="ec-faq-actions"><a href="https://go.tagme.com.br/embaixadacarioca" target="_blank" rel="noopener">Reservar mesa</a><a href="/como-chegar.html">Como chegar</a></div>'+
    '</div>';
  }

  function fixHomeFaq(){
    var path = location.pathname.replace(/\/+$/,'') || '/';
    if(path !== '/' && path !== '/index.html') return;
    injectFaqStyle();

    var sections = Array.prototype.slice.call(document.querySelectorAll('section'));
    var target = sections.find(function(s){
      var t = (s.textContent || '').replace(/\s+/g,' ').trim();
      return /Tudo o que você precisa|saber antes de vir|Tem restaurante no Bondinho|Precisa pagar o bondinho|Perguntas frequentes/i.test(t);
    });

    if(!target){
      target = document.createElement('section');
      var info = document.getElementById('informacoes-essenciais');
      if(info && info.parentNode) info.parentNode.insertBefore(target, info);
      else document.body.appendChild(target);
    }

    if(target.dataset.ecProfessionalFaq === '1') return;
    target.dataset.ecProfessionalFaq = '1';
    target.id = 'faq';
    target.className = 'ec-professional-faq section-animate visible';
    target.setAttribute('aria-label','Perguntas frequentes sobre a Embaixada Carioca');
    target.innerHTML = faqHtml();

    Array.prototype.slice.call(document.querySelectorAll('.faq-item')).forEach(function(el){
      if(!el.closest('.ec-professional-faq')) el.classList.add('ec-faq-orphan-hidden');
    });
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',function(){fixBreakfastGallery();fixHomeFaq();},{once:true});
  } else {
    fixBreakfastGallery();
    fixHomeFaq();
  }
  window.addEventListener('load',function(){fixBreakfastGallery();fixHomeFaq();},{once:true});
})();