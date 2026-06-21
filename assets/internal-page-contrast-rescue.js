(function(){
  'use strict';
  if (window.ecInternalPageContrastRescueLoaded) return;
  window.ecInternalPageContrastRescueLoaded = true;

  function markPage(){
    var path = location.pathname.toLowerCase();
    if (path === '/' || path === '/index.html') document.body.classList.add('ec-page-home', 'ec-lang-pt');
    if (path === '/en/' || path === '/en/index.html') document.body.classList.add('ec-page-home', 'ec-lang-en');
    if (path === '/es/' || path === '/es/index.html') document.body.classList.add('ec-page-home', 'ec-lang-es');
    if (path.indexOf('guia-do-rio') >= 0) document.body.classList.add('ec-page-guia-do-rio');
    if (path.indexOf('eventos') >= 0) document.body.classList.add('ec-page-eventos');
    if (path.indexOf('morro-da-urca') >= 0) document.body.classList.add('ec-page-morro-da-urca');
    if (path.indexOf('parque-bondinho') >= 0) document.body.classList.add('ec-page-parque-bondinho');
  }

  function injectStyle(){
    if (document.getElementById('ec-internal-page-contrast-rescue-style')) return;
    var css = `
      :root{
        --ec-rescue-blue:#00405a;
        --ec-rescue-blue-dark:#002f3f;
        --ec-rescue-cream:#f6efde;
        --ec-rescue-paper:#fffaf0;
        --ec-rescue-gray:#485156;
        --ec-rescue-orange:#f59b1e;
        --ec-rescue-green:#335d4a;
      }

      /* P0 RESPONSIVE SAFETY V2 — carregado via JS global, sem alterar HTML/SEO. */
      @media (max-width: 1100px) {
        html body { overflow-x:hidden!important; }
        html body nav.top .nav-inner,
        html body #topnav.top .nav-inner {
          max-width:100vw!important;
          padding-left:clamp(14px,2.6vw,28px)!important;
          padding-right:clamp(14px,2.6vw,28px)!important;
          gap:10px!important;
        }
        html body nav.top .brand-logo,
        html body #topnav.top .brand-logo {
          width:52px!important;
          height:52px!important;
          min-width:52px!important;
          min-height:52px!important;
          max-width:52px!important;
          max-height:52px!important;
        }
        html body nav.top .nav-rating-badge,
        html body nav.top .lang-switcher,
        html body #topnav.top .nav-rating-badge,
        html body #topnav.top .lang-switcher { display:none!important; }
        html body nav.top .nav-links,
        html body #topnav.top .nav-links {
          gap:10px!important;
          justify-content:flex-end!important;
          min-width:0!important;
        }
        html body nav.top .nav-links a,
        html body #topnav.top .nav-links a {
          font-size:9.5px!important;
          letter-spacing:.055em!important;
          max-width:104px!important;
          overflow:hidden!important;
          text-overflow:ellipsis!important;
          white-space:nowrap!important;
        }
        html body nav.top .btn,
        html body #topnav.top .btn {
          min-width:118px!important;
          max-width:168px!important;
          height:46px!important;
          min-height:46px!important;
          padding:0 14px!important;
          font-size:9.5px!important;
          letter-spacing:.07em!important;
        }
        html body header.hero .hero-content,
        html body header.page-hero .page-hero-content {
          gap:28px!important;
          padding-left:clamp(22px,4vw,44px)!important;
          padding-right:clamp(22px,4vw,44px)!important;
        }
        html body section {
          padding-top:clamp(72px,8vw,112px)!important;
          padding-bottom:clamp(72px,8vw,112px)!important;
        }
        html body .wrap,
        html body .container,
        html body .ec-wrap {
          padding-left:clamp(20px,4vw,44px)!important;
          padding-right:clamp(20px,4vw,44px)!important;
        }
        html body .momentos-grid,
        html body .ratings-row,
        html body .mini-quotes,
        html body .eventos-grid,
        html body .cards-grid,
        html body .ec-cc-grid,
        html body .ec-priority-query-grid {
          grid-template-columns:repeat(2,minmax(0,1fr))!important;
          gap:22px!important;
        }
        html body .sec-head {
          grid-template-columns:minmax(0,1fr)!important;
          gap:24px!important;
          margin-bottom:44px!important;
        }
        html body .sec-head .lede { grid-column:1 / -1!important; }
      }

      @media (min-width:768px) and (max-width:1100px) and (max-height:820px) {
        html body header.hero,
        html body header#conteudo-principal.hero,
        html body header#main-content.hero {
          min-height:620px!important;
          height:auto!important;
        }
        html body header.hero .hero-content,
        html body header#conteudo-principal.hero .hero-content,
        html body header#main-content.hero .hero-content {
          grid-template-columns:minmax(0,1fr)!important;
          align-items:end!important;
          padding-top:92px!important;
          padding-bottom:86px!important;
        }
        html body header.hero .hero-side,
        html body header#conteudo-principal.hero .hero-side,
        html body header#main-content.hero .hero-side,
        html body header.hero .hero-logo,
        html body header#conteudo-principal.hero .hero-logo,
        html body header#main-content.hero .hero-logo { display:none!important; }
        html body header.hero h1,
        html body header.hero h1 * {
          font-size:clamp(34px,5.2vw,52px)!important;
          line-height:1!important;
        }
        html body header.hero .hero-sub {
          max-width:620px!important;
          margin-bottom:24px!important;
          font-size:15.5px!important;
          line-height:1.42!important;
        }
        html body header.hero .hero-bottom-bar {
          min-height:52px!important;
          padding:10px 24px!important;
          gap:14px!important;
          font-size:8.5px!important;
          letter-spacing:.10em!important;
          line-height:1.25!important;
          overflow:hidden!important;
        }
      }

      @media (max-width:900px) {
        html body nav.top .nav-links,
        html body nav.top .lang-switcher,
        html body nav.top .nav-rating-badge,
        html body #topnav.top .nav-links,
        html body #topnav.top .lang-switcher,
        html body #topnav.top .nav-rating-badge { display:none!important; }
        html body header.hero .hero-content {
          display:block!important;
          padding-top:92px!important;
          padding-bottom:96px!important;
        }
        html body header.hero .hero-ctas {
          display:grid!important;
          grid-template-columns:1fr!important;
          gap:10px!important;
          max-width:360px!important;
        }
        html body header.hero .hero-ctas .btn,
        html body header.hero .btn {
          width:100%!important;
          justify-content:center!important;
          min-height:48px!important;
        }
        html body .momentos-grid,
        html body .ratings-row,
        html body .mini-quotes,
        html body .eventos-grid,
        html body .cards-grid,
        html body .ec-cc-grid,
        html body .ec-combos-grid,
        html body .visao-grid,
        html body .feijoada-grid,
        html body .ec-priority-query-grid {
          grid-template-columns:minmax(0,1fr)!important;
        }
        html body section {
          padding-top:72px!important;
          padding-bottom:72px!important;
        }
        html body .mobile-bottom-nav,
        html body nav.mobile-bottom-nav {
          min-height:calc(66px + env(safe-area-inset-bottom,0px))!important;
        }
        html body { padding-bottom:calc(74px + env(safe-area-inset-bottom,0px))!important; }
      }

      @media (max-width:820px) and (max-height:640px) {
        html body header.hero { min-height:560px!important; }
        html body header.hero .hero-content {
          padding-top:78px!important;
          padding-bottom:76px!important;
        }
        html body header.hero h1,
        html body header.hero h1 * { font-size:clamp(30px,7.2vw,42px)!important; }
        html body header.hero .hero-eyebrow,
        html body header.hero .eyebrow { margin-bottom:16px!important; }
        html body header.hero .hero-bottom-bar { display:none!important; }
      }

      /* Base: remove texto fantasma em páginas internas críticas. */
      body.ec-page-guia-do-rio .article-body *,
      body.ec-page-eventos #faq *,
      body.ec-page-eventos .faq *,
      body.ec-page-eventos .capacity *,
      body.ec-page-eventos #capacity *,
      body.ec-page-morro-da-urca main *,
      body.ec-page-parque-bondinho main *{
        opacity:1!important;
        visibility:visible!important;
        filter:none!important;
        mix-blend-mode:normal!important;
        text-shadow:none!important;
        -webkit-text-stroke:0!important;
        -webkit-background-clip:border-box!important;
        background-clip:border-box!important;
      }

      /* GUIA DO RIO — cards claros dentro do artigo: texto sempre escuro. */
      body.ec-page-guia-do-rio .article-body .guia-card,
      body.ec-page-guia-do-rio .article-body .guia-intro-box,
      body.ec-page-guia-do-rio .article-body .guia-roteiro,
      body.ec-page-guia-do-rio .article-body .guia-reservation-links,
      body.ec-page-guia-do-rio .article-body .tip-box,
      body.ec-page-guia-do-rio .article-body .highlight,
      body.ec-page-guia-do-rio .article-body .info-box,
      body.ec-page-guia-do-rio .article-body .card,
      body.ec-page-guia-do-rio .article-body article,
      body.ec-page-guia-do-rio .article-body table,
      body.ec-page-guia-do-rio .article-body tr,
      body.ec-page-guia-do-rio .article-body td,
      body.ec-page-guia-do-rio .article-body th{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card,
      body.ec-page-guia-do-rio .article-body .guia-intro-box,
      body.ec-page-guia-do-rio .article-body .tip-box,
      body.ec-page-guia-do-rio .article-body .highlight,
      body.ec-page-guia-do-rio .article-body .info-box,
      body.ec-page-guia-do-rio .article-body .card{
        background:var(--ec-rescue-paper)!important;
        border-color:rgba(0,64,90,.16)!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card h1,
      body.ec-page-guia-do-rio .article-body .guia-card h2,
      body.ec-page-guia-do-rio .article-body .guia-card h3,
      body.ec-page-guia-do-rio .article-body .guia-card h4,
      body.ec-page-guia-do-rio .article-body .guia-card h5,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h1,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h2,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h3,
      body.ec-page-guia-do-rio .article-body .guia-intro-box h4,
      body.ec-page-guia-do-rio .article-body .tip-box h3,
      body.ec-page-guia-do-rio .article-body .highlight h3,
      body.ec-page-guia-do-rio .article-body .info-box h3,
      body.ec-page-guia-do-rio .article-body .card h3,
      body.ec-page-guia-do-rio .article-body table th,
      body.ec-page-guia-do-rio .article-body table strong{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
        font-weight:800!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card p,
      body.ec-page-guia-do-rio .article-body .guia-card li,
      body.ec-page-guia-do-rio .article-body .guia-card td,
      body.ec-page-guia-do-rio .article-body .guia-card span,
      body.ec-page-guia-do-rio .article-body .guia-intro-box p,
      body.ec-page-guia-do-rio .article-body .guia-intro-box li,
      body.ec-page-guia-do-rio .article-body .tip-box p,
      body.ec-page-guia-do-rio .article-body .highlight p,
      body.ec-page-guia-do-rio .article-body .info-box p,
      body.ec-page-guia-do-rio .article-body .card p,
      body.ec-page-guia-do-rio .article-body table td{
        color:var(--ec-rescue-gray)!important;
        -webkit-text-fill-color:var(--ec-rescue-gray)!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card strong,
      body.ec-page-guia-do-rio .article-body .guia-intro-box strong,
      body.ec-page-guia-do-rio .article-body .tip-box strong,
      body.ec-page-guia-do-rio .article-body .highlight strong,
      body.ec-page-guia-do-rio .article-body .info-box strong,
      body.ec-page-guia-do-rio .article-body .card strong{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
        font-weight:900!important;
      }

      body.ec-page-guia-do-rio .article-body .guia-card a,
      body.ec-page-guia-do-rio .article-body .guia-intro-box a,
      body.ec-page-guia-do-rio .article-body .tip-box a,
      body.ec-page-guia-do-rio .article-body .highlight a,
      body.ec-page-guia-do-rio .article-body .info-box a,
      body.ec-page-guia-do-rio .article-body .card a{
        color:#9a6400!important;
        -webkit-text-fill-color:#9a6400!important;
        font-weight:900!important;
      }

      /* GUIA DO RIO — áreas escuras fora dos cards: texto claro consistente. */
      body.ec-page-guia-do-rio main > section,
      body.ec-page-guia-do-rio .topic-authority,
      body.ec-page-guia-do-rio footer{
        color:var(--ec-rescue-cream)!important;
      }
      body.ec-page-guia-do-rio main > section h1,
      body.ec-page-guia-do-rio main > section h2,
      body.ec-page-guia-do-rio main > section h3,
      body.ec-page-guia-do-rio main > section h4,
      body.ec-page-guia-do-rio .topic-authority h1,
      body.ec-page-guia-do-rio .topic-authority h2,
      body.ec-page-guia-do-rio .topic-authority h3,
      body.ec-page-guia-do-rio footer h1,
      body.ec-page-guia-do-rio footer h2,
      body.ec-page-guia-do-rio footer h3{
        color:var(--ec-rescue-cream)!important;
        -webkit-text-fill-color:var(--ec-rescue-cream)!important;
      }
      body.ec-page-guia-do-rio main > section > .wrap > p,
      body.ec-page-guia-do-rio .topic-authority p,
      body.ec-page-guia-do-rio footer p{
        color:rgba(246,239,222,.92)!important;
        -webkit-text-fill-color:rgba(246,239,222,.92)!important;
      }

      /* EVENTOS — FAQ em fundo claro (cards brancos/bege): texto escuro e legível. */
      body.ec-page-eventos #faq,
      body.ec-page-eventos section#faq,
      body.ec-page-eventos .faq,
      body.ec-page-eventos .faq-grid{
        color:var(--ec-rescue-blue)!important;
      }

      body.ec-page-eventos #faq h1,
      body.ec-page-eventos #faq h2,
      body.ec-page-eventos #faq h3,
      body.ec-page-eventos #faq h4,
      body.ec-page-eventos #faq summary,
      body.ec-page-eventos .faq h1,
      body.ec-page-eventos .faq h2,
      body.ec-page-eventos .faq h3,
      body.ec-page-eventos .faq h4{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
        font-weight:800!important;
      }

      body.ec-page-eventos #faq p,
      body.ec-page-eventos #faq li,
      body.ec-page-eventos #faq td,
      body.ec-page-eventos #faq span,
      body.ec-page-eventos .faq p,
      body.ec-page-eventos .faq li{
        color:var(--ec-rescue-gray)!important;
        -webkit-text-fill-color:var(--ec-rescue-gray)!important;
      }

      body.ec-page-eventos #faq strong,
      body.ec-page-eventos .faq strong{
        color:var(--ec-rescue-green)!important;
        -webkit-text-fill-color:var(--ec-rescue-green)!important;
        font-weight:900!important;
      }

      body.ec-page-eventos #faq a,
      body.ec-page-eventos .faq a{
        color:#9a6400!important;
        -webkit-text-fill-color:#9a6400!important;
        font-weight:900!important;
      }

      /* EVENTOS — Cards .qa (FAQ cards brancos): garantir legibilidade máxima. */
      body.ec-page-eventos .qa,
      body.ec-page-eventos .faq .qa{
        background:#ffffff!important;
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
      }
      body.ec-page-eventos .qa h3,
      body.ec-page-eventos .faq .qa h3{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
        font-weight:800!important;
      }
      body.ec-page-eventos .qa p,
      body.ec-page-eventos .faq .qa p{
        color:var(--ec-rescue-gray)!important;
        -webkit-text-fill-color:var(--ec-rescue-gray)!important;
      }

      /* Cards claros genéricos em páginas internas: sempre texto escuro. */
      body.ec-page-eventos .card-light,
      body.ec-page-eventos .white-card,
      body.ec-page-eventos [class*="light-card"],
      body.ec-page-eventos [style*="background:#fff"],
      body.ec-page-eventos [style*="background: #fff"],
      body.ec-page-eventos [style*="background:#f6efde"],
      body.ec-page-eventos [style*="background: #f6efde"],
      body.ec-page-eventos [style*="background:#fffaf0"],
      body.ec-page-eventos [style*="background: #fffaf0"]{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
      }
      body.ec-page-eventos .card-light h3,
      body.ec-page-eventos .white-card h3,
      body.ec-page-eventos [class*="light-card"] h3,
      body.ec-page-eventos [style*="background:#fff"] h3,
      body.ec-page-eventos [style*="background: #fff"] h3,
      body.ec-page-eventos [style*="background:#f6efde"] h3,
      body.ec-page-eventos [style*="background: #f6efde"] h3,
      body.ec-page-eventos [style*="background:#fffaf0"] h3,
      body.ec-page-eventos [style*="background: #fffaf0"] h3{
        color:var(--ec-rescue-blue)!important;
        -webkit-text-fill-color:var(--ec-rescue-blue)!important;
      }
      body.ec-page-eventos .card-light p,
      body.ec-page-eventos .white-card p,
      body.ec-page-eventos [class*="light-card"] p,
      body.ec-page-eventos [style*="background:#fff"] p,
      body.ec-page-eventos [style*="background: #fff"] p,
      body.ec-page-eventos [style*="background:#f6efde"] p,
      body.ec-page-eventos [style*="background: #f6efde"] p,
      body.ec-page-eventos [style*="background:#fffaf0"] p,
      body.ec-page-eventos [style*="background: #fffaf0"] p{
        color:var(--ec-rescue-gray)!important;
        -webkit-text-fill-color:var(--ec-rescue-gray)!important;
      }
    `;
    var style = document.createElement('style');
    style.id = 'ec-internal-page-contrast-rescue-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function run(){
    markPage();
    injectStyle();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once:true });
  else run();
  window.addEventListener('load', run, { once:true });
})();
