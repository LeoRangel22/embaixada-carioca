(function(){
  'use strict';
  if (window.ecMenuItemSchemaEnhanced) return;
  window.ecMenuItemSchemaEnhanced = true;

  var restaurantId = 'https://www.embaixadacarioca.com/#restaurant';
  var placeId = 'https://www.embaixadacarioca.com/#parque-bondinho-pao-de-acucar';

  function currentLanguage(){
    var path = String(location.pathname || '').toLowerCase();
    var htmlLang = String(document.documentElement.lang || '').toLowerCase();
    if (path === '/en/' || path.indexOf('/en/') === 0 || htmlLang.indexOf('en') === 0) return 'en';
    if (path === '/es/' || path.indexOf('/es/') === 0 || htmlLang.indexOf('es') === 0) return 'es';
    return 'pt-BR';
  }

  function currentUrl(){
    var origin = location.origin || 'https://www.embaixadacarioca.com';
    var path = location.pathname || '/';
    if (path === '/index.html') path = '/';
    return origin + path;
  }

  function normalizeSchemaType(type){
    if (type === 'EventVenue') return 'Place';
    if (type === 'DiscussionForumPosting') return 'Article';
    if (type === 'Comment') return 'CreativeWork';
    return type;
  }

  function normalizeSchemaTypes(value){
    if (Array.isArray(value)) return value.map(normalizeSchemaType);
    return normalizeSchemaType(value);
  }

  function stripRatingFields(value){
    if (!value || typeof value !== 'object') return value;
    if (Array.isArray(value)) return value.map(stripRatingFields);
    var out = {};
    Object.keys(value).forEach(function(key){
      if (key === 'aggregateRating' || key === 'review' || key === 'reviews') return;
      if (key === '@type') {
        out[key] = normalizeSchemaTypes(value[key]);
        return;
      }
      out[key] = stripRatingFields(value[key]);
    });
    return out;
  }

  function cleanLegacySchemas(){
    document.querySelectorAll('script[type="application/ld+json"]').forEach(function(script){
      if (script.id === 'ec-restaurant-schema' || script.id === 'ec-expanded-menuitem-schema') return;
      var raw = script.textContent || '';
      if (!raw.trim()) return;
      try {
        var cleaned = stripRatingFields(JSON.parse(raw));
        script.textContent = JSON.stringify(cleaned);
      } catch(e) {}
    });
  }

  var restaurantSchema = {
    '@context': 'https://schema.org',
    '@type': 'Restaurant',
    '@id': restaurantId,
    'name': 'Embaixada Carioca Bar & Restaurante',
    'alternateName': ['Embaixada Carioca', 'Restaurante Embaixada Carioca'],
    'url': 'https://www.embaixadacarioca.com/',
    'telephone': '+55 21 96683-7556',
    'email': 'eventos@embaixadacarioca.com.br',
    'image': 'https://www.embaixadacarioca.com/assets/hero.jpg',
    'logo': 'https://www.embaixadacarioca.com/assets/logo.png',
    'priceRange': '$$$',
    'servesCuisine': ['Brazilian', 'Carioca', 'Feijoada', 'Breakfast', 'Bar'],
    'acceptsReservations': true,
    'reservationUrl': 'https://go.tagme.com.br/embaixadacarioca',
    'address': {
      '@type': 'PostalAddress',
      'streetAddress': 'Av. Pasteur, 520 — Parque Bondinho Pão de Açúcar, Morro da Urca',
      'addressLocality': 'Rio de Janeiro',
      'addressRegion': 'RJ',
      'postalCode': '22290-240',
      'addressCountry': 'BR'
    },
    'geo': {
      '@type': 'GeoCoordinates',
      'latitude': -22.9508333,
      'longitude': -43.1641667
    },
    'openingHours': 'Mo-Su 08:30-21:00',
    'openingHoursSpecification': [{
      '@type': 'OpeningHoursSpecification',
      'dayOfWeek': [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
      ],
      'opens': '08:30',
      'closes': '21:00'
    }],
    'containedInPlace': {
      '@type': 'TouristAttraction',
      '@id': placeId,
      'name': 'Parque Bondinho Pão de Açúcar',
      'url': 'https://www.bondinho.com.br/'
    },
    'hasMap': 'https://www.google.com/maps/search/?api=1&query=Embaixada%20Carioca%20Morro%20da%20Urca',
    'sameAs': [
      'https://www.instagram.com/embaixadacarioca/'
    ],
    'inLanguage': currentLanguage(),
    'mainEntityOfPage': currentUrl()
  };

  var menuSchema = {
    '@context': 'https://schema.org',
    '@type': 'Menu',
    '@id': 'https://www.embaixadacarioca.com/#menu',
    'name': 'Cardápio Embaixada Carioca',
    'url': 'https://www.embaixadacarioca.com/cardapio.html',
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
    'provider': {'@id': restaurantId}
  };

  function injectSchema(id, data){
    if (document.getElementById(id)) return;
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.id = id;
    s.textContent = JSON.stringify(data);
    document.head.appendChild(s);
  }

  function inject(){
    cleanLegacySchemas();
    injectSchema('ec-restaurant-schema', restaurantSchema);
    injectSchema('ec-expanded-menuitem-schema', menuSchema);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, { once:true });
  else inject();
})();
