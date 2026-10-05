"""Reading layout, original diagrams and documented corrections for the handbook."""
import html
import re

DATE = '5 octombrie 2026'

# These are project-specific process diagrams, not replicas of vendor screens.
META = {
 'index': ('Privire de ansamblu', 'Alegi traseul potrivit și pornești mediul local.', 'Folderul proiectului și acces la computer.', 'Știi unde lucrezi și în ce ordine configurezi site-ul.',
  [('cpanel.html','server','cPanel','Copie de siguranță'),('wordpress.html','layers','WordPress','Temă și pagini'),('magazin.html','bag','Magazin','Produse și plată'),('email.html','mail','Email','Mesaje livrate'),('smartbill.html','receipt','SmartBill','Documente și SPV'),('lansare.html','rocket','Lansare','Verificări finale')],
  'Urmează numerele de la 01 la 06. Promovarea începe după verificarea comenzilor și a contactului.'),
 'cpanel': ('Fundația site-ului', 'Pregătești o copie de lucru protejată.', 'Acces cPanel; identificarea site-ului existent.', 'Ai backup, HTTPS și un loc sigur pentru modificări.',
  [('#conectare','key','Acces','Panoul găzduirii'),('#backup','shield','Backup','Fișiere + bază de date'),('#copie-wpt','layers','Copie de lucru','Alegi o singură rută'),('#https','lock','HTTPS','Certificat valid'),('#protectie','shield','Protecție','Acces și integrări'),('#php','server','Pregătire','PHP și încărcare')],
  'Alege 4A, 4B sau 4C, după instrumentele din contul tău. Sunt variante alternative, nu trei instalări de făcut.'),
 'wordpress': ('Structura atelierului', 'Instalezi pachetul și înveți să editezi.', 'Copie de lucru pregătită și un administrator WordPress.', 'Paginile, meniul și produsele importate pot fi previzualizate.',
  [('#acces','key','Administrator','Contul WordPress'),('#backup','shield','Copie de lucru','Înainte de schimbări'),('#pachet','box','Pachetul ZIP','Temă + modul'),('#editare','edit','Conținut','Pagini și imagini'),('#local','monitor','Exercițiu local','WordPress pe 9400')],
  'Tema controlează aspectul, modulul CR Print importă structura, iar WooCommerce administrează catalogul.'),
 'magazin': ('Comenzi online', 'Configurezi cele două variante ale navei.', 'WooCommerce activ, specificații și prețuri confirmate.', 'Poți verifica o comandă fizică, digitală și mixtă.',
  [('#setari','settings','Setări','România și RON'),('#fizic','box','Produs fizic','Stoc și colet'),('#digital','download','Produs digital','Fișier protejat'),('#plata','card','Plată','Confirmare reală'),('#operare','receipt','Comandă','Urmărești statusul')],
  'Fizicul are livrare. Digitalul are drept de descărcare. Plata, statusul și accesul trebuie verificate împreună.'),
 'email': ('Mesaje care ajung', 'Conectezi formularul și emailurile magazinului.', 'Inbox funcțional și date SMTP sau cont Brevo.', 'Primești mesajul de test, solicitarea și emailul comenzii.',
  [('#flux','edit','Formular','Clientul trimite'),('#flux','receipt','Înregistrare','Solicitări 3D'),('#smtp-concret','mail','WP Mail SMTP','Transportul mesajului'),('#dns-cpanel','shield','Autentificare','SPF și DKIM'),('#teste','check','Inbox','Verifici primirea')],
  'Salvarea solicitării și livrarea emailului sunt rezultate separate. „Trimis” în aplicație nu dovedește primirea în inbox.'),
 'smartbill': ('Facturi, fără confuzii', 'Legi comenzile de documentele firmei.', 'Cont SmartBill, contabil și abonament verificat.', 'Ai un flux de facturare verificat, apoi îl poți automatiza.',
  [('#abonament','key','Eligibilitate','Abonament și acces'),('#date-firma','settings','Datele firmei','Serii și fiscalitate'),('#manual','receipt','Prima factură','Flux manual'),('#plugin','layers','Integrare','API, dacă este inclus'),('#ciorne','check','Verificare','Ciornă și totaluri'),('#efactura','shield','SPV','Conectare separată')],
  'Factura, încasarea și transmiterea în SPV au verificări distincte. Nu le considera confirmate printr-un singur status WooCommerce.'),
 'promovare': ('Buget folosit cu sens', 'Alegi o ofertă și un singur test plătit.', 'Site funcțional, marjă calculată; 300–600 lei/lună.', 'Ai o ofertă clară și urmărești cererile care devin comenzi.',
  [('#alegere-oferta','box','Oferta','Un serviciu clar'),('#prioritate','target','Canalul','Un test concentrat'),('#masurare','chart','Măsurare','Cereri și cost'),('#plan','calendar','Rutină','Răspuns și oferte')],
  'Acesta este un plan propus pentru CR Print. Rezultatele se decid din solicitări calificate, comenzi și marjă, nu din aprecieri.'),
 'google': ('Cereri din căutare', 'Lansezi o campanie Search restrânsă.', 'Cont Google Ads, pagină FDM și măsurare verificată.', 'Poți urmări căutarea, solicitarea și costul ei.',
  [('#pregatire','key','Cont','RON și facturare'),('#contact-event','chart','Conversie','Solicitare înregistrată'),('#campanie','target','Căutare','Zona servită'),('#keywords','search','Cuvinte','Intenție relevantă'),('#anunt','edit','Reclamă','Aceeași ofertă'),('#rutina','check','Optimizare','Cost și calitate')],
  'Lanțul urmărit: căutare → reclamă → pagină relevantă → solicitare validă → ofertă. Un clic nu este o vânzare.'),
 'meta': ('Facebook și Instagram', 'Testezi o ofertă vizuală cu formular.', 'Pagina firmei, acces publicitar și politica de confidențialitate.', 'Primești solicitări și le califici înainte de ofertare.',
  [('#cont','key','Conturile','Accesul firmei'),('#creativ','monitor','Materialul','Obiect și proces'),('#campanie','target','Campania','Solicitări'),('#meta-click','edit','Formularul','Întrebări utile'),('#pixel','chart','Rezultatele','Cost și comenzi')],
  'Formularul instantaneu rămâne în Meta. Dacă trimiți spre site, configurarea pixelului și consimțământul sunt o etapă suplimentară.'),
 'tiktok': ('Procesul în imagini', 'Începi cu videoclipuri organice.', 'Telefon, obiecte reale și timp pentru răspunsuri.', 'Ai materiale de proces și poți evalua interesul real.',
  [('#buget','chart','Buget','Verifici pragurile'),('#organic','calendar','Plan organic','Ritm realist'),('#idei','box','Subiecte','Obiecte și explicații'),('#tiktok-click','monitor','Publicare','Clipuri verticale'),('#tiktok-ads-click','target','Reclame','Doar cu buget separat')],
  'La bugetul tău, propunerea este conținut organic pe TikTok și un singur alt canal plătit. Pragurile Ads Manager sunt explicate separat.'),
 'lansare': ('Ultima verificare', 'Treci de la copia de lucru la site-ul public.', 'Magazin, email și facturare deja verificate.', 'Publici după o listă de verificări și păstrezi o rutină.',
  [('#seo','search','Găsire','URL-uri și informații'),('#performanta','chart','Performanță','Mobil și încărcare'),('#aria','check','Accesibilitate','Tastatură și contrast'),('#legal','receipt','Documente','Date comerciale'),('#checklist','shield','Control final','Listă bifabilă'),('#publicare-click','rocket','Publicare','Copie → site public')],
  'Publicarea nu trebuie să suprascrie comenzile noi. Confirmă procedura de transfer cu gazda înainte de apăsarea butonului.'),
 'depanare': ('Când ceva nu merge', 'Identifici cauza înainte să schimbi setări.', 'URL, mesaj de eroare și acces la mediul afectat.', 'Poți face o verificare simplă sau cere ajutor concret.',
  [('#probleme','search','Simptom','Ce vezi exact'),('#erori-concrete','layers','Mediul','4173, 9400 sau găzduire'),('#erori-concrete','settings','Verificare','Un pas pe rând'),('#ajutor','mail','Ajutor','Pași și eroare'),('#fisiere','box','Fișiere','Locul potrivit')],
  'Aceeași eroare poate avea cauze diferite local și în WordPress. Identifică mediul, apoi verifică o singură componentă.'),
}

AUDIT = {
 'index': ('Instrumentele de bază au variante gratuite; serviciile de găzduire, email și plăți au condiții separate.', 'Prețurile de hosting și cifrele calculatorului sunt repere de planificare, nu oferte sau rezultate promise.', 'Furnizorul, planul SmartBill și prețurile reale ale navei trebuie confirmate.'),
 'cpanel': ('Backupul complet cPanel nu se restaurează din aceeași interfață; restaurarea completă ține de gazdă/WHM.', 'WP Toolkit, Softaculous, AutoSSL și versiunile PHP disponibile depind de configurația gazdei.', 'Procedura exactă de clonare și restaurare trebuie confirmată în contul tău.'),
 'wordpress': ('Instalarea temei prin ZIP și reviziile editorului sunt documentate de WordPress. Pachetul CR Print este specific acestui proiect.', 'Cerințele WooCommerce și compatibilitatea pluginurilor se verifică pentru versiunile instalate.', 'Editarea paginilor importate folosește momentan HTML personalizat; nu este un constructor vizual complet.'),
 'magazin': ('Virtual și Descărcabil au roluri diferite. Accesul în Procesare depinde de opțiunea de acordare după plată.', 'Metoda protejată de descărcare trebuie susținută de server; redirecționarea nesigură expune URL-ul.', 'Transportul, taxele, licența, prețul și confirmarea plății rămân de configurat pentru firmă.'),
 'email': ('WP Mail SMTP Lite include Other SMTP și Brevo. Brevo Free publică 300 de trimiteri pe zi la data consultării.', 'SPF/DKIM se configurează la DNS-ul autoritativ. Valorile SMTP se iau din cont, nu se presupun.', 'Am verificat documentația; livrarea reală la hi@crprint.ro se confirmă printr-un test pe găzduirea ta.'),
 'smartbill': ('Integrarea oficială indică abonamente eligibile. Facturarea, încasarea și autorizarea SPV sunt fluxuri separate.', 'Compatibilitatea declarată în pagina pluginului nu certifică automat combinația ta de versiuni.', 'Abonamentul și datele fiscale nu sunt presupuse. Începe manual dacă integrarea nu este inclusă.'),
 'promovare': ('Google Business Profile are un flux oficial de revendicare și verificare. Eligibilitatea firmei se verifică separat.', 'Bugetele, publicul și ritmul postărilor de aici sunt propuneri pentru atelier, nu reguli ale platformelor.', 'Nu am inventat costuri pe clic sau volume locale. Folosește estimările contului și rezultatele proprii.'),
 'google': ('Bugetul mediu zilnic nu este un plafon zilnic rigid. Importul din Analytics cere conturi conectate și eveniment configurat.', 'Site Kit nu conectează automat formularul CR Print; există un eveniment separat, explicat în acest capitol.', 'Numele unor meniuri diferă după limbă și interfață. Confirmă etichetele și consimțământul în Tag Assistant.'),
 'meta': ('Integrarea WooCommerce și codul oficial Meta documentează evenimentele și identificatorul comun pentru deduplicare.', 'Paginile publice Meta despre formulare și Reels au redirecționat la autentificare. Nu am putut verifica automat ecranele din cont.', 'Pașii Ads Manager sunt orientativi; verifică opțiunile efective înainte de publicare. Un formular primit nu este o comandă.'),
 'tiktok': ('Documentația TikTok actualizată în iulie 2026 indică bugetele minime și biblioteca muzicală comercială.', 'Pragurile Ads Manager sunt în USD în documentație. Moneda și disponibilitatea opțiunilor se verifică în cont.', 'Planul organic este o propunere pentru bugetul tău; nu garantează vizualizări sau vânzări.'),
 'lansare': ('Documentația Google descrie datele structurate, iar Your Europe explică informarea consumatorilor și retragerea.', 'WCAG oferă cerințe verificabile; o listă bifată și atributele ARIA nu certifică singure conformitatea.', 'Obligațiile fiscale și documentele firmei se stabilesc pentru situația reală. Nu sunt incluse cote sau termene fiscale presupuse.'),
 'depanare': ('Pașii locali corespund lansatoarelor din proiect. Configurările SMTP, WooCommerce și cPanel se raportează la documentația oficială.', 'Un răspuns de succes al aplicației nu certifică livrarea emailului, încasarea sau transmiterea în SPV.', 'Verifică întâi mediul și versiunile. Accesul în contul gazdei și al firmei nu a fost folosit pentru acest audit.'),
}

ICONS = {
 'server':'<rect x="4" y="4" width="16" height="6" rx="2"/><rect x="4" y="14" width="16" height="6" rx="2"/><path d="M7 7h.01M7 17h.01M11 7h6M11 17h6"/>',
 'layers':'<path d="m12 3 9 5-9 5-9-5 9-5ZM3 12l9 5 9-5M3 16l9 5 9-5"/>',
 'bag':'<path d="M5 7h14l1 14H4L5 7ZM8 7V5a4 4 0 0 1 8 0v2"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 7 9 6 9-6"/>',
 'receipt':'<path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3ZM9 7h6M9 11h6M9 15h3"/>',
 'rocket':'<path d="M9 15c-3-3 1-10 11-11 0 9-7 14-11 11ZM9 10H5l-3 5h7M14 15v4l-5 3v-7M5 19l-2 2"/><circle cx="16" cy="8" r="1.5"/>',
 'key':'<circle cx="8" cy="9" r="5"/><path d="m12 13 8 8 2-2-3-3 2-2-3-3"/>',
 'shield':'<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
 'lock':'<rect x="5" y="10" width="14" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',
 'box':'<path d="m12 3 9 5v9l-9 5-9-5V8l9-5ZM3 8l9 5 9-5M12 13v9M7.5 5.5l9 5"/>',
 'edit':'<path d="m15 4 5 5-11 11H4v-5L15 4ZM12 7l5 5M4 4h5M4 8h2"/>',
 'monitor':'<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M12 17v4M8 21h8m-6-13 5 3-5 3V8Z"/>',
 'settings':'<path d="M5 3v18M12 3v18M19 3v18M2 7h6M9 16h6M16 9h6"/>',
 'download':'<path d="M12 3v12m-5-5 5 5 5-5M4 15v6h16v-6"/>',
 'card':'<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 10h20M6 15h4"/>',
 'check':'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
 'target':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 'chart':'<path d="M4 3v18h17M8 17v-6M13 17V7M18 17V4"/>',
 'calendar':'<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4M17 3v4M3 11h18M7 15h2M13 15h4"/>',
 'search':'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
}

def icon(name):
    return '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS.get(name,ICONS['check'])+'</svg>'

def diagram(key, content):
    nodes = META[key][4]
    # A target can be removed or renamed during an editorial update. Do not emit a broken link.
    ids = set(re.findall(r'id="([^"]+)"',content))
    items = []
    for i,(href,symbol,title,desc) in enumerate(nodes,1):
        tag='a' if not href.startswith('#') or href[1:] in ids else 'div'
        link=' href="'+html.escape(href)+'"' if tag=='a' else ''
        items.append(f'<li><{tag}{link}><span class="flow-icon">{icon(symbol)}</span><span class="flow-number">{i:02}</span><strong>{html.escape(title)}</strong><span class="flow-desc">{html.escape(desc)}</span></{tag}></li>')
    return '<figure class="flow-map"><figcaption><span class="eyebrow">HARTA CAPITOLULUI</span><h2>Vezi întâi cum se leagă lucrurile.</h2></figcaption><ol>'+''.join(items)+'</ol><p class="flow-caption">'+META[key][5]+'</p></figure>'

def summary(key):
    _, goal, needs, result, *_ = META[key]
    return '<dl class="chapter-brief">'+''.join('<div><dt>'+icon(symbol)+label+'</dt><dd>'+html.escape(text)+'</dd></div>' for label,symbol,text in [('Scop','target',goal),('Ai nevoie de','key',needs),('La final','check',result)])+'</dl>'

def audit_panel(key,content):
    sources=[]
    seen=set()
    for url,title in re.findall(r'<p class="source">.*?<a href="([^"]+)"[^>]*>(.*?)</a>',content):
        if url in seen:continue
        seen.add(url)
        label=re.sub('<[^>]+>','',title).replace(' ↗','')
        blocked='facebook.com/business/ads/' in url
        extra='<small>Redirecționează la autentificare; conținut neconsultat automat.</small>' if blocked else ''
        sources.append('<li><a href="'+html.escape(url)+'" target="_blank" rel="noopener">'+html.escape(label)+' <span aria-hidden="true">↗</span></a>'+extra+'</li>')
    facts,variable,limit=AUDIT[key]
    items=''.join('<li><strong>'+title+'</strong><span>'+html.escape(text)+'</span></li>' for title,text in [('Documentat',facts),('Depinde de configurare',variable),('De confirmat pentru tine',limit)])
    return '<details class="audit-panel" id="surse"><summary>'+icon('shield')+'<span><strong>Surse și verificări</strong><small>Consultate la '+DATE+' · inclusiv limitele verificării</small></span><span class="detail-plus" aria-hidden="true">+</span></summary><div class="audit-body"><ul class="audit-notes">'+items+'</ul><p>Diagramele explică fluxul propus pentru CR Print; nu sunt capturi ale interfețelor. Exemplele de buget și campanii sunt recomandări de lucru, separate de regulile documentate.</p><ol class="source-list">'+''.join(sources)+'</ol></div></details>'

def readable_sections(content):
    count=0
    def wrap(match):
        nonlocal count
        count+=1
        ident,title,body=match.groups()
        return f'<section class="chapter-block" id="{ident}"><details class="section-panel" open><summary><span class="section-number">{count:02}</span><h2>{title}</h2><span class="detail-plus" aria-hidden="true">+</span></summary><div class="section-body">{body}</div></details></section>'
    return re.sub(r'<section class="chapter-block" id="([^"]+)"><h2>(.*?)</h2>(.*?)</section>',wrap,content,flags=re.S)

def branch(title, root, left, right, caption):
    return '<figure class="branch-map"><figcaption>'+html.escape(title)+'</figcaption><div class="branch-root">'+icon('receipt')+root+'</div><div class="branch-lanes">'+''.join('<div><span>'+icon(symbol)+'</span><h3>'+heading+'</h3><p>'+body+'</p></div>' for symbol,heading,body in [left,right])+'</div><p class="flow-caption">'+caption+'</p></figure>'

def audit_content(P,block,steps,note,source):
    def replace(key,old,new):
        a,b,c=P[key]
        if old not in c:raise ValueError('Missing audited text in '+key+': '+old[:50])
        P[key]=(a,b,c.replace(old,new))
    def append(key,ident,extra):
        a,b,c=P[key]
        pattern=r'(<section class="chapter-block" id="'+ident+r'">.*?)(</section>)'
        c,count=re.subn(pattern,lambda m:m[1]+extra+m[2],c,flags=re.S)
        if count!=1:raise ValueError('Missing audited section '+key+'/'+ident)
        P[key]=(a,b,c)

    replace('email','La verificarea din 2 octombrie 2026','La verificarea din 5 octombrie 2026')
    replace('google','Purchase se trimite din confirmarea Woo, cu order ID unic, valoare și RON. Transferul neîncasat se distinge de venit încasat.',
      'Pentru Google Analytics, evenimentul <code>purchase</code> folosește <code>transaction_id</code> unic, valoare și moneda RON. Verifică momentul trimiterii în integrarea aleasă: o comandă plasată prin transfer nu dovedește încasarea.')
    replace('google','În Tags/Etichete → New/Nou alege Google Analytics: GA4 Event. Introdu ID-ul de măsurare al proprietății. Nume eveniment trimis: generate_lead. Atașează declanșatorul creat. Salvează.',
      'Verifică întâi că eticheta Google pentru proprietatea GA4 este instalată și se încarcă înaintea evenimentelor. Dacă Site Kit o instalează deja, nu mai adăuga încă o configurație care dublează <code>page_view</code>. În Tags/Etichete → New/Nou alege Google Analytics: GA4 Event, introdu ID-ul G-… și verifică asocierea cu eticheta Google. Nume eveniment: <code>generate_lead</code>. Atașează declanșatorul creat și salvează.')
    append('google','contact-event',note('La importul în Google Ads verifică legătura cu proprietatea Analytics și etichetarea automată. Conversiile create prin Analytics pot fi secundare: alege ca principală numai acțiunea validată pe care vrei să o folosești pentru licitare. Nu importa aceeași solicitare de două ori.')+source('Google — importul evenimentelor Analytics','https://support.google.com/google-ads/answer/2375435?hl=ro'))
    append('google','pregatire',source('Google Analytics — purchase, transaction_id și moneda','https://developers.google.com/analytics/devguides/collection/ga4/ecommerce'))
    replace('meta','Testează PageView, Lead valid și Purchase cu order ID unic.',
      'Testează PageView, Lead valid și Purchase. Pentru aceeași cumpărare trimisă prin browser și server verifică același <code>event_name</code> și identificatorul comun <code>event_id</code> în ambele fluxuri; simpla prezență a unui <code>order_id</code> în date nu confirmă deduplicarea.')
    replace('meta',source('Meta — ghid Lead Generation','https://about.fb.com/ltam/wp-content/uploads/sites/14/2023/11/LeadGenerationGuide.pdf'),
      '<p class="note">Setările campaniei de mai sus sunt un traseu orientativ. Paginile Meta cu detalii despre formulare solicită autentificare; verifică opțiunile și previzualizarea disponibile în contul tău.</p>')
    append('meta','pixel',source('Meta — identificatorul comun browser/server în codul oficial','https://github.com/facebook/facebook-for-woocommerce/blob/main/facebook-commerce-events-tracker.php'))
    append('magazin','digital',note('În WooCommerce → Setări → Produse → Produse descărcabile, opțiunea <strong>Grant access to downloadable products after payment</strong> acordă acces și când comanda este în <strong>Procesare</strong>. Fără ea, accesul se acordă în <strong>Finalizată</strong>. O comandă compusă numai din produse Virtual + Descărcabil poate fi finalizată automat după confirmarea plății. Verifică separat coșul mixt și metoda de plată.')+
      branch('Două produse, două moduri de livrare','Comanda pentru nava „24 Septembrie”',
        ('box','Machetă fizică','Produs fizic → colet → metodă de transport → livrare.'),
        ('download','Model digital','Virtual + Descărcabil → plată confirmată → permisiune → fișier.'),
        'Pentru coșul mixt verifici transportul machetei și accesul digital în aceeași comandă. Nu folosi rambursul pentru o comandă doar digitală.'))
    append('smartbill','rol',branch('Trei verificări separate','Comanda WooCommerce',
      ('receipt','Documentul','WooCommerce → SmartBill → factură. Transmiterea în SPV se verifică separat.'),
      ('card','Banii','Bancă / procesator / curier → confirmare → înregistrarea încasării.'),
      'O factură emisă nu înseamnă automat bani încasați. Emailul cu PDF și confirmarea SPV nu sunt același rezultat.'))
    append('tiktok','organic',source('TikTok — biblioteca muzicală comercială','https://ads.tiktok.com/resources/help/article/how-to-use-the-commercial-music-library?lang=en'))
    append('tiktok','tiktok-ads-click',source('TikTok — autorizarea contului pentru Spark Ads','https://ads.tiktok.com/resources/help/article/how-to-request-tiktok-account-ad-delivery-permissions-in-business-center?lang=en'))
    # Use the current canonical URL returned by TikTok, retaining the original chapter text.
    a,b,c=P['tiktok'];P['tiktok']=(a,b,c.replace('https://ads.tiktok.com/help/article/budget?lang=en','https://ads.tiktok.com/resources/help/article/budget?lang=en'))
    append('lansare','aria',note('Repere WCAG 2.2: text obișnuit cu contrast de cel puțin <strong>4,5:1</strong>, text mare <strong>3:1</strong>, operare de la tastatură și rearanjare la o lățime echivalentă de <strong>320 pixeli CSS</strong>, cu excepțiile standardului. Zoomul la 200% este o verificare suplimentară, nu înlocuiește verificarea rearanjării.')+source('W3C — WCAG 2.2','https://www.w3.org/TR/WCAG22/'))
    append('lansare','legal',note('Pentru conținut digital plătit livrat imediat, verifică înainte de acces: acordul expres pentru începerea furnizării, confirmarea că persoana înțelege pierderea dreptului de retragere și confirmarea contractului pe un suport durabil. Bifa generală de acceptare a termenilor nu rezolvă singură aceste cerințe. Macheta standard și produsul personalizat au situații diferite.')+source('Comisia Europeană — interpretarea drepturilor consumatorilor, articolul 16(m)','https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A52021XC1229%2804%29'))
    append('wordpress','acces',source('WooCommerce — cerințe actuale de server','https://woocommerce.com/document/server-requirements/'))
    append('index','calculator',source('Google Ads — buget mediu zilnic și limita lunară','https://support.google.com/google-ads/answer/6385083?hl=en-GB'))
    append('depanare','erori-concrete',source('WordPress Playground — lansatorul CLI oficial','https://developer.wordpress.org/playground/developers/local-development/wp-playground-cli/')+source('WP Mail SMTP — configurare și testare SMTP','https://wpmailsmtp.com/docs/how-to-set-up-the-other-smtp-mailer-in-wp-mail-smtp/')+source('WooCommerce — permisiunile descărcărilor','https://woocommerce.com/document/digital-downloadable-product-handling/'))
    for key,(title,subtitle,content) in list(P.items()):
        # Improve Romanian labels while preserving exact vendor menu names where useful.
        content=content.replace('pot produce leaduri','pot produce solicitări').replace('video-ul','videoclipul').replace('keywords ↗','cuvintelor cheie ↗').replace('Checklist pentru','Listă de verificare pentru')
        P[key]=(title,subtitle,content)
