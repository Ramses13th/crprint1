from pathlib import Path
import json,struct,numpy as np
root=Path(__file__).resolve().parents[1]
mesh=json.loads((root/'tools/ship-geometry.json').read_text())[0]
v=np.array(mesh['vertices'],dtype=float);idx=np.array(mesh['indices']).reshape(-1,3)
mn,mx=v.min(0),v.max(0);v=(v-(mn+mx)/2)/(mx-mn).max()*7
# Vertex clustering makes a lower-detail public preview; the full FBX remains separate.
cells=np.round(v/.045).astype(int)
unique,inverse=np.unique(cells,axis=0,return_inverse=True)
centers=np.zeros((len(unique),3));count=np.bincount(inverse)
for a in range(3):centers[:,a]=np.bincount(inverse,weights=v[:,a])/count
tri=inverse[idx];tri=tri[(tri[:,0]!=tri[:,1])&(tri[:,1]!=tri[:,2])&(tri[:,2]!=tri[:,0])]
tri=np.unique(tri,axis=0).astype('<u4');pos=centers.astype('<f4')
pb=pos.tobytes();ib=tri.tobytes();binary=pb+ib
doc={'asset':{'version':'2.0','generator':'CR Print original FBX preview / vertex clustering'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'meshes':[{'primitives':[{'attributes':{'POSITION':0},'indices':1,'material':0}]}],'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[.87,.83,.75,1],'metallicFactor':0,'roughnessFactor':.75},'doubleSided':True}],'buffers':[{'byteLength':len(binary)}],'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':len(pb),'target':34962},{'buffer':0,'byteOffset':len(pb),'byteLength':len(ib),'target':34963}],'accessors':[{'bufferView':0,'componentType':5126,'count':len(pos),'type':'VEC3','min':pos.min(0).tolist(),'max':pos.max(0).tolist()},{'bufferView':1,'componentType':5125,'count':tri.size,'type':'SCALAR'}]}
j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*((-len(j))%4);binary+=b'\0'*((-len(binary))%4)
blob=struct.pack('<III',0x46546C67,2,12+8+len(j)+8+len(binary))+struct.pack('<II',len(j),0x4E4F534A)+j+struct.pack('<II',len(binary),0x004E4942)+binary
(root/'models/nava-preview.glb').write_bytes(blob)
print(f'Preview: {len(pos)} vertices, {len(tri)} triangles, {len(blob)} bytes')
