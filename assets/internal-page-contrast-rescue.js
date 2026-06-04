(function(){
  'use strict';
  if (window.ecInternalPageContrastRescueLoaded) return;
  window.ecInternalPageContrastRescueLoaded = true;

  function markPage(){
    var path = location.pathname.toLowerCase();
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
