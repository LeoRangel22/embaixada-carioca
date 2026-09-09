# Navegação útil para visitantes — 09/09/2026

Auditoria no navegador das 24 páginas internas principais em viewport mobile (390px).

## Problemas corrigidos

- 20 links de rodapé “Acessibilidade / Accessibility / Accesibilidad” apontavam apenas para `#`. Agora levam à seção de orientação na página de acesso no idioma correspondente.
- Dois links “pular ao conteúdo” em EN/ES apontavam para um id inexistente e estavam em português. Traduzidos, com alvo no main e tabindex para navegação assistiva.
- Criadas orientações curtas PT/EN/ES em Como Chegar para consultar necessidades específicas com a equipe antes da reserva. Sem prometer rampas, elevadores, banheiros adaptados ou condições não verificadas.

## Evidência

- Antes: 22 atalhos visíveis sem destino válido.
- Depois: zero atalhos locais quebrados nas mesmas 24 páginas.
- Três blocos de orientação visíveis em 390px, largura dentro da tela e texto azul sobre fundo claro.
- Teste de preservação das 24 páginas: PASS (preços, canonical/hreflang e JSON-LD comparados ao HEAD anterior).
- Guards de rating e de chaves duplicadas: PASS, 115 páginas.

## Próxima sequência de impacto

1. Revisar a correspondência entre fotos e legendas e os textos longos de páginas comerciais EN/ES.
2. Testar o caminho completo de orçamento/reserva, distinguindo clique de conversão concluída.
3. Medir velocidade em celular com dados de campo e laboratório antes de otimizar recursos.

Não é certificação WCAG AAA nem avaliação do acesso físico ao restaurante. O escopo desta auditoria é navegação por âncoras visíveis, não todos os links externos do site.
