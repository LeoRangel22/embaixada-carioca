# Final Growth Items Report

Status: **PASS**

## Itens de código/site concluídos
- Aviso: reserva não inclui ingresso do Parque Bondinho.
- Landing page: restaurantes românticos no Rio de Janeiro com vista.
- R2D2 avançado: visitante recorrente, interesse por página e sugestão de idioma.
- Schema MenuItem ampliado: picanha, feijoada, bobó, caipirinha, chope, café da manhã.
- Sitemap atualizado com página romântica: **False**.

## Checklist externo obrigatório
### GA4
- Abrir GA4 DebugView.
- Clicar em Reservar no site publicado.
- Confirmar evento `ec_reservation_click`.
- Marcar `ec_reservation_click` como conversão.
- Criar exploração por página de origem: Home, Café, Almoço, Morro da Urca e Romântico.

### TripAdvisor / GEO externo
- Revisar descrição PT/EN/ES.
- Subir fotos de vista, café da manhã, picanha, caipirinhas e eventos.
- Responder avaliações recentes.
- Garantir categoria correta e link para site oficial.
- Buscar citações em blogs de viagem, hotéis, receptivos e guias anglófonos.

### Performance pós-deploy
- Rodar Lighthouse mobile na Home.
- Validar LCP, CLS, TBT e peso total.
- Confirmar que os scripts defer não atrasaram renderização.
- Consolidar CSS emergencial depois da estabilização visual.
