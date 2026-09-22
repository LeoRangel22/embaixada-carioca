# Lote editorial de CTR — 21/09/2026

## Estado da entrega

Preparado e testado sobre `master`, base `f16e47c6`. Publicação autorizada pelo responsável em 22/09/2026; este relatório acompanha o lote enviado para publicação. A entrega só deve ser considerada publicada após confirmação do deploy e leitura das URLs de produção. Este relatório não confirma melhoria de ranking, CTR ou reservas: esses resultados devem ser medidos após a publicação.

## Escopo

12 páginas, em quatro famílias PT/EN/ES:

| Família | PT | EN | ES |
|---|---|---|---|
| Home | `index.html` | `en/index.html` | `es/index.html` |
| Cardápio | `cardapio.html` | `en/cardapio.html` | `es/cardapio.html` |
| Morro da Urca | `morro-da-urca.html` | `en/morro-da-urca.html` | `es/morro-da-urca.html` |
| Onde comer | `onde-comer-no-pao-de-acucar.html` | `en/where-to-eat-near-sugarloaf.html` | `es/donde-comer-cerca-del-pan-de-azucar.html` |

## Alterações preparadas

- Títulos, descrições e metadados de compartilhamento alinhados à intenção de restaurante, refeições e visita ao Parque Bondinho em dez páginas.
- Títulos e descrições EN/ES de Onde Comer preservados para não interromper o teste editorial iniciado em agosto.
- Aberturas das homes mais diretas, preservando identidade visual, imagem, horários e premiações.
- Link visível para o cardápio online completo, com preços e opções de idioma, nas três páginas de cardápio: `https://livemenu.app/menu/61cb5857aa455a0012ebbdcf`.
- Morro da Urca: abertura orientada a passeio, vista e refeição; remoção da alegação de único restaurante completo do complexo no trecho revisto; links de acesso e almoço no idioma correspondente.
- Onde Comer: seção localizada de planejamento da refeição, esclarecendo localização dentro do parque e diferença entre reserva de mesa e condições de acesso ao atrativo.
- Remoção da comparação PT sem comprovação sobre outros restaurantes e de blocos genéricos repetitivos selecionados nas páginas Onde Comer.
- Seletores de idioma de Morro da Urca e Onde Comer mantêm o visitante no artigo equivalente.
- Substituição do horário fixo de pôr do sol no quadro lateral de Onde Comer por informação estável sobre a primeira parada do Bondinho.
- Correção de contraste restrita ao hero legado de Morro da Urca, em `assets/css/ec-visitor-guide.css`, preservando a foto existente.
- `lastmod` atualizado para 22/09/2026 somente nas 12 URLs alteradas no sitemap.

## Verificação

| Verificação | Resultado |
|---|---|
| Teste existente de experiência das três homes | PASS |
| Teste existente de design de 24 páginas internas | PASS |
| Um H1 e uma meta description por página do lote | PASS — 12 páginas |
| JSON-LD parseável e idêntico ao baseline | PASS — 12 páginas |
| Canonical e hreflang preservados | PASS — 12 páginas |
| Links locais absolutos apontando para arquivos/diretórios existentes | PASS — 12 páginas |
| Link do cardápio online presente em PT/EN/ES | PASS |
| Sitemap XML válido | PASS |
| `git diff --check` com configuração normal do repositório | PASS |
| Prévia local desktop e celular | Conferida; sem rolagem horizontal nos testes do lote |

Os testes locais bloquearam o envio de dados ao Analytics. O ajuste de contraste foi conferido também em uma origem local nova, sem cache anterior. A validação visual foi dirigida aos trechos alterados; não constitui certificação WCAG/AAA nem auditoria integral de todas as seções antigas.

## Limites e próximos passos

1. Publicar o lote autorizado e confirmar o deploy e as 12 URLs ao vivo.
2. Ajustes autorizados no GA4 concluídos em 22/09/2026: `ec_reservation_click` mantido como intenção de reserva; `whatsapp_click` marcado como principal; `click_reservar`, `ec_outbound_conversion_click`, `form_start` e `click_whatsapp` desmarcados como principais. Eventos auxiliares e histórico não foram apagados. As demais metas foram preservadas. A lista final foi conferida no painel. Clique de reserva não é reserva concluída; clique de WhatsApp não é conversa ou venda confirmada.
3. Depois da publicação, verificar o conteúdo ao vivo e registrar a data de início da medição.
4. Comparar janelas equivalentes de 28 dias por página, consulta, idioma e dispositivo. Acompanhar cliques, impressões, CTR e cliques de reserva sem tratá-los como reservas concluídas.
5. Preservar a medição EN/ES de Onde Comer e evitar novas trocas de título sem avaliar o teste em curso.
6. Prosseguir em lote separado com URLs comerciais ainda não indexadas, integração de reservas concluídas e revisão das seções antigas não abordadas aqui.

Não houve alteração em DNS, Cloudflare, workflows, imagens, preços de produtos ou conteúdo de JSON-LD neste lote. Os dados privados de GSC/GA4 usados na priorização permanecem fora deste relatório do repositório.
