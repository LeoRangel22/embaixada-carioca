/* Transporte de mesma origem. Fotos e tokens nunca entram na URL. */
(() => {
  'use strict';
  window.reposicaoApi = async function(nome, payload) {
    const requestId = crypto.randomUUID();
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), nome === 'analisarImagens' ? 150000 : 65000);
    try {
      const response = await fetch('/abastecer/api', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        credentials: 'omit', cache: 'no-store', signal: controller.signal,
        body: JSON.stringify({requestId, action: nome, payload})
      });
      if (!response.headers.get('content-type')?.includes('application/json')) {
        throw new Error('Servidor temporariamente indisponível. Sua contagem foi preservada; tente novamente.');
      }
      const result = await response.json();
      if (!response.ok || result.ok !== true) {
        throw new Error(result.error || 'Falha temporária na conexão com o servidor.');
      }
      if (result.requestId !== requestId || result.apiVersion !== '2.6') {
        throw new Error('Resposta do servidor incompatível. Sua contagem foi preservada; atualize a página.');
      }
      return result.data;
    } catch (error) {
      if (error.name === 'AbortError') throw new Error('Tempo de resposta excedido. Sua contagem foi preservada; tente sincronizar.');
      if (error instanceof TypeError) throw new Error('Falha de conexão. Sua contagem foi preservada; tente sincronizar.');
      throw error;
    } finally { clearTimeout(timer); }
  };
})();
