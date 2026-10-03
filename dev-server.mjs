import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root=path.dirname(fileURLToPath(import.meta.url));
const port=Number(process.env.PORT||process.argv[2]||4173);
const dataDir=path.join(os.tmpdir(),'crprint-local-demo');
await fs.mkdir(dataDir,{recursive:true});
const catalogFile=path.join(root,'data/catalog.json');
const adminToken=crypto.randomBytes(32).toString('hex');
const challenges=new Map(), rate=new Map(), dedup=new Map();
let writeTurn=Promise.resolve();
const ports=[4173,4174].includes(port)?[port,port===4173?4174:4173]:[port];
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.webm':'video/webm','.fbx':'application/octet-stream','.glb':'model/gltf-binary','.zip':'application/zip','.xml':'application/xml','.txt':'text/plain; charset=utf-8','.woff2':'font/woff2','.csv':'text/csv; charset=utf-8'};
const readJson=async(file,fallback)=>{try{return JSON.parse(await fs.readFile(file,'utf8'));}catch{return fallback;}};
const saveJson=async(file,value)=>{const tmp=file+'.tmp';await fs.writeFile(tmp,JSON.stringify(value,null,2));await fs.rename(tmp,file);};
const clean=(value,max=1000)=>String(value??'').trim().slice(0,max);
const mailOk=value=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
const json=(res,code,value)=>{res.writeHead(code,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(value));};
async function body(req){let result='';for await(const chunk of req){result+=chunk;if(Buffer.byteLength(result)>100000)throw Error('body');}return JSON.parse(result||'{}');}
const catalog=()=>readJson(catalogFile,[]);
const listFile=type=>path.join(dataDir,type+'.json');
async function addRecord(type,value){const entries=await readJson(listFile(type),[]);entries.unshift(value);await saveJson(listFile(type),entries.slice(0,1000));}
function originOk(req){return !req.headers.origin||req.headers.origin===`http://${req.headers.host}`;}
function limited(req){const now=Date.now();const key=req.socket.remoteAddress;const recent=(rate.get(key)||[]).filter(time=>now-time<60000);recent.push(now);rate.set(key,recent);return recent.length>20;}
function productValid(p){return /^[a-z0-9][a-z0-9-]{2,79}$/.test(p.id)&&p.name.length>=3&&['physical','digital'].includes(p.kind)&&Number.isInteger(p.price)&&p.price>=0&&p.price<=10000000&&Number.isInteger(p.stock)&&p.stock>=0&&p.stock<=10000&&/^images\/[a-zA-Z0-9_.-]+\.(?:webp|png|jpg)$/.test(p.image);}
const handleRequest=async(req,res)=>{
 let release;
 try{
  if(!ports.some(p=>req.headers.host===`127.0.0.1:${p}`||req.headers.host===`localhost:${p}`))return json(res,403,{error:'Gazdă nepermisă.'});
  const url=new URL(req.url,`http://${req.headers.host}`);let pathname=decodeURIComponent(url.pathname);
  res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('X-Robots-Tag','noindex, nofollow');res.setHeader('Referrer-Policy','strict-origin-when-cross-origin');
  if(pathname.startsWith('/api/')){
   if(!originOk(req))return json(res,403,{error:'Origine nepermisă.'});
   if(req.method==='POST'){const previous=writeTurn;writeTurn=new Promise(resolve=>release=resolve);await previous;}
   if(req.method==='GET'&&pathname==='/api/config')return json(res,200,{demo:true,emailConfigured:false,adminLocalOnly:true});
   if(req.method==='GET'&&pathname==='/api/products')return json(res,200,(await catalog()).filter(p=>p.active));
   if(req.method==='GET'&&pathname==='/api/challenge'){
    const a=crypto.randomInt(2,8),b=crypto.randomInt(1,6),id=crypto.randomUUID();challenges.set(id,{answer:a+b,time:Date.now()});
    for(const[key,value]of challenges)if(Date.now()-value.time>600000)challenges.delete(key);
    return json(res,200,{id,question:`${a} + ${b}`});
   }
   if(pathname.startsWith('/api/admin')){
    if(req.method==='GET'&&pathname==='/api/admin-session')return json(res,200,{token:adminToken,localOnly:true});
    if(req.headers['x-admin-token']!==adminToken)return json(res,403,{error:'Sesiunea de administrare a expirat. Reîncarcă pagina.'});
    if(req.method==='GET'&&pathname==='/api/admin-data')return json(res,200,{products:await catalog(),orders:await readJson(listFile('orders'),[]),messages:await readJson(listFile('messages'),[])});
    if(req.method==='POST'&&pathname==='/api/admin-products'){
     const incoming=await body(req);const p={id:clean(incoming.id,80),name:clean(incoming.name,120),kind:incoming.kind,price:Number(incoming.price),stock:Number(incoming.stock),active:Boolean(incoming.active),image:clean(incoming.image,150),description:clean(incoming.description,1200),demo:true};
     if(!productValid(p))return json(res,422,{error:'Verifică numele, identificatorul, prețul, stocul și imaginea locală.'});
     const products=await catalog();const i=products.findIndex(x=>x.id===p.id);if(i>=0)products[i]=p;else products.push(p);await saveJson(catalogFile,products);return json(res,200,{ok:true});
    }
    if(req.method==='POST'&&pathname==='/api/admin-order'){
     const{id,status}=await body(req);if(!['new','processing','completed','cancelled'].includes(status))return json(res,422,{error:'Stare invalidă.'});
     const orders=await readJson(listFile('orders'),[]);const order=orders.find(o=>o.id===id);if(!order)return json(res,404,{error:'Comanda nu există.'});order.status=status;await saveJson(listFile('orders'),orders);return json(res,200,{ok:true});
    }
    return json(res,404,{error:'Ruta nu există.'});
   }
   if(req.method==='POST'&&limited(req))return json(res,429,{error:'Prea multe cereri. Așteaptă un minut.'});
   if(req.method==='POST'&&pathname==='/api/contact'){
    const payload=await body(req);const challenge=challenges.get(payload.challengeId);
    if(payload.company_website||!challenge||Date.now()-challenge.time<900||Date.now()-challenge.time>600000||Number(payload.answer)!==challenge.answer)return json(res,422,{error:'Verificarea anti-spam nu este validă. Încearcă noul calcul.'});
    const message={id:'MSG-'+crypto.randomBytes(4).toString('hex').toUpperCase(),name:clean(payload.name,100),email:clean(payload.email,180),phone:clean(payload.phone,40),service:clean(payload.service,100),message:clean(payload.message,5000),createdAt:new Date().toISOString(),demo:true};
    if(!payload.consent||message.name.length<2||!mailOk(message.email)||message.message.length<10)return json(res,422,{error:'Adaugă un nume, un email valid și cel puțin 10 caractere despre proiect.'});
    challenges.delete(payload.challengeId);await addRecord('messages',message);return json(res,201,{ok:true,demo:true,emailSent:false,id:message.id,message:'Solicitarea a fost înregistrată. Îți răspundem în timpul programului.'});
   }
   if(req.method==='POST'&&pathname==='/api/orders'){
    const p=await body(req);const key=clean(req.headers['idempotency-key']||p.idempotencyKey,100);if(key&&dedup.has(key))return json(res,200,dedup.get(key));
    const products=await catalog();if(!Array.isArray(p.items)||!p.items.length||p.items.length>30)return json(res,422,{error:'Coșul este gol sau invalid.'});
    let subtotal=0,physical=false;const items=[],seen=new Set();
    for(const entry of p.items){const item=products.find(x=>x.id===entry.id&&x.active);const q=Number(entry.quantity);if(seen.has(entry.id)||!item||!Number.isInteger(q)||q<1||q>Math.min(item.stock,100))return json(res,422,{error:'Un produs sau cantitatea sa nu mai este disponibilă.'});seen.add(entry.id);subtotal+=item.price*q;physical||=item.kind==='physical';items.push({id:item.id,name:item.name,kind:item.kind,quantity:q,price:item.price});}
    const c=p.customer||{};const customer={name:clean(c.name,100),email:clean(c.email,180),phone:clean(c.phone,40),address:clean(c.address,180),city:clean(c.city,80),county:clean(c.county,80),postalCode:clean(c.postalCode,15)};
    if(customer.name.length<2||!mailOk(customer.email))return json(res,422,{error:'Numele și emailul sunt necesare.'});
    if(physical&&!['courier','pickup'].includes(p.shipping))return json(res,422,{error:'Alege livrarea sau ridicarea din atelier.'});
    const shipping=physical?(p.shipping==='courier'?'courier':'pickup'):'digital';if(shipping==='courier'&&(!customer.address||!customer.city||!customer.county))return json(res,422,{error:'Completează adresa pentru livrare.'});
    const shippingCost=shipping==='courier'?1900:0;const order={id:'CR-'+crypto.randomBytes(4).toString('hex').toUpperCase(),items,customer,shipping,subtotal,shippingCost,total:subtotal+shippingCost,status:'new',payment:'demo',notes:clean(p.notes,1000),createdAt:new Date().toISOString(),demo:true};
    await addRecord('orders',order);const result={ok:true,id:order.id,total:order.total,shipping,demo:true,emailSent:false};if(key)dedup.set(key,result);return json(res,201,result);
   }
   return json(res,404,{error:'Ruta nu există.'});
  }
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);return res.end();}
  if(pathname.endsWith('/'))pathname+='index.html';
  const filename=path.resolve(root,'.'+pathname);if(!filename.startsWith(root+path.sep)||pathname.includes('\0')||pathname.split('/').some(p=>p.startsWith('.'))||/\.(?:php|mjs)$/.test(pathname)){res.writeHead(404);return res.end('Not found');}
  const stat=await fs.stat(filename);if(!stat.isFile())throw Error('notfound');
  res.setHeader('Content-Type',types[path.extname(filename)]||'application/octet-stream');res.setHeader('Cache-Control','no-cache');res.setHeader('Content-Length',stat.size);
  if(req.method==='HEAD')return res.end();res.end(await fs.readFile(filename));
 }catch(error){if(!res.headersSent)json(res,error.code==='ENOENT'?404:400,{error:'Cererea nu poate fi procesată.'});else res.end();}finally{release?.();}
};
for(const p of ports){const server=http.createServer(handleRequest);server.on('error',error=>{if(p!==port&&error.code==='EADDRINUSE')console.log(`Portul alternativ ${p} este deja ocupat.`);else{console.error(error.message);process.exitCode=1;}});server.listen(p,'127.0.0.1',()=>console.log(`CR Print demo: http://127.0.0.1:${p} · admin: /admin.html · date private: ${dataDir}`));}
