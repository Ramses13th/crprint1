import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';

export async function startViewer(viewer){
 if(viewer.dataset.loaded)return;viewer.dataset.loaded='loading';
 const host=viewer.querySelector('[data-viewer-canvas]'),loading=viewer.querySelector('.viewer-loading'),status=viewer.querySelector('[data-viewer-status]'),poster=viewer.querySelector('.viewer-poster');
 loading.hidden=false;
 let renderer,controls,scene,resizeObserver,visibilityObserver,frame=0,interacting=false,visible=true,disposed=false;
 try{
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.5));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.2;
  host.append(renderer.domElement);renderer.domElement.tabIndex=0;renderer.domElement.setAttribute('role','img');renderer.domElement.setAttribute('aria-label','Model 3D al navei 24 Septembrie. Săgeți pentru rotire, plus și minus pentru zoom.');
  scene=new THREE.Scene();const camera=new THREE.PerspectiveCamera(36,1,.05,100);camera.position.set(4,2.8,7);
  controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.09;controls.enablePan=false;controls.minDistance=3;controls.maxDistance=17;controls.maxPolarAngle=Math.PI*.85;
  scene.add(new THREE.HemisphereLight(0xffffff,0x787579,2.1));const key=new THREE.DirectionalLight(0xfff2de,3.2);key.position.set(-4,6,5);scene.add(key);const rim=new THREE.DirectionalLight(0xffffff,1.8);rim.position.set(4,3,-4);scene.add(rim);
  let model;
  const report=progress=>{if(progress.total)status.textContent='Modelul se încarcă: '+Math.round(progress.loaded/progress.total*100)+'%';};
  if(viewer.dataset.modelSrc.endsWith('.glb')){const {GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js');model=(await new GLTFLoader().loadAsync(viewer.dataset.modelSrc,report)).scene;}else{const {FBXLoader}=await import('three/addons/loaders/FBXLoader.js');model=await new FBXLoader().loadAsync(viewer.dataset.modelSrc,report);}
  const box=new THREE.Box3().setFromObject(model),size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());const scale=7/Math.max(size.x,size.y,size.z);model.position.sub(center);const group=new THREE.Group();group.add(model);group.scale.setScalar(scale);scene.add(group);
  const materials=[];model.traverse(node=>{if(node.isMesh){if(!node.geometry.attributes.normal)node.geometry.computeVertexNormals();node.material=new THREE.MeshStandardMaterial({color:0xded3bf,roughness:.73,metalness:.04,side:THREE.DoubleSide});materials.push(node.material);}});
  controls.target.set(0,0,0);controls.update();controls.saveState();
  function render(){if(disposed||!visible||document.hidden)return;renderer.render(scene,camera);}
  function tick(){frame=0;if(disposed||!visible||document.hidden)return;const changed=controls.update();render();if(interacting||changed)frame=requestAnimationFrame(tick);}
  function request(){if(!frame&&!disposed)frame=requestAnimationFrame(tick);}
  controls.addEventListener('start',()=>{interacting=true;request();});controls.addEventListener('end',()=>{interacting=false;request();});controls.addEventListener('change',render);
  function resize(){if(disposed)return;const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();render();}
  resizeObserver=new ResizeObserver(resize);resizeObserver.observe(host);resize();
  visibilityObserver=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)request();else if(frame){cancelAnimationFrame(frame);frame=0;}},{threshold:.05});visibilityObserver.observe(viewer);
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&frame){cancelAnimationFrame(frame);frame=0;}else request();});
  poster.hidden=true;loading.hidden=true;viewer.querySelector('.viewer-toolbar').hidden=false;viewer.querySelector('.viewer-help').hidden=false;viewer.dataset.loaded='ready';
  const wire=viewer.querySelector('[data-viewer-wireframe]');wire.addEventListener('click',()=>{const active=wire.getAttribute('aria-pressed')!=='true';wire.setAttribute('aria-pressed',String(active));materials.forEach(m=>{m.wireframe=active;m.color.set(active?0xc91d37:0xded3bf);});render();});viewer.querySelector('[data-viewer-reset]').addEventListener('click',()=>{controls.reset();request();});
  renderer.domElement.addEventListener('keydown',event=>{const key=event.key;if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-'].includes(key))return;event.preventDefault();const offset=camera.position.clone().sub(controls.target);const spherical=new THREE.Spherical().setFromVector3(offset);if(key==='ArrowLeft')spherical.theta-=.12;if(key==='ArrowRight')spherical.theta+=.12;if(key==='ArrowUp')spherical.phi=Math.max(.1,spherical.phi-.1);if(key==='ArrowDown')spherical.phi=Math.min(controls.maxPolarAngle,spherical.phi+.1);if(key==='+'||key==='=')spherical.radius=Math.max(controls.minDistance,spherical.radius*.9);if(key==='-')spherical.radius=Math.min(controls.maxDistance,spherical.radius*1.1);camera.position.copy(controls.target).add(new THREE.Vector3().setFromSpherical(spherical));controls.update();render();});
  const cleanup=()=>{disposed=true;cancelAnimationFrame(frame);resizeObserver.disconnect();visibilityObserver.disconnect();controls.dispose();scene.traverse(node=>{if(node.isMesh){node.geometry.dispose();for(const material of Array.isArray(node.material)?node.material:[node.material])material.dispose();}});renderer.dispose();};addEventListener('pagehide',event=>{if(!event.persisted)cleanup();},{once:true});
  render();
 }catch(error){viewer.dataset.loaded='';renderer?.dispose();host.replaceChildren();loading.hidden=true;poster.hidden=false;const button=viewer.querySelector('[data-viewer-start]');button.disabled=false;button.textContent='Reîncearcă modelul 3D';const help=viewer.querySelector('.viewer-help');help.hidden=false;help.textContent='Previzualizarea 3D nu este disponibilă în acest browser. Folosește galeria de imagini ca alternativă.';throw error;}
}
