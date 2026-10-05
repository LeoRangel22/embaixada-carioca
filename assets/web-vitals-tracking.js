(function(){
  'use strict';
  if (window.ecWebVitalsLoaded || !('PerformanceObserver' in window)) return;
  window.ecWebVitalsLoaded = true;
  var values = { lcp: 0, cls: 0, inp: 0 };
  function observe(type, callback){
    try {
      var observer = new PerformanceObserver(function(list){ list.getEntries().forEach(callback); });
      observer.observe({type:type, buffered:true});
    } catch (error) {}
  }
  observe('largest-contentful-paint', function(entry){ values.lcp = Math.round(entry.startTime); });
  observe('layout-shift', function(entry){ if (!entry.hadRecentInput) values.cls += entry.value; });
  observe('event', function(entry){ if (entry.duration > values.inp) values.inp = Math.round(entry.duration); });
  function send(){
    if (window.ecWebVitalsSent) return;
    window.ecWebVitalsSent = true;
    var metrics = [
      ['LCP', values.lcp, 2500],
      ['CLS', Math.round(values.cls * 1000), 100],
      ['INP', values.inp, 200]
    ];
    metrics.forEach(function(metric){
      if (!metric[1] || typeof window.gtag !== 'function') return;
      window.gtag('event', 'web_vital', {
        metric_name: metric[0],
        metric_value: metric[1],
        metric_rating: metric[1] <= metric[2] ? 'good' : 'needs_improvement',
        page_path: location.pathname,
        non_interaction: true
      });
    });
  }
  addEventListener('pagehide', send, {once:true});
  addEventListener('visibilitychange', function(){ if (document.visibilityState === 'hidden') send(); });
})();
