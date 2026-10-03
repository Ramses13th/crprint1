import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
const source=process.argv[2];
const modulePath=process.argv[3];
const {FBXLoader}=await import(pathToFileURL(modulePath));
const bytes=fs.readFileSync(source);
const model=new FBXLoader().parse(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
model.updateMatrixWorld(true);
const meshes=[];
model.traverse(object=>{
 if(!object.isMesh)return;
 const g=object.geometry,p=g.attributes.position,indices=g.index?.array;
 const vertices=[];
 for(let i=0;i<p.count;i++){
  const e=object.matrixWorld.elements,x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  vertices.push([e[0]*x+e[4]*y+e[8]*z+e[12],e[1]*x+e[5]*y+e[9]*z+e[13],e[2]*x+e[6]*y+e[10]*z+e[14]]);
 }
 meshes.push({vertices,indices:indices?Array.from(indices):Array.from({length:p.count},(_,i)=>i)});
});
fs.writeFileSync('tools/ship-geometry.json',JSON.stringify(meshes));
console.log(JSON.stringify({meshes:meshes.length,vertices:meshes.reduce((n,m)=>n+m.vertices.length,0)}));
