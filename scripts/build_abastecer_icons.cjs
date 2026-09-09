// Render the official vector mark with an opaque brand background for launchers.
const fs=require('node:fs');
const path=require('node:path');
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.resolve(__dirname,'..');
const dir=path.join(root,'abastecer/icons');
const logo=fs.readFileSync(path.join(root,'abastecer/logo.svg'),'utf8');
function svg(size){const offset=(512-size)/2;const mark=logo.replace('<svg ',`<svg x="${offset}" y="${offset}" width="${size}" height="${size}" `);return `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" fill="#00405a"/>${mark}</svg>`;}
(async()=>{
 fs.mkdirSync(dir,{recursive:true});
 // The maskable mark fits inside the central circle of radius 40% of the width.
 for(const [kind,markSize,sizes] of [['any',448,[192,512]],['maskable',384,[512]]]){
  const source=svg(markSize);fs.writeFileSync(path.join(dir,`abastecer-${kind}-v1.svg`),source);
  for(const size of sizes)await sharp(Buffer.from(source)).resize(size,size).png().toFile(path.join(dir,`abastecer-${kind}-${size}-v1.png`));
 }
})();
