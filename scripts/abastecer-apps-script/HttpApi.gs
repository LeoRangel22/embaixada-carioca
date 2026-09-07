/** API para a interface /abastecer/. Mantém autenticação e regras existentes. */
function doPost(e) {
  let requestId = '';
  let resultado;
  try {
    if (!e || !e.postData || !e.postData.contents || e.postData.contents.length > 20000000) {
      throw new Error('Solicitação inválida ou imagens muito grandes.');
    }
    const entrada = JSON.parse(e.postData.contents);
    if (!entrada || typeof entrada !== 'object' || Array.isArray(entrada) ||
        !/^[a-zA-Z0-9_-]{16,80}$/.test(entrada.requestId || '')) {
      throw new Error('Identificação da solicitação inválida.');
    }
    requestId = entrada.requestId;
    // Lista explícita: jamais despachar pelo nome de uma função global.
    const rotas = Object.freeze({
      carregarAplicacao: () => carregarAplicacao(),
      abrirSessao: () => abrirSessao(entrada.payload),
      carregarCatalogo: () => carregarCatalogo(entrada.payload),
      analisarImagens: () => analisarImagens(entrada.payload),
      salvarAuditoria: () => salvarAuditoria(entrada.payload),
      consultarRodada: () => consultarRodada(entrada.payload),
      finalizarRodada: () => finalizarRodada(entrada.payload),
      registrarCompartilhamento: () => registrarCompartilhamento(entrada.payload)
    });
    if (typeof entrada.action !== 'string' || !Object.prototype.hasOwnProperty.call(rotas, entrada.action)) {
      throw new Error('Operação não permitida.');
    }
    resultado = {ok: true, apiVersion: '2.6', requestId: requestId, data: rotas[entrada.action]()};
  } catch (erro) {
    const mensagem = erro instanceof SyntaxError ? 'Solicitação inválida.' : String(erro.message || 'Falha temporária no servidor.');
    resultado = {ok: false, apiVersion: '2.6', requestId: requestId, error: mensagem};
  }
  return ContentService.createTextOutput(JSON.stringify(resultado)).setMimeType(ContentService.MimeType.JSON);
}
