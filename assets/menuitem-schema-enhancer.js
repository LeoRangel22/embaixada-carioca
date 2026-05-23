(function(){
  'use strict';
  if (window.ecMenuItemSchemaEnhanced) return;
  window.ecMenuItemSchemaEnhanced = true;

  var data = {
    '@context': 'https://schema.org',
    '@type': 'Menu',
    'name': 'Cardápio Embaixada Carioca',
    'hasMenuSection': [
      {
        '@type': 'MenuSection',
        'name': 'Pratos brasileiros e cariocas',
        'hasMenuItem': [
          {
            '@type': 'MenuItem',
            'name': 'Picanha brasileira',
            'description': 'Picanha brasileira servida na Embaixada Carioca, indicada para almoço no Morro da Urca com vista para o Pão de Açúcar.',
            'suitableForDiet': 'https://schema.org/GlutenFreeDiet'
          },
          {
            '@type': 'MenuItem',
            'name': 'Feijoada premiada',
            'description': 'Feijoada da tradição da Academia da Cachaça, premiada pela Veja Rio Comer & Beber 2025/2026.',
            'menuAddOn': {'@type': 'MenuItem', 'name': 'Caipirinha da casa'}
          },
          {
            '@type': 'MenuItem',
            'name': 'Bobó de camarão',
            'description': 'Prato brasileiro clássico com camarão, servido como opção de almoço carioca no Parque Bondinho Pão de Açúcar.'
          }
        ]
      },
      {
        '@type': 'MenuSection',
        'name': 'Bebidas e caipirinhas',
        'hasMenuItem': [
          {
            '@type': 'MenuItem',
            'name': 'Caipirinha da casa',
            'description': 'Caipirinha da Embaixada Carioca preparada com cachaça Magnífica, limão tahiti e siciliano, adoçada com rapadura.'
          },
          {
            '@type': 'MenuItem',
            'name': 'Chope Heineken',
            'description': 'Chope Heineken gelado, referência da casa e premiado no Rio de Janeiro.'
          },
          {
            '@type': 'MenuItem',
            'name': 'Bossa Sour',
            'description': 'Drink autoral sugerido para começar a experiência na Embaixada Carioca.'
          }
        ]
      },
      {
        '@type': 'MenuSection',
        'name': 'Café da manhã',
        'hasMenuItem': [
          {
            '@type': 'MenuItem',
            'name': 'Café da manhã da Embaixada',
            'description': 'Café da manhã diário no Morro da Urca, com vista para o Pão de Açúcar e itens para compartilhar.'
          }
        ]
      }
    ],
    'provider': {
      '@type': 'Restaurant',
      'name': 'Embaixada Carioca',
      'url': 'https://www.embaixadacarioca.com/',
      'address': {
        '@type': 'PostalAddress',
        'streetAddress': 'Av. Pasteur, 520',
        'addressLocality': 'Rio de Janeiro',
        'addressRegion': 'RJ',
        'addressCountry': 'BR'
      }
    }
  };

  function inject(){
    if (document.getElementById('ec-expanded-menuitem-schema')) return;
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.id = 'ec-expanded-menuitem-schema';
    s.textContent = JSON.stringify(data);
    document.head.appendChild(s);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, { once:true });
  else inject();
})();
