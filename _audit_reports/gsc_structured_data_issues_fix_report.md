# GSC Structured Data Issues Fix

Status geral: **PASS**

## Exportações tratadas
- FAQ: O campo FAQPage está duplicado
- Events: offers / performer ausentes
- Discussion forum: DiscussionForumPosting inválido
- Videos: uploadDate inválido ou sem fuso horário
- Unparsable structured data: Propriedade única duplicada

## Resumo
- Arquivos HTML escaneados: 87
- Arquivos alterados: 10
- Duplicate keys normalizadas: 0
- FAQPage duplicados removidos: 10
- DiscussionForumPosting/Comment removidos: 0
- VideoObject uploadDate corrigidos: 0
- Event fields corrigidos: 0
- JSON-LD parse errors remanescentes: 0

## Arquivos alterados
- `cafe-da-manha.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `en/almoco.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `en/cardapio.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `en/index.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `es/almoco.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `es/cardapio.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `es/index.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `eventos.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `feijoada.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
- `index.html` — duplicate_keys=0, faq_removed=1, forum_removed=0, video_dates_fixed=0, events_fixed=0
