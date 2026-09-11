const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');const vm=require('node:vm');const path=require('node:path');
const code=fs.readFileSync(path.join(__dirname,'../../scripts/abastecer-apps-script/Code.gs'),'utf8');
class Sheet{
 constructor(rows=[]){this.rows=rows.map(r=>r.slice());this.failWrite=null;}
 getLastRow(){return this.rows.length;} getDataRange(){return this.getRange(1,1,this.rows.length,Math.max(1,...this.rows.map(r=>r.length)));}
 getRange(r,c,h=1,w=1){const s=this;return {
 getRow:()=>r,getValues:()=>Array.from({length:h},(_,i)=>Array.from({length:w},(_,j)=>s.rows[r+i-1]?.[c+j-1]??'')),
 getDisplayValues(){return this.getValues().map(row=>row.map(String));},getValue(){return this.getValues()[0][0];},
 setValues(v){if(s.failWrite){const f=s.failWrite;s.failWrite=null;throw new Error(f);}v.forEach((row,i)=>row.forEach((x,j)=>{s.rows[r+i-1]??=[];s.rows[r+i-1][c+j-1]=x;}));return this;},
 createTextFinder(v){return {matchEntireCell(){return this;},findNext(){for(let i=r;i<r+h;i++)if(String(s.rows[i-1]?.[c-1])===v)return s.getRange(i,c);return null;}}}
 };}
 appendRow(r){this.rows.push(r.slice());}deleteRow(r){this.rows.splice(r-1,1);}
}
function env(){
 const sheets={Registros:new Sheet([Array(12).fill('Header')]),Contagens:new Sheet([Array(12).fill('Header')]),Rodadas:new Sheet([Array(10).fill('Header')]),SolicitacoesLocais:new Sheet([Array(14).fill('Header')])};
 const ss={getSheetByName:n=>sheets[n]||null,insertSheet(n){return sheets[n]=new Sheet();}};
 const c=vm.createContext({console,Date,Set,Map,Number,JSON,Math,Utilities:{formatDate:()=> '20260907'},Session:{getScriptTimeZone:()=> 'America/Sao_Paulo'},LockService:{getScriptLock:()=>({tryLock:()=>true,releaseLock(){}})},SpreadsheetApp:{flush(){}}});vm.runInContext(code,c);
 c.hash_=x=>require('node:crypto').createHash('sha256').update(x).digest('base64url');c.obterSpreadsheet_=()=>ss;c.validarSessao_=()=>({operador:'Leo',selfieUrl:'private'});c.verificarPayloadAssinado_=x=>x;c.configurarAbaSolicitacoes_=()=>{};c.equipamentosDoLocal_=()=>['Esquerda','Centro','Direita'];c.lerMetasLocais_=()=>[{skuId:'AGUA',produto:'Água',idealLocal:80}];c.obterModelo_=()=> 'mock';
 return {c,ss,sheets};
}
const rid='round_12345678901234567890';
let sequence=0;function add(e,fridge,id,qty,commit=true){const capture=new Date(1700000000000+sequence++);e.sheets.Contagens.appendRow([rid,id,new Date(),'Bar',fridge,'AGUA','Água','1',true,qty,qty,'alta']);if(commit)e.sheets.Registros.appendRow([new Date(),'Leo','private','Bar',fridge,'','',id,'mock',1,1,rid,capture]);}
function round(e){e.sheets.Rodadas.appendRow([rid,new Date(),'Bar','Leo',3,3,'Pronta para finalizar','','',new Date()]);}
function req(id,fridge,qty){return {sessionToken:'ok',auditoriaId:id,comprovanteAnalise:{auditoriaId:id,rodadaId:rid,operador:'Leo',local:'Bar',geladeira:fridge,itens:[{skuId:'AGUA',produto:'Água',prateleira:'1',contado_ia:qty,confianca:'alta'}],meta:{capturadaEm:Date.now()}},contagensFinais:[{skuId:'AGUA',contado_humano:qty}]};}
test('água distribuída 20+15+10 gera reposição 35 para meta 80',()=>{const e=env();round(e);add(e,'Esquerda','audit_esq_12345678',20);add(e,'Centro','audit_ctr_12345678',15);add(e,'Direita','audit_dir_12345678',10);const r=e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:e.c.progressoRodada_(e.ss,rid,'Bar').versao});assert.equal(r.totalUnidades,35);assert.equal(r.itens[0].estoqueAtual,45);});
test('detalhes órfãos não concluem equipamento nem entram na soma',()=>{const e=env();add(e,'Esquerda','a',20);add(e,'Centro','orphan',999,false);assert.equal(e.c.progressoRodada_(e.ss,rid,'Bar').concluidas,1);});
test('reenvio de auditoria antiga não apaga nem substitui a mais recente',()=>{const e=env();round(e);add(e,'Esquerda','audit_antigo_123456',20);add(e,'Esquerda','audit_recente_12345',30);e.c.salvarAuditoria(req('audit_antigo_123456','Esquerda',99));const rows=e.c.contagensConfirmadas_(e.ss,rid,'Bar');assert.equal(rows.length,1);assert.equal(rows[0][10],30);assert.equal(e.sheets.Contagens.rows.length,3);});
test('rodada já finalizada não bloqueia confirmação de foto mais nova',()=>{const e=env();round(e);e.sheets.Rodadas.rows[1][7]='SOL-FINAL';const r=e.c.salvarAuditoria(req('audit_novo_12345678','Esquerda',99));assert.equal(r.progresso.concluidas,1);assert.equal(r.superada,false);});
test('pedido salvo antes de falha em Rodadas é recuperado com valores originais',()=>{const e=env();round(e);for(const f of ['Esquerda','Centro','Direita'])add(e,f,f,10);e.sheets.Rodadas.failWrite='interrupção simulada';assert.throws(()=>e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:e.c.progressoRodada_(e.ss,rid,'Bar').versao}),/interrupção/);const r=e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:e.c.progressoRodada_(e.ss,rid,'Bar').versao});assert.equal(r.totalUnidades,50);assert.equal(e.sheets.SolicitacoesLocais.rows.length,2);});
test('nova auditoria grava detalhes antes do commit e retoma após falha',()=>{const e=env();e.sheets.Registros.appendRow=()=>{throw Error('queda antes do commit');};assert.throws(()=>e.c.salvarAuditoria(req('audit_123456789012','Esquerda',20)),/queda/);assert.equal(e.c.progressoRodada_(e.ss,rid,'Bar').concluidas,0);e.sheets.Registros.appendRow=Sheet.prototype.appendRow;const r=e.c.salvarAuditoria(req('audit_123456789012','Esquerda',20));assert.equal(r.progresso.concluidas,1);assert.equal(e.sheets.Contagens.rows.length,2);});
test('pedido sem déficit mantém operador e data após repetição',()=>{const e=env();round(e);for(const f of ['Esquerda','Centro','Direita'])add(e,f,f,40);const a=e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:e.c.progressoRodada_(e.ss,rid,'Bar').versao}),b=e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:e.c.progressoRodada_(e.ss,rid,'Bar').versao});assert.equal(a.totalUnidades,0);assert.equal(b.operador,'Leo');assert.equal(b.criadoEm,a.criadoEm);});
test('IDs de pedido preservam diferenças além dos primeiros seis caracteres',()=>{const e=env();assert.notEqual(e.c.gerarSolicitacaoId_('aaaaaa-1111111111111111',new Date()),e.c.gerarSolicitacaoId_('aaaaaa-2222222222222222',new Date()));});
test('IA omissa, duplicada ou com quantidade inválida é rejeitada',()=>{const e=env();const catalog=[{skuId:'COCA'},{skuId:'COCA_ZERO'}];const row=id=>({sku_id:id,quantidade:5,confianca:'alta'});assert.throws(()=>e.c.validarContagemIA_({contagem:[row('COCA')]},catalog),/incompleta/);assert.throws(()=>e.c.validarContagemIA_({contagem:[row('COCA'),row('COCA')]},catalog),/duplicados/);assert.throws(()=>e.c.validarContagemIA_({contagem:[row('COCA'),{...row('COCA_ZERO'),quantidade:-1}]},catalog),/inválida/);e.c.validarContagemIA_({contagem:[row('COCA'),row('COCA_ZERO')]},catalog);});
test('quantidades vazias, fracionárias e infinitas não viram zero',()=>{const e=env();for(const x of ['',null,-1,1.5,Infinity,'1,5'])assert.throws(()=>e.c.quantidadeValida_(x,'água'));assert.equal(e.c.quantidadeValida_('12','água'),12);});
test('metas desativadas não são reativadas por fallback',()=>{const e=env();e.sheets.MetasLocais=new Sheet([['Local','SKU ID','Produto','Estoque Ideal Local','Ativo'],['Bar','AGUA','Água',80,false]]);const fn=vm.runInContext('('+code.match(/function lerMetasLocais_[\s\S]*?(?=\nfunction montarCatalogoSkusLocal_)/)[0]+')',e.c);assert.equal(fn('Bar').length,0);});
test('metas duplicadas são bloqueadas; número bruto 1000 é preservado',()=>{const e=env();e.sheets.MetasLocais=new Sheet([['Local','SKU ID','Produto','Estoque Ideal Local','Ativo'],['Bar','AGUA','Água',1000,true]]);const fn=vm.runInContext('('+code.match(/function lerMetasLocais_[\s\S]*?(?=\nfunction montarCatalogoSkusLocal_)/)[0]+')',e.c);assert.equal(fn('Bar')[0].idealLocal,1000);e.sheets.MetasLocais.appendRow(['Bar','AGUA','Água',80,true]);assert.throws(()=>fn('Bar'),/duplicada/);});

test('pessoas e rodadas diferentes contribuem para o mesmo estoque do local',()=>{
 const e=env();round(e);add(e,'Esquerda','audit_um_123456789',20);add(e,'Centro','audit_dois_1234567',15);add(e,'Direita','audit_tres_1234567',10);
 e.sheets.Registros.rows[2][1]='Bia';e.sheets.Registros.rows[2][11]='round_bia_1234567890';e.sheets.Contagens.rows[2][0]='round_bia_1234567890';
 assert.equal(e.c.progressoRodada_(e.ss,rid,'Bar').concluidas,3);
 const r=e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:e.c.progressoRodada_(e.ss,rid,'Bar').versao});assert.equal(r.totalUnidades,35);
});
test('primeiro envio atrasado de foto antiga não substitui foto nova de outro auditor',()=>{
 const e=env();round(e);const newer=req('audit_new_123456789','Esquerda',30);newer.comprovanteAnalise.meta.capturadaEm=Date.now()-1000;e.c.salvarAuditoria(newer);
 e.c.validarSessao_=()=>({operador:'Bia',selfieUrl:'private'});const older=req('audit_old_123456789','Esquerda',999);older.comprovanteAnalise.operador='Bia';older.comprovanteAnalise.rodadaId='round_bia_1234567890';older.comprovanteAnalise.meta.capturadaEm=Date.now()-60000;
 const r=e.c.salvarAuditoria(older);assert.equal(r.superada,true);assert.equal(e.c.contagensConfirmadas_(e.ss,rid,'Bar')[0][10],30);assert.equal(e.sheets.Registros.rows.length,3);
});
test('foto nova interrompida antes de confirmação não substitui o estoque válido',()=>{
 const e=env();add(e,'Esquerda','audit_confirmed_123',12);add(e,'Esquerda','audit_orphan_123456',80,false);assert.equal(e.c.contagensConfirmadas_(e.ss,rid,'Bar')[0][10],12);
});
test('duas pessoas gerando pedido da mesma base recebem o mesmo ID',()=>{
 const e=env();round(e);for(const f of ['Esquerda','Centro','Direita'])add(e,f,'audit_'+f,10);
 const versao=e.c.progressoRodada_(e.ss,rid,'Bar').versao;
 const a=e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:versao});e.c.validarSessao_=()=>({operador:'Bia'});
 const b=e.c.finalizarRodada({sessionToken:'ok',rodadaId:'round_bia_1234567890',local:'Bar',versaoBase:versao});assert.equal(b.solicitacaoId,a.solicitacaoId);assert.equal(e.sheets.SolicitacoesLocais.rows.length,2);
});
test('base alterada por outro operador exige conferir atualização antes de pedir',()=>{
 const e=env();round(e);for(const f of ['Esquerda','Centro','Direita'])add(e,f,'audit_'+f,10);const versao=e.c.progressoRodada_(e.ss,rid,'Bar').versao;add(e,'Centro','audit_atualizado_123',40);
 assert.throws(()=>e.c.finalizarRodada({sessionToken:'ok',rodadaId:rid,versaoBase:versao}),/atualizadas/);assert.equal(e.sheets.SolicitacoesLocais.rows.length,1);
});
test('consulta de outro auditor retorna horários e não exige posse da rodada',()=>{
 const e=env();round(e);add(e,'Esquerda','audit_esq_12345678',10);e.c.validarSessao_=()=>({operador:'Bia'});
 const r=e.c.consultarRodada({sessionToken:'ok',rodadaId:rid});assert.equal(r.encontrada,true);assert.equal(r.progresso.detalhes[0].operador,'Leo');assert.ok(r.progresso.detalhes[0].capturadaEm);
});
test('horário ausente ou futuro é rejeitado; recibo antigo usa horário original estimado',()=>{
 const e=env(),now=Date.now();assert.throws(()=>e.c.validarHorarioFoto_(undefined,now));assert.throws(()=>e.c.validarHorarioFoto_(now+120000,now));assert.equal(e.c.validarHorarioFoto_(now-1000,now),now-1000);assert.equal(e.c.horarioAnalise_({exp:now+172800000,meta:{duracaoMs:5000}}),now-5000);
});

test('ocultação nunca mantém confiança alta e produto não identificado não aceita quantidade',()=>{const {c}=env();const catalogo=[{skuId:'AGUA'}];const resposta={contagem:[{sku_id:'AGUA',quantidade:21,confianca:'alta',cobertura:'parcial'}]};c.validarContagemIA_(resposta,catalogo);assert.equal(resposta.contagem[0].confianca,'baixa');assert.throws(()=>c.validarContagemIA_({contagem:[{sku_id:'AGUA',quantidade:3,confianca:'media',cobertura:'nao_identificado'}]},catalogo),/não identificado/);});

test('servidor rejeita contagem nova sem conferência e aceita correção explícita',()=>{const e=env();const p=req('audit_conferencia_123','Esquerda',21);p.comprovanteAnalise.itens[0].requerConferencia=true;p.comprovanteAnalise.itens[0].planejado=true;assert.throws(()=>e.c.salvarAuditoria(p),/Confira o total físico/);assert.equal(e.sheets.Registros.rows.length,1);p.contagensFinais[0].conferido=true;p.contagensFinais[0].contado_humano=48;e.c.salvarAuditoria(p);assert.equal(e.sheets.Contagens.rows[1][10],48);});
test('seis fotos são aceitas e o limite de bytes continua ativo',()=>{const {c}=env();const f='data:image/jpeg;base64,/9j/';assert.equal(c.validarFotos_(Array(6).fill(f)).length,6);assert.throws(()=>c.validarFotos_(Array(7).fill(f)),/limite/);assert.throws(()=>c.validarFotos_(Array(6).fill(f+'a'.repeat(810000))),/tamanho/);});
