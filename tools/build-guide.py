from pathlib import Path
import json,re,html
root=Path(__file__).resolve().parents[1];out=root/'ghid';out.mkdir(exist_ok=True)
def note(t):return '<aside class="note">'+t+'</aside>'
def steps(xs):return '<ol class="steps">'+''.join('<li>'+x+'</li>' for x in xs)+'</ol>'
def source(t,u):return '<p class="source">Sursă oficială: <a href="'+u+'" target="_blank" rel="noopener">'+t+' ↗</a></p>'
def block(i,t,b):return '<section class="chapter-block" id="'+i+'"><h2>'+t+'</h2>'+b+'</section>'
P={}
P['index']=('Harta de lansare','Un atelier online, construit în ordinea potrivită.',
'''<div class="roadmap"><a href="wordpress.html"><b>01</b><strong>Pregătește WordPress</strong><span>Acces, copie de lucru, temă și import.</span></a><a href="magazin.html"><b>02</b><strong>Configurează magazinul</strong><span>Produse, livrare, plată și comenzi.</span></a><a href="email.html"><b>03</b><strong>Activează emailurile</strong><span>WP Mail SMTP și teste reale.</span></a><a href="lansare.html"><b>04</b><strong>Verifică și lansează</strong><span>SEO, accesibilitate și documente.</span></a><a href="promovare.html"><b>05</b><strong>Promovează cu buget mic</strong><span>O campanie, o ofertă, rezultate urmărite.</span></a></div>'''+
block('situatia','De unde pornim',note('<strong>CR Print 3D · Constanța</strong><br>Vei vinde macheta fizică și modelul digital al navei „24 Septembrie”. Buget media: 300–600 lei/lună. Găzduirea nu este identificată încă, WooCommerce nu este activat. 149/49 lei și curierul 19 lei sunt exemple demo, nu prețuri confirmate.')+
'''<p>Nu cumpăra încă alte abonamente. Află ce ai deja și fă o copie de lucru a site-ului existent. Acest ghid este un site separat, fără indexare publică.</p><div class="comparison"><div><h3>Demo rapid · 4173</h3><p>Design, coș, comenzi și administrare locală. Fără încasări sau email trimis.</p><a href="../admin.html">Administrare demo ↗</a></div><div><h3>WordPress local · 9400</h3><p>Tema, WooCommerce și WP Mail SMTP într-un mediu de exercițiu. Produsele și comenzile folosesc WordPress.</p><a href="http://127.0.0.1:9400/wp-admin/">Panoul WordPress ↗</a></div></div>''')+
block('costuri','Un start fără abonamente inutile','''<div class="table-wrap"><table><thead><tr><th>Componentă</th><th>Alegere inițială</th><th>Cost</th></tr></thead><tbody><tr><td>WordPress & tema</td><td>CR Print Studio din proiect</td><td>Fără abonament pentru cod</td></tr><tr><td>WooCommerce</td><td>Pluginul de bază</td><td>Gratuit; extensiile sunt separate</td></tr><tr><td>WP Mail SMTP</td><td>Lite</td><td>Gratuit; serviciul email este separat</td></tr><tr><td>Hosting, domeniu, inbox</td><td>Verifică contractul actual</td><td>În funcție de furnizor și reînnoire</td></tr><tr><td>Plată manuală</td><td>Transfer; ramburs pentru fizic</td><td>Funcțiile Woo sunt gratuite; banca/curierul pot taxa</td></tr><tr><td>Reclame</td><td>Un test concentrat</td><td>300–600 lei/lună, separat de hosting</td></tr></tbody></table></div><p>Ca plafon de planificare, poți căuta hosting în jur de 30–60 lei/lună. Este un reper de buget, nu o ofertă verificată; nu include automat domeniul, TVA sau emailul. Compară prețul la reînnoire, backupul, suportul și resursele. Dacă hostingul actual funcționează bine, nu este obligatoriu să îl schimbi.</p>'''+source('WooCommerce','https://wordpress.org/plugins/woocommerce/')+source('WP Mail SMTP','https://wordpress.org/plugins/wp-mail-smtp/'))+
block('calculator','Calculator pentru buget și profit','''<form class="calculator" id="budget-calculator"><div><label for="budget">Buget lunar reclame (lei)</label><input id="budget" type="number" min="0" value="450"></div><div><label for="revenue">Venit/comandă fără TVA (lei)</label><input id="revenue" type="number" min="1" value="149"></div><div><label for="cost">Cost variabil total (lei)</label><input id="cost" type="number" min="0" value="75"></div><div><label for="profit">Profit dorit după reclamă (lei)</label><input id="profit" type="number" min="0" value="30"></div><div><label for="close">Leaduri care cumpără (%)</label><input id="close" type="number" min="1" max="100" value="25"></div><output id="calculator-result" aria-live="polite"></output></form><p>Include material, muncă, energie, pierderi, ambalare, comisioane și transportul suportat de tine. Calculatorul arată limite economice orientative; nu prezice vânzări. Prețurile exemplelor sunt demo.</p>''')+
block('glosar','Cuvinte pe care le vei întâlni','''<dl><dt>Temă</dt><dd>Aspectul și structura paginilor: CR Print Studio.</dd><dt>Plugin</dt><dd>Funcție suplimentară: WooCommerce gestionează magazinul; WP Mail SMTP transportă emailuri.</dd><dt>Staging</dt><dd>Copie de lucru separată de site-ul public.</dd><dt>DNS</dt><dd>Setările domeniului pentru site și email. Valorile se copiază din furnizor, nu se ghicesc.</dd><dt>Lead calificat</dt><dd>Solicitare pentru ceva ce poți livra profitabil.</dd><dt>CPL / CPA</dt><dd>Cost pe solicitare / cost pe comandă.</dd></dl>'''))

P['wordpress']=('WordPress de la zero','Acces, copie de lucru, instalare și import fără să pierzi site-ul existent.',
block('acces','1. Identifică găzduirea și accesul',steps([
'Caută în email facturile pentru „crprint.ro”, „hosting”, „cPanel”, „Plesk” și „WordPress”. Furnizorul domeniului poate fi diferit de gazda serverului.',
'Deschide <strong>crprint.ro/wp-admin/</strong> și conectează-te cu un administrator. Dacă nu ai acces, folosește recuperarea contului sau cere datele persoanei care a configurat site-ul.',
'În <strong>Instrumente → Sănătatea site-ului → Informații → Server</strong>, notează WordPress/PHP. Această pagină nu identifică întotdeauna firma de hosting.',
'Cere gazdei: panou, backup complet, staging, HTTPS, PHP suportat, memorie, DNS și inbox hi@crprint.ro. Nu publica parole sau chei în GitHub.',
'Pentru pachet, folosește PHP 8.3 sau mai nou suportat de pluginurile tale. Verifică cerințele actuale WooCommerce înainte de instalare.'
])+source('WordPress — ecranele de administrare','https://wordpress.org/documentation/article/administration-screens/')+source('WooCommerce — cerințe','https://wordpress.org/plugins/woocommerce/'))+
block('backup','2. Backup și staging',steps([
'Creează din hosting un backup cu <strong>fișiere și baza de date</strong>. Instrumente → Export din WordPress nu este un backup complet.',
'Descarcă o copie și notează procedura de restaurare. Cere gazdei să confirme cum recuperezi site-ul, nu doar că există backup.',
'Creează staging din panoul gazdei sau cere o copie pe un subdomeniu de lucru. Poți exersa și în WordPress Playground local.',
'În staging activează <strong>Setări → Citire → Descurajează motoarele de căutare</strong> și protejează copia prin autentificare de la hosting. Noindex nu protejează datele.',
'Separă emailurile și plățile de test. Nu copia comenzi fictive în baza live.'
]))+
block('pachet','3. Instalează tema, pluginul și structura',note('<a href="../wordpress/crprint-studio.zip" download><strong>crprint-studio.zip</strong> — tema ↓</a><br><a href="../wordpress/crprint-core.zip" download><strong>crprint-core.zip</strong> — formular și import ↓</a>')+steps([
'În staging: <strong>Aspect → Teme → Adaugă → Încarcă temă</strong>. Alege crprint-studio.zip, instalează și activează. Nu încărca tot repositoryul ca temă.',
'<strong>Module/Pluginuri → Adaugă → Încarcă modul</strong>: alege crprint-core.zip și activează.',
'Caută WooCommerce (Automattic) și WP Mail SMTP (WPForms) în directorul de pluginuri. Instalează și activează versiunile oficiale. Pro nu este necesar pentru configurația de bază.',
'Parcurge setările Woo: adresa reală, România și RON. Activează doar funcțiile necesare. Regimul TVA se stabilește cu contabilul.',
'<strong>Instrumente → CR Print — configurare → Creează pagini și produse în ciornă</strong>. Importul păstrează conținutul existent; nu încarcă fișierul digital comercial.',
'În <strong>Pagini → Toate paginile</strong>, verifică noile ciorne și previzualizarea. Un slug deja folosit poate produce o pagină nouă cu prefix crprint-. Publică numai paginile corecte.',
'<strong>Setări → Citire</strong>: alege o pagină statică și noua pagină Acasă. Nu selecta pagina veche care conține alt builder.',
'<strong>Aspect → Meniuri</strong>: verifică CR Print principal, poziția Navigare principală și linkurile. Actualizează meniul dacă schimbi URL-uri.',
'<strong>Setări → Legături permanente</strong>: alege URL-uri lizibile și salvează. Păstrează adresele vechi sau creează 301 spre echivalente.',
'Configurează produsele, SMTP și documentele. Nu publica prețurile demo sau paginile juridice demonstrative.'
])+source('WordPress — încărcarea unei teme','https://wordpress.org/documentation/article/appearance-themes-screen/'))+
block('editare','4. Cum editezi după import',steps([
'<strong>Produse → Toate produsele → Editează</strong>: preț, stoc, descriere, galerie, fișiere. În WordPress nu edita shop.js pentru catalog.',
'<strong>Pagini → pagina dorită → Editează</strong>: layoutul importat este într-un bloc HTML personalizat. Schimbă textul dintre etichete și verifică Previzualizare înainte de Actualizează.',
'Pentru pagini noi simple poți folosi blocurile native. Eliminarea întregului bloc HTML al unei pagini importate elimină layoutul special.',
'Pentru imagini de pagină, încarcă în Media și înlocuiește src. Actualizează/elimină srcset dacă imaginea se schimbă și păstrează alt descriptiv. Imaginile produselor se editează direct în Woo.',
'Logo-ul, headerul, footerul și stilurile comune sunt în temă. Pentru schimbări globale, folosește o nouă versiune a temei sau o temă copil, cu backup.',
'Nu este necesar un builder plătit. Editare vizuală completă pentru toate componentele poate fi o etapă separată prin blocuri WordPress dedicate.'
]))+
block('local','5. WordPress local, pentru exercițiu',steps([
'Demo rapid: terminal în folderul proiectului, <code>node dev-server.mjs</code>, apoi portul 4173 și /admin.html. Nu necesită baze de date.',
'Pentru WordPress real local, folosește Node.js ≥24.18 din sursa oficială. Dublu-click pe <code>Start-WordPress.cmd</code> din proiect. La prima pornire se descarcă WordPress și pluginurile oficiale. Lasă fereastra deschisă.',
'Deschide <strong>http://127.0.0.1:9400/wp-admin/</strong>. Produsele și comenzile folosesc WooCommerce. Nu expune acest mediu ca server public.',
'Configurația Playground publică exemple doar local și dezactivează indexarea. Plata este DEMO: nu trimite bani. Emailurile externe sunt oprite. Produsele, comenzile și paginile se păstrează în <code>%LOCALAPPDATA%/CRPrint/wordpress-demo</code>. Fă backup și exportă schimbările utile.',
'În producție instalează ZIP-urile pe staging și configurează separat setările reale. Nu importa comenzile de test.'
])+'''<pre><code>powershell -NoProfile -ExecutionPolicy Bypass -File ./Start-WordPress.ps1</code></pre>'''+source('WordPress Playground — CLI oficial','https://developer.wordpress.org/playground/developers/local-development/wp-playground-cli/')))

P['magazin']=('Magazinul WooCommerce','Produse fizice și digitale, transport, plată și administrarea comenzilor.',
block('setari','1. Setările de bază',steps([
'<strong>WooCommerce → Setări → General</strong>: adresa firmei, România, moneda RON. Decide cu contabilul taxele și dacă prețurile includ TVA.',
'<strong>Avansat → Configurare pagini</strong>: Magazin, Coș, Checkout și Contul meu. Designul este optimizat pentru coduri scurte (shortcodes) <code>[woocommerce_cart]</code> și <code>[woocommerce_checkout]</code>; introdu-le în paginile corespunzătoare dacă folosești varianta clasică.',
'<strong>Conturi și confidențialitate</strong>: permite cumpărarea fără cont dacă nu ai un motiv să-l impui; configurează păstrarea datelor.',
'Completează termenii și confidențialitatea reale și selectează paginile în setări. Textele demo trebuie înlocuite.',
'La Emailuri verifică „Comandă nouă”, destinatarul și expeditorul. Transportul emailurilor se configurează în WP Mail SMTP.'
])+source('WooCommerce — configurare','https://woocommerce.com/document/woocommerce-setup-wizard/'))+
block('fizic','2. Nava printată: configurează produsul',steps([
'Editează produsul importat în ciornă, tip <strong>Produs simplu</strong>. Pentru fizic, nu bifa Virtual/Descărcabil.',
'Confirmă scara, dimensiunile, materialul, timpul de producție și finisajul. 149 lei este demo. Calculează material, muncă, pierderi, ambalaj și taxe.',
'Descriere scurtă: utilizare și dimensiuni. Descriere lungă: material, finisaj, ce include coletul, termen și îngrijire.',
'Inventar: păstrează SKU nava-24-septembrie pentru legătura cu viewerul. Setează stoc real sau termen clar de producție la comandă. Stocul 20 este demo.',
'Livrare: adaugă greutatea și dimensiunile coletului. Nu confunda dimensiunile modelului cu ambalajul.',
'Încarcă imaginea și galeria. Randările provin din FBX; completează cu fotografii ale machetei fabricate înainte de vânzare.',
'Dacă ai scări/culori cu preț sau stoc diferit, folosește produs variabil. La început, o variantă clară este mai simplu de administrat.',
'Verifică pe telefon și publică după confirmarea specificațiilor și prețului. Pagina principală citește produsele publicate în Woo.'
]))+
block('digital','3. Fișierul digital FBX',steps([
'Editează produsul digital: bifează <strong>Virtual</strong> și <strong>Descărcabil</strong>. Păstrează SKU nava-24-septembrie-digital.',
'Creează ZIP cu FBX complet și LICENTA.txt. Definește utilizarea, modificarea, revânzarea și distribuția. Verifică drepturile asupra modelului.',
'Încarcă ZIP-ul la „Fișiere descărcabile” din formularul produsului. Nu folosi URL-ul public al FBX-ului demo/GitHub drept fișier comercial.',
'<strong>Setări → Produse → Produse descărcabile</strong>: alege Force Downloads sau X-Accel/X-Sendfile dacă hostingul îl suportă. Evită fallbackul de redirect nesigur.',
'Stabilește limita/expirarea conform licenței. Livrarea digitală se face după plată confirmată; o comandă cu transfer bancar neîncasat nu trebuie tratată ca plătită.',
'Tema include GLB simplificat public. Orice model încărcat în browser poate fi extras, deci previewul nu trebuie să fie fișierul complet vândut.',
'Verifică neautentificat că URL-ul direct al arhivei plătite nu este accesibil. Apoi testează descărcarea din comanda plătită/test și Contul meu.',
'Implementează informările și acordurile pentru livrare digitală și retragere. Checkboxul demonstrativ nu acoperă cerințele comerciale finale.'
])+source('Woo — virtual/descărcabil','https://woocommerce.com/document/managing-products/virtual-downloadable/')+source('Woo — protecția descărcărilor','https://woocommerce.com/document/digital-downloadable-product-handling/'))+
block('plata','4. Livrare și plată cu costuri mici',steps([
'<strong>Livrare → Zone</strong>: România, tarif fix după oferta curierului și ridicare locală din atelier. 19 lei este demo, nu cotație.',
'Testează coș fizic, digital și mixt. Digitalul singur nu trebuie să ceară transport. Comunică separat producția și timpul curierului.',
'<strong>Plăți → Plăți offline → Transfer bancar</strong>: IBAN-ul firmei, beneficiar, instrucțiuni cu numărul comenzii. Verifică încasarea înainte de procesare.',
'Rambursul este o opțiune pentru fizic dacă ai contract și accepți costurile/refuzurile. Restricționează la transporturi eligibile și nu permite pentru exclusiv virtual.',
'Pentru digitale poți porni cu transfer și validare manuală. Pentru plată online ulterioară compară comision, contract, decontare și rambursări la furnizori disponibili în România.',
'Configurează facturarea, TVA și raportările cu contabilul. Nu trata setările demo ca recomandare fiscală.'
])+source('Woo — transfer bancar','https://woocommerce.com/document/bacs/')+source('Woo — ramburs','https://woocommerce.com/document/cash-on-delivery/'))+
block('operare','5. Operațiuni și import CSV',steps([
'<strong>WooCommerce → Comenzi</strong>: verifică varianta, datele, transportul și notele. „În așteptare” la transfer nu înseamnă bani încasați.',
'Confirmă încasarea, apoi procesează fizicul. Notează scara/materialul și termenul în notele interne.',
'Fă AWB manual în portalul curierului la început. Un plugin de curier plătit nu este obligatoriu.',
'Verifică emailurile și permisiunile digitale; nu marca plătit doar pentru a forța o descărcare.',
'Produse → Export/Import folosește CSV. Exportul demo din admin este UTF-8 și creează ciorne. Completează imagini și fișiere în Woo și evită duplicatele după SKU.',
'Actualizează stocul și marja reală. Comenzile fictive nu intră în rapoartele comerciale.'
])+source('Woo — import/export CSV','https://woocommerce.com/document/product-csv-importer-exporter/')))

P['email']=('Email & anti-spam','WP Mail SMTP, inbox real și verificarea livrării.',
block('flux','1. Cum circulă mesajul',note('Formular → validare pe server → salvare în Solicitări 3D → wp_mail → WP Mail SMTP → furnizor email → hi@crprint.ro.')+
'''<p>CR Print Core păstrează solicitările în WordPress pentru administratori. WP Mail SMTP este folosit și de WooCommerce. Confirmarea tehnică a trimiterii nu dovedește primirea în inbox.</p><p>Demo-ul rapid 4173 salvează local fără email. În Playground, emailurile externe sunt oprite explicit pentru exercițiu. Testele reale de livrare se fac în staging, după configurarea furnizorului.</p>''')+
block('inbox','2. Verifică adresa',steps([
'Cere gazdei să confirme că hi@crprint.ro este un inbox funcțional. Brevo sau alt serviciu de trimitere nu creează automat un inbox.',
'Trimite manual către hi@crprint.ro din altă adresă și verifică primirea și răspunsul. Rezolvă MX/inbox înainte de formular.',
'<strong>Instrumente → CR Print — configurare</strong>: destinatar hi@crprint.ro.',
'<strong>WooCommerce → Setări → Emailuri → Comandă nouă</strong>: verifică adresa operațională. Expeditorul și destinatarul sunt setări diferite.'
]))+
block('smtp','3. Inboxul hostingului prin Other SMTP',steps([
'<strong>WP Mail SMTP → Setări → General</strong>: From Email hi@crprint.ro, From Name CR Print 3D. Force From Email dacă toate mesajele site-ului trebuie să folosească această adresă.',
'Alege Other SMTP dacă gazda îl suportă. Cere server, port, criptare, utilizator și parolă/parolă de aplicație; nu copia parametri exemplu.',
'587/TLS și 465/SSL sunt combinații frecvente, dar folosește exact valorile furnizorului. Nu elimina criptarea pentru a ascunde o eroare.',
'Salvează și trimite din <strong>Instrumente → Test email</strong> către un inbox controlat.',
'Other SMTP păstrează autentificarea în configurația WordPress. Limitează administratorii și nu publica parole. Dacă ai opțiune API, poate fi mai potrivită.',
'Pentru conexiune refuzată, cere gazdei verificarea portului și autentificării. Parola greșită și portul blocat sunt probleme diferite.'
])+source('WP Mail SMTP — Other SMTP','https://wpmailsmtp.com/docs/how-to-set-up-the-other-smtp-mailer-in-wp-mail-smtp/'))+
block('brevo','4. Alternativa API: Brevo',note('La verificarea din 2 octombrie 2026, Brevo Free include până la 300 trimiteri/zi. Confirmă condițiile actuale și aprobarea contului. Mailerul Brevo de bază nu necesită WP Mail SMTP Pro.')+steps([
'Creează contul cu date reale și confirmă-l. Verifică dacă Free acoperă volumul dorit.',
'Adaugă crprint.ro în expeditori/domenii și autentifică domeniul. Copiază exact valorile DNS din cont.',
'Dacă nu știi unde se editează DNS, cere gazdei să adauge valorile. Nu schimba nameserverele întregului domeniu pentru email și nu șterge înregistrările existente. SPF/DKIM/DMARC se configurează pentru furnizorii folosiți, fără SPF duplicate.',
'Creează o cheie API dedicată. În WP Mail SMTP alege Brevo și introdu cheia în câmpul API. Nu pune cheia în JavaScript sau în GitHub.',
'Folosește expeditorul din domeniul autentificat. Testează și verifică inbox, Spam și jurnalul serviciului.'
])+source('Brevo — planuri','https://help.brevo.com/hc/en-us/articles/208589409-About-Brevo-s-pricing-plans')+source('WP Mail SMTP — Brevo','https://wpmailsmtp.com/docs/how-to-set-up-the-sendinblue-mailer-in-wp-mail-smtp/'))+
block('teste','5. Testează întregul flux',steps([
'Primește efectiv testul SMTP în două inboxuri controlate. Verifică Spam și eventualele erori de autentificare.',
'Trimite Contact, verifică Solicitări 3D și inboxul. Reply trebuie să ajungă la solicitant prin Reply-To.',
'Plasează o comandă fizică de test: notificare admin, confirmare client și email de status.',
'Testează digitalul: plată confirmată, link de descărcare, HTTPS, nume și prețuri corecte.',
'La eroare SMTP, solicitarea CR Print rămâne salvată. Verifică panoul și răspunde manual. Nu presupune că Lite păstrează jurnalul complet al tuturor emailurilor Woo.',
'Nu folosi emailul vizitatorului ca From. From este domeniul firmei; Reply-To este solicitantul.'
]))+
block('spam','6. Anti-spam și cache','''<p>Formularul are nonce, honeypot, calcul validat pe server, limită de frecvență și validarea datelor. Reduce spamul, fără garanția eliminării lui. Nu acceptă uploaduri; fișierele se pot trimite separat pe email.</p><p><strong>Exclude Contact din cache HTML</strong>, deoarece provocarea expiră. Exclude și Coș, Checkout și Contul meu. Dacă spamul crește, adaugă ulterior Turnstile verificat pe server; un checkbox decorativ nu este protecție.</p><p>Stabilește păstrarea solicitărilor și accesul la date. Nu publica exporturi cu date personale.</p>'''))

P['promovare']=('Strategie 300–600 lei','O ofertă clară, un canal plătit și rezultate urmărite.',
block('prioritate','1. Ce promovăm mai întâi',note('Propunere pentru CR Print: cereri locale de printare la comandă și prototipare. Colecția navală este o nișă care se validează separat.')+
'''<div class="table-wrap"><table><thead><tr><th>Segment</th><th>Nevoie</th><th>Ofertă</th></tr></thead><tbody><tr><td>Firme mici / ateliere</td><td>Carcasă, suport, prototip</td><td>Analiza fișierului și estimare</td></tr><tr><td>Creatori / pasionați</td><td>Au model, nu imprimantă</td><td>FDM/SLA potrivit detaliului</td></tr><tr><td>Branduri / organizatori</td><td>Promoționale în lot mic</td><td>Mostră, apoi serie confirmată</td></tr><tr><td>Pasionați de nave</td><td>Machetă sau FBX specific</td><td>Produs cu galerie și licență clară</td></tr></tbody></table></div><p>Alege un segment pentru primul test. Modelele anatomice pot fi prezentate pentru educație; nu formula promisiuni clinice sau certificări nesusținute. Componentele trebuie promovate în utilizări pe care le poți valida.</p>''')+
block('buget','2. Concentrează bugetul',steps([
'300 lei: un singur test plătit în jur de 10 lei/zi, ținând cont de media lunară. Nu împărți suma între patru platforme.',
'450 lei: aproximativ 14–15 lei/zi pentru Search local. Celelalte canale rămân organice.',
'600 lei: aproximativ 19–20 lei/zi sau teste succesive Google/Meta. Două perioade scurte nu oferă automat comparație statistică sigură.',
'Bugetul media este separat de găzduire, materiale, taxe și timpul tău. Verifică regulile zilnice ale platformei.',
'Dacă Keyword Planner arată CPC prea mare pentru testul tău, începe organic sau testează Meta; nu forța Search doar pentru că apare primul.'
]))+
block('oferta','3. Oferta și pagina','''<p>Exemplu propriu: <strong>„Ai un model 3D? Trimite-l pentru o estimare. FDM și SLA în Constanța, cu livrare în România.”</strong> Trimite FDM la pagina FDM, SLA la SLA. Tehnologia, tariful de pornire, telefonul și formularul trebuie găsite imediat.</p><p>10 lei/oră nu este prețul total al oricărui obiect. Explică „de la”, materialul, dimensiunea și timpul. Folosește dovezi reale; imaginile generate cu IA rămân etichetate concepte.</p><p>Răspunsul de ofertare cere: scop, fișier/dimensiuni, material, cantitate, termen și livrare. Urmărește oferta până la acceptare sau refuz.</p>''')+
block('plan','4. Primele 30 de zile','''<div class="timeline"><article><b>Săptămâna 1</b><p>Specificații, prețuri, email, formular, tracking. Profil Google Business eligibil și trei exemple reale.</p></article><article><b>Săptămâna 2</b><p>O campanie. Verifică termenii și leadurile, notează sursa și serviciul.</p></article><article><b>Săptămâna 3</b><p>Elimină intenții nepotrivite, clarifică oferta și publică timelapse/material.</p></article><article><b>Săptămâna 4</b><p>Comenzi încasate, venit și marjă după publicitate. Documentează următorul test.</p></article></div>'''+source('Google Business — revendicare','https://support.google.com/business/answer/2911778?hl=en'))+
block('masurare','5. Măsurarea utilă','''<p>Ține un tabel privat: dată, sursă, serviciu, lead calificat, ofertă, comandă confirmată, cost direct și venit. Nu pune nume sau emailuri în UTM.</p><ul><li>CPL calificat = cheltuială / solicitări potrivite.</li><li>CPA = cheltuială / comenzi confirmate.</li><li>Marjă înainte de reclame = venit fără TVA − cost variabil.</li><li>CPA maxim dorit = marjă − profit dorit.</li></ul><p>Scenariu propriu: 149 lei venit − 75 cost − 30 profit = CPA maxim 44 lei. Dacă 25% din leadurile calificate cumpără, CPL țintă este 11 lei. Nu este performanță estimată.</p><p>După cheltuirea de două ori CPA-ul maxim fără comandă, inspectează oferta, termenii și pagina. La volume mici, o singură conversie nu dovedește un „câștigător”.</p>'''))

P['google']=('Google Ads pas cu pas','Un test Search local, cu intenție și cost controlate.',
block('pregatire','1. Cont și conversii',steps([
'Cont al firmei în ads.google.com. Confirmă România, RON, fusul orar și facturarea înainte de activare.',
'Definește conversia principală: solicitare validă înregistrată sau comandă. Vizita pe Contact și clickul pe telefon sunt semnale separate.',
'În Obiective/Conversii configurează website prin GTM sau integrarea aleasă, cu controlul consimțământului. Măsoară confirmarea serverului, nu apăsarea butonului.',
'Purchase se trimite din confirmarea Woo, cu order ID unic, valoare și RON. Transferul neîncasat se distinge de venit încasat.',
'Testează diagnosticele și o comandă de test. Nu număra testele în analiza comercială.'
])+source('Google — conversii web','https://support.google.com/google-ads/answer/16560108?hl=en'))+
block('campanie','2. Campania inițială',steps([
'Creează Search pentru cereri, de exemplu RO_CT_Search_Printare3D_Test01. Verifică obiectivul, rețeaua și setările efective.',
'Propunere de start: doar căutarea Google pentru control. Decide explicit opțiunile Display și partenerii.',
'Constanța și aria servită; pentru local folosește opțiunea de prezență. Targetarea bazată și pe interes poate include alte zone.',
'Română dacă reclama și pagina sunt în română. Extinde doar cu pagini și răspunsuri potrivite.',
'Un grup pentru printare la comandă. Nu amesteca imprimante de vânzare, cursuri, scanare și digitale.',
'Cu conversii verificate, evaluează licitarea pentru conversii. Fără date utile, un test de clickuri cu CPC limitat, unde este disponibil, poate explora cererea. Nu aplica automat creșteri de buget.',
'La majoritatea campaniilor cu buget mediu zilnic, Google poate cheltui până la dublu într-o zi și până la 30,4 × media pe lună. 450/30,4 ≈ 14,80 lei/zi.',
'Apelurile se pot programa când răspunzi, 10–18. Formularul poate primi cereri în afara programului cu așteptare clară.'
])+source('Google — Search','https://support.google.com/google-ads/answer/9510373?hl=en')+source('Google — locații','https://support.google.com/google-ads/answer/1722043?hl=en')+source('Google — bugete','https://support.google.com/google-ads/answer/2375454?hl=en'))+
block('keywords','3. Cuvinte și excluderi','''<p>Set propus pentru CR Print:</p><pre><code>[printare 3d constanta]
[imprimare 3d constanta]
"printare 3d la comanda"
"servicii printare 3d"
"prototipare 3d constanta"</code></pre><p>Exact și expresie pot acoperi și variante apropiate/intenții. Exact nu înseamnă numai caractere identice. Verifică raportul termenilor reali.</p><p>Excluderi de analizat: gratis, curs, job, angajare, imprimantă de vânzare, download gratuit. Nu exclude automat STL: clientul poate avea fișier și nevoie de printare.</p><p>Folosește Keyword Planner pentru cerere și cost actual. Nu sunt incluse CPC/volume inventate pentru Constanța.</p>'''+source('Google — potrivire keywords','https://support.google.com/google-ads/answer/14996023?hl=en'))+
block('anunt','4. Reclama și pagina','''<p>Titluri propuse: „Printare 3D în Constanța”, „Trimite Modelul Pentru Ofertă”, „FDM & SLA La Comandă”, „De La Idee La Obiect”. Descriere: „Ai un fișier sau o schiță? Discutăm materialul, dimensiunile și termenul. Cere o estimare CR Print 3D.”</p><p>„De la” trebuie să se aplice serviciului și să fie explicat pe pagină. Nu promite cel mai ieftin sau instant fără dovezi. Adaugă sitelinkuri FDM, SLA, portofoliu/contact și numărul corect.</p><p>Testează apelul și formularul pe telefon. Folosește o pagină cu aceeași ofertă, nu pagina principală generică pentru toate intențiile.</p>''')+
block('rutina','5. Optimizarea',steps([
'Primele zile: erori, cheltuială și intenții evident greșite. Nu rescrie tot contul la fiecare oră.',
'De două ori/săptămână: termenii reali, CPL calificat, leaduri și răspuns. Adaugă excluderi relevante.',
'Săptămânal: oferte, comenzi încasate și marjă. Clickuri fără lead: verifică relevanța/pagina/formularul. Leaduri fără comenzi: ofertă/preț/calificare.',
'Extinde orașe sau servicii numai cu capacitate de livrare și justificare economică.',
'Ține jurnalul schimbărilor. Oprește testul care depășește limita economică fără învățare utilă.'
])))

P['meta']=('Facebook & Instagram','Un singur sistem Meta, materiale potrivite și cereri calificate.',
block('cont','1. Pregătește conturile',steps([
'Pagina Facebook a firmei și Instagram profesional, conectate în Business Suite. Verifică persoanele cu acces.',
'Cont publicitar al firmei, RON/fus orar/facturare corecte. Activează 2FA pentru administratori.',
'Pentru instant forms pregătește politica reală de confidențialitate. Pentru website, Pixel și consimțământ.',
'Facebook/Instagram pot fi plasamente ale aceleiași campanii. Nu cere două abonamente sau bugete independente.',
'Cu 300–600 lei total, testează Meta într-o perioadă dedicată, fără a fragmenta automat bugetul Google.'
]))+
block('campanie','2. Solicitări în Ads Manager',steps([
'Creează Leads pentru cereri de ofertă. Sales se testează pentru produse cu cumpărare și măsurare validă.',
'Alege instant form sau website. Pentru mesaje, verifică destinațiile disponibile și capacitatea de răspuns.',
'Constanța și zona servită. Audiență simplă, fără multe interese care restrâng excesiv.',
'Un ad set, două materiale și buget controlat. Dată de final pentru test; verifică recomandările înainte de publicare.',
'Poți porni cu Advantage+ placements dacă materialele arată bine în toate previzualizările.',
'Formular scurt: contact, obiect, dimensiuni/cantitate și termen. O întrebare concretă filtrează cereri.',
'Mesaj final: programul de răspuns și cum trimite modelul. Fără promisiuni de ofertă instant universală.',
'Verifică primirea leadurilor în Business Suite/Ads Manager. Export manual privat este suficient la volum mic.'
])+source('Meta — ghid Lead Generation','https://about.fb.com/ltam/wp-content/uploads/sites/14/2023/11/LeadGenerationGuide.pdf'))+
block('creativ','3. Trei direcții creative pentru atelier','''<div class="three-cards"><article><h3>Fișier → piesă</h3><p>Video scurt: model, print, obiect în mână. „Ai un model? Hai să-i dăm formă.”</p></article><article><h3>Problemă rezolvată</h3><p>Suport/carcasă în utilizare, dimensiune și material. Un caz real cu acord de publicare.</p></article><article><h3>Seria pilot</h3><p>Mostră și lot mic. „Testăm prima piesă, apoi stabilim seria.”</p></article></div><p>Versiuni 9:16 pentru Reels/Stories și 4:5 pentru Feed. Ideea în primele secunde, subtitrări, margini libere pentru interfață. Inteligența artificială poate susține direcția vizuală, dar nu se prezintă ca fotografie a unei comenzi reale.</p>'''+source('Meta — Reels placements','https://www.facebook.com/business/ads/facebook-instagram-reels-ads'))+
block('pixel','4. Pixel și analiză','''<p>În Events Manager creează/selectează sursa firmei și conectează prin integrarea WordPress/Woo aleasă, cu consimțământ. Nu instala două integrări care dublează Purchase. Pixel/CAPI împreună necesită deduplicare.</p><p>Testează PageView, Lead valid și Purchase cu order ID unic. Nu pune date personale sau mesaje în URL. Analizează CPL calificat și comenzi încasate: leaduri ieftine nepotrivite nu sunt performanță.</p><p>La acest buget compară două idei creative, nu zece audiențe. Verifică dacă oamenii răspund și dacă solicitarea este realizabilă profitabil.</p>''')+
block('organic','5. Organic fără buget suplimentar','''<p>Trei postări/săptămână: transformare, explicație FDM/SLA și obiect real în utilizare. Telefon, locație și ofertă în profil. Fixează un post despre comandă.</p><p>Luni: fișier/piesă. Miercuri: material/limitări. Vineri: nava în 3D și macheta reală. Nu cumpăra urmăritori și nu trimite mesaje comerciale în masă.</p>'''))

P['tiktok']=('TikTok: organic întâi','Procesul 3D este vizual; bugetele minime complică un start plătit mic.',
block('buget','1. Praguri și buget',note('TikTok Ads Manager indică praguri de peste 50 USD pentru bugetul campaniei și peste 20 USD/zi pentru ad group; pragul total al grupului depinde de zile. Verifică valorile din cont și moneda locală. Acestea nu sunt recomandarea noastră de cheltuială.')+
'''<p>Cu 300–600 lei/lună, un test Ads Manager poate consuma rapid bugetul. Recomandarea CR Print: organic acum, plătit când există materiale validate și buget separat. Promote din aplicație are alte condiții; nu îl echivala automat cu Ads Manager sau vânzări.</p>'''+source('TikTok — bugete oficiale','https://ads.tiktok.com/resources/help/article/budget?lang=en'))+
block('organic','2. Plan organic de o lună',steps([
'Filmează vertical, în lumină bună. Arată procesul și o mână pentru scară, păstrând logo-ul real.',
'Primele secunde: rezultatul/problema. „Din fișier în obiect”, „Piesa care lipsea”, „Cât de mici pot fi detaliile?”.',
'Un subiect și subtitrări lizibile. 15–25 secunde este un exemplu de format, nu regulă a algoritmului.',
'Trei clipuri pe săptămână o lună; refolosește în Reels cu muzică și materiale cu drepturi comerciale.',
'Pas clar: dimensiuni/fișier pentru ofertă, viewerul 3D sau întrebare. Nu promite printare perfectă a oricărui fișier.',
'Măsoară vizite relevante, mesaje și cereri. Cere sursa declarată dacă trackingul nu este disponibil.'
]))+
block('ads','3. Ads Manager când ai buget separat',steps([
'Creează TikTok for Business cu țara și datele reale. Verifică eligibilitatea și opțiunile actuale pentru România.',
'Configurează facturare, acces, Pixel/Events API și consimțământ prin integrarea aleasă.',
'Obiectiv după rezultat: solicitare sau cumpărare. Un ad group, aria de livrare și materiale validate organic.',
'Buget și durată cu pragurile reale afișate. Nu folosi automat bugetul actual dacă depășește limita ta de risc.',
'Spark Ads necesită autorizarea postului și contului potrivit. Folosește drepturi comerciale pentru muzică.',
'Testează pagina și conversia înainte de activare. Judecă leadurile și marja, nu vizualizările.'
]))+
block('idei','4. Cinci clipuri propuse','''<ol><li>Nava: digital → randare → machetă fabricată.</li><li>FDM versus SLA, cu materialele explicate.</li><li>Timelapse și ce intră în estimarea de cost.</li><li>Schiță simplă → componentă modelată.</li><li>Mostră promoțională → serie mică.</li></ol><p>Etichetează randările și imaginile generate cu IA. Nu prezenta video placeholder ca filmare reală din atelier.</p>'''))

P['lansare']=('SEO & lansare','Verificări înainte de comenzi reale și rutină după lansare.',
block('seo','1. SEO cu informații corecte',steps([
'Pagină distinctă pentru fiecare serviciu, titlu clar, un H1, aplicații/material/preț/proces. Texte utile proprii, fără repetiții artificiale.',
'Nume, adresă, program 10–18, telefon și email identice în site și profilul Google eligibil.',
'Tema oferă metadata de bază și LocalBusiness. Woo generează datele produselor reale. Fără recenzii sau certificări inventate.',
'Cu plugin SEO, verifică o singură sursă pentru metadata/sitemap și evită schema locală duplicată. Premium nu este obligatoriu.',
'Search Console: verifică domeniul și trimite /wp-sitemap.xml sau sitemapul pluginului SEO. Nu folosi sitemapul static demo pentru WP.',
'Păstrează URL-uri vechi sau configurează 301 individuale spre echivalente. Verifică canonical și linkuri.',
'Pe live elimină descurajarea indexării după verificare; staging, ghid, coș/checkout rămân fără indexare.'
])+source('Google — LocalBusiness','https://developers.google.com/search/docs/appearance/structured-data/local-business'))+
block('performanta','2. Performanță',steps([
'Testează pagina principală, serviciu, produs, coș și checkout pe mobil/conexiune lentă. PageSpeed/Lighthouse: LCP, CLS, INP pe paginile reale. Nu sunt promise scoruri perfecte.',
'WebP responsive, fonturi sistem, 3D la cerere și video discret reduc încărcarea inutilă. Nu activa autoplay greu pe orice telefon.',
'Cache compatibil al gazdei; exclude Contact, Coș, Checkout, Contul meu și utilizatorii autentificați. Nu dubla pluginuri de cache.',
'Nu activa agregare/minificare agresivă fără verificare. Import maps, modulele 3D și scripturile Woo pot fi afectate.',
'Înainte de update major: backup, staging, comandă și email de test, apoi live.'
]))+
block('aria','3. Accesibilitate',steps([
'Tab/Shift+Tab: focus vizibil, ordine logică; Escape închide meniul mobil.',
'Zoom 200%, viewport îngust și texte lungi: prețuri/butoane/etichete lizibile.',
'Nume accesibile pentru temă, coș și viewer. Erori explicate în text, nu doar culoare.',
'Galerie alternativă la 3D, săgeți și +/− în canvas. Pe telefon viewerul se activează la cerere.',
'Reduce motion în sistem trebuie să oprească intro/typewriter/mișcarea decorativă.',
'Verifică contrastul ambelor teme și formularele cu cititor de ecran. ARIA nu înseamnă automat certificare.'
]))+
block('legal','4. Date comerciale și documente','''<p>Completează comerciantul real, contactul, prețuri/taxe, plată, transport, termen, reclamații, garanții și retragere. Pagina de termeni din prototip trebuie completată și verificată înainte de producție.</p><p>Vânzarea la distanță are în general retragere de 14 zile, cu excepții precum produse după specificații/personalizate și anumite situații digitale. Nu orice obiect printat este automat personalizat. Pentru livrare digitală imediată, implementează acordurile și informarea aplicabile.</p><p>Politica trebuie să descrie operator, scopuri, temeiuri, destinatari, păstrare și drepturi. Documentează hosting, email, curier, plăți și analiză. Înainte de pixeli, oferă alegere reală pentru tracking și testează accept/refuz.</p><p>Cu contabilul: TVA, facturare și raportări, mai ales pentru digitale în alte țări. Nu trata taxele demo ca recomandare fiscală.</p>'''+source('Your Europe — vânzare la distanță','https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/ecommerce-distance-selling/index_en.htm')+source('Your Europe — drepturi cumpărători','https://europa.eu/youreurope/citizens/consumers/shopping/shopping-consumer-rights/index_en.htm'))+
block('checklist','5. Lista de lansare','<div class="checklist">'+''.join('<label><input type="checkbox" data-launch-check="'+str(i)+'"><span>'+t+'</span></label>' for i,t in enumerate([
'Backup și restaurare documentate; staging protejat.',
'Logo, telefon, email, adresă și program corecte.',
'Prețuri și specificații reale; demo-uri convertite/eliminate.',
'Fizic, digital și coș mixt verificate pe mobil.',
'Transport/plată corecte; niciun IBAN demo.',
'SMTP primit efectiv; Contact și emailuri Woo verificate.',
'Fișier complet protejat, previzualizare separată.',
'Documente și acorduri digitale completate.',
'Keyboard, focus, reduce motion și ambele teme verificate.',
'301, canonical, sitemap și Search Console verificate.',
'Analytics/pixeli conform consimțământului, fără PII în URL.',
'Indexare doar live; ghid/admin demo în afara site-ului comercial.',
'Testele în afara rapoartelor live și acces admin controlat.',
'Procedură de ofertare, producție, livrare și răspuns.'
]))+'</div>')+
block('rutina','6. După lansare','''<p>Zilnic: cereri, comenzi, email și erori. Săptămânal: marjă, reclame, stocuri, actualizări/backup. Lunar: produse profitabile, pagini care aduc leaduri și următorul test. Păstrează ghidul local și datele clienților în afara repositoryului.</p>'''))

P['depanare']=('Depanare','Diagnostice rapide și fișierele proiectului.',
block('probleme','Probleme frecvente','''<div class="table-wrap"><table><thead><tr><th>Simptom</th><th>Verifică / acțiune</th></tr></thead><tbody><tr><td>Tema nu se instalează</td><td>ZIP corect, limită upload, PHP. Cere gazdei limită/SFTP.</td></tr><tr><td>Pagina principală veche</td><td>Setări → Citire, pagina nouă și cache.</td></tr><tr><td>404</td><td>Starea de ciornă, meniurile și legăturile permanente.</td></tr><tr><td>Magazin gol</td><td>Woo activ și produse publicate după confirmarea prețurilor.</td></tr><tr><td>Email lipsă</td><td>Inbox, mailer, DNS, Spam și solicitarea salvată.</td></tr><tr><td>Calcul expirat</td><td>Exclude Contact din cache și reîncarcă.</td></tr><tr><td>Checkout blocat</td><td>Plată/livrare eligibile, HTTPS, cache; testează tipurile separat.</td></tr><tr><td>Viewer indisponibil</td><td>WebGL, importmap, fișier și agregare scripturi; galerie alternativă.</td></tr><tr><td>Admin demo offline</td><td>node dev-server.mjs, apoi 4173/admin.html.</td></tr><tr><td>Playground nu pornește</td><td>Node ≥24.18, rețea și port 9400 liber. Citește terminalul.</td></tr></tbody></table></div>''')+
block('ajutor','Ce trimiți când ceri ajutor','''<p>URL, pași, rezultat așteptat/actual, versiuni WP/PHP/Woo și captură fără date personale. Pentru email: test SMTP primit sau nu, solicitare salvată sau nu. Nu trimite parole/chei în conversații publice.</p>''')+
block('fisiere','Fișierele proiectului','''<ul><li>HTML + design.css: demo de design.</li><li>dev-server.mjs: API local.</li><li>data/catalog.json: produse demo, fără date personale.</li><li>wordpress/crprint-studio.zip: temă.</li><li>wordpress/crprint-core.zip: formular/import.</li><li>wordpress/blueprint.json: WordPress local.</li><li>models/nava-preview.glb: previzualizare publică simplificată.</li><li>models/NAVA 24 SEPTEMBRIE.fbx: original complet public în demo.</li></ul><p>Serverul 4173 păstrează mesaje și comenzi în directorul temporar crprint-local-demo al computerului, separat de repository. WordPress Playground păstrează datele în %LOCALAPPDATA%/CRPrint/wordpress-demo; fă backup și exportă datele utile.</p>'''))
from importlib.util import spec_from_file_location,module_from_spec
details_spec=spec_from_file_location('guide_details',root/'tools/guide-details.py')
details=module_from_spec(details_spec);details_spec.loader.exec_module(details)
details.expand(P,block,steps,note,source)
setup_spec=spec_from_file_location('guide_setup',root/'tools/guide-cpanel-smartbill.py')
setup=module_from_spec(setup_spec);setup_spec.loader.exec_module(setup)
setup.adapt(P,block,steps,note,source)
quick_start = block('pornire-rapida','Pornește magazinul local în 3 pași',steps([
'Deschide folderul <strong>CRPRINT</strong> și fă dublu clic pe <strong>Start-Demo.cmd</strong>. Nu trebuie să pornești un server separat pentru magazin.',
'Așteaptă mesajul cu adresa <strong>http://127.0.0.1:4173/</strong>. Păstrează fereastra deschisă cât folosești site-ul.',
'Deschide <a href="../magazin.html">magazinul</a> sau <a href="../admin.html">administrarea produselor și comenzilor</a>. Din administrare poți modifica produsele; schimbările se salvează pe acest computer.'
])+note('Dacă site-ul se deschide deja, serverul este pornit: nu mai deschide încă o fereastră. Pentru oprire, apasă <strong>Ctrl+C</strong> în fereastra serverului. La următoarea utilizare, pornește din nou Start-Demo.cmd.')+'<p><a href="../PORNIRE-MAGAZIN.md">Instrucțiuni scurte și soluții pentru erori →</a></p><p>Pentru administrarea în WooCommerce, pornește separat <strong>Start-WordPress.cmd</strong>, așteaptă confirmarea din fereastră, apoi deschide <a href="http://127.0.0.1:9400/wp-admin/">panoul WordPress</a>. Prima pornire durează mai mult și necesită internet. Detaliile sunt în <a href="wordpress.html">capitolul WordPress</a>.</p>')
title, subtitle, content = P['index']
P['index'] = (title, subtitle, quick_start + content)
order=list(P)
for key,(title,subtitle,content) in P.items():
    nav=''.join(f'<a href="{k}.html" {"aria-current=page" if k==key else ""}><span>{i+1:02}</span>{html.escape(v[0])}</a>' for i,(k,v) in enumerate(P.items()))
    anchors=''.join('<a href="#'+i+'">'+re.sub('<[^>]+>','',t)+'</a>' for i,t in re.findall(r'<section class="chapter-block" id="([^"]+)"><h2>(.*?)</h2>',content))
    nxt=order[(order.index(key)+1)%len(order)]
    doc=f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{html.escape(title)} — Ghid CR Print 3D</title><link rel="icon" href="../images/logo-og-512.png"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('crprint-guide-theme')||'light'}}catch(e){{}}</script><link rel="stylesheet" href="guide.css"></head><body><a class="skip" href="#content">Sari la conținut</a><header><a class="guide-brand" href="index.html"><img src="../images/cr-print-logo-original.webp" alt="" width="36" height="36"><strong>CR Print <span>/ MANUAL DE LANSARE</span></strong></a><div><button class="theme-button" aria-label="Schimbă tema ghidului" type="button">◐</button><a href="../index.html">Vezi site-ul ↗</a></div></header><div class="guide-shell"><aside class="sidebar"><label class="search-label" for="guide-search">Caută în ghid</label><input type="search" id="guide-search" placeholder="SMTP, produs, Google…"><div class="search-results" hidden role="status"></div><nav aria-label="Capitole">{nav}</nav><div class="progress"><span data-progress></span><progress max="{len(P)}" value="0" aria-label="Progres"></progress></div><small>Actualizat: 5 octombrie 2026<br>cPanel și SmartBill: documentație oficială consultată. Opțiunile diferă după pachet.</small></aside><main id="content"><div class="guide-hero"><p class="eyebrow">CR PRINT 3D / {order.index(key)+1:02}</p><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div><nav class="chapter-toc" aria-label="În acest capitol">{anchors}</nav>{content}<div class="chapter-end"><button type="button" data-complete="{key}">Marchează capitolul ca parcurs ✓</button><a href="{nxt}.html">Următorul: {P[nxt][0]} →</a></div><footer>Ghid de lucru CR Print 3D · România · Parolele și datele clienților rămân în afara proiectului public.</footer></main></div><script src="guide.js" defer></script></body></html>'''
    (out/f'{key}.html').write_text(doc,encoding='utf-8')
(out/'search-index.json').write_text(json.dumps([{'title':v[0],'url':k+'.html','text':re.sub('<[^>]+>',' ',v[2])} for k,v in P.items()],ensure_ascii=False),encoding='utf-8')
print(f'Built guide: {len(P)} chapters')
