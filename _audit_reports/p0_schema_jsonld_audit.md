# P0 Schema JSON-LD Audit

Status geral: **PASS**
Score mínimo: **86**

## Critérios
- Bloco `<script type="application/ld+json">` válido.
- Tipos mínimos: Restaurant, FAQPage, Menu, BreadcrumbList, WebSite e WebPage.
- Proibido usar `aggregateRating`, `ratingValue`, `reviewCount`, `ratingCount`, `bestRating` ou `worstRating` no JSON-LD.
- O rating do Google pode aparecer no texto visível, mas não no schema estruturado.
- Score mínimo: 90.

## Resultados
- `index.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ImageObject, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Organization, PostalAddress, Question, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `en/index.html` — FAIL — score 86 — blocos válidos 1
  - Faltando: BreadcrumbList
  - Encontrado: Answer, FAQPage, GeoCoordinates, OpeningHoursSpecification, PostalAddress, Question, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `es/index.html` — FAIL — score 86 — blocos válidos 1
  - Faltando: BreadcrumbList
  - Encontrado: Answer, FAQPage, GeoCoordinates, OpeningHoursSpecification, PostalAddress, Question, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `almoco.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Neighborhood, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction
- `en/almoco.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Neighborhood, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction
- `es/almoco.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Neighborhood, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction
- `cafe-da-manha.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, Neighborhood, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, TouristAttraction, WebPage
- `en/cafe-da-manha.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, Neighborhood, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, TouristAttraction, WebPage
- `es/cafe-da-manha.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, Neighborhood, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, TouristAttraction, WebPage
- `cardapio.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Neighborhood, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction
- `restaurante-morro-da-urca.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, GeoCoordinates, ItemList, ListItem, LocationFeatureSpecification, Neighborhood, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, TouristAttraction, WebPage, WebSite
- `eventos.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, EventVenue, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Neighborhood, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, TouristAttraction, WebPage, WebSite
- `en/eventos.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: Answer, BreadcrumbList, EventVenue, FAQPage, GeoCoordinates, ImageObject, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, Service, SpeakableSpecification, TouristAttraction, VideoObject, WebPage, WebSite
- `es/eventos.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: Answer, BreadcrumbList, ContactPoint, EventVenue, FAQPage, GeoCoordinates, ImageObject, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, Service, SpeakableSpecification, TouristAttraction, VideoObject, WebPage
- `guia-do-rio.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, Article, BreadcrumbList, City, FAQPage, GeoCoordinates, HowTo, HowToStep, ListItem, LocationFeatureSpecification, MonetaryAmount, Neighborhood, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification
- `restaurantes-romanticos-rio-de-janeiro.html` — PASS — score 100 — blocos válidos 1
  - Encontrado: AdministrativeArea, Answer, BreadcrumbList, City, FAQPage, GeoCoordinates, ListItem, Neighborhood, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, TouristAttraction, WebPage, WebSite
