# Navegação e ações da home — refinamento de 9 de setembro de 2026

## Escopo

Homes PT, EN e ES. Ajustes no componente CSS existente, sem alterar conteúdo, fotografias, URLs de destino, horários, prêmios, metadados ou JSON-LD. Sem modificações nas páginas internas e no aplicativo abastecer.

## Problemas tratados

- Menu em caixa alta e com espaçamento excessivo: tipografia mais discreta, sem transformação para maiúsculas.
- Botão de reserva desproporcional: dimensão compacta, mantendo área de toque mínima de 44 px no topo.
- Excesso de caixas: selo de avaliações sem fundo/borda; links secundários do hero sem contorno, mas sublinhados e com área de toque mínima de 48 px.
- Animações decorativas de pulsação/brilho nos botões: removidas nas homes.
- Regra legada translateX(28px) no selo: removida, pois provocava colisão com a reserva em 1440 px. Deslocamento artificial do seletor de idioma também removido.
- Ícone de localização colado ao texto: espaçamento explícito.
- Cache: nova versão do CSS referenciada nas três homes.

## Verificação

Teste Chromium em PT/EN/ES, com larguras 320, 390, 768, 1024, 1440 e 1920 px; checagem do hero, menu inicial e menu após rolagem. Screenshots desktop/mobile e primeira seção após o hero. Teste de conteúdo/destinos da home aprovado. Guardas de JSON-LD e rating aprovados em 115 HTMLs, sem pendências.

Resultado final: 18 combinações aprovadas; zero sobreposições nos componentes testados, zero overflow horizontal e zero erros JavaScript. Menu mobile abre/fecha e seletor de idioma permanece disponível nas nove combinações mobile/tablet. Nenhuma colisão no topo antes ou após rolagem.

## Outros pontos observados para próximo lote

1. Rever o espaço vertical entre título e texto de “Os três momentos”, que perde continuidade visual no desktop.
2. Padronizar os ícones da navegação inferior mobile: emojis coloridos destoam da identidade sóbria.
3. Encurtar editorialmente a linha de localização acima do título, hoje longa e repetitiva. Preservar informação útil e intenção de busca, sem esconder conteúdo via CSS.
4. Evitar novas camadas de estilos corretivos: consolidar regras antigas por componente, com teste antes/depois. A colisão do selo demonstra o risco dos deslocamentos artificiais.

Esses pontos não foram tratados como falha geral do site nem como certificação de acessibilidade. A captura de página inteira, sem rolagem, não comprova ausência de conteúdo nas seções com carregamento/renderização adiada.
