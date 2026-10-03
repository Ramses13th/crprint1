from pathlib import Path
import re,json,shutil,zipfile,importlib.util
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sitebuilder',root/'tools/build-site.py');site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)
theme=root/'wordpress/crprint-studio';assets=theme/'assets';templates=theme/'layouts';templates.mkdir(parents=True,exist_ok=True);assets.mkdir(exist_ok=True)
def element(text,tag,cls):
    opening=re.search(r'<'+tag+r'\b[^>]*class="[^"]*\b'+re.escape(cls)+r'\b[^"]*"[^>]*>',text)
    if not opening:raise ValueError(cls)
    depth=0
    for match in re.finditer(r'</?'+tag+r'\b[^>]*>',text[opening.start():]):
        depth+=-1 if match.group().startswith('</') else 1
        if depth==0:return text[opening.start():opening.start()+match.end()]
    raise ValueError('unclosed '+cls)
for name in ['design.css','script.js','model-viewer.js']:shutil.copy2(root/name,assets/name)
shutil.copy2(root/'wordpress/wordpress.css',assets/'wordpress.css')
shutil.copytree(root/'vendor',assets/'vendor',dirs_exist_ok=True)
(assets/'models').mkdir(exist_ok=True);shutil.copy2(root/'models/nava-preview.glb',assets/'models/nava-preview.glb')
(assets/'images').mkdir(exist_ok=True)
names=['crprint-atelier-generated','crprint-series-generated','crprint-promo-generated','crprint-modeling-generated','nava-studio','nava-side','nava-detail','portfolio-medical','portfolio-prototip','portfolio-personalizat','hero-video-poster','service-fdm','service-sla','service-scanning','service-facescan']
for name in names:
    for path in (root/'images').glob(name+'*.webp'):shutil.copy2(path,assets/'images'/path.name)
for name in ['cr-print-logo-original.webp','logo-og-512.png','3d-printing-loop.webm']:shutil.copy2(root/'images'/name,assets/'images'/name)
for key in ['index','despre','servicii','portofoliu','contact','modelare-3d','printare-fdm','printare-sla','scanare-3d','facescan','confidentialitate','termeni']:
    text=(root/'data'/f'page-{key}.html').read_text(encoding='utf-8')
    if key=='index':text=text.replace(element(text,'div','shop-showcase'),'[crprint_store_showcase]')
    if key=='contact':
        form=element(text,'form','form-panel');(templates/'contact-form.html').write_text(re.sub(r'<noscript>.*?</noscript>','',form,flags=re.S),encoding='utf-8');text=text.replace(form,'[crprint_contact_form]')
    (templates/f'{key}.html').write_text(text,encoding='utf-8')
(templates/'header.html').write_text(site.header('index'),encoding='utf-8')
(templates/'footer.html').write_text(site.footer(),encoding='utf-8')
(templates/'viewer.html').write_text(site.viewer(),encoding='utf-8')
shutil.copy2(root/'data/pages.json',templates/'pages.json')
for folder in [theme,root/'wordpress/crprint-core']:
    output=root/'wordpress'/f'{folder.name}.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in folder.rglob('*'):
            if path.is_file():archive.write(path,path.relative_to(folder.parent))
    print(output.name,output.stat().st_size)
with zipfile.ZipFile(root/'wordpress/nava-demo.zip','w',zipfile.ZIP_DEFLATED) as demo:
    demo.write(root/'models/NAVA 24 SEPTEMBRIE.fbx','NAVA 24 SEPTEMBRIE.fbx')
    demo.writestr('CITESTE-MA.txt','Fisier demonstrativ pentru fluxul local. Inainte de vanzare trebuie confirmate licenta si drepturile de utilizare. Nu implica o plata reala.')
blueprint=json.loads((root/'wordpress/blueprint.json').read_text(encoding='utf-8'))
blueprint['steps']=[s for s in blueprint['steps'] if s['step'] not in ('runPHP','writeFile','mkdir','login','setSiteLanguage')]
blueprint['steps'] += [
    {'step':'setSiteLanguage','language':'ro_RO'},
    {'step':'mkdir','path':'/wordpress/wp-content/uploads/woocommerce_uploads'},
    {'step':'writeFile','path':'/wordpress/wp-content/uploads/woocommerce_uploads/nava-demo.zip','data':{'resource':'bundled','path':'/nava-demo.zip'}},
    {'step':'writeFile','path':'/wordpress/wp-content/uploads/woocommerce_uploads/.htaccess','data':'Require all denied\n'},
    {'step':'writeFile','path':'/wordpress/wp-content/uploads/woocommerce_uploads/index.php','data':'<?php // No directory listing.'},
    {'step':'runPHP','code':(root/'wordpress/demo-setup.php').read_text(encoding='utf-8')},
    {'step':'login'}
]
(root/'wordpress/blueprint.json').write_text(json.dumps(blueprint,ensure_ascii=False,indent=2),encoding='utf-8')

repair=dict(blueprint)
repair['steps']=[dict(s,ifAlreadyInstalled='overwrite') if s['step'] in ('installTheme','installPlugin') else s for s in blueprint['steps'] if s['step']!='installPlugin' or s.get('pluginData',{}).get('resource')=='bundled']
(root/'wordpress/repair.json').write_text(json.dumps(repair,ensure_ascii=False,indent=2),encoding='utf-8')
