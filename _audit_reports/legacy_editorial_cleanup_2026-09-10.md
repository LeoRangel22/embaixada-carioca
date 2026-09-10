# Legibilidade, repetição e fotos — lote de 10/09/2026

## Escopo

Café da Manhã, Cardápio e Guia do Rio, nas versões PT/EN/ES (9 páginas).
Este relatório descreve um lote delimitado, não uma certificação de todo o site.

## Correções

- Seções antigas tinham texto claro sobre fundo creme no navegador. Aplicada uma camada de leitura restrita às seções selecionadas: texto azul-escuro, espaçamento e listas com numeração normal, sem fragmentar frases em colunas.
- Corrigida também a legibilidade da seção `cardapio-completo` em português.
- Removidos 4 blocos redundantes de Café da Manhã PT. Esses blocos repetiam localização, produtos e horários e incluíam afirmações conflitantes sobre a vista, exclusividade e acesso. Mantidas as seções principais de produtos, horários/reserva e FAQ. Os IDs antigos continuam disponíveis como âncoras.
- Removido 1 segundo guia de escolha do Cardápio PT; preservado o primeiro passo a passo.
- Galeria de Café da Manhã reconstruída nos 3 idiomas com 2 imagens reais inspecionadas: mesa de café da manhã e visitante com xícara diante do Pão de Açúcar.
- As fotos antes descritas como mesa posta e café romântico mostravam, respectivamente, visitante com taça e uma banda. Foram retiradas desta galeria, sem apagar os arquivos originais.
- Retirada da galeria de café a foto de sanduíche, sem remover produtos do cardápio. Legendas e textos alternativos da nova galeria foram escritos integralmente em cada idioma.
- Rótulos visíveis “Resposta direta · SEO + GEO” substituídos por linguagem para visitantes nas seções selecionadas.
- Títulos e textos das seções de avaliações com contraste corrigido; cartões empilhados no celular para evitar recortes laterais. Conteúdo dos depoimentos não foi validado nem reescrito neste lote.

## Preservação

JSON-LD, canonical, hreflang e conjunto de preços comparados com a versão anterior. Nenhum produto foi removido das seções de cardápio. Não foram alteradas regras de acesso ou horários operacionais nas seções principais. Não foram ativados workflows de reescrita automática.

## Verificação

- `scripts/test_inner_design.py`: PASS nas 24 páginas de proteção.
- `scripts/schema_rating_guard.py --check`: PASS, 115 arquivos, 0 ocorrências.
- Verificação de diferenças e espaços: PASS.
- Testes responsivos: PASS em 27 combinações (9 páginas × 390/768/1440 px), sem transbordamento horizontal ou textos fora da tela nas seções revisadas. Cor computada dos títulos, parágrafos, listas e legendas verificada após o carregamento.
- Inspeção de capturas da galeria de café e do passo a passo do cardápio, incluindo celular e desktop: fotos correspondentes às legendas, leitura e espaçamento corrigidos. Isto não equivale a certificação WCAG do site inteiro.

## Limites e próximos lotes

As demais imagens do site ainda não estão integralmente auditadas. O nome de um arquivo não é prova do prato, da bebida ou da ocasião mostrada. Dúvidas de identificação exigem confirmação do restaurante. Permanecem fora deste lote a revisão completa das avaliações/depoimentos e a consolidação estrutural do HTML legado. Há oportunidades adicionais de contraste no logotipo da navegação móvel.
