const UPSTREAM = 'https://script.google.com/macros/s/AKfycbwEksAlApW1Ct3EcvEoQJJv3pVNWTCxOu4Zty_jZU1GnBv0ehYi4h1KpY81EssF_MoEfw/exec';
const ALLOWED = new Set(['carregarAplicacao','abrirSessao','carregarCatalogo','analisarImagens','salvarAuditoria','consultarRodada','finalizarRodada','registrarCompartilhamento']);
const MAX_BYTES = 20000000;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {status, headers: {
    'Content-Type':'application/json; charset=utf-8', 'Cache-Control':'no-store',
    'X-Content-Type-Options':'nosniff', 'X-Robots-Tag':'noindex, nofollow',
    'Referrer-Policy':'no-referrer'
  }});
}

async function readLimited(request) {
  if (Number(request.headers.get('content-length')) > MAX_BYTES) throw new Error('too-large');
  const reader = request.body?.getReader();
  if (!reader) throw new Error('invalid');
  const decoder = new TextDecoder();
  let size = 0, text = '';
  try {
    while (true) {
      const part = await reader.read();
      if (part.done) break;
      size += part.value.byteLength;
      if (size > MAX_BYTES) { await reader.cancel(); throw new Error('too-large'); }
      text += decoder.decode(part.value, {stream:true});
    }
    return text + decoder.decode();
  } finally { reader.releaseLock(); }
}

export async function onRequest({request}) {
  if (request.method !== 'POST') return json({ok:false,error:'Método não permitido.'},405);
  const origin = request.headers.get('origin');
  if (origin && origin !== new URL(request.url).origin) return json({ok:false,error:'Origem não permitida.'},403);
  if (request.headers.get('sec-fetch-site') === 'cross-site') return json({ok:false,error:'Origem não permitida.'},403);
  if (!/^application\/json(?:;|$)/i.test(request.headers.get('content-type') || '')) return json({ok:false,error:'Formato não permitido.'},415);
  let body;
  try { body = JSON.parse(await readLimited(request)); }
  catch(e) { return json({ok:false,error:e.message==='too-large'?'Imagens muito grandes. Reduza a quantidade de fotos.':'Solicitação inválida.'},e.message==='too-large'?413:400); }
  if (!body || !ALLOWED.has(body.action) || !/^[a-zA-Z0-9_-]{16,80}$/.test(body.requestId || '')) return json({ok:false,error:'Operação não permitida.'},400);
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), body.action === 'analisarImagens' ? 145000 : 60000);
  try {
    // Não repetir POST aqui: a fila do app conserva o ID de auditoria/pedido.
    // O Google responde com 302 para o resultado; fetch segue como GET.
    const upstream = await fetch(UPSTREAM, {
      method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},
      body:JSON.stringify({requestId:body.requestId,action:body.action,payload:body.payload}),
      redirect:'follow',signal:controller.signal
    });
    if (!upstream.ok || !upstream.headers.get('content-type')?.includes('application/json')) {
      return json({ok:false,error:'Servidor temporariamente indisponível. Sua contagem foi preservada.'},502);
    }
    const result = await upstream.json();
    if (result.apiVersion !== '2.6' || result.requestId !== body.requestId || typeof result.ok !== 'boolean') {
      return json({ok:false,error:'Resposta incompatível do servidor. Sua contagem foi preservada.'},502);
    }
    return json(result);
  } catch(e) {
    return json({ok:false,error:e.name==='AbortError'?'Tempo de resposta excedido. Sua contagem foi preservada; tente sincronizar.':'Falha temporária na conexão com o servidor. Sua contagem foi preservada.'},504);
  } finally { clearTimeout(timer); }
}
