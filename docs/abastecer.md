# Abastecer — interface no domínio próprio

URL: https://www.embaixadacarioca.com/abastecer/

A versão 2.7 compartilha a última contagem confirmada de cada equipamento entre operadores e entre os dois endereços. Não há exclusividade de rodada: outra pessoa pode fotografar e conferir o equipamento a qualquer momento.

## Publicação

- `abastecer/`: interface estática, marca oficial, manifesto e transporte de mesma origem.
- `functions/abastecer/api.js`: encaminha somente oito operações permitidas ao Apps Script, sem cache e sem repetir POST automaticamente.
- `functions/abastecer/_middleware.js`: libera câmera no próprio domínio e aplica CSP, noindex e no-store somente nesta área.
- `scripts/abastecer-apps-script/HttpApi.gs`: deve existir no projeto Google vinculado à implantação atual. Não contém credenciais.
- `scripts/build_cloudflare_pages.py`: inclui a pasta abastecer na saída existente `_site`.

O backend continua validando sessões, comprovantes da IA, rodadas e idempotência. Fotos e tokens são enviados apenas no corpo HTTPS, nunca em parâmetros de URL. As requisições passam pelo Cloudflare antes de chegar ao Google. O proxy não armazena fotos, tokens ou respostas e não imprime o conteúdo das requisições.

## Limites da migração

IndexedDB e sessionStorage são separados por origem. Rascunhos do endereço Google não são movidos automaticamente. Isso não impede uma nova contagem por outra pessoa ou no novo endereço. O histórico já confirmado permanece na mesma planilha. Rascunhos são preservados por operador no aparelho; envios pendentes permanecem na fila.

O manifesto permite adicionar um atalho à tela inicial. Não é introduzido um service worker de cache de fotos ou respostas operacionais. A fila e os rascunhos existentes continuam sendo usados para falhas de conexão com a página carregada.

## Regra de atualização

A foto mais recente, após conferência e gravação, substitui integralmente a contagem anterior daquele equipamento. O horário da captura é assinado no comprovante da análise; um envio antigo atrasado fica no histórico e não substitui uma captura posterior. Para um conjunto de fotos complementares, vale a primeira captura. Registros anteriores à atualização exibem horário estimado.

A tela mostra os horários e responsáveis das contagens em uso. Gerar o pedido é uma ação explícita após completar os equipamentos. O servidor exige a mesma versão dos totais revisados e impede pedidos duplicados para o mesmo conjunto de contagens.

Publicar primeiro `Code.gs`, `AppJs.html` e `Index.html` deste diretório de scripts no Apps Script, preservando `Styles.html`, `HttpApi.gs` e a implantação existente; depois publicar a interface do site. A coluna de horário da foto é acrescentada ao salvar, sem apagar o histórico.

## Verificação

`node --test tests/abastecer/*.test.cjs`

Validar também os guards de JSON-LD e executar o build habitual. A câmera física, a qualidade da contagem da IA e a entrega no WhatsApp dependem do teste operacional no celular.

Para reverter apenas a migração, retire o lote deste commit do site e use o endereço anterior. O arquivo `HttpApi.gs` pode permanecer publicado sem modificar a interface antiga.
