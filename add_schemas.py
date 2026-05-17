#!/usr/bin/env python3
"""
add_schemas.py
Implementa:
  - TouristAttraction em parque-bondinho.html (PT, EN, ES)
  - FoodEvent em cafe-da-manha.html e entardecer.html (PT, EN, ES)
"""
import json
import re

# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS POR IDIOMA
# ─────────────────────────────────────────────────────────────────────────────

# ── TouristAttraction: Parque Bondinho Pão de Açúcar ──────────────────────────
TOURIST_PT = {
    "@context": "https://schema.org",
    "@type": "TouristAttraction",
    "@id": "https://www.embaixadacarioca.com/parque-bondinho#tourist-attraction",
    "name": "Parque Bondinho Pão de Açúcar",
    "alternateName": ["Bondinho do Pão de Açúcar", "Teleférico do Pão de Açúcar", "Sugarloaf Cable Car"],
    "description": "O Parque Bondinho Pão de Açúcar é um dos pontos turísticos mais famosos do mundo, com teleférico que conecta o Morro da Urca (227 m) ao Pão de Açúcar (396 m). Dentro do parque, a Embaixada Carioca é o único restaurante completo do Morro da Urca, com reservas disponíveis, café da manhã diário e feijoada premiada.",
    "url": "https://www.embaixadacarioca.com/parque-bondinho",
    "sameAs": [
        "https://bondinho.com.br",
        "https://www.wikidata.org/wiki/Q739558",
        "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"
    ],
    "image": [
        "https://www.embaixadacarioca.com/img/parque-bondinho-pao-de-acucar.webp",
        "https://www.embaixadacarioca.com/img/morro-da-urca-vista.webp"
    ],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Avenida Pasteur, 520",
        "addressLocality": "Urca",
        "addressRegion": "Rio de Janeiro",
        "postalCode": "22290-240",
        "addressCountry": "BR"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": -22.9494,
        "longitude": -43.1546
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"],
            "opens": "08:30",
            "closes": "20:00"
        },
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Friday","Saturday","Sunday"],
            "opens": "08:30",
            "closes": "21:00"
        }
    ],
    "touristType": ["Turistas internacionais", "Famílias", "Casais", "Aventureiros"],
    "isAccessibleForFree": False,
    "publicAccess": True,
    "amenityFeature": [
        {"@type": "LocationFeatureSpecification", "name": "Teleférico / Bondinho", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Restaurante com Vista Panorâmica", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Trilhas na Natureza", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Área de Eventos", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Reservas Online", "value": True}
    ],
    "hasMap": "https://maps.google.com/?q=Parque+Bondinho+Pão+de+Açúcar",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": 7779,
        "bestRating": "5",
        "worstRating": "1"
    },
    "containsPlace": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "description": "O único restaurante completo do Morro da Urca, dentro do Parque Bondinho Pão de Açúcar. Café da manhã, almoço e entardecer todos os dias, com reservas disponíveis.",
        "url": "https://www.embaixadacarioca.com",
        "servesCuisine": ["Gastronomia Brasileira", "Frutos do Mar", "Churrasco"],
        "priceRange": "$$",
        "reservationUrl": "https://go.tagme.com.br/embaixadacarioca",
        "acceptsReservations": True
    },
    "isPartOf": {
        "@type": "TouristDestination",
        "name": "Rio de Janeiro",
        "url": "https://www.embaixadacarioca.com/guia-do-rio"
    }
}

TOURIST_EN = {
    "@context": "https://schema.org",
    "@type": "TouristAttraction",
    "@id": "https://www.embaixadacarioca.com/en/parque-bondinho#tourist-attraction",
    "name": "Sugarloaf Mountain Cable Car — Parque Bondinho",
    "alternateName": ["Sugarloaf Cable Car", "Pão de Açúcar Cable Car", "Bondinho do Pão de Açúcar"],
    "description": "Sugarloaf Mountain Cable Car (Parque Bondinho) is one of the world's most iconic tourist attractions, connecting Urca Hill (227 m) to Sugarloaf Mountain (396 m). Inside the park, Embaixada Carioca is the only full-service restaurant on Urca Hill, offering breakfast, lunch and sunset experiences with reservations available.",
    "url": "https://www.embaixadacarioca.com/en/parque-bondinho",
    "sameAs": [
        "https://bondinho.com.br",
        "https://en.wikipedia.org/wiki/Sugarloaf_Mountain"
    ],
    "image": [
        "https://www.embaixadacarioca.com/img/parque-bondinho-pao-de-acucar.webp",
        "https://www.embaixadacarioca.com/img/morro-da-urca-vista.webp"
    ],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Avenida Pasteur, 520",
        "addressLocality": "Urca",
        "addressRegion": "Rio de Janeiro",
        "postalCode": "22290-240",
        "addressCountry": "BR"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": -22.9494,
        "longitude": -43.1546
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"],
            "opens": "08:30",
            "closes": "20:00"
        },
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Friday","Saturday","Sunday"],
            "opens": "08:30",
            "closes": "21:00"
        }
    ],
    "touristType": ["International Tourists", "Families", "Couples", "Adventure Seekers"],
    "isAccessibleForFree": False,
    "publicAccess": True,
    "amenityFeature": [
        {"@type": "LocationFeatureSpecification", "name": "Cable Car", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Panoramic Restaurant", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Nature Trails", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Event Space", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Online Reservations", "value": True}
    ],
    "hasMap": "https://maps.google.com/?q=Sugarloaf+Mountain+Rio+de+Janeiro",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": 7779,
        "bestRating": "5",
        "worstRating": "1"
    },
    "containsPlace": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "description": "The only full-service restaurant on Urca Hill, inside Parque Bondinho Pão de Açúcar. Breakfast, lunch and sunset experiences available daily, with reservations.",
        "url": "https://www.embaixadacarioca.com/en",
        "servesCuisine": ["Brazilian Cuisine", "Seafood", "Churrasco"],
        "priceRange": "$$",
        "reservationUrl": "https://go.tagme.com.br/embaixadacarioca",
        "acceptsReservations": True
    },
    "isPartOf": {
        "@type": "TouristDestination",
        "name": "Rio de Janeiro",
        "url": "https://www.embaixadacarioca.com/en/guia-do-rio"
    }
}

TOURIST_ES = {
    "@context": "https://schema.org",
    "@type": "TouristAttraction",
    "@id": "https://www.embaixadacarioca.com/es/parque-bondinho#tourist-attraction",
    "name": "Pan de Azúcar Teleférico — Parque Bondinho",
    "alternateName": ["Teleférico Pan de Azúcar", "Bondinho Pão de Açúcar", "Sugarloaf Cable Car"],
    "description": "El Parque Bondinho Pão de Açúcar es uno de los puntos turísticos más famosos del mundo, con teleférico que conecta el Morro da Urca (227 m) con el Pan de Azúcar (396 m). Dentro del parque, Embaixada Carioca es el único restaurante completo del Morro da Urca, con reservas disponibles, desayuno diario y feijoada premiada.",
    "url": "https://www.embaixadacarioca.com/es/parque-bondinho",
    "sameAs": [
        "https://bondinho.com.br",
        "https://es.wikipedia.org/wiki/Pan_de_Az%C3%BAcar_(Brasil)"
    ],
    "image": [
        "https://www.embaixadacarioca.com/img/parque-bondinho-pao-de-acucar.webp"
    ],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Avenida Pasteur, 520",
        "addressLocality": "Urca",
        "addressRegion": "Rio de Janeiro",
        "postalCode": "22290-240",
        "addressCountry": "BR"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": -22.9494,
        "longitude": -43.1546
    },
    "touristType": ["Turistas internacionales", "Familias", "Parejas"],
    "isAccessibleForFree": False,
    "publicAccess": True,
    "amenityFeature": [
        {"@type": "LocationFeatureSpecification", "name": "Teleférico", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Restaurante Panorámico", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Senderos Naturales", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Reservas Online", "value": True}
    ],
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.8",
        "reviewCount": 7779,
        "bestRating": "5",
        "worstRating": "1"
    },
    "containsPlace": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "description": "El único restaurante completo del Morro da Urca, dentro del Parque Bondinho. Desayuno, almuerzo y atardecer todos los días, con reservas disponibles.",
        "url": "https://www.embaixadacarioca.com/es",
        "servesCuisine": ["Gastronomía Brasileña", "Mariscos", "Churrasco"],
        "priceRange": "$$",
        "reservationUrl": "https://go.tagme.com.br/embaixadacarioca",
        "acceptsReservations": True
    }
}

# ── FoodEvent: Café da Manhã ──────────────────────────────────────────────────
CAFE_EVENT_PT = {
    "@context": "https://schema.org",
    "@type": "FoodEvent",
    "@id": "https://www.embaixadacarioca.com/cafe-da-manha#food-event",
    "name": "Café da Manhã com Vista para o Pão de Açúcar — Embaixada Carioca",
    "description": "O único café da manhã com vista panorâmica para o Pão de Açúcar e a Baía de Guanabara, servido todos os dias no Morro da Urca. Frutas tropicais, tapioca, pão de queijo, ovos mexidos e o melhor café do Rio, a 227 metros de altitude dentro do Parque Bondinho.",
    "url": "https://www.embaixadacarioca.com/cafe-da-manha",
    "image": "https://www.embaixadacarioca.com/img/cafe-da-manha-vista-pao-de-acucar.webp",
    "startDate": "2026-01-01T08:30:00-03:00",
    "endDate": "2026-12-31T11:30:00-03:00",
    "eventSchedule": {
        "@type": "Schedule",
        "repeatFrequency": "P1D",
        "startTime": "08:30",
        "endTime": "11:30",
        "byDay": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    },
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "Embaixada Carioca — Morro da Urca",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Avenida Pasteur, 520 — Morro da Urca",
            "addressLocality": "Urca",
            "addressRegion": "Rio de Janeiro",
            "postalCode": "22290-240",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.9494,
            "longitude": -43.1546
        }
    },
    "organizer": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "url": "https://www.embaixadacarioca.com",
        "telephone": "+55-21-99999-0000",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": 7779,
            "bestRating": "5"
        }
    },
    "offers": {
        "@type": "Offer",
        "url": "https://go.tagme.com.br/embaixadacarioca",
        "availability": "https://schema.org/InStock",
        "validFrom": "2026-01-01",
        "priceCurrency": "BRL",
        "description": "Reserva de mesa para o café da manhã com vista panorâmica"
    },
    "typicalAgeRange": "0-99",
    "inLanguage": "pt-BR",
    "keywords": "café da manhã Pão de Açúcar, café da manhã Morro da Urca, café da manhã com vista Rio de Janeiro, breakfast Sugarloaf Mountain"
}

CAFE_EVENT_EN = {
    "@context": "https://schema.org",
    "@type": "FoodEvent",
    "@id": "https://www.embaixadacarioca.com/en/cafe-da-manha#food-event",
    "name": "Breakfast with Sugarloaf Mountain View — Embaixada Carioca",
    "description": "The only daily breakfast with a panoramic view of Sugarloaf Mountain and Guanabara Bay, served every day on Urca Hill at 227 meters altitude inside Parque Bondinho. Tropical fruits, tapioca, cheese bread, scrambled eggs and the best coffee in Rio.",
    "url": "https://www.embaixadacarioca.com/en/cafe-da-manha",
    "image": "https://www.embaixadacarioca.com/img/cafe-da-manha-vista-pao-de-acucar.webp",
    "startDate": "2026-01-01T08:30:00-03:00",
    "endDate": "2026-12-31T11:30:00-03:00",
    "eventSchedule": {
        "@type": "Schedule",
        "repeatFrequency": "P1D",
        "startTime": "08:30",
        "endTime": "11:30",
        "byDay": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    },
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "Embaixada Carioca — Urca Hill (Morro da Urca)",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Avenida Pasteur, 520 — Urca Hill",
            "addressLocality": "Urca",
            "addressRegion": "Rio de Janeiro",
            "postalCode": "22290-240",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.9494,
            "longitude": -43.1546
        }
    },
    "organizer": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "url": "https://www.embaixadacarioca.com/en",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": 7779,
            "bestRating": "5"
        }
    },
    "offers": {
        "@type": "Offer",
        "url": "https://go.tagme.com.br/embaixadacarioca",
        "availability": "https://schema.org/InStock",
        "priceCurrency": "BRL",
        "description": "Table reservation for breakfast with panoramic view"
    },
    "inLanguage": "en",
    "keywords": "breakfast Sugarloaf Mountain, breakfast Urca Hill, breakfast with view Rio de Janeiro, cafe da manha Pao de Acucar"
}

CAFE_EVENT_ES = {
    "@context": "https://schema.org",
    "@type": "FoodEvent",
    "@id": "https://www.embaixadacarioca.com/es/cafe-da-manha#food-event",
    "name": "Desayuno con Vista al Pan de Azúcar — Embaixada Carioca",
    "description": "El único desayuno diario con vista panorámica al Pan de Azúcar y la Bahía de Guanabara, servido todos los días en el Morro da Urca a 227 metros de altitud dentro del Parque Bondinho. Frutas tropicales, tapioca, pan de queso, huevos revueltos y el mejor café de Río.",
    "url": "https://www.embaixadacarioca.com/es/cafe-da-manha",
    "image": "https://www.embaixadacarioca.com/img/cafe-da-manha-vista-pao-de-acucar.webp",
    "startDate": "2026-01-01T08:30:00-03:00",
    "endDate": "2026-12-31T11:30:00-03:00",
    "eventSchedule": {
        "@type": "Schedule",
        "repeatFrequency": "P1D",
        "startTime": "08:30",
        "endTime": "11:30",
        "byDay": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    },
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "Embaixada Carioca — Morro da Urca",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Avenida Pasteur, 520 — Morro da Urca",
            "addressLocality": "Urca",
            "addressRegion": "Rio de Janeiro",
            "postalCode": "22290-240",
            "addressCountry": "BR"
        }
    },
    "organizer": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "url": "https://www.embaixadacarioca.com/es"
    },
    "offers": {
        "@type": "Offer",
        "url": "https://go.tagme.com.br/embaixadacarioca",
        "availability": "https://schema.org/InStock",
        "priceCurrency": "BRL",
        "description": "Reserva de mesa para el desayuno con vista panorámica"
    },
    "inLanguage": "es",
    "keywords": "desayuno Pan de Azúcar, desayuno Morro da Urca, desayuno con vista Río de Janeiro"
}

# ── FoodEvent: Entardecer / Sunset ────────────────────────────────────────────
SUNSET_EVENT_PT = {
    "@context": "https://schema.org",
    "@type": "FoodEvent",
    "@id": "https://www.embaixadacarioca.com/entardecer#food-event",
    "name": "Entardecer no Morro da Urca — Drinks e Pôr do Sol com Vista para o Pão de Açúcar",
    "description": "O entardecer mais bonito do Rio de Janeiro, com caipirinhas de cachaça Magnífica premiada, Chopp Heineken (eleito o melhor da cidade) e petiscos autorais enquanto o sol se põe sobre o Pão de Açúcar. Todos os dias, a partir das 16h, no Morro da Urca dentro do Parque Bondinho.",
    "url": "https://www.embaixadacarioca.com/entardecer",
    "image": "https://www.embaixadacarioca.com/img/entardecer-por-do-sol-pao-de-acucar.webp",
    "startDate": "2026-01-01T16:00:00-03:00",
    "endDate": "2026-12-31T21:00:00-03:00",
    "eventSchedule": {
        "@type": "Schedule",
        "repeatFrequency": "P1D",
        "startTime": "16:00",
        "endTime": "21:00",
        "byDay": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    },
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "Embaixada Carioca — Morro da Urca",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Avenida Pasteur, 520 — Morro da Urca",
            "addressLocality": "Urca",
            "addressRegion": "Rio de Janeiro",
            "postalCode": "22290-240",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.9494,
            "longitude": -43.1546
        }
    },
    "organizer": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "url": "https://www.embaixadacarioca.com",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": 7779,
            "bestRating": "5"
        }
    },
    "offers": {
        "@type": "Offer",
        "url": "https://go.tagme.com.br/embaixadacarioca",
        "availability": "https://schema.org/InStock",
        "priceCurrency": "BRL",
        "description": "Reserva de mesa para o entardecer com vista panorâmica"
    },
    "performer": {
        "@type": "MusicGroup",
        "name": "DJ Tommax",
        "description": "DJ residente nos eventos de sunset da Embaixada Carioca"
    },
    "inLanguage": "pt-BR",
    "keywords": "entardecer Pão de Açúcar, pôr do sol Morro da Urca, sunset Rio de Janeiro, happy hour Pão de Açúcar, caipirinha Morro da Urca"
}

SUNSET_EVENT_EN = {
    "@context": "https://schema.org",
    "@type": "FoodEvent",
    "@id": "https://www.embaixadacarioca.com/en/entardecer#food-event",
    "name": "Sunset at Urca Hill — Drinks with Sugarloaf Mountain View",
    "description": "The most beautiful sunset in Rio de Janeiro, with award-winning caipirinhas, Heineken draft beer (voted best in the city) and gourmet snacks as the sun sets over Sugarloaf Mountain. Every day from 4 PM on Urca Hill inside Parque Bondinho.",
    "url": "https://www.embaixadacarioca.com/en/entardecer",
    "image": "https://www.embaixadacarioca.com/img/entardecer-por-do-sol-pao-de-acucar.webp",
    "startDate": "2026-01-01T16:00:00-03:00",
    "endDate": "2026-12-31T21:00:00-03:00",
    "eventSchedule": {
        "@type": "Schedule",
        "repeatFrequency": "P1D",
        "startTime": "16:00",
        "endTime": "21:00",
        "byDay": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    },
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "Embaixada Carioca — Urca Hill (Morro da Urca)",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Avenida Pasteur, 520 — Urca Hill",
            "addressLocality": "Urca",
            "addressRegion": "Rio de Janeiro",
            "postalCode": "22290-240",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.9494,
            "longitude": -43.1546
        }
    },
    "organizer": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "url": "https://www.embaixadacarioca.com/en",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": 7779,
            "bestRating": "5"
        }
    },
    "offers": {
        "@type": "Offer",
        "url": "https://go.tagme.com.br/embaixadacarioca",
        "availability": "https://schema.org/InStock",
        "priceCurrency": "BRL",
        "description": "Table reservation for sunset experience with panoramic view"
    },
    "inLanguage": "en",
    "keywords": "sunset Sugarloaf Mountain, sunset Urca Hill, happy hour Rio de Janeiro, caipirinha Sugarloaf, sunset drinks Rio"
}

SUNSET_EVENT_ES = {
    "@context": "https://schema.org",
    "@type": "FoodEvent",
    "@id": "https://www.embaixadacarioca.com/es/entardecer#food-event",
    "name": "Atardecer en el Morro da Urca — Drinks con Vista al Pan de Azúcar",
    "description": "El atardecer más hermoso de Río de Janeiro, con caipirinhas de cachaça premiada, chopp Heineken (elegido el mejor de la ciudad) y tapas mientras el sol se pone sobre el Pan de Azúcar. Todos los días desde las 16h en el Morro da Urca dentro del Parque Bondinho.",
    "url": "https://www.embaixadacarioca.com/es/entardecer",
    "image": "https://www.embaixadacarioca.com/img/entardecer-por-do-sol-pao-de-acucar.webp",
    "startDate": "2026-01-01T16:00:00-03:00",
    "endDate": "2026-12-31T21:00:00-03:00",
    "eventSchedule": {
        "@type": "Schedule",
        "repeatFrequency": "P1D",
        "startTime": "16:00",
        "endTime": "21:00",
        "byDay": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    },
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {
        "@type": "Place",
        "name": "Embaixada Carioca — Morro da Urca",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Avenida Pasteur, 520 — Morro da Urca",
            "addressLocality": "Urca",
            "addressRegion": "Rio de Janeiro",
            "postalCode": "22290-240",
            "addressCountry": "BR"
        }
    },
    "organizer": {
        "@type": "Restaurant",
        "@id": "https://www.embaixadacarioca.com/#restaurant",
        "name": "Embaixada Carioca",
        "url": "https://www.embaixadacarioca.com/es"
    },
    "offers": {
        "@type": "Offer",
        "url": "https://go.tagme.com.br/embaixadacarioca",
        "availability": "https://schema.org/InStock",
        "priceCurrency": "BRL",
        "description": "Reserva de mesa para el atardecer con vista panorámica"
    },
    "inLanguage": "es",
    "keywords": "atardecer Pan de Azúcar, puesta de sol Morro da Urca, happy hour Río de Janeiro, caipirinha Pan de Azúcar"
}

# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÃO DE INSERÇÃO
# ─────────────────────────────────────────────────────────────────────────────

def inject_schema(filepath, schema_obj, schema_id_marker):
    """Injeta um schema JSON-LD antes de </head>, evitando duplicatas."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar se já existe
    if schema_id_marker in content:
        print(f"  ⚠️  {filepath} — schema já existe ({schema_id_marker}), pulando")
        return False

    schema_json = json.dumps(schema_obj, indent=2, ensure_ascii=False)
    schema_block = f'\n<script type="application/ld+json">\n{schema_json}\n</script>\n'

    if '</head>' not in content:
        print(f"  ❌ {filepath} — </head> não encontrado")
        return False

    new_content = content.replace('</head>', schema_block + '</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


# ─────────────────────────────────────────────────────────────────────────────
# EXECUÇÃO
# ─────────────────────────────────────────────────────────────────────────────

tasks = [
    # (filepath, schema_obj, id_marker)
    # TouristAttraction
    ('parque-bondinho.html',    TOURIST_PT, '#tourist-attraction'),
    ('en/parque-bondinho.html', TOURIST_EN, '#tourist-attraction'),
    ('es/parque-bondinho.html', TOURIST_ES, '#tourist-attraction'),
    # FoodEvent: Café da Manhã
    ('cafe-da-manha.html',    CAFE_EVENT_PT, 'cafe-da-manha#food-event'),
    ('en/cafe-da-manha.html', CAFE_EVENT_EN, 'cafe-da-manha#food-event'),
    ('es/cafe-da-manha.html', CAFE_EVENT_ES, 'cafe-da-manha#food-event'),
    # FoodEvent: Entardecer
    ('entardecer.html',    SUNSET_EVENT_PT, 'entardecer#food-event'),
    ('en/entardecer.html', SUNSET_EVENT_EN, 'entardecer#food-event'),
    ('es/entardecer.html', SUNSET_EVENT_ES, 'entardecer#food-event'),
]

ok = 0
skip = 0
err = 0

for filepath, schema_obj, marker in tasks:
    try:
        result = inject_schema(filepath, schema_obj, marker)
        if result:
            print(f"  ✅ {filepath}")
            ok += 1
        else:
            skip += 1
    except Exception as e:
        print(f"  ❌ {filepath}: {e}")
        err += 1

print(f"\nResultado: {ok} inseridos | {skip} já existiam | {err} erros")
