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
- `index.html` — FAIL — score 86 — blocos válidos 8
  - Faltando: WebPage
  - Encontrado: Answer, BreadcrumbList, ContactPoint, EntryPoint, FAQPage, FoodEstablishment, GeoCoordinates, ImageObject, ListItem, LocalBusiness, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction
- `en/index.html` — FAIL — score 86 — blocos válidos 7
  - Faltando: WebPage
  - Encontrado: Answer, BreadcrumbList, ContactPoint, FAQPage, FoodEstablishment, GeoCoordinates, ListItem, LocalBusiness, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, TouristAttraction
- `es/index.html` — FAIL — score 86 — blocos válidos 7
  - Faltando: WebPage
  - Encontrado: Answer, BreadcrumbList, ContactPoint, FAQPage, FoodEstablishment, GeoCoordinates, ListItem, LocalBusiness, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, TouristAttraction
- `almoco.html` — PASS — score 100 — blocos válidos 5
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, WebPage, WebSite
- `en/almoco.html` — PASS — score 100 — blocos válidos 7
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, WebPage, WebSite
- `es/almoco.html` — PASS — score 100 — blocos válidos 5
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, MenuItem, MenuSection, Menú, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, WebPage, WebSite
- `cafe-da-manha.html` — PASS — score 100 — blocos válidos 8
  - Encontrado: Answer, BreadcrumbList, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, WebPage, WebSite
- `en/cafe-da-manha.html` — PASS — score 100 — blocos válidos 7
  - Encontrado: Answer, BreadcrumbList, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, WebPage, WebSite
- `es/cafe-da-manha.html` — PASS — score 100 — blocos válidos 7
  - Encontrado: Answer, BreadcrumbList, FAQPage, FoodEvent, GeoCoordinates, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Place, PostalAddress, Question, ReserveAction, Restaurant, Schedule, SpeakableSpecification, WebPage, WebSite
- `cardapio.html` — PASS — score 100 — blocos válidos 6
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, LocationFeatureSpecification, Menu, MenuItem, MenuSection, Offer, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, SpeakableSpecification, WebPage, WebSite
- `restaurante-morro-da-urca.html` — FAIL — score 86 — blocos válidos 5
  - Faltando: WebPage
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ItemList, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, PostalAddress, Question, ReserveAction, Restaurant, WebSite
- `eventos.html` — PASS — score 100 — blocos válidos 6
  - Encontrado: Answer, BreadcrumbList, FAQPage, ListItem, LocationFeatureSpecification, PostalAddress, Question, ReserveAction, Restaurant, WebPage, WebSite
- `en/eventos.html` — PASS — score 100 — blocos válidos 11
  - Encontrado: Answer, BreadcrumbList, EventVenue, FAQPage, GeoCoordinates, ImageObject, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, Service, SpeakableSpecification, VideoObject, WebPage, WebSite
- `es/eventos.html` — PASS — score 100 — blocos válidos 11
  - Encontrado: Answer, BreadcrumbList, ContactPoint, EventVenue, FAQPage, GeoCoordinates, ImageObject, ListItem, LocationFeatureSpecification, OpeningHoursSpecification, Organization, PostalAddress, Question, ReserveAction, Restaurant, Service, SpeakableSpecification, TouristAttraction, VideoObject, WebPage
- `guia-do-rio.html` — FAIL — score 86 — blocos válidos 5
  - Faltando: FAQPage
  - Encontrado: Article, BreadcrumbList, GeoCoordinates, HowTo, HowToStep, ListItem, LocationFeatureSpecification, MonetaryAmount, OpeningHoursSpecification, Organization, PostalAddress, ReserveAction, Restaurant, SpeakableSpecification, WebPage, WebSite
- `restaurantes-romanticos-rio-de-janeiro.html` — PASS — score 100 — blocos válidos 5
  - Encontrado: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ListItem, PostalAddress, Question, ReserveAction, Restaurant, WebPage, WebSite
