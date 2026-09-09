# Manual operacional obrigatório

Ao alterar uma operação, tela, botão, regra de contagem, sincronização ou compartilhamento, revise o manual em `abastecer/manual`. O manual deve manter exatamente cinco slides verticais, linguagem de celular e identidade Embaixada Carioca.

1. Consulte `current.json` e crie uma nova pasta sem sobrescrever versões anteriores.
2. Atualize `conteudo.json`, os exemplos e as ilustrações afetadas. Gere PPTX, PDF, PNGs e página HTML a partir desse conteúdo.
3. Atualize o `data-app-version` e o link Como usar nos dois Index.html.
4. Após renderizar e conferir os cinco slides, feche a versão com `scripts/manual/release.py`. O build falha se código e manual divergirem. Não remova esse controle para publicar.
5. Publique os arquivos nativos no Apps Script existente e o site com o manual correspondente na mesma entrega. Verifique o link.

O controle compara arquivos e versões. A revisão semântica do conteúdo exige conferir o fluxo real antes de fechar a versão. Correções técnicas sem impacto também devem registrar uma nova versão compatível quando alterarem os arquivos monitorados.
