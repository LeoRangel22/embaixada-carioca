# Abastecer — interface no domínio próprio

URL: https://www.embaixadacarioca.com/abastecer/

A interface 2.6 usa os mesmos serviços e regras operacionais da versão 2.5 do Apps Script. A alteração do Google adiciona apenas `HttpApi.gs`, sem migrar ou recriar planilhas. O endereço antigo continua funcionando para finalizar rodadas que ainda estejam salvas naquele navegador.

## Publicação

- `abastecer/`: interface estática, marca oficial, manifesto e transporte de mesma origem.
- `functions/abastecer/api.js`: encaminha somente oito operações permitidas ao Apps Script, sem cache e sem repetir POST automaticamente.
- `functions/abastecer/_middleware.js`: libera câmera no próprio domínio e aplica CSP, noindex e no-store somente nesta área.
- `scripts/abastecer-apps-script/HttpApi.gs`: deve existir no projeto Google vinculado à implantação atual. Não contém credenciais.
- `scripts/build_cloudflare_pages.py`: inclui a pasta abastecer na saída existente `_site`.

O backend continua validando sessões, comprovantes da IA, rodadas e idempotência. Fotos e tokens são enviados apenas no corpo HTTPS, nunca em parâmetros de URL. As requisições passam pelo Cloudflare antes de chegar ao Google. O proxy não armazena fotos, tokens ou respostas e não imprime o conteúdo das requisições.

## Limites da migração

IndexedDB e sessionStorage são separados por origem. Rascunhos do endereço Google não são movidos automaticamente. Finalize rodadas pendentes pelo endereço anterior antes de iniciar outra no novo endereço. O histórico já confirmado permanece na mesma planilha.

O manifesto permite adicionar um atalho à tela inicial. Não é introduzido um service worker de cache de fotos ou respostas operacionais. A fila e os rascunhos existentes continuam sendo usados para falhas de conexão com a página carregada.

## Verificação

`node --test tests/abastecer/*.test.cjs`

Validar também os guards de JSON-LD e executar o build habitual. A câmera física, a qualidade da contagem da IA e a entrega no WhatsApp dependem do teste operacional no celular.

Para reverter apenas a migração, retire o lote deste commit do site e use o endereço anterior. O arquivo `HttpApi.gs` pode permanecer publicado sem modificar a interface antiga.
