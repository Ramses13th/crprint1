"""Additional, concrete beginner workflows for the separate Romanian manual."""
def expand(P, block, steps, note, source):
    def add(key, ident, title, content):
        a,b,c=P[key];P[key]=(a,b,c+block(ident,title,content))
    add('index','citeste-intai','Începe aici: ce faci astăzi, în ordine',steps([
        'Deschide folderul CRPRINT pe computer. Un folder este locul în care sunt fișierele site-ului; nu trebuie să le deschizi pe fiecare.',
        'Dublu-click pe <strong>Start-Demo.cmd</strong>. Se deschide o fereastră de terminal, adică fereastra care ține serverul pornit. Păstreaz-o deschisă. Dacă Windows arată o extensie ascunsă, caută fișierul cu numele Start-Demo, de tip Windows Command Script.',
        'În bara de adrese a browserului scrie <strong>http://127.0.0.1:4173/</strong>. Această adresă funcționează pe computerul tău. Nu este crprint.ro și nu este un link pe care îl trimiți clienților.',
        'Intră în Magazin, adaugă o machetă și verifică Coșul. Folosește date fictive la exercițiul de comandă. Panoul rapid este la <a href="../admin.html">administrare</a>; comenzile și mesajele apar acolo.',
        'Dublu-click pe <strong>Start-WordPress.cmd</strong>. Prima pornire poate dura câteva minute fiindcă descarcă WordPress. Nu închide terminalul. Așteaptă adresa cu portul 9400 și deschide <a href="http://127.0.0.1:9400/wp-admin/">panoul WordPress local</a>.',
        'Exersează schimbarea unui preț în Produse și verificarea unei comenzi. În acest mediu nu se trimit emailuri externe și nu se încasează bani. Aceste protecții sunt intenționate; aspectul pentru vizitatori este cel al unui magazin normal.',
        'După exerciții, urmează capitolul cPanel pentru găzduirea ta, apoi WordPress, magazin, email și SmartBill. Nu încărca baza locală cu comenzile fictive peste site-ul existent.'
    ])+note('<strong>La sfârșitul exercițiului:</strong> ai două ferestre de terminal deschise și poți vedea atât designul rapid, cât și panoul WordPress. Ca să oprești un server, selectează fereastra lui și apasă Ctrl+C. Datele WordPress rămân pentru următoarea pornire.'))
    add('index','trusa','Pregătește o singură fișă privată', '<p>Într-un document păstrat numai de tine, notează următoarele. Nu pune parole în acest ghid, în GitHub sau într-un document public.</p>'+steps([
        'Domeniu: crprint.ro. Cine l-a cumpărat și când expiră? Domeniul este numele; găzduirea este computerul conectat permanent la internet care ține site-ul.',
        'Găzduire: firmă, link spre panoul clientului, emailul contului, data și costul reînnoirii. Nu știi firma? Caută factura, extrasul de plată sau întreabă persoana care a făcut site-ul.',
        'WordPress: adresa de administrare, utilizatorul administrator și metoda de recuperare a accesului. Administrator înseamnă că ai acces la Teme, Pluginuri și Setări.',
        'Email: cine găzduiește căsuța hi@crprint.ro și cum intri în ea. SMTP înseamnă serviciul care trimite emailuri din site; poate fi diferit de locul unde citești mesajele.',
        'Datele firmei: denumire legală, adresă, CUI, număr de înregistrare, regim TVA, cont bancar. Completează-le din actele reale împreună cu contabilul.',
        'Produse: prețuri confirmate, costuri, scară/dimensiuni, material, culoare, termen și drepturi pentru fișierul digital. În proiect, valorile de pornire sunt 149 lei, 49 lei și 19 lei transport; înlocuiește-le înainte de vânzare.',
        'Reclame: conturile firmei și un plafon lunar ales, de exemplu 450 lei. Acest buget este pentru afișarea reclamelor și este separat de găzduire, producție și eventuale taxe.'
    ]))
    add('wordpress','hosting-concret','6. Cum pregătești găzduirea când nu știi furnizorul',steps([
        'În emailul cu care ai cumpărat domeniul caută „crprint.ro”, apoi „factură”, „hosting”, „găzduire”, „cPanel” și „Plesk”. Deschide factura și identifică firma și site-ul ei oficial.',
        'Intră în contul de client al acelei firme. Dacă parola lipsește, folosește recuperarea contului cu emailul tău. Nu încerca să schimbi DNS până nu știi ce servicii sunt acolo.',
        'Caută secțiunea Servicii / Găzduire / Hosting și un buton de tip Administrare, cPanel sau Plesk. Denumirile diferă. Dacă nu există, trimite mesajul de mai jos suportului.',
        'Cere o copie separată a site-ului existent, numită copie de lucru sau staging. Lucrează pe acea copie. Un backup îți permite restaurarea, dar nu îți oferă automat o copie pe care să lucrezi.',
        'Verifică dacă adresa copiei începe cu HTTPS și dacă accesul este protejat. Dacă browserul arată avertisment de certificat, cere gazdei să îl repare.',
        'Dacă nu ai deloc găzduire, cere o ofertă pentru un singur site WordPress cu WooCommerce, SSL/HTTPS, backup și restaurare, suport în română și PHP actual. Cere separat costul primului an și costul de reînnoire.',
        'Compară două sau trei oferte pe aceleași cerințe. Întreabă dacă includ email, staging și migrare. Un preț foarte mic în primul an poate avea o reînnoire mai mare. Nu plăti pentru constructor de pagini sau extensii premium înainte să fie necesare.'
    ])+'''<h3>Mesaj pe care îl poți trimite suportului</h3><pre><code>Bună ziua! Dețin crprint.ro și vreau să instalez o temă personalizată,
WooCommerce și WP Mail SMTP. Vă rog să confirmați:
1. ce pachet de găzduire am și costul de reînnoire;
2. cum intru în panoul de găzduire și în WordPress;
3. cum fac backup complet și cum îl restaurez;
4. cum creați o copie de lucru protejată (staging);
5. versiunea PHP, HTTPS și limita pentru încărcarea temei ZIP;
6. unde este găzduită hi@crprint.ro și setările SMTP/DNS;
7. dacă includeți ajutor pentru publicarea copiei de lucru.
Nu doresc să fie înlocuit site-ul existent înainte de verificare.</code></pre>''')
    add('wordpress','instalare-click','7. Instalarea pachetului, click cu click',steps([
        'Deschide panoul WordPress al <strong>copiei de lucru</strong>. În partea stângă sunt meniurile. Dacă nu vezi Aspect sau Pluginuri/Module, contul tău probabil nu are rolul Administrator.',
        'În computer deschide CRPRINT → wordpress. Aici sunt <strong>crprint-studio.zip</strong> și <strong>crprint-core.zip</strong>. Lasă-le arhive ZIP. Nu le extrage înainte de încărcare.',
        'În WordPress apasă Aspect → Teme → Adaugă temă → Încarcă temă → Alege fișierul. Selectează crprint-studio.zip. Apasă Instalează acum, așteaptă mesajul de succes, apoi Activează.',
        'Apasă Pluginuri/Module → Adaugă → Încarcă modul. Selectează crprint-core.zip → Instalează acum → Activează. Tema controlează aspectul; CR Print Core oferă importul și formularul.',
        'În Pluginuri → Adaugă caută WooCommerce. Verifică autorul Automattic și apasă Instalează, apoi Activează. Repetă pentru WP Mail SMTP, autor WPForms. Nu ai nevoie să cumperi versiunea Pro pentru acești pași.',
        'Dacă WooCommerce pornește un asistent, completează țara România, adresa reală a atelierului și moneda RON. Poți sări peste recomandările de extensii plătite. Nu inventa date de firmă sau de TVA.',
        'Apasă Instrumente → CR Print — configurare. Introdu hi@crprint.ro în câmpul destinatar și salvează. Apasă <strong>Creează pagini și produse în ciornă</strong>. Ciornă înseamnă că pagina sau produsul nu este public încă.',
        'În Pagini → Toate paginile găsește paginile noi. Folosește Previzualizează la Acasă și Contact. În Produse verifică cele două variante ale navei. Importul nu completează automat toate specificațiile și nici licența comercială.',
        'Dacă există deja pagini cu aceleași adrese, verifică noile pagini cu prefix crprint-. Importul păstrează conținutul vechi. Notează ID-ul sau adresa paginii noi ca să nu alegi varianta greșită la pagina principală.',
        'Corectează conținutul, imaginile și datele. Publică paginile verificate, apoi mergi în Setări → Citire → Pagina ta de pornire afișează → O pagină statică. La Pagina de pornire alege noua Acasă → Salvează modificările.',
        'În Aspect → Meniuri selectează CR Print principal. La Setări meniu bifează Navigare principală. Pentru un link greșit, extinde elementul și alege pagina corectă sau URL-ul corect → Salvează meniul.',
        'În Setări → Legături permanente selectează Nume articol, dacă acesta este formatul decis pentru noul site. Apasă Salvează. Pentru un site existent, păstrează adresele care funcționează sau pregătește redirecționări înainte de schimbare.'
    ])+note('<strong>Ce trebuie să vezi:</strong> noua pagină Acasă, meniul în română, un magazin administrat de WooCommerce și formularul Contact. Dacă tot vezi site-ul vechi, verifică pagina statică și golește cache-ul copiei de lucru. Cache înseamnă o copie temporară a paginii.'))
    add('wordpress','editare-exemple','8. Exercițiu: modifică un text și o imagine',steps([
        'În Pagini → Toate paginile deschide Contact → Editează. Layoutul importat este un bloc HTML personalizat. HTML este textul care descrie structura paginii; etichetele sunt fragmentele dintre &lt; și &gt;.',
        'Folosește căutarea editorului sau Ctrl+F pentru „O idee bună”. Înlocuiește numai cuvintele vizibile; păstrează etichetele h1, span, div și ghilimelele din atribute.',
        'Apasă Previzualizează → Previzualizare într-o filă nouă. Dacă arată bine, revino și apasă Actualizează. Dacă ai greșit, folosește Revizii pentru a reveni la versiunea anterioară.',
        'Formularul este introdus prin <code>[crprint_contact_form]</code>. Acesta este un shortcode: o comandă scurtă care afișează formularul. Nu îl șterge când schimbi textul paginii.',
        'Pentru o imagine obișnuită: Media → Adaugă fișier media → Selectează fișiere. Încarcă o imagine deținută de tine. Deschide-o în bibliotecă și completează Text alternativ cu o descriere a obiectului.',
        'Copiază URL-ul fișierului. În HTML-ul paginii caută imaginea și înlocuiește valoarea atributului src. Dacă există srcset cu vechile imagini, elimină acel atribut întreg sau înlocuiește toate variantele; altfel browserul poate afișa în continuare imaginea veche.',
        'Păstrează o copie a blocului înainte să îl modifici. Pentru imagini și descrieri de produs nu ai nevoie de HTML: folosește editorul WooCommerce din capitolul Magazin.',
        'Pentru logo, header și footer nu modifica fiecare pagină: sunt elemente comune ale temei. Păstrează logo-ul original și cere o actualizare a temei pentru schimbări globale. Un editor vizual pentru aceste componente poate fi adăugat ulterior.'
    ])+source('Editorul WordPress și reviziile','https://wordpress.org/documentation/article/revisions/'))
    add('magazin','produs-fizic-click','6. Primul produs fizic: fiecare câmp',steps([
        'În panoul WordPress mergi la Produse → Toate produsele. Apasă Editează la Nava · 24 Septembrie. Pentru un produs complet nou folosește Produse → Adaugă produs.',
        'În câmpul mare de sus scrie numele. În descrierea lungă explică ce primește clientul: dimensiuni, scară, material, culoare, finisaj și utilizare. Nu spune că este o fotografie a produsului dacă este o randare.',
        'Caută caseta Date produs. Selectează Produs simplu. Pentru machetă lasă <strong>Virtual</strong> și <strong>Descărcabil</strong> debifate.',
        'În fila General completează Preț normal cu prețul confirmat. Nu scrie „lei” în câmp. Lasă Preț promoțional gol dacă nu ai o reducere reală. Exemplul 149 este un exercițiu, nu o recomandare de marjă.',
        'În Inventar păstrează SKU-ul <code>nava-24-septembrie</code>; SKU este codul produsului. El conectează și previzualizarea 3D din temă. Pentru alte produse folosește coduri proprii unice.',
        'Dacă ai machete gata fabricate, bifează Gestionare stoc și introdu cantitatea reală. Dacă produci la comandă, explică termenul și alege politica de disponibilitate potrivită; nu afirma „20 în stoc” dacă nu există 20 de produse.',
        'În Livrare completează greutatea și dimensiunile ambalajului dacă le cunoști. Verifică unitățile din WooCommerce → Setări → Produse. Nu folosi dimensiunile navei fără ambalaj pentru calculul curierului.',
        'În Descriere scurtă produs scrie două propoziții clare: ce este și pentru cine. În dreapta, Imagine produs → Setează imaginea → Biblioteca media. Alege nava-studio. Galerie produs → Adaugă imagini și selectează vederea laterală și cealaltă perspectivă.',
        'În Categorii produs adaugă Machete navale. La Vizibilitate catalog lasă Magazin și rezultate de căutare, dacă vrei să poată fi găsit. Publică numai după verificarea specificațiilor.',
        'Apasă Previzualizează și citește pagina ca un client. Verifică prețul, disponibilitatea, imaginile și butonul Adaugă în coș. Apasă Actualizează după orice schimbare ulterioară.'
    ])+note('<strong>Nu confunda:</strong> Produse este catalogul; Media este biblioteca imaginilor; WooCommerce → Comenzi este lista comenzilor. Modificarea unui produs în WordPress nu modifică automat catalogul rapid de pe portul 4173.'))
    add('magazin','digital-click','7. Varianta digitală și fișierul protejat',steps([
        'În Produse deschide Nava · fișier digital FBX. În Date produs selectează Produs simplu și bifează Virtual și Descărcabil. Virtual elimină transportul; Descărcabil oferă fișierul clientului eligibil.',
        'Păstrează SKU <code>nava-24-septembrie-digital</code>. Introdu prețul real și descrie formatul FBX, ce aplicații îl pot deschide și conținutul arhivei. Nu afirma compatibilitate fără să o verifici.',
        'Pregătește pe computer o arhivă ZIP cu modelul și un fișier CITEȘTE-MĂ care explică utilizarea și licența. Înainte de vânzare confirmă că deții drepturile pentru model și pentru distribuirea fișierului.',
        'În General → Fișiere descărcabile apasă Adaugă fișier. La Nume scrie „Nava 24 Septembrie — FBX”. La URL fișier apasă Alege fișier → Încarcă fișiere și încarcă arhiva prin editorul produsului.',
        'Nu folosi drept fișier plătit un link spre models/NAVA… din site-ul rapid sau spre GitHub. Acela este un fișier public. Previzualizarea mică GLB poate rămâne publică; originalul comercial trebuie gestionat separat.',
        'La Limită descărcări poți folosi 5, iar la Expirare descărcare poți folosi 30 zile dacă această condiție este anunțată clientului. Lasă câmpurile goale dacă alegi fără limită; decizia trebuie reflectată în termeni.',
        'În WooCommerce → Setări → Produse → Produse descărcabile selectează metoda de descărcare potrivită găzduirii. Începe cu Forțează descărcările și verifică protecția; pentru fișiere mari cere gazdei suport X-Accel-Redirect/X-Sendfile.',
        'La plată manuală, comanda poate rămâne În așteptare. Nu îi acorda acces digital înainte de confirmarea plății. După confirmare, schimbă statusul eligibil și verifică emailul/linkul de descărcare.',
        'Testează într-un browser fără cont de administrator. Un link copiat dintr-o comandă nu trebuie să devină o cale publică nelimitată spre fișier. Verifică și expirarea/limita stabilite.',
        'Documentele pentru conținut digital și acordurile privind livrarea imediată/dreptul de retragere necesită configurare juridică explicită. Nu presupune că bifa generală de termeni rezolvă această cerință.'
    ])+source('Gestionarea fișierelor descărcabile','https://woocommerce.com/document/digital-downloadable-product-handling/'))
    add('magazin','transport-click','8. Ridicare și curier în România',steps([
        'Mergi la WooCommerce → Setări → General. Adresa magazinului trebuie să fie cea reală. La țări de vânzare și livrare selectează România pentru început. Salvează.',
        'Deschide fila Livrare → Zone de livrare → Adaugă zonă. Nume: România. Regiuni: România. Apasă Adaugă metodă de livrare → Tarif fix.',
        'La metoda Tarif fix apasă Editează. Nume afișat: Curier. Cost: tariful real negociat; 19 este valoarea exemplului. Starea taxei se stabilește cu contabilul. Salvează.',
        'În aceeași zonă apasă Adaugă metodă → Ridicare locală. Nume: Ridicare din Constanța. Cost: 0 dacă ridicarea este gratuită. Salvează.',
        'Dacă ai zone mai specifice, pune-le înaintea zonelor generale. WooCommerce folosește prima zonă care se potrivește adresei. O zonă duplicată poate ascunde metodele pe care tocmai le-ai adăugat.',
        'În magazin adaugă numai macheta fizică, intră în Coș, scrie o adresă românească fictivă și verifică ambele metode. Adaugă apoi numai modelul digital: nu trebuie să apară cost de transport.',
        'Pentru fizic plus digital, transportul se aplică produsului fizic. Verifică totalul. Publică separat termenul de producție și termenul estimat al curierului.',
        'Un tarif fix nu generează automat AWB. La început poți crea AWB din contul curierului și îl comunici clientului. O integrare de curier poate fi adăugată după ce vezi un volum constant de comenzi.'
    ])+source('Zone de livrare WooCommerce','https://woocommerce.com/document/setting-up-shipping-zones/'))
    add('magazin','plata-comenzi-click','9. Plata manuală și prima comandă reală',steps([
        'În WooCommerce → Setări → Plăți alege Transfer bancar direct și apasă Gestionează. Activează numai pe site-ul pregătit pentru vânzare.',
        'Titlu: Transfer bancar. Descriere: clientul primește detaliile după comandă. În Conturi bancare completează numai contul real al firmei, numele titularului și IBAN-ul. Cere contabilului să le confirme.',
        'Dacă oferi ramburs, activează Plata la livrare și limiteaz-o la metodele de curier/ridicare pentru care este potrivită. Nu oferi ramburs unui fișier digital. Comisionul curierului trebuie inclus în calcul.',
        'Nu este obligatoriu un procesator de card pentru lansarea inițială. Dacă îl adaugi ulterior, compară comisioanele, termenii și suportul WooCommerce și testează mai întâi în modul sandbox al furnizorului.',
        'În WooCommerce → Comenzi apasă o comandă. Verifică produsul, cantitatea, contactul, totalul, livrarea și notele. Numărul comenzii nu înseamnă că banii au intrat.',
        'Pentru transfer, verifică extrasul bancar. Abia după confirmarea plății schimbi statusul în Procesare, dacă sunt produse de pregătit. Statusul Finalizată este folosit după îndeplinirea comenzii.',
        'În Note comandă poți adăuga o notă privată pentru atelier sau o notă pentru client. Alege intenționat tipul: o notă pentru client poate trimite email.',
        'Un status de comandă nu emite automat factura fiscală. Stabilește cu contabilul programul de facturare și obligațiile de raportare. Nu inventa o integrare fiscală din setările Woo.',
        'Înainte de vânzare efectivă, fă o comandă controlată fizică, una digitală și una mixtă; verifică inboxul, transportul și descărcările. Anulează comenzile de probă în mod organizat, separat de rapoartele reale.'
    ])+source('Transfer bancar în WooCommerce','https://woocommerce.com/document/bacs/')+source('Plata la livrare','https://woocommerce.com/document/cash-on-delivery/'))
    add('email','smtp-concret','5. WP Mail SMTP: configurația cu emailul găzduirii',steps([
        'Cere gazdei setările SMTP pentru hi@crprint.ro: server, port, criptare, utilizator și metoda de autentificare. Cere și acces la inbox. Nu presupune că parola WordPress este parola emailului.',
        'În WordPress intră în WP Mail SMTP → Settings/Setări → General. La From Email/Email expeditor scrie hi@crprint.ro. La From Name/Nume expeditor scrie CR Print 3D.',
        'Activează Force From Email dacă acest expeditor trebuie folosit de toate emailurile site-ului. Acest lucru evită trimiterea ca și cum clientul ar fi expeditorul; adresa clientului este folosită doar pentru răspuns.',
        'La Mailer selectează Other SMTP/Alt SMTP dacă folosești datele gazdei. SMTP Host este serverul primit. Encryption/Criptare și SMTP Port trebuie să corespundă între ele: folosește combinația exactă indicată de furnizor, nu o valoare ghicită.',
        'Activează Authentication dacă gazda cere autentificare. Username este de obicei adresa completă hi@crprint.ro, dar verifică instrucțiunile. Introdu parola în panoul privat. Nu o pune în GitHub sau în capturi.',
        'Apasă Save Settings/Salvează. Mergi la WP Mail SMTP → Tools/Instrumente → Email Test. Introdu o adresă de email pe care o poți citi și trimite testul.',
        'Deschide inboxul și Spam. Un mesaj de succes în WordPress înseamnă că serviciul a acceptat trimiterea, nu dovedește că mesajul a ajuns în inbox. Verificarea reală este primirea mesajului.',
        'Dacă testul eșuează, copiază numai codul erorii și descrierea fără parole. Cere gazdei să verifice portul, autentificarea și accesul SMTP de pe server.',
        'Dacă emailul ajunge în Spam, cere verificarea SPF și DKIM. Acestea sunt înregistrări DNS care arată că serviciul are voie să trimită pentru domeniu. Nu crea două înregistrări SPF separate și nu șterge alte înregistrări după ureche.',
        'După SMTP, intră în Instrumente → CR Print — configurare și verifică destinatarul hi@crprint.ro. Trimite formularul Contact dintr-un browser obișnuit și verifică mesajul în inbox și în Solicitări 3D.',
        'În WooCommerce → Setări → Emailuri verifică destinatarul emailului Comandă nouă, numele expeditorului și emailurile activate. Fă o comandă de probă și verifică atât emailul atelierului, cât și al cumpărătorului.'
    ])+note('<strong>Local:</strong> WordPress-ul de pe 9400 păstrează solicitările, dar blochează intenționat emailul extern. Configurează și verifică SMTP pe copia de lucru a găzduirii. Instalarea ZIP-urilor pe găzduire nu activează protecția locală CRPRINT_LOCAL_DEMO.')+source('Configurarea Other SMTP','https://wpmailsmtp.com/docs/how-to-set-up-the-other-smtp-mailer-in-wp-mail-smtp/'))
    add('email','brevo-concret','8. Alternativă: Brevo, dacă gazda nu oferă SMTP bun',steps([
        'Deschide site-ul oficial Brevo și compară planul gratuit cu necesarul tău. Limita și funcțiile pot evolua; nu cumpăra un plan numai pentru a trimite primele solicitări.',
        'Creează un cont al firmei și confirmă emailul. În setările expeditorilor/domeniilor adaugă crprint.ro. Brevo îți afișează înregistrările DNS necesare.',
        'Trimite gazdei exact acele înregistrări sau introdu-le în panoul DNS dacă știi unde se gestionează domeniul. Nu schimba nameserverele și nu șterge MX-urile pentru această operațiune: MX controlează unde primești email.',
        'Revino în Brevo și apasă verificarea/autentificarea domeniului după propagarea DNS. Adaugă expeditorul hi@crprint.ro.',
        'În setările SMTP & API generează cheia necesară integrării Brevo. Cheia API este o parolă pentru aplicație; păstreaz-o privată.',
        'În WP Mail SMTP → Settings selectează Brevo, introdu cheia API și salvează. Păstrează From Email hi@crprint.ro și numele CR Print 3D.',
        'Rulează Email Test, citește emailul primit, apoi testează formularul și comanda WooCommerce. Nu configura în paralel două pluginuri SMTP pentru aceleași emailuri.',
        'Emailul de ofertare sau de comandă este tranzacțional. Nu introduce automat persoanele din formular într-o listă de marketing fără acordul corespunzător.'
    ])+source('Integrarea Brevo în WP Mail SMTP','https://wpmailsmtp.com/docs/how-to-set-up-the-sendinblue-mailer-in-wp-mail-smtp/'))
    add('promovare','alegere-oferta','6. Oferta de început și clienții potriviți CR Print', '<div class="comparison"><div><h3>Servicii locale, intenție clară</h3><p>Prototipuri, carcase, suporturi și piese pentru proiecte. Pagina de destinație explică materialul, ce fișier trimiți și cum primești estimarea. O solicitare este bună dacă poți produce piesa, ai informații suficiente și rămâne marjă.</p></div><div><h3>Produse vizuale</h3><p>Macheta navală pentru pasionați, decor sau cadouri. Pagina produsului trebuie să aibă dimensiuni, termen, fotografii ale obiectului fabricat și condiții clare. Modelul digital are un public diferit și o licență distinctă.</p></div></div><p>Acestea sunt ipoteze de test pentru atelier, nu rezultate de piață demonstrate. Începe cu oferta pe care o poți livra cel mai ușor și profitabil. Evită afirmații de utilizare medicală, rezistență certificată sau siguranță pentru piese critice dacă nu ai validarea necesară.</p>'+steps([
        'Alege pentru prima lună o singură ofertă: de exemplu printare FDM la comandă în Constanța. Nu amesteca cinci tehnologii, macheta și fișierul digital într-un singur anunț.',
        'Alege o pagină de destinație: printare-fdm pentru serviciu, produsul navei pentru machetă. Verifică pe telefon că prețul de pornire și contactul sunt ușor de găsit.',
        'Pregătește trei exemple reale și un video de proces. Imaginile generate sunt potrivite pentru concepte; nu le prezenta ca dovezi ale unor comenzi fabricate.',
        'Cu 300 lei/lună ai aproximativ 9,87 lei/zi ca medie Google; cu 600 lei, aproximativ 19,74 lei/zi. Alege un canal plătit. Nu împărți 450 lei în patru campanii active.',
        'Dacă alegi Google Search, caută cereri cu intenție. Dacă alegi Meta, începe cu o ofertă vizuală și formular de solicitare. Pentru TikTok păstrează conținut organic la acest buget.',
        'Răspunde solicitărilor în program. Notează câte au informații suficiente, câte primesc ofertă și câte devin comenzi profitabile. Nu judeca testul numai după aprecieri sau numărul de clickuri.'
    ]))
    add('google','google-click','6. Prima campanie Google Search, de la ecranul gol',steps([
        'Intră în Google Ads cu contul firmei. Creează contul dacă lipsește. Alege România pentru facturare, RON pentru monedă și fusul orar potrivit. Verifică atent înainte de confirmare; moneda nu este o setare pe care să o schimbi ușor ulterior.',
        'Dacă asistentul împinge o campanie automată, caută opțiunea de configurare manuală/mai multe opțiuni. Numele butoanelor poate varia. Scopul este o campanie de tip Căutare/Search, nu un tip ales automat fără verificare.',
        'În Campanii apasă plus → Campanie nouă. Alege obiectivul Solicitări/Leads dacă ai măsurarea funcțională sau Creează fără îndrumarea unui obiectiv. Selectează Căutare/Search.',
        'Introdu URL-ul paginii FDM publicate și numește campania <code>RO | Constanta | FDM | Search</code>. Selectează numai conversiile relevante. O simplă vizualizare de pagină nu este o solicitare.',
        'Pentru un test inițial fără istoric poți folosi Maximizează clickurile cu plafon de CPC, dacă interfața oferă opțiunea. CPC este costul unui click. Plafonul se alege din estimarea de piață și marjă, nu după o cifră universală. După conversii corect măsurate și suficiente date reevaluezi strategia.',
        'În Rețele debifează Rețeaua de display. Pentru un prim test controlat poți debifa și partenerii de căutare. Păstrează căutările Google.',
        'În Locații caută Constanța sau o rază potrivită atelierului. În Opțiuni locație selectează Prezență: persoane aflate sau prezente regulat în zona vizată. Nu lăsa automat prezență sau interes dacă vrei un test local.',
        'La Limbă începe cu română; dacă alegi și engleză, reclama și pagina trebuie să rămână inteligibile publicului vizat. La Programare reclame alege orele în care poți gestiona cererile sau păstrează toate orele dacă formularul este fluxul principal.',
        'Creează un grup de anunțuri FDM. Introdu cuvinte restrânse din lista de mai sus, fiecare pe un rând. Parantezele pătrate înseamnă potrivire exactă; ghilimelele potrivire expresie. Acestea pot include variante apropiate, nu garantează că se caută exact aceleași litere.',
        'Scrie reclama responsivă cu titluri distincte și descrieri clare. URL final: pagina FDM, nu pagina principală dacă oferta este FDM. Verifică limitele de caractere afișate de platformă și previzualizarea pe mobil.',
        'Adaugă linkuri de site spre Contact, Prețuri/Servicii și Portofoliu, dacă paginile sunt publicate. Adaugă telefonul atelierului dacă răspunzi în intervalul stabilit.',
        'La Buget introdu media zilnică: bugetul lunar împărțit la 30,4. De exemplu 450 / 30,4 ≈ 14,80 lei. Google poate cheltui mai mult într-o anumită zi în limitele oficiale; acesta nu este un plafon fix pe fiecare zi.',
        'În ecranul de revizuire verifică locația, rețelele, bugetul, pagina, facturarea și conversiile. Creează campania și pune-o pe Pauză până când ai verificat măsurarea și formularul. Publicarea/activarea începe consumul de buget.',
        'În Cuvinte cheie → Cuvinte cheie negative adaugă excluderile potrivite: gratis, curs, job, imprimantă de cumpărat, tutorial etc. Nu exclude „model” sau „piesă” dacă acestea sunt chiar intențiile dorite.',
        'După activare, în Termeni de căutare verifică ce au căutat oamenii. Elimină căutările irelevante, verifică solicitările primite și notează costul. La buget mic, câteva clickuri nu oferă o concluzie statistică solidă.'
    ])+source('Crearea unei campanii Google Ads','https://support.google.com/google-ads/answer/6324971?hl=ro')+source('Bugete și limite de cheltuieli','https://support.google.com/google-ads/answer/2375454?hl=ro'))
    add('google','masurare-click','7. Măsurare: configurare minimă înainte să optimizezi',steps([
        'Separă două rezultate: <strong>solicitare</strong> și <strong>cumpărare</strong>. Clickul pe telefon sau WhatsApp este un semnal de interes; nu dovedește că ai primit o cerere calificată sau bani.',
        'Pentru început ține un tabel privat cu data, sursa declarată de client, serviciul, oferta, comanda și venitul. Întreabă natural „De unde ai aflat de noi?”. Acest tabel funcționează și înainte de instrumentele automate.',
        'Pentru instrumente Google, instalează Site Kit by Google din directorul oficial WordPress. Deschide Site Kit → Start setup și conectează contul firmei. Confirmă domeniul public și Search Console. Nu conecta localhost ca site de producție.',
        'Analytics/Ads adaugă măsurare și cerințe de consimțământ. Configurează mai întâi o platformă de consimțământ compatibilă. O opțiune este CookieYes plus WP Consent API; verifică planul și limitele disponibile înainte de alegere.',
        'Site Kit → Settings → Admin Settings permite configurarea Consent mode. Folosește un singur sistem pentru semnalele Google; nu activa în paralel setări contradictorii în Site Kit și în platforma de consimțământ.',
        'În Site Kit → Settings → Connected Services → Analytics conectează sau creează proprietatea Google Analytics a firmei. În Ads conectează contul publicitar dacă alegi integrarea respectivă. Nu conecta AdSense: acela este pentru afișarea de reclame ale altora pe site.',
        'Site Kit → Settings → Connected Services → Analytics sau Ads → Edit → Plugin conversion tracking poate detecta WooCommerce. Formularul nostru CR Print Core nu este în lista formularelor suportate automat; pentru el tema include evenimentul verificat crprint_contact_success, care trebuie conectat separat.',
        'În Google Ads → Obiective → Conversii → Rezumat → Conversie nouă selectează Site web. Definește Achiziție cu valoare/monedă și identificator de tranzacție pentru WooCommerce. Dacă imporți din Analytics, selectează evenimentul verificat. Nu înregistra aceeași achiziție ca obiectiv principal prin două metode.',
        'Pentru formularul personalizat folosește evenimentul crprint_contact_success inclus, emis numai după înregistrarea verificată de server. Nu folosi clickul pe buton ca echivalent al trimiterii și nu trimite nume, email, telefon sau textul mesajului în Analytics.',
        'Folosește Tag Assistant/diagnosticul conversiei, fă o comandă de probă și confirmă evenimentul o singură dată, cu valoarea și moneda corecte. Testează și refuzul consimțământului. Nu folosi datele de test pentru evaluarea vânzărilor.',
        'Dacă măsurarea nu este încă verificată, păstrează obiectivele nesigure ca secundare și monitorizează manual cererile. Nu activa o strategie de optimizare pentru conversii care sunt în realitate doar pagini vizitate.'
    ])+source('Site Kit — instalare','https://sitekit.withgoogle.com/documentation/getting-started/install/')+source('Site Kit — Consent mode','https://sitekit.withgoogle.com/documentation/using-site-kit/consent-mode/')+source('Site Kit — plugin conversion tracking','https://sitekit.withgoogle.com/documentation/using-site-kit/plugin-conversion-tracking/')+source('CookieYes — configurare WordPress','https://www.cookieyes.com/documentation/cookieyes-plugin-setup/'))
    add('google','contact-event','8. Conectează formularul CR Print la Google Tag Manager',steps([
        'Acest pas este opțional până când activezi măsurarea. Tema emite crprint_contact_success numai pentru o solicitare înregistrată, fără nume, email, telefon sau mesaj. Nu trimite date personale ca parametri de analiză.',
        'În Google Tag Manager creează un cont al firmei și un container Web pentru crprint.ro. Containerul primește un cod GTM-… . În Site Kit → Settings → Connect More Services → Tag Manager conectează containerul. Nu instala încă un plugin care îl încarcă a doua oară.',
        'În Analytics → Administrare → Fluxuri de date → fluxul Web găsește ID-ul de măsurare G-… . Folosește proprietatea corectă, aceeași conectată în Site Kit.',
        'În Tag Manager → Triggers/Declanșatoare → New/Nou → Custom Event/Eveniment personalizat. Nume eveniment: crprint_contact_success. Nume declanșator: CR Print — solicitare înregistrată. Salvează.',
        'În Tags/Etichete → New/Nou alege Google Analytics: GA4 Event. Introdu ID-ul de măsurare al proprietății. Nume eveniment trimis: generate_lead. Atașează declanșatorul creat. Salvează.',
        'Verifică în Consent Settings/Setări consimțământ cum este controlată eticheta. Pentru un flux în care eticheta trebuie blocată înainte de acord, configurează cerința analytics_storage și verifică acest comportament cu platforma de consimțământ. Nu considera bannerul suficient fără test.',
        'Apasă Preview/Previzualizare, conectează pagina Contact publică și trimite o solicitare de probă. Trebuie să apară crprint_contact_success, iar eticheta generate_lead să fie declanșată conform alegerii de consimțământ. Un formular invalid nu trebuie să declanșeze conversia.',
        'În Analytics DebugView/raportul în timp real verifică generate_lead. În Tag Manager apasă Submit/Trimite pentru a publica versiunea verificată. Dă-i un nume clar, de exemplu „Formular CR Print, prima versiune”.',
        'În Analytics → Administrare → Evenimente marchează generate_lead ca eveniment cheie când este disponibil. Leagă contul Google Ads. În Google Ads → Obiective → Conversii importă evenimentul verificat din proprietatea Analytics.',
        'Pentru solicitări folosește numărarea potrivită unui lead, nu valoarea unei vânzări presupuse. Verifică diagnosticul și păstrează numai o conversie principală pentru aceeași acțiune. O solicitare înregistrată nu înseamnă automat solicitare calificată.'
    ])+source('Declanșator pentru eveniment personalizat','https://support.google.com/tagmanager/answer/7679219?hl=ro')+source('Etichete GA4 Event','https://support.google.com/tagmanager/answer/13034206?hl=ro')+source('Conversii din Analytics în Google Ads','https://support.google.com/google-ads/answer/2375435?hl=ro'))
    add('meta','meta-click','6. Facebook și Instagram: prima reclamă cu formular',steps([
        'Pregătește pagina Facebook CR Print 3D și un cont profesional Instagram. Completează telefonul, emailul, Constanța și adresa site-ului. În Meta Business Suite verifică faptul că firma controlează aceste pagini.',
        'În setările portofoliului de afaceri adaugă/selectează pagina, contul Instagram și contul publicitar. Dacă sunt administrate de altcineva, cere acces prin roluri; nu împărți parola personală.',
        'Deschide Ads Manager/Managerul de reclame. Verifică țara, moneda RON, fusul orar și facturarea contului. Activează autentificarea în doi pași pentru persoanele cu acces.',
        'Apasă Creează → Solicitări/Leads. Nume: <code>CR Print | Constanta | Oferta FDM</code>. Pentru primul test alege un singur set de reclame și un buget pe care îl poți controla.',
        'La locația conversiei alege Formulare instantanee/Instant forms dacă vrei solicitări în Meta. Această variantă nu cere un pixel pe site ca să primească formularul, dar ai nevoie de linkul politicii reale de confidențialitate.',
        'În setul de reclame selectează pagina firmei, bugetul zilnic și intervalul. Dacă folosești 450 lei pentru o lună de 30 zile, reperul este 15 lei/zi. Verifică restricțiile și limitele contului, nu presupune că media zilnică este un plafon rigid.',
        'Public țintă: adulți din Constanța/zona de lucru sau România numai dacă oferta poate fi livrată național. Începe cu o audiență rezonabilă, nu cu multe interese suprapuse. Verifică exact opțiunile disponibile în cont.',
        'La plasamente poți folosi Advantage+ dacă materialele arată bine în toate previzualizările. Dacă faci un test doar Facebook/Instagram, controlează plasamentele și exclude suprafețele nepotrivite. Nu tăia plasamente fără un motiv verificabil.',
        'În reclamă selectează identitatea Facebook și Instagram. Încarcă un video vertical de 10–20 secunde cu obiectul real și procesul. Creează încă o reclamă în același set, cu o imagine reală bună. Nu crea zece seturi cu bugete foarte mici.',
        'Text exemplu: „Ai o schiță sau un model 3D? Îl transformăm într-o piesă. FDM și SLA în Constanța, cu livrare în România. Trimite detaliile pentru o estimare.” Folosește această afirmație numai pentru oferta și livrarea efectiv disponibile.',
        'Apasă Creează formular. Nume: Solicitare proiect 3D. Alege varianta cu pas de revizuire/intenție mai mare, dacă este disponibilă. Titlu: Spune-ne ce vrei să realizăm.',
        'Cere nume și o metodă de contact. Adaugă întrebări de calificare: „Ce obiect vrei?”, „Ai model 3D sau o schiță?”, „Dimensiuni și cantitate?” și „Când ai nevoie de el?”. Nu cere date sensibile inutile.',
        'La Confidențialitate introdu adresa politicii publicate pe crprint.ro. La ecranul de final explică următorul pas: răspuns în timpul programului și contactul atelierului. Nu promite un termen pe care nu îl poți respecta.',
        'Previzualizează formularul și reclama pe fiecare plasament, verifică ortografia și decuparea textului. Publică numai după ce sunt corecte. Campania începe să consume bani când este activă și aprobată.',
        'În Business Suite → Centrul de solicitări/Leads Center sau instrumentele formularelor verifică cererile primite. Descarcă-le numai într-un loc privat și răspunde în program. Nu le lăsa neprocesate zile întregi.',
        'În Ads Manager compară Cost pe solicitare cu <strong>Cost pe solicitare calificată</strong> calculat din tabelul tău. Cinci persoane fără proiect concret pot valora mai puțin decât o singură cerere bună.'
    ])+source('Meta — formulare pentru solicitări','https://www.facebook.com/business/ads/lead-ads'))
    add('meta','meta-site','7. Când trimiți reclama către magazin', '<p>Pentru vânzarea machetei poți alege obiectivul Vânzări/Sales și Site web ca destinație. Fă acest lucru după ce produsul, plata, transportul și emailurile sunt verificate. La un buget mic nu porni simultan și campania de solicitări, și încă o campanie de magazin fără un motiv.</p>'+steps([
        'În Events Manager/Managerul de evenimente creează sau selectează sursa de date a firmei. Folosește integrarea oficială WooCommerce/Meta disponibilă și documentată pentru versiunea ta.',
        'Conectează contul firmei și verifică ce acces ceri. Configurează consimțământul înainte de activarea pixelului. O integrare instalată nu garantează că un vizitator care refuză este respectat.',
        'În Test Events/Evenimente de test vizitează un produs, adaugă în coș și efectuează o comandă de probă. Verifică ViewContent, AddToCart și Purchase unde sunt implementate.',
        'Dacă browserul și serverul trimit aceeași cumpărare, verifică deduplicarea. Nu instala două pluginuri care trimit Purchase pentru aceeași comandă. Nu adăuga manual cod pixel dacă integrarea îl adaugă deja.',
        'În reclama de vânzare folosește pagina exactă a machetei, poze ale obiectului fabricat, preț și termen. Păstrează randările etichetate ca randări.',
        'Nu trimite emailurile sau textul solicitărilor în parametrii URL. Parametri precum utm_source=instagram și utm_campaign=nava sunt pentru identificarea campaniei, nu pentru identificarea persoanei.'
    ])+source('Meta — integrarea WooCommerce','https://woocommerce.com/document/facebook-for-woocommerce/'))
    add('tiktok','tiktok-click','5. TikTok organic: prima lună, concret',steps([
        'Pe contul CR Print completează numele atelierului, Constanța și o descriere scurtă: „Printare, modelare și scanare 3D. Idei digitale, obiecte reale.” Verifică opțiunile de link disponibile pentru tipul contului.',
        'Filmează cu telefonul vertical, cu lumină bună și fundal ordonat. Înregistrează procesul și obiectul real. Nu ai nevoie de cameră scumpă pentru primele clipuri.',
        'Clip 1: în primele două secunde arată obiectul finit, apoi modelul și imprimarea. Text: „De la fișier la piesa pe care o ții în mână”. Încheie cu „Trimite modelul pentru o estimare”.',
        'Clip 2: arată o piesă practică și spune ce problemă rezolvă. Explică materialul și limitele reale. Clip 3: arată un detaliu de modelare sau scanare.',
        'Publică trei clipuri pe săptămână timp de patru săptămâni. Nu schimba stilul și oferta după fiecare postare. Răspunde la comentarii și notează întrebările utile pentru paginile site-ului.',
        'Pentru un cont comercial folosește sunete pe care ai dreptul să le utilizezi, inclusiv biblioteca comercială TikTok atunci când este disponibilă. O melodie populară nu este automat licențiată pentru reclamă.',
        'Urmărește retenția, vizitele profilului și solicitările reale. O vizualizare nu este o comandă. Păstrează cel mai clar clip ca material pentru un eventual test plătit ulterior.'
    ])+'<h3>Un scenariu de 15 secunde pentru nava „24 Septembrie”</h3><ol><li>0–2 secunde: nava întreagă, cu textul „Un model. Sute de detalii.”</li><li>2–6 secunde: rotire în vizualizator și un detaliu al geometriei.</li><li>6–11 secunde: procesul real de fabricare sau macheta reală, dacă este deja produsă.</li><li>11–15 secunde: varianta fizică/digitală și îndemnul „Vezi modelul în magazin”. Dacă ai numai randări, spune clar că sunt randări.</li></ol>')
    add('tiktok','tiktok-ads-click','6. TikTok Ads: pașii când ai buget separat',steps([
        'Intră în TikTok for Business/Ads Manager și creează contul firmei cu datele reale. Completează țara, moneda și facturarea. Verifică pragurile minime în interfață înainte să aloci buget.',
        'În Assets/Tools → Events creează/selectează sursa pentru site dacă vrei conversii pe site. Folosește integrarea oficială WooCommerce disponibilă și testează evenimentele cu consimțământ configurat.',
        'În Campaign → Create alege obiectivul care corespunde rezultatului: solicitări sau vânzări pe site. Nu alege trafic și apoi evalua campania ca și cum ar fi optimizată pentru cumpărări.',
        'La grupul de reclame selectează România sau zonele disponibile potrivite. Nu presupune că poți selecta Constanța în orice cont. Verifică vârsta, programul, plasamentele și minimul de buget.',
        'Folosește un singur grup și două sau trei clipuri verticale pe care le-ai verificat organic. Păstrează mesajul important în zona sigură a previzualizării, fără elemente acoperite de butoane.',
        'Dacă folosești Spark Ads, autorizează postarea contului propriu prin fluxul oficial. Nu presupune că poți transforma în reclamă orice clip al altcuiva.',
        'Introdu pagina produsului/serviciului, verifică parametrii campaniei și evenimentul de optimizare. Revizuiește bugetul și pune campania pe pauză până când testul conversiilor este corect.',
        'După activare, compară solicitările calificate și marja cu cheltuiala. Nu crește bugetul numai fiindcă video-ul are multe vizualizări. La 300–600 lei lunar, recomandarea de început rămâne conținut organic aici și un singur alt canal plătit.'
    ])+source('TikTok — bugete minime','https://ads.tiktok.com/help/article/budget?lang=en'))
    add('lansare','publicare-click','7. Ziua publicării: ce faci și în ce ordine',steps([
        'Confirmă cu gazda cum se publică staging-ul. Nu apăsa un buton care copiază întreaga bază peste site-ul public fără să știi dacă există comenzi noi sau alte date care s-ar pierde.',
        'Fă un backup complet imediat înainte de schimbare și notează punctul de restaurare. Notează cine poate face restaurarea dacă publicarea eșuează.',
        'Verifică documentele comerciale, prețurile și specificațiile. Aspectul actual al site-ului nu afișează avertismente de demonstrație; această alegere nu înlocuiește informațiile obligatorii pentru vânzarea reală.',
        'Confirmă că pe găzduire nu este activă constanta CRPRINT_LOCAL_DEMO. Ea aparține numai lansatorului local. Nu copia fișierele serverului de exercițiu ca soluție de hosting.',
        'Verifică HTTPS, adresa WordPress și adresa site-ului în Setări → General. Un certificat valid trebuie să acopere domeniul final. Nu schimba aceste adrese fără un plan de acces/restaurare.',
        'Publică tema și paginile prin procedura gazdei. Golește cache-ul site-ului și al CDN-ului dacă există. Verifică într-o fereastră privată, fără cont de administrator.',
        'În Setări → Citire debifează Descurajează motoarele de căutare pe site-ul public. Lasă această opțiune activă pe staging. Ghidul și administrarea locală nu trebuie publicate ca pagini comerciale.',
        'Testează telefonul, emailul, formularul, harta la cerere, meniul mobil, coșul și finalizarea. Fă o comandă controlată cu plata potrivită și verifică emailurile, statusul și fișierul digital.',
        'Deschide vechile adrese importante de pe crprint.ro. Dacă s-au schimbat, configurează redirecționări 301 spre paginile echivalente. Nu redirecționa toate paginile greșite spre Acasă.',
        'În Google Search Console selectează proprietatea domeniului și trimite sitemapul generat de WordPress/pluginul SEO ales. Nu încărca sitemap.xml al prototipului dacă URL-urile magazinului sunt diferite.',
        'Verifică paginile de servicii: un titlu principal, o descriere clară, Constanța, telefon și o întrebare/ofertă utilă. Imaginile trebuie să aibă text alternativ, iar performanța se verifică pe telefon și conexiune mobilă.',
        'Activează reclama numai după aceste verificări. În primele zile verifică zilnic cererile, comenzile, emailurile și erorile. Păstrează o metodă de contact direct chiar dacă formularul are o problemă.'
    ]))
    add('depanare','erori-concrete','4. Dacă ceva nu merge: pași simpli', '<h3>„Catalogul nu se poate încărca” pe computer</h3>'+steps([
        'Verifică dacă fereastra Start-Demo este încă deschisă. Dacă nu, pornește Start-Demo.cmd.',
        'Deschide adresa cu portul 4173. O pagină deschisă direct ca fișier nu are server pentru salvarea comenzilor. Reîncarcă pagina o singură dată.',
        'Dacă apare „port ocupat”, există deja un server pe acel port. Nu porni copii repetate. Oprește fereastra veche cu Ctrl+C sau pornește explicit pe alt port.',
        'În WordPress, magazinul gol se verifică altfel: WooCommerce activ, produse publicate, vizibilitate catalog și stoc. Catalogul WordPress nu citește data/catalog.json.'
    ])+'<h3>Tema ZIP este prea mare sau „lipsește style.css”</h3>'+steps([
        'Verifică că ai ales wordpress/crprint-studio.zip, nu ZIP-ul întregului GitHub. Arhiva temei trebuie să conțină folderul crprint-studio cu style.css.',
        'Dacă limita de încărcare este prea mică, cere gazdei să o mărească sau să instaleze tema prin SFTP. Nu elimina fișiere la întâmplare ca să faci ZIP-ul mai mic.',
        'Pentru o actualizare, păstrează backupul și confirmă în ecranul WordPress înlocuirea versiunii existente numai dacă arhiva este noua versiune a aceleiași teme.'
    ])+'<h3>Formularul spune succes, dar nu vezi email</h3>'+steps([
        'Pe 4173/9400 este normal ca emailul extern să fie oprit. Verifică solicitarea în administrare/Solicitări 3D.',
        'Pe găzduire verifică mai întâi WP Mail SMTP → Email Test. Dacă nu ajunge, problema nu se rezolvă schimbând textul butonului formularului.',
        'Dacă Email Test ajunge, verifică destinatarul din Instrumente → CR Print — configurare, Spam și filtrele inboxului. Solicitarea este salvată separat în WordPress.',
        'Dacă verificarea anti-spam expiră imediat, exclude pagina Contact din cache și reîncarcă. Tokenurile și calculele nu trebuie păstrate într-o copie veche a paginii.'
    ])+'<h3>Produsul digital nu are descărcare</h3>'+steps([
        'Verifică produsul: Virtual și Descărcabil bifate, fișier adăugat, produs salvat.',
        'Verifică statusul comenzii și plata. În așteptare nu înseamnă plată confirmată.',
        'Verifică limită, expirare și permisiunile descărcării din comandă. Cere gazdei verificarea metodei de livrare/protecției dacă linkul produce o eroare.'
    ]))
