# Legibilidade, repetição e legendas — 09/09/2026

## Escopo concluído

Como Chegar PT/EN/ES e duas imagens das galerias de Eventos PT/EN/ES.

- Contraste explícito de texto azul sobre fundos claros nas seções antigas de acesso.
- Listas em fluxo normal, sem dividir o endereço em uma coluna estreita; dimensões adaptadas ao celular.
- Seis seções redundantes removidas (dois blocos por idioma). Mantido o passo a passo principal de quatro etapas, transportes, ingresso, endereço, mapa, FAQ e assistência ao visitante.
- Uma lista adicional repetida removida do bloco GPS em PT; endereço e link do mapa mantidos.
- Removida a rotina específica de PT que aplicava estilos inline após o carregamento; folha de estilo comum substitui sua função de contraste.
- Barra de reserva duplicada oculta nas páginas de acesso; navegação inferior continua disponível.
- Duas fotos conferidas visualmente: `evento-chandon-opt.webp` mostra visitante com xícara; `grupo-amigos-opt.webp` mostra visitante com taça. Corrigidas legendas e textos alternativos nos três idiomas, sem afirmar evento, marca de bebida, grupo ou tipo de bebida não comprovado.

## Verificações

- 9 cenários (PT/EN/ES × 390/768/1440): sem overflow horizontal, sem texto fora da tela; títulos, parágrafos e listas visíveis com preenchimento azul; quatro etapas no roteiro e ausência dos dois blocos redundantes.
- Inspeção visual da lista em inglês no celular confirmou endereço em fluxo e leitura clara.
- Teste de preservação de preços, canonical/hreflang e JSON-LD nas 24 páginas internas: PASS.
- Guard de Review/Rating/AggregateRating: PASS, 115 páginas.

## Limites e continuidade

Não é auditoria integral de todas as fotos do site, certificação WCAG nem atualização factual de horários de transporte. Outras páginas antigas e associações foto/prato ainda precisam de revisão individual. Nenhum produto ou preço foi incluído neste lote.
