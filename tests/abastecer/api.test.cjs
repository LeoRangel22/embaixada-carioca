const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
const requestId='test_request_123456789';
const loadProxy=()=>import('data:text/javascript;base64,'+Buffer.from(fs.readFileSync(path.join(root,'functions/abastecer/api.js'))).toString('base64'));
function req(action='carregarAplicacao',more={}){return new Request('https://www.embaixadacarioca.com/abastecer/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({requestId,action,...more})});}
test('proxy rejeita ações administrativas, origem externa e GET antes de chamar o Google',async()=>{
  const {onRequest}=await loadProxy();
  assert.equal((await onRequest({request:req('configurarAplicacao')})).status,400);
  const r=req();r.headers.set('Origin','https://example.com');
  assert.equal((await onRequest({request:r})).status,403);
  assert.equal((await onRequest({request:new Request('https://www.embaixadacarioca.com/abastecer/api')})).status,405);
});
test('proxy preserva ID e conteúdo sem duplicar POST; resposta fica fora do cache',async()=>{
  const {onRequest}=await loadProxy();const old=global.fetch;let calls=0;
  global.fetch=async(url,init)=>{calls++;const data=JSON.parse(init.body);assert.equal(data.payload.auditoriaId,'audit-original');assert.equal(data.requestId,requestId);assert.equal(init.redirect,'follow');return Response.json({ok:true,apiVersion:'2.6',requestId,data:{status:'sucesso'}});};
  try {const response=await onRequest({request:req('salvarAuditoria',{payload:{auditoriaId:'audit-original'}})});assert.equal((await response.json()).ok,true);assert.equal(response.headers.get('cache-control'),'no-store');assert.equal(calls,1);}finally{global.fetch=old;}
});
test('proxy rejeita HTML de login e resposta vinculada a outro ID',async()=>{
  const {onRequest}=await loadProxy();const old=global.fetch;
  try {global.fetch=async()=>new Response('<html>login</html>',{headers:{'Content-Type':'text/html'}});assert.equal((await onRequest({request:req()})).status,502);
    global.fetch=async()=>Response.json({ok:true,apiVersion:'2.6',requestId:'another'});assert.equal((await onRequest({request:req()})).status,502);
  }finally{global.fetch=old;}
});
function gas(){const context={ContentService:{MimeType:{JSON:'json'},createTextOutput(text){return {text,setMimeType(){return this;}};}},carregarAplicacao:()=>({operadores:['Operador teste']}),carregarCatalogo:token=>{if(token!=='valid')throw new Error('Sessão inválida.');return {catalogo:{}};}};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'scripts/abastecer-apps-script/HttpApi.gs'),'utf8'),context);return data=>JSON.parse(context.doPost({postData:{contents:JSON.stringify({requestId,...data})}}).text);}
test('API Google libera somente operações explicitamente listadas',()=>{
  const post=gas();for(const action of ['configurarAplicacao','desativarPinOperacional','constructor','toString','__proto__','exigirExecucaoAdministrativa_'])assert.equal(post({action}).ok,false);
  const data=post({action:'carregarAplicacao'});assert.equal(data.requestId,requestId);assert.equal(data.apiVersion,'2.6');assert.equal(data.ok,true);
});
test('API Google preserva validação de sessão e erros operacionais',()=>{
  const post=gas();assert.equal(post({action:'carregarCatalogo',payload:'valid'}).ok,true);const invalid=post({action:'carregarCatalogo',payload:'invalid'});assert.equal(invalid.ok,false);assert.match(invalid.error,/Sessão inválida/);
});
test('interface é direta, sem iframe e sem funções administrativas ou google.script.run',()=>{
  const html=fs.readFileSync(path.join(root,'abastecer/index.html'),'utf8');
  assert.doesNotMatch(html,/<iframe|<\?!=/);assert.match(html,/width=device-width/);assert.match(html,/noindex/);
  for(const file of ['app.v2.8.js','api.v2.6.js'])assert.doesNotMatch(fs.readFileSync(path.join(root,'abastecer',file),'utf8'),/google\.script\.run|GEMINI_API_KEY|configurarAplicacao/);
});
test('política da área de abastecimento permite câmera e mantém segurança do documento',async()=>{
  const source=fs.readFileSync(path.join(root,'functions/abastecer/_middleware.js'));
  const {onRequest}=await import('data:text/javascript;base64,'+source.toString('base64'));
  const response=await onRequest({next:async()=>new Response('app',{headers:{'Permissions-Policy':'camera=()'}})});
  assert.match(response.headers.get('Permissions-Policy'),/camera=\(self\)/);assert.equal(response.headers.get('X-Frame-Options'),'DENY');assert.match(response.headers.get('Content-Security-Policy'),/connect-src 'self'/);
});
