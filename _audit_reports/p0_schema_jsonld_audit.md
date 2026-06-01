# P0 Schema JSON-LD Audit

Status geral: **PASS**
Score mínimo: **100**

## Critérios
- Bloco `<script type="application/ld+json">` válido.
- Tipos mínimos: Restaurant, FAQPage, Menu, BreadcrumbList, WebSite e WebPage.
- Proibido usar `aggregateRating`, `ratingValue`, `reviewCount`, `ratingCount`, `bestRating` ou `worstRating` no JSON-LD.
- O rating do Google pode aparecer no texto visível, mas não no schema estruturado.
- Score mínimo: 90.

## Resultados
- `index.html` — PASS — score 100 — blocos válidos 9
  - Encontrado: Answer, BreadcrumbList, ContactPoint, EntryPoint, FAQPage, FoodEstablishment, GeoCoordinates, ImageObject, ListItem, LocalBusiness, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction
- `en/index.html` — PASS — score 100 — blocos válidos 8
  - Encontrado: Answer, BreadcrumbList, ContactPoint, FAQPage, FoodEstablishment, GeoCoordinates, ListItem, LocalBusiness, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification
- `es/index.html` — PASS — score 100 — blocos válidos 8
  - Encontrado: Answer, BreadcrumbList, ContactPoint, FAQPage, FoodEstablishment, GeoCoordinates, ListItem, LocalBusiness, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification
- `almoco.html` — PASS — score 100 — blocos válidos 5
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `en/almoco.html` — PASS — score 100 — blocos válidos 7
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `es/almoco.html` — PASS — score 100 — blocos válidos 5
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, MenuItem, MenuSection, Menú, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `cafe-da-manha.html` — PASS — score 100 — blocos válidos 8
  - Encontrado: Answer, BreadcrumbList, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `en/cafe-da-manha.html` — PASS — score 100 — blocos válidos 7
  - Encontrado: Answer, BreadcrumbList, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `es/cafe-da-manha.html` — PASS — score 100 — blocos válidos 7
  - Encontrado: Answer, BreadcrumbList, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `cardapio.html` — PASS — score 100 — blocos válidos 6
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `restaurante-morro-da-urca.html` — PASS — score 100 — blocos válidos 6
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ItemList, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `eventos.html` — PASS — score 100 — blocos válidos 6
  - Encontrado: Answer, BreadcrumbList, FAQPage, ListItem, LocationFeatureSpecification, PostalAddress, Question, ReserveAction, Restaurant, TouristAttraction, WebPage, WebSite
- `en/eventos.html` — PASS — score 100 — blocos válidos 11
  - Encontrado: Answer, BreadcrumbList, EventVenue, FAQPage, GeoCoordinates, ImageObject, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, Service, SpeakableSpecification, TouristAttraction, VideoObject, WebPage, WebSite
- `es/eventos.html` — PASS — score 100 — blocos válidos 11
  - Encontrado: Answer, BreadcrumbList, ContactPoint, EventVenue, FAQPage, GeoCoordinates, ImageObject, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, Service, SpeakableSpecification, TouristAttraction, VideoObject, WebPage
- `guia-do-rio.html` — PASS — score 100 — blocos válidos 6
  - Encontrado: Answer, Article, BreadcrumbList, FAQPage, GeoCoordinates, HowTo, HowToStep, ListItem, LocationFeatureSpecification, MonetaryAmount, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `restaurantes-romanticos-rio-de-janeiro.html` — PASS — score 100 — blocos válidos 5
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, PostalAddress, Question, ReserveAction, Restaurant, TouristAttraction, WebPage, WebSite
