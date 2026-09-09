import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {resolvePresentationFont,finalizePresentation} from '/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs';
import path from 'node:path';
const workspaceDir=process.env.MANUAL_BUILD_DIR,root=process.cwd(),dir=path.join(root,'abastecer/manual',process.env.MANUAL_VERSION||'2.8.0');
if(!workspaceDir||!path.isAbsolute(workspaceDir))throw Error('MANUAL_BUILD_DIR absoluto obrigatório');
const data=JSON.parse(await fs.readFile(dir+'/conteudo.json','utf8'));
const font=resolvePresentationFont({fontFamily:"DejaVu Sans"});console.log('font',font);
const p=Presentation.create({slideSize:{width:720,height:1280}});
const ink='#00405a',cream='#fbf7ef',muted='#415462';
function text(sl,txt,x,y,w,h,size=34,bold=false,color=ink){const s=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});s.text=txt;s.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none'};return s;}
for(let i=0;i<5;i++){
 const d=data.slides[i],s=p.slides.add();s.background.fill=cream;s.shapes.add({geometry:'rect',position:{left:0,top:0,width:720,height:125},fill:ink,line:{fill:'none',width:0}});
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(root,'abastecer/logo.svg'))),contentType:'image/svg+xml',alt:'Embaixada Carioca',fit:'contain',position:{left:48,top:28,width:74,height:76}});
 text(s,'EMBAIXADA CARIOCA',140,38,520,32,24,true,'#ffffff');text(s,'REPOSIÇÃO • GUIA DO CELULAR',140,72,520,30,19,false,'#efe4d1');
 text(s,`${i+1} / 5`,48,142,610,32,23,true,muted);
 text(s,d.title,48,193,624,126,52,true);
 text(s,d.subtitle,48,320,624,85,30,false,muted);
 let y=420;
 if(d.image){let h=i===4?265:345;s.images.add({blob:new Uint8Array(await fs.readFile(dir+'/'+d.image)),contentType:'image/png',alt:d.title+' — ilustração',fit:'contain',position:{left:80,top:y,width:560,height:h}});y+=h+25;}
 else {
   text(s,d.tableLabel,48,y,624,28,21,true,muted);y+=46;
   const rows=d.table.length,cols=d.table[0].length,h=i===2?160:252;
   const table=s.tables.add({rows,columns:cols,left:48,top:y,width:624,height:h,columnWidths:cols===3?[344,140,140]:[440,184],values:d.table});
   table.borders.assign({fill:'#cfc6b6',width:1});
   for(let rr=0;rr<rows;rr++)for(let c=0;c<cols;c++){let cell=table.getCell(rr,c);cell.fill=rr===0?ink:rr===rows-1?'#eadcc5':'#ffffff';cell.text.style={typeface:font,fontSize:i===2?32:29,bold:rr===0||rr===rows-1,color:rr===0?'#ffffff':ink};}
   y+=h+26;
   if(d.formula){text(s,d.formula,48,y,624,80,34,true);y+=84;}
 }
 let sizes=i===4?29:i===3?31:32;
 let gap=i===4?112:i===3?85:83;
 for(let j=0;j<d.steps.length;j++){text(s,`${j+1}`,48,y,48,gap-4,sizes,true);text(s,d.steps[j],102,y,568,gap-4,sizes,false);y+=gap;}
 let noteY=Math.max(y+16,i===2?958:1090);if(i===4)noteY=1090;
 text(s,d.note,48,noteY,624,122,i===4?26:28,true);
 text(s,`Manual ${data.version}  •  ${data.date}`,48,1230,624,30,19,false,muted);
 s.speakerNotes.textFrame.setText('Guia operacional da Embaixada Carioca. Fonte: código do app '+data.appUrl+' versão '+data.version+'. Nomes dos botões correspondem à interface. Números nas tabelas são exemplos ilustrativos, não o estoque real. Ilustrações geradas, não representam funcionários reais. '+(i===4?'Abrir o WhatsApp não comprova recebimento. Não existe confirmação de entrega integrada neste fluxo.':''));
 await fs.writeFile(`${workspaceDir}/build/slide-${i+1}.png`,new Uint8Array(await (await p.export({slide:s,format:'png',scale:1})).arrayBuffer()));
}
const candidatePath=workspaceDir+'/build/candidate.pptx';await(await PresentationFile.exportPptx(p)).save(candidatePath);
const result=await finalizePresentation({workspaceDir,candidatePath,finalPath:workspaceDir+'/output/Manual-Embaixada-Carioca-'+data.version+'-vertical.pptx',pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','6858000,12192000','--validate-heading-fit','--require-native-table-slide','3','--require-native-table-slide','4'],explicitTotalSlideCount:5,requiredNativeTableOwnerSlides:[3,4],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:workspaceDir+'/build/validation-vertical.json'});console.log(result);
