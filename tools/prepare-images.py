from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json, numpy as np

ROOT=Path(__file__).resolve().parents[1]
def optimize(source,name):
    im=Image.open(source).convert('RGB')
    for width,suffix in [(1536,''),(960,'-960'),(480,'-480')]:
        copy=im.copy();copy.thumbnail((width,width*2))
        copy.save(ROOT/'images'/f'{name}{suffix}.webp','WEBP',quality=83,method=6)

if __name__=='__main__':
    import sys
    if len(sys.argv)>2:
        optimize(sys.argv[1],sys.argv[2]);raise SystemExit
    meshes=json.loads((ROOT/'tools/ship-geometry.json').read_text())
    vertices=np.array(meshes[0]['vertices'],dtype=float)
    indices=np.array(meshes[0]['indices']).reshape(-1,3)
    mn,mx=vertices.min(0),vertices.max(0)
    vertices=(vertices-(mn+mx)/2)/(mx-mn).max()
    normals=np.cross(vertices[indices[:,1]]-vertices[indices[:,0]],vertices[indices[:,2]]-vertices[indices[:,0]])
    normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-10)
    light=np.array([-.3,.85,.6]);light/=np.linalg.norm(light)
    intensity=.35+.65*np.abs(normals@light)
    for name,eye in [('nava-studio',[.75,.48,1.3]),('nava-side',[.12,.25,1.8]),('nava-detail',[-.75,.5,1.15])]:
        W,H=2400,1800
        forward=np.array(eye,dtype=float);forward/=np.linalg.norm(forward)
        right=np.cross(np.array([0.,1.,0.]),forward);right/=np.linalg.norm(right)
        up=np.cross(forward,right)
        projected=np.column_stack([vertices@right,-vertices@up])
        pmin,pmax=projected.min(0),projected.max(0)
        scale=min(W*.82/(pmax[0]-pmin[0]),H*.66/(pmax[1]-pmin[1]))
        projected=(projected-(pmin+pmax)/2)*scale+np.array([W/2,H*.46])
        depth=vertices@forward
        im=Image.new('RGB',(W,H),'#eeebe6');draw=ImageDraw.Draw(im)
        for y in range(H):
            t=y/H;draw.line((0,y,W,y),fill=tuple(int(c-t*16) for c in (244,241,235)))
        shadow=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shadow)
        sd.ellipse((W*.14,H*.65,W*.88,H*.77),fill=(36,30,31,65));shadow=shadow.filter(ImageFilter.GaussianBlur(38));im=Image.alpha_composite(im.convert('RGBA'),shadow);draw=ImageDraw.Draw(im)
        order=np.argsort(depth[indices].mean(1))
        for i in order:
            pts=[tuple(p) for p in projected[indices[i]]]
            value=float(intensity[i]);color=tuple(int(c*value) for c in (227,215,197))
            draw.polygon(pts,fill=color)
        im.convert('RGB').resize((1600,1200),Image.Resampling.LANCZOS).save(ROOT/'images'/f'{name}.webp','WEBP',quality=89,method=6)
        optimize(ROOT/'images'/f'{name}.webp',name)
        print(name)
