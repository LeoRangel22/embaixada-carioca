(function(){
  'use strict';
  if (window.ecCtrMetaOverridesLoaded) return;
  window.ecCtrMetaOverridesLoaded = true;

  var path = String(location.pathname || '/').toLowerCase();
  var rules = {
    '/morro-da-urca.html': {
      title: 'Morro da Urca: Onde Comer, O Que Fazer e Como Chegar | Embaixada Carioca',
      description: 'Guia do Morro da Urca: onde comer na 1ª parada do Bondinho, o que fazer, como chegar, vista para o Pão de Açúcar, café da manhã e almoço brasileiro.'
    },
    '/en/morro-da-urca.html': {
      title: 'Urca Hill: Where to Eat, What to Do and How to Get There | Embaixada Carioca',
      description: 'Guide to Urca Hill in Rio: where to eat at the first Sugarloaf Cable Car stop, what to do, how to get there, breakfast, Brazilian lunch and views.'
    },
    '/es/morro-da-urca.html': {
      title: 'Morro da Urca: Dónde Comer, Qué Hacer y Cómo Llegar | Embaixada Carioca',
      description: 'Guía del Morro da Urca: dónde comer en la primera parada del Bondinho, qué hacer, cómo llegar, desayuno, almuerzo brasileño y vista al Pan de Azúcar.'
    },
    '/parque-bondinho.html': {
      title: 'Onde Comer no Parque Bondinho Pão de Açúcar | Morro da Urca',
      description: 'Onde comer no Parque Bondinho Pão de Açúcar: Embaixada Carioca no Morro da Urca, 1ª parada do bondinho, com café da manhã, almoço, caipirinha e vista.'
    },
    '/en/parque-bondinho.html': {
      title: 'Where to Eat at Sugarloaf Cable Car Park | Urca Hill',
      description: 'Where to eat at Sugarloaf Cable Car Park: Embaixada Carioca at Urca Hill, first cable car stop, with breakfast, Brazilian lunch, caipirinhas and views.'
    },
    '/es/parque-bondinho.html': {
      title: 'Dónde Comer en el Parque Bondinho Pan de Azúcar | Morro da Urca',
      description: 'Dónde comer en el Parque Bondinho Pan de Azúcar: Embaixada Carioca en el Morro da Urca, primera parada del teleférico, con desayuno, almuerzo y vista.'
    },
    '/como-chegar.html': {
      title: 'Como Chegar à Embaixada Carioca | Av. Pasteur 520, Urca',
      description: 'Como chegar à Embaixada Carioca: use Av. Pasteur 520, Praia Vermelha, Urca. Restaurante na 1ª parada do Bondinho, no Morro da Urca.'
    },
    '/en/how-to-get-there.html': {
      title: 'How to Get to Embaixada Carioca | Av. Pasteur 520, Urca',
      description: 'How to get to Embaixada Carioca: use Av. Pasteur 520, Praia Vermelha, Urca. Restaurant at the first Sugarloaf Cable Car stop on Urca Hill.'
    },
    '/es/como-llegar.html': {
      title: 'Cómo Llegar a Embaixada Carioca | Av. Pasteur 520, Urca',
      description: 'Cómo llegar a Embaixada Carioca: use Av. Pasteur 520, Praia Vermelha, Urca. Restaurante en la primera parada del Bondinho, Morro da Urca.'
    }
  };

  var data = rules[path];
  if (!data) return;

  function setMeta(selector, attr, value){
    var el = document.querySelector(selector);
    if (!el) return;
    el.setAttribute(attr, value);
  }

  document.title = data.title;
  setMeta('meta[name="description"]', 'content', data.description);
  setMeta('meta[property="og:title"]', 'content', data.title);
  setMeta('meta[property="og:description"]', 'content', data.description);
})();
