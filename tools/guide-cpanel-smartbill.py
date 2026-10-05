"""cPanel and SmartBill beginner path, added after the general guide content."""
import re


def adapt(P, block, steps, note, source):
    def replace(key, ident, title, body):
        a, b, c = P[key]
        pattern = r'<section class="chapter-block" id="' + re.escape(ident) + r'">.*?</section>'
        c, count = re.subn(pattern, lambda _: block(ident, title, body), c, flags=re.S)
        if count != 1:
            raise ValueError(f'Missing or duplicate guide section: {key}/{ident}')
        P[key] = (a, b, c)

    def append(key, ident, title, body):
        a, b, c = P[key]
        P[key] = (a, b, c + block(ident, title, body))

    table = lambda heads, rows: '<div class="table-wrap"><table><thead><tr>' + ''.join('<th>' + h + '</th>' for h in heads) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + c + '</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>'

    replace('index', 'situatia', 'De unde pornim: cPanel + WordPress + SmartBill',
        note('<strong>Configurația ta:</strong> găzduire administrată prin cPanel și facturare în SmartBill. Nu știm încă firma de hosting, pachetul SmartBill sau instrumentele incluse în cPanel. Ghidul îți arată cum le identifici, fără să presupună că trebuie cumpărate alte abonamente.') +
        '<p>Vei vinde macheta fizică și modelul digital al navei „24 Septembrie”. Prețurile 149/49 lei și transportul de 19 lei sunt valori de exercițiu; le confirmi înainte de publicare. Bugetul pentru reclame rămâne 300–600 lei/lună, separat de costurile tehnice.</p>' +
        table(['Unde intri', 'Ce administrezi', 'Cum îl recunoști'], [
            ['cPanel', 'Găzduirea: fișiere, copii de siguranță, domeniu, PHP și, dacă este inclus, email.', 'Linkul din contul firmei de hosting.'],
            ['WordPress / WooCommerce', 'Paginile, produsele, coșul, comenzile și clienții.', 'Adresa site-ului urmată de /wp-admin/.'],
            ['SmartBill', 'Facturile, încasările și conectarea e-Factura; stocurile doar dacă folosești gestiune.', 'Contul tău din cloud.smartbill.ro.'],
            ['Computerul tău · 4173 / 9400', 'Exercițiile locale și previzualizarea.', 'Start-Demo.cmd / Start-WordPress.cmd.'],
        ]) + '<p><strong>Ordinea:</strong> cPanel → WordPress → magazin → email → SmartBill → lansare → reclame. Cele trei panouri au conturi diferite. O parolă de cPanel nu este automat parola WordPress, a emailului sau a SmartBill.</p>')

    a, b, c = P['index']
    c = c.replace('<tr><td>Reclame</td>', '<tr><td>SmartBill</td><td>Folosești întâi abonamentul existent; verifici eligibilitatea API</td><td>Fără un upgrade presupus; facturare manuală dacă integrarea nu este inclusă</td></tr><tr><td>Reclame</td>')
    c = c.replace('Ca plafon de planificare, poți căuta hosting în jur de 30–60 lei/lună.', 'Ai deja găzduire cu cPanel: verifică întâi costul și resursele pachetului actual. Numai dacă trebuie schimbat, poți folosi 30–60 lei/lună ca plafon orientativ de planificare.')
    P['index'] = (a, b, c)

    replace('index', 'trusa', 'Pregătește fișa privată pentru cPanel și SmartBill', steps([
        'Deschide un document privat pe computer și numește-l „Date pentru lansarea CR Print”. Nu îl adăuga în folderul public al site-ului sau în GitHub.',
        'Notează firma de hosting, linkul contului de client, linkul cPanel și data reînnoirii. cPanel este panoul, nu numele firmei de găzduire. Verifică pe factură cine îți furnizează găzduirea.',
        'În cPanel caută WP Toolkit și WordPress Manager by Softaculous. Notează care există. Notează dacă apare deja crprint.ro în lista instalărilor WordPress.',
        'Notează adresa WordPress a site-ului existent, administratorul și metoda de recuperare. Parolele se păstrează într-un manager de parole, separat de notițele care pot fi trimise suportului.',
        'În SmartBill verifică firma selectată și numele abonamentului. Notează dacă ai acces la Contul meu → Integrări → Informații API. Nu copia tokenul în această fișă sau în capturi.',
        'Notează unde este găzduită hi@crprint.ro. Prezența cPanel nu dovedește că emailul este tot la hosting; poate exista un serviciu extern.',
        'Pregătește datele comerciale confirmate: denumire, CUI/CIF, adresă fiscală, cont bancar, regim TVA, seria de facturare. Adresa atelierului și adresa fiscală pot fi diferite.',
        'Pentru navă: preț real, dimensiuni, material, termen de fabricație, stoc real și drepturi de distribuire a fișierului. Stabilește cu contabilul cum se facturează macheta, fișierul digital, serviciile și transportul.',
    ]))

    P['cpanel'] = ('cPanel de la zero', 'De la prima conectare până la o copie de lucru pregătită pentru tema CR Print.',
        block('panouri', '1. Înțelege ce ai în față',
            '<p>Începe cu două file în browser: una pentru cPanel, una pentru acest ghid. Lucrează pe rând și verifică rezultatul fiecărei etape. Pentru moment, scopul este o copie de lucru separată a site-ului, nu înlocuirea imediată a crprint.ro.</p>' +
            table(['Termen din panou', 'Înseamnă', 'Pentru CR Print'], [
                ['Hosting / găzduire', 'Serviciul care ține site-ul pe internet.', 'Ai deja cPanel; verifică pachetul existent înainte să cumperi altul.'],
                ['Domain / domeniu', 'Numele prin care se deschide site-ul.', 'crprint.ro'],
                ['Subdomain / subdomeniu', 'O adresă separată în același domeniu.', 'staging.crprint.ro este exemplul din ghid, încă necreat.'],
                ['Document Root', 'Folderul servit de adresa respectivă.', 'Îl citești din Domains; nu presupui că toate adresele folosesc public_html.'],
                ['Database / bază de date', 'Conținutul, setările, produsele și comenzile WordPress.', 'Copia de lucru trebuie să aibă bază separată.'],
                ['Staging / copie de lucru', 'Site separat pe care pregătești schimbările.', 'Îl verifici înainte de publicare.'],
            ]) +
            note('Adresele staging.crprint.ro din acest capitol sunt exemple de configurare. Nu presupune că acea adresă există deja. Mai întâi creezi copia și verifici domeniul rezultat.')) +
        block('conectare', '2. Prima conectare în cPanel', steps([
            'Intră pe site-ul firmei de hosting pe care îl folosești deja. Deschide contul de client cu datele tale. Nu trebuie să trimiți nimănui parola pentru a urma ghidul.',
            'Caută Servicii / Găzduire / Hosting. Alege pachetul pentru crprint.ro, apoi butonul Conectare cPanel / Login to cPanel. Dacă ai deja linkul oficial de cPanel în emailul gazdei, îl poți folosi.',
            'Pe pagina principală cPanel găsește câmpul de căutare. Folosește-l pentru numele în engleză din acest ghid. Panoul poate fi tradus, dar denumirile în engleză te ajută să găsești aceleași funcții.',
            'Caută Domains. Identifică crprint.ro și notează Document Root. Nu modifica domeniul sau folderul în această etapă.',
            'Revino la căutare și caută WP Toolkit, apoi Softaculous. Dacă găsești unul dintre ele, deschide lista instalărilor și identifică site-ul existent. Dacă lista este goală, nu instala peste el; folosește Scan / Import dacă există sau cere gazdei să identifice instalarea.',
            'Verifică în contul gazdei spațiul disponibil, backupul inclus și costul reînnoirii. Funcțiile cPanel diferă între pachete; un buton lipsă se clarifică cu suportul, nu prin cumpărarea imediată a altui abonament.',
        ]) + source('cPanel — gestionarea domeniilor', 'https://docs.cpanel.net/cpanel/domains/domains/')) +
        block('backup', '3. Fă prima copie de siguranță', steps([
            'În căutarea cPanel scrie Backup Wizard. Deschide funcția și alege Back Up → Full Backup.',
            'Alege Home Directory ca destinație și emailul tău pentru notificare, apoi Generate Backup. Așteaptă finalizarea; pentru conturi mari poate dura.',
            'Revino în zona de descărcare și descarcă arhiva .tar.gz pe computer. Păstreaz-o într-un folder privat, cu data și numele site-ului. Nu o pune în public_html sau GitHub.',
            'Cere gazdei să confirme procedura de restaurare. cPanel nu restaurează automat backupul complet din panoul obișnuit; restaurarea completă se face prin gazdă/WHM. Nu presupune că butonul Restore poate restaura întreaga arhivă.',
            'Dacă gazda oferă JetBackup sau alt instrument, notează ultima copie validă și cere pașii pentru restaurarea simultană a fișierelor și bazei de date. Acest ghid nu presupune că acel instrument este inclus.',
        ]) + source('cPanel — Backup Wizard și limita restaurării complete', 'https://docs.cpanel.net/cpanel/files/backup-wizard/') +
            '<p><strong>Rezultat:</strong> ai o copie descărcată, o dată și o persoană/procedură pentru restaurare. Backupul este asigurarea revenirii; încă nu este o instalare pe care să editezi pagini.</p>') +
        block('copie-wpt', '4A. Dacă ai WP Toolkit: clonează site-ul', steps([
            'Deschide WP Toolkit în cPanel. În cardul crprint.ro alege Clone / Clonează. Verifică sursa: trebuie să fie site-ul existent, nu o altă instalare.',
            'În fereastra de clonare alege un subdomeniu nou pentru copia de lucru, de exemplu staging.crprint.ro. Verifică destinația afișată; nu trebuie să fie crprint.ro sau folderul site-ului public.',
            'Pornește clonarea cu Start și așteaptă confirmarea. Notează adresa copiei. Dacă apare o opțiune de suprascriere a unei destinații existente, cere gazdei o destinație liberă înainte să continui.',
            'Deschide copia și panoul său /wp-admin/. Verifică că adresa din browser este cea a copiei, inclusiv când editezi o pagină. Continuă cu HTTPS și protejarea copiei de mai jos.',
        ]) + source('cPanel — clonarea WordPress prin WP Toolkit', 'https://support.cpanel.net/hc/en-us/articles/4412719249431-How-do-I-clone-a-WordPress-website') +
            note('Folosești fie ruta WP Toolkit, fie ruta Softaculous. Nu trebuie să creezi două copii de lucru pentru aceleași schimbări.')) +
        block('copie-softaculous', '4B. Dacă ai Softaculous: creează staging', steps([
            'În cPanel deschide WordPress Manager by Softaculous / Softaculous Apps Installer. Intră în All Installations / lista instalărilor.',
            'Identifică instalarea crprint.ro și alege Create Staging. Dacă site-ul instalat anterior nu este în listă, folosește Import/Scan sau cere gazdei să îl înregistreze în Softaculous.',
            'Alege HTTPS și destinația separată disponibilă. Poate fi un subdomeniu pregătit de gazdă sau un folder staging; verifică adresa finală și baza de date nouă afișate în formular.',
            'Apasă Create Staging, așteaptă succesul și deschide linkul rezultat. Verifică că pagina și panoul WordPress se deschid la adresa copiei.',
            'Lasă Push to Live pentru etapa de lansare. Nu este butonul de salvare a unei pagini și poate înlocui fișierele și baza de date ale site-ului public.',
        ]) + source('Softaculous — staging și ce poate înlocui Push to Live', 'https://www.softaculous.com/blog/prevent-breaking-your-live-website-with-our-staging-feature/')) +
        block('instalare-noua', '4C. Dacă nu ai clonare sau nu există WordPress',
            '<p>Dacă WordPress există deja, cea mai simplă rută este să ceri gazdei o copie protejată. Dacă pornești o instalare nouă, folosește o destinație separată și goală. Nu instala peste site-ul existent.</p>' + steps([
            'Trimite suportului mesajul de la finalul capitolului. Cere staging cu bază de date separată, HTTPS și acces de administrator. Această variantă te scutește de configurarea manuală a bazei.',
            'Dacă gazda îți cere să creezi subdomeniul: cPanel → Domains → Create A New Domain. Introdu staging.crprint.ro și dezactivează partajarea folderului cu domeniul principal, dacă opțiunea există. Notează folderul separat propus.',
            'În WP Toolkit → Install WordPress sau în instalatorul WordPress disponibil, selectează numai destinația nouă. Protocol: HTTPS. Nume: CR Print — copie de lucru. Limbă: română. Creează un administrator și salvează parola privat.',
            'Dacă formularul are In Directory și vrei site-ul la rădăcina subdomeniului, lasă acel câmp gol. Dacă scrii wp, adresa va include /wp/. Verifică URL-ul final înainte de instalare.',
            'După confirmare, deschide adresa oferită și /wp-admin/. Dacă lipsesc instalatorul sau drepturile necesare, gazda face această etapă; nu ai nevoie de un VPS pentru a instala tema.',
        ]) + source('cPanel — WP Toolkit pentru instalare și administrare', 'https://docs.cpanel.net/knowledge-base/cpanel-developed-plugins/wp-toolkit/') +
            '<p><strong>Rezultat:</strong> WordPress gol sau copie a site-ului, pe o adresă separată. Capitolul următor instalează tema și conținutul CR Print în această destinație.</p>') +
        block('https', '5. Verifică HTTPS înainte de conectări', steps([
            'Caută SSL/TLS Status în cPanel. În unele versiuni este în SSL/TLS Certificates. Identifică domeniul copiei și crprint.ro.',
            'Verifică dacă certificatul este activ și acoperă adresa folosită. Dacă lipsește, folosește opțiunea AutoSSL oferită de gazdă sau cere emiterea certificatului.',
            'Deschide copia cu https://. Dacă browserul afișează avertisment de certificat, cere gazdei să corecteze certificatul și DNS-ul, apoi verifică din nou.',
        ]) + source('cPanel — SSL/TLS Status', 'https://docs.cpanel.net/cpanel/security/ssl-tls-status/')) +
        block('protectie', '6. Protejează copia și oprește integrările reale', steps([
            'În cPanel caută Directory Privacy. Selectează folderul copiei, folosind Document Root notat. Alege Edit → Password protect this directory, scrie un nume și salvează.',
            'Creează utilizatorul de acces în aceeași pagină și salvează. Aceasta este o autentificare suplimentară înainte de WordPress. Verifică într-o fereastră privată că site-ul cere autentificare.',
            'În WordPress-ul copiei: Setări → Citire → bifează Descurajează motoarele de căutare. Această bifă este o instrucțiune pentru motoare, nu o parolă.',
        ]) + source('cPanel — Directory Privacy', 'https://docs.cpanel.net/cpanel/files/directory-privacy/') +
            '<h3>Checklist pentru copia unui site comercial</h3>' + steps([
                'Dacă ai clonat un magazin activ, dezactivează pluginul SmartBill în copie înainte să creezi comenzi sau să schimbi statusuri. Clonarea poate copia și tokenul real.',
                'Dezactivează plățile reale și automatizările de facturare, curier sau marketing din copie. Folosește emailuri controlate și date fictive. Cere gazdei/dezvoltatorului blocarea emailurilor externe dacă s-au copiat clienți reali.',
                'Nu conecta tokenul SmartBill real în WordPress-ul local. Pentru exerciții de integrare, folosește numai un cont SmartBill de test confirmat de suport. „Emite ciornă” nu este un sandbox și poate trimite date în contul conectat.',
                'Verifică programările și automatizările copiate înainte de teste. Protecția cu parolă nu oprește cererile trimise de server către SmartBill sau către un serviciu email.',
            ]) + '<p>Pe computer, lansatoarele noastre opresc emailurile externe. Pe o copie creată în hosting aceste protecții locale nu apar automat.</p>') +
        block('php', '7. Pregătește PHP și încărcarea temei',
            '<p>PHP este limbajul în care rulează WordPress. Verifică întâi versiunea pe copia de lucru. Nu schimba versiunea tuturor domeniilor pentru a rezolva o singură instalare.</p>' + steps([
            'În cPanel caută MultiPHP Manager. Identifică domeniul copiei și versiunea curentă. Alege o versiune suportată de WordPress, WooCommerce și pluginurile tale, apoi Apply numai pentru copia de lucru.',
            'Pentru acest proiect, PHP 8.3 sau o versiune mai nouă compatibilă este punctul de plecare. Confirmă cu gazda și testează integrarea SmartBill. Cerințele minime vechi ale unui plugin nu sunt o recomandare să folosești PHP ieșit din suport.',
            'Dacă panoul oferă Select PHP Version în loc de MultiPHP Manager, folosește instrumentul gazdei. Cere-i să confirme extensiile necesare WordPress/WooCommerce și cURL pentru conexiunile către servicii.',
        ]) + source('cPanel — alegerea versiunii PHP', 'https://docs.cpanel.net/cpanel/software/multiphp-manager-for-cpanel/') +
            '<h3>Dacă WordPress refuză ZIP-ul pentru că este prea mare</h3>' + steps([
                'Caută MultiPHP INI Editor → Basic Mode. Selectează domeniul copiei. Dacă opțiunile sunt blocate, cere gazdei modificarea.',
                'Pentru pachetul actual, poți cere upload_max_filesize 32M și post_max_size 40M. Sunt valori propuse pentru încărcare, nu cerințe universale. post_max_size trebuie să fie cel puțin cât upload_max_filesize.',
                'O memorie PHP de 256M este un punct de plecare pentru acest magazin mic; se ajustează după consum și limitele pachetului. Nu rezolvă automat lipsa resurselor de hosting.',
                'Salvează, redeschide încărcarea temei în WordPress și verifică limita afișată. Nu activa afișarea erorilor PHP pentru vizitatori.',
            ]) + source('cPanel — MultiPHP INI Editor', 'https://docs.cpanel.net/cpanel/software/multiphp-ini-editor-for-cpanel/')) +
        block('fisiere', '8. Ce fișiere urci și unde',
            table(['Fișier din proiect', 'Locul corect', 'Rol'], [
                ['wordpress/crprint-studio.zip', 'WordPress → Aspect → Teme → Adaugă → Încarcă temă', 'Designul și componentele comune.'],
                ['wordpress/crprint-core.zip', 'WordPress → Pluginuri → Adaugă → Încarcă modul', 'Formularul și importul structurii.'],
                ['Imagini de produse', 'Editorul produsului WooCommerce / Media', 'Galeria și imaginea principală.'],
                ['Arhiva comercială FBX', 'Produs descărcabil WooCommerce', 'Fișier oferit după plata eligibilă.'],
                ['Start-Demo.cmd, dev-server.mjs, admin.html, ghid/', 'Rămân pe computer', 'Exerciții și documentație locală.'],
            ]) +
            '<p>Nu încărca tot folderul CRPRINT în public_html pentru a obține magazinul WordPress. Instalarea temei și pluginului este ruta pregătită pentru acest proiect. ZIP-ul întregului repository GitHub nu este ZIP de temă.</p>' +
            '<h3>File Manager doar dacă instalarea prin WordPress nu merge</h3>' + steps([
                'În cPanel → File Manager deschide folderul WordPress al copiei. Verifică prezența wp-admin, wp-content și wp-includes.',
                'În wp-content/themes încarcă crprint-studio.zip prin Upload, apoi Extract. Trebuie să rezulte wp-content/themes/crprint-studio/style.css, fără un folder suplimentar deasupra.',
                'În wp-content/plugins încarcă și extrage crprint-core.zip. Trebuie să rezulte wp-content/plugins/crprint-core/crprint-core.php.',
                'Revino în WordPress și activează tema și pluginul. Încărcarea fișierelor nu le activează automat. Dacă sunt versiuni existente, folosește procedura de actualizare cu backup; nu extrage peste ele fără să verifici destinația.',
            ]) + source('cPanel — Upload și Extract în File Manager', 'https://docs.cpanel.net/cpanel/files/file-manager/') +
            '<p>Continuă cu <a href="wordpress.html#instalare-click">instalarea pachetului, clic cu clic</a>, apoi cu <a href="magazin.html">produsele și comenzile</a>.</p>') +
        block('suport', '9. Mesaj gata de copiat pentru gazdă',
            '''<p>Completează numele și trimite acest mesaj prin contul de suport al gazdei. Nu adăuga parole sau tokenuri.</p><pre><code>Bună ziua! Folosesc cPanel pentru crprint.ro și pregătesc un site
WordPress cu temă personalizată, WooCommerce, WP Mail SMTP și SmartBill.
Vă rog să confirmați:
1. pachetul actual, limitele și costul de reînnoire;
2. instalarea WordPress existentă și folderul ei;
3. backup complet și procedura de restaurare;
4. o copie protejată cu parolă, HTTPS și bază separată;
5. WP Toolkit/Softaculous și opțiunile de publicare disponibile;
6. PHP suportat și limitele pentru încărcarea temei ZIP;
7. dacă hi@crprint.ro este la voi și datele SMTP securizate;
8. acces HTTPS/cURL către SmartBill din server.
Vreau să verific copia înainte de înlocuirea site-ului existent.</code></pre>'''))

    replace('wordpress', 'acces', '1. Deschide WordPress-ul pregătit în cPanel',
        note('Urmează întâi <a href="cpanel.html">cPanel de la zero</a>. Acest capitol începe după ce ai copia de lucru și acces de administrator.') + steps([
            'Deschide adresa copiei urmată de /wp-admin/. Dacă ai WP Toolkit, poți folosi și Log in de pe cardul copiei. Verifică domeniul din browser înainte de orice editare.',
            'În WordPress: Setări → General → Limba site-ului: Română. Fus orar: București. Salvează. Meniurile pot fi afișate și în limba contului administratorului.',
            'Dacă nu vezi Aspect și Pluginuri, verifică rolul Administrator sau cere gazdei accesul potrivit. cPanel și WordPress folosesc autentificări diferite.',
            'În Instrumente → Sănătatea site-ului → Informații verifică WordPress, PHP și serverul. Notează versiunile pentru cazul în care un plugin are o problemă.',
        ]))
    replace('wordpress', 'backup', '2. Confirmă că lucrezi pe copia potrivită', steps([
        'Verifică backupul și procedura de restaurare din <a href="cpanel.html#backup">capitolul cPanel</a>. Nu începe instalarea fără să știi cum revii la situația anterioară.',
        'Adresa din browser trebuie să fie copia de lucru. Deschide crprint.ro într-o altă filă și verifică faptul că site-ul public este încă cel existent.',
        'Verifică autentificarea suplimentară a copiei și descurajarea indexării. Dacă ai clonat un magazin, oprește SmartBill, plățile și automatizările reale în copie înainte de exerciții.',
        'Păstrează datele clienților existente în afara exporturilor de probă și a GitHub. Nu transfera comenzile fictive din computer în magazinul public.',
    ]))
    replace('wordpress', 'hosting-concret', '6. Punctul de control: cPanel este pregătit',
        '<p>Dacă încă nu ai o copie funcțională, revino la <a href="cpanel.html">cPanel de la zero</a>. Dacă ai terminat acel capitol, nu mai ai de căutat alt furnizor sau alt panou.</p>' +
        table(['Trebuie să existe', 'Cum verifici'], [
            ['Backup', 'Arhivă descărcată și procedură de restaurare confirmată.'],
            ['Copie separată', 'URL și bază de date diferite de cele ale site-ului public.'],
            ['HTTPS și acces privat', 'Certificat valid și autentificare înainte de WordPress.'],
            ['Administrator WordPress', 'Vezi meniurile Aspect și Pluginuri.'],
            ['Fișierele proiectului', 'Ai cele două ZIP-uri din folderul wordpress.'],
        ]))

    replace('email', 'inbox', '2. Identifică inboxul hi@crprint.ro în cPanel', steps([
        'În cPanel caută Email Accounts. Identifică hi@crprint.ro. Dacă există, apasă Check Email și deschide webmailul disponibil pentru a verifica mesajele.',
        'Dacă adresa nu există, confirmă întâi cu gazda unde este găzduit emailul. Dacă există la un serviciu extern, folosești datele acelui serviciu; nu recreezi aceeași adresă în cPanel și nu schimbi MX la întâmplare.',
        'Dacă gazda confirmă că emailul este local și adresa trebuie creată: Email Accounts → Create. Domeniu: crprint.ro. Nume: hi. Alege o parolă puternică și o cotă de spațiu potrivită, apoi Create. Păstrează parola privat.',
        'Dintr-un alt inbox controlat trimite un mesaj către hi@crprint.ro. Deschide webmailul și răspunde. Continuă cu SMTP după ce primirea și răspunsul funcționează.',
    ]) + source('cPanel — crearea unei căsuțe email', 'https://docs.cpanel.net/cpanel/email/create-an-email-account/'))
    replace('email', 'smtp', '3. Ia parametrii SMTP din cPanel', steps([
        'În Email Accounts, lângă hi@crprint.ro, apasă Connect Devices. Găsește zona Mail Client Manual Settings / Secure SSL/TLS Settings.',
        'Notează serverul de ieșire, portul SMTP, criptarea și utilizatorul. Folosește valorile afișate pentru contul tău; nu presupune că serverul este mail.crprint.ro.',
        'Parola este a căsuței email, nu a cPanel sau WordPress. IMAP și POP sunt pentru primire; în WP Mail SMTP ai nevoie de datele SMTP pentru trimitere.',
        'Dacă valorile sau criptarea nu sunt clare, cere gazdei combinația exactă. 465/SSL și 587/TLS sunt exemple uzuale, nu valori confirmate pentru contul tău.',
    ]) + source('cPanel — Connect Devices și setările securizate', 'https://docs.cpanel.net/cpanel/email/set-up-mail-client/'))
    replace('email', 'smtp-concret', '7. Completează WP Mail SMTP cu datele din cPanel',
        table(['Câmp în WordPress', 'Valoare pentru proiect'], [
            ['From Email', 'hi@crprint.ro, dacă aceasta este căsuța autentificată.'],
            ['From Name', 'CR Print 3D'],
            ['Mailer', 'Other SMTP pentru emailul găzduirii.'],
            ['SMTP Host / Port / Encryption', 'Datele securizate din Connect Devices, confirmate de gazdă.'],
            ['Authentication / Username / Password', 'Autentificare activă; utilizatorul și parola căsuței.'],
        ]) + '<p>În WP Mail SMTP → Setări → General completează câmpurile, activează Force From Email dacă același expeditor trebuie folosit peste tot și salvează. În Tools/Instrumente → Email Test trimite către un inbox controlat și verifică primirea. Other SMTP păstrează credențialele în WordPress: limitează administratorii și actualizează setarea când schimbi parola emailului.</p>' +
        source('WP Mail SMTP — câmpuri și testul Other SMTP', 'https://wpmailsmtp.com/docs/how-to-set-up-the-other-smtp-mailer-in-wp-mail-smtp/') +
        '<p>Pentru CR Print, verifică separat destinatarul din Instrumente → CR Print — configurare și notificarea WooCommerce → Setări → Emailuri → Comandă nouă. Apoi trimite formularul și verifică Solicitări 3D, inboxul și Reply-To. WP Mail SMTP nu configurează emailurile trimise direct de SmartBill Cloud.</p>')
    append('email', 'dns-cpanel', '9. Dacă emailul ajunge în Spam: SPF și DKIM în cPanel', steps([
        'În cPanel caută Email Deliverability și selectează Manage pentru crprint.ro. Verifică starea SPF și DKIM.',
        'Dacă cPanel gestionează DNS-ul autoritar, gazda îți poate confirma dacă Repair poate publica valorile recomandate. Dacă DNS-ul este în alt serviciu, valorile se adaugă acolo, nu doar în copia locală a zonei cPanel.',
        'Trimite gazdei valorile recomandate și lista serviciilor care trimit deja pentru domeniu. Cere un SPF coerent, fără două înregistrări SPF separate, și verificarea DKIM/DMARC. Nu înlocui înregistrările existente cu unele ghicite.',
        'Repetă testul către două inboxuri și verifică Spam. Dacă mesajele nu se livrează, cere și verificarea reputației serverului și limitelor de trimitere ale pachetului.',
    ]) + source('cPanel — Email Deliverability', 'https://docs.cpanel.net/cpanel/email/email-deliverability-in-cpanel/'))

    P['smartbill'] = ('SmartBill & facturare', 'De la verificarea abonamentului până la prima comandă facturată corect.',
        block('rol', '1. Ce face SmartBill în magazinul tău',
            '<p><strong>Fluxul propus:</strong> clientul comandă în WooCommerce → tu verifici comanda și plata → emiți factura în SmartBill → pregătești livrarea sau accesul digital → urmărești încasarea și statusul e-Factura.</p>' +
            table(['Element', 'Unde îl verifici', 'Ce dovedește'], [
                ['Comandă', 'WooCommerce → Comenzi', 'Ce a cerut clientul și ce total are comanda.'],
                ['Plată', 'Bancă / procesator / borderoul curierului', 'Dacă și cât ai încasat efectiv.'],
                ['Factură', 'SmartBill', 'Documentul emis pentru tranzacție.'],
                ['Email cu factura', 'SmartBill și inboxul clientului', 'Transmiterea PDF-ului; nu confirmă plata sau validarea ANAF.'],
                ['e-Factura', 'SmartBill → statusul transmiterii în SPV', 'Transmiterea și rezultatul procesării, separat de PDF.'],
            ]) +
            '<p>Mai întâi învață fluxul manual. Automatizarea se activează după ce aceleași date și totaluri trec corect prin toate etapele. Conectarea API nu este încă făcută în acest proiect; capitolul te ghidează în conturile tale.</p>') +
        block('abonament', '2. Verifică abonamentul înainte să instalezi integrarea',
            '<p>Pagina oficială SmartBill precizează că modulul WooCommerce poate fi folosit cu <strong>Platinum, Gestiune Plus sau eCommerce</strong>; sincronizarea stocului este disponibilă în <strong>eCommerce</strong>. Pluginul poate emite facturi manual sau la schimbarea statusului și poate trimite factura clientului. Suportul său vizează configurarea integrării.</p>' +
            source('SmartBill — funcțiile și abonamentele integrării', 'https://api.smartbill.ro/plugins.html') + steps([
                'Conectează-te în SmartBill și verifică firma selectată. Caută informațiile despre abonamentul activ; dacă nu le vezi, întreabă administratorul contului sau suportul SmartBill.',
                'Verifică dacă există Contul meu → Integrări → Informații API. Dacă opțiunea lipsește, cere confirmarea eligibilității abonamentului, nu cumpăra un plugin neoficial ca să o înlocuiești.',
                'Dacă abonamentul actual nu permite integrarea, poți începe cu facturare manuală în SmartBill. WooCommerce continuă să gestioneze comenzile. Treci la integrare când economia de timp justifică diferența de abonament.',
                'Dacă ai deja un plan compatibil, continuă cu configurarea. Pentru una-două machete și fișiere digitale, nu ai nevoie automat de sincronizare de gestiune; stocul WooCommerce poate fi suficient la început.',
            ]) +
            '''<h3>Mesaj pentru SmartBill</h3><pre><code>Folosesc deja SmartBill și pregătesc un magazin WooCommerce pentru
machete printate 3D, fișiere digitale și servicii personalizate.
Vă rog să confirmați dacă abonamentul meu permite pluginul/API,
limitele incluse, costul unei eventuale diferențe de abonament și
cum pot testa fără facturi reale. Vreau și confirmarea compatibilității
cu versiunile WordPress, WooCommerce și PHP pe care le folosesc.
Nu am nevoie momentan de sincronizare de stoc dacă implică un cost suplimentar.</code></pre>''') +
        block('date-firma', '3. Pregătește firma, banca și seria de documente', steps([
            'În SmartBill → Configurare → Date firmă verifică denumirea, CUI/CIF și adresa fiscală din actele firmei. Nu copia automat Bravilor 4 dacă este doar adresa atelierului.',
            'În Configurare → Conturi bancare verifică IBAN-ul și titularul. Folosește aceleași date confirmate în plata prin transfer din WooCommerce.',
            'Înainte de emitere, confirmă cu contabilul regimul TVA și tratamentul machetelor, serviciilor, fișierelor digitale și transportului. Nu copia cotele sau bifele fiscale din exemple.',
        ]) + source('SmartBill — datele firmei și conturile preluate pe factură', 'https://ajutor.smartbill.ro/article/46-factura') +
            '<h3>Seria magazinului</h3>' + steps([
                'În Configurare → Serii verifică seriile existente. Poți folosi o serie existentă sau una separată pentru magazin, stabilită cu contabilul.',
                'Pentru o serie nouă, alege tipul documentului, denumirea și primul număr corect. CRWEB este doar un exemplu de nume; nu reseta o serie existentă la 0001.',
                'Salvează și notează seria aleasă. SmartBill alocă numerele în ordine; primul număr trebuie verificat înainte de prima emitere. Selectezi aceeași serie ulterior în plugin.',
            ]) + source('SmartBill — serii și numerotare', 'https://ajutorgestiune.smartbill.ro/article/266-serii')) +
        block('manual', '4. Prima factură manuală, fără integrare API', steps([
            'Deschide WooCommerce → Comenzi și selectează comanda. Verifică datele clientului, adresa de facturare, articolele, cantitățile, reducerile, transportul, taxele și totalul. Notează numărul comenzii.',
            'În SmartBill intră în Emitere → Factură. Selectează clientul sau completează datele necesare din comanda verificată. Pentru persoană juridică, verifică datele firmei și CUI-ul; nu factura automat pe persoana de contact.',
            'Adaugă pozițiile cu denumiri clare: macheta, fișierul digital sau serviciul efectiv livrat. Cantitățile și prețurile trebuie să corespundă comenzii. Include transportul și reducerile astfel încât totalurile să coincidă.',
            'La observații/mențiuni poți nota numărul comenzii WooCommerce, ca să găsești legătura ulterior. Verifică moneda RON, seria și datele înainte de emitere.',
            'Pentru exercițiu, păstrează documentul ca ciornă dacă această opțiune este disponibilă și nu folosi clienți reali. Nu emite facturi numerotate de probă în firma de producție.',
            'Pentru o tranzacție reală, emite după procedura și momentul stabilite cu contabilul. Adaugă numărul facturii în nota privată a comenzii WooCommerce.',
            'Trimite documentul clientului din SmartBill și verifică încasarea separat. Dacă facturezi manual, nu emite ulterior încă o factură din plugin pentru aceeași comandă.',
        ]) + '<p>Acesta este fluxul de operare propus pentru atelier. Nu înseamnă că orice comandă neplătită trebuie facturată imediat; momentul și tipul documentului se stabilesc pentru tranzacția ta.</p>') +
        block('plugin', '5. Instalează pluginul oficial și conectează contul', steps([
            'Pe WordPress-ul pregătit pentru integrare: Pluginuri → Adaugă modul. Caută SmartBill Facturare si Gestiune, autor smartbill. Compară cu pagina oficială de mai jos, apoi Instalează și Activează.',
            'În SmartBill → Contul meu → Integrări → Informații API găsești tokenul. În WordPress → SmartBill → Autentificare introdu emailul contului și tokenul, apoi autentifică-te.',
            'Completează Cod Fiscal pentru firma corectă și salvează. Este important dacă același cont SmartBill are mai multe firme.',
            'În setări alege seria pregătită și verifică regimul TVA, moneda, transportul și unitatea de măsură. Păstrează facturarea automată oprită până la verificarea totalurilor.',
        ]) + source('SmartBill — instalare, autentificare și configurare', 'https://ajutorgestiune.smartbill.ro/article/878-instalarea-modulului-smartbill-la-woocommerce') +
            '<p>Tokenul este o credențială privată. Îl introduci numai în panoul autorizat al WordPress-ului destinat integrării. Nu îl pune în JavaScript, capturi, ghid sau GitHub. Pentru staging folosește un cont de test confirmat; nu presupune că există un mod sandbox automat.</p>' +
            note('La verificarea din 5 octombrie 2026, changelogul SmartBill 3.4.10 menționează HPOS, WordPress 7.0 și WooCommerce 10.7.0. Acest lucru nu certifică automat combinația locală WordPress 7.1.2 / WooCommerce 11.1.2. Confirmă suportul pentru versiunile instalate și testează pe copie; nu dezactiva HPOS sau securitatea prin presupunere.') +
            source('Pluginul oficial SmartBill — ciorne și compatibilitate declarată', 'https://wordpress.org/plugins/smartbill-facturare-si-gestiune/')) +
        block('checkout-date', '6. Verifică datele care trec din comandă în factură',
            '<p>Pentru CR Print, compară o comandă și documentul SmartBill într-un tabel simplu. Nu este suficient ca pluginul să spună „Conectat”. Verifici efectiv ce a preluat.</p>' +
            table(['Câmp', 'Ce verifici'], [
                ['Client persoană fizică', 'Numele și adresa de facturare sunt corecte; nu cerem automat CNP tuturor cumpărătorilor.'],
                ['Client persoană juridică', 'Denumirea firmei, CUI/CIF și adresa fiscală sunt disponibile și mapate corect.'],
                ['Machetă fizică', 'SKU, denumire, cantitate, preț și taxă conform configurării confirmate.'],
                ['Model digital', 'Nu are transport; este tratat corect fără scădere de stoc fizic.'],
                ['Transport', 'Este inclus o singură dată și are tratamentul fiscal stabilit.'],
                ['Reducere', 'Cuponul/reducerea și rotunjirile duc la același total.'],
                ['Email client', 'Factura ajunge la persoana potrivită; nu la emailul de administrator.'],
            ]) +
            '<p>Dacă finalizarea WooCommerce nu afișează sau nu transmite câmpurile pentru firmă/CUI, nu adăuga primul plugin de checkout găsit. Verifică suportul SmartBill pentru checkoutul folosit și maparea câmpurilor. Pentru blocurile WooCommerce, compatibilitatea extensiilor se verifică separat. Poți testa checkoutul clasic ca alternativă, fără să schimbi direct site-ul public.</p>') +
        block('ciorne', '7. Verificarea inițială: ciorne și facturare manuală',
            '<p>Pluginul recomandă opțiunea <strong>Emite ciornă</strong> pentru verificarea inițială: documentul nu primește număr, iar totalul poate fi comparat cu comanda. Este tot o comunicare cu acel cont SmartBill, nu o simulare complet locală.</p>' + steps([
                'Folosește contul SmartBill de test confirmat sau păstrează integrarea deconectată până ai o procedură agreată. În contul real nu crea documente fictive și nu trimite emailuri către clienți de test inventați.',
                'În setările pluginului activează Emite ciornă, oprește emiterea automată și trimiterea automată a documentelor. Folosește numai inboxuri controlate pentru exercițiu.',
                'Creează o comandă pentru fizic, una pentru digital și una mixtă. Deschide fiecare comandă și folosește acțiunea SmartBill de emitere manuală disponibilă în versiunea instalată.',
                'Deschide documentul rezultat în SmartBill. Compară totalul, transportul, reducerile, datele clientului și tratamentul fiscal. Dacă există o eroare, corectează setările înainte de orice automatizare.',
                'Pentru aceeași comandă verifică istoricul și documentul existent înainte de a repeta emiterea. Dacă o cerere expiră, documentul poate exista deja în SmartBill.',
            ]) + '<p>După exercițiu, notează ce combinație de versiuni și setări a funcționat. Pentru primele comenzi reale păstrează emiterea manuală; confirmă datele cu contabilul înainte de a dezactiva modul ciornă.</p>') +
        block('automatizare', '8. Automatizarea potrivită pentru fiecare plată',
            '<p>Următoarele sunt reguli de lucru propuse, nu setări universale de contabilitate. Stabilește momentul facturării și al raportării cu contabilul. O schimbare de status WooCommerce nu dovedește singură încasarea.</p>' +
            table(['Scenariu', 'Verificarea ta', 'Regula inițială propusă'], [
                ['Transfer bancar', 'Banii au intrat în contul firmei.', 'Verificare manuală a plății, apoi emitere conform procedurii.'],
                ['Ramburs pentru machetă', 'Livrarea și încasarea din borderoul curierului.', 'Nu marca factura încasată doar pentru că ai pregătit coletul.'],
                ['Card', 'Procesatorul confirmă plata, nu doar browserul clientului.', 'Automatizează după testarea procesatorului și a statusului transmis.'],
                ['Fișier digital', 'Plata confirmată și dreptul de acces corect.', 'Fără ramburs și fără cost de transport.'],
                ['Serviciu personalizat', 'Ofertă acceptată, avans/etapă/livrare, după caz.', 'Facturare manuală pentru termenii proiectului.'],
            ]) + steps([
                'După ce emiterea manuală funcționează, identifică în SmartBill setarea de facturare automată la statusul comenzii. Alege un singur punct de emitere pentru fiecare flux.',
                'Testează ce se întâmplă când comanda trece prin Procesare și Finalizată. Trebuie să existe o singură factură pentru tranzacția urmărită, nu una la fiecare schimbare de status.',
                'Activează trimiterea automată către client numai după verificarea documentului și a destinatarului. Emailul WooCommerce de confirmare a comenzii poate rămâne separat de factura SmartBill.',
                'Pentru primele comenzi reale compară zilnic: număr comandă, document, total, plată și livrare. Dacă apar duplicate sau diferențe, oprește emiterea automată și revino temporar la fluxul manual.',
            ])) +
        block('stoc', '9. Stoc: începe simplu, sincronizează doar dacă ai nevoie',
            '<p>La început poți ține stocul machetelor în WooCommerce și facturarea în SmartBill. Dacă ai abonament eCommerce și gestiune, sincronizarea identifică produsele prin cod sau denumire. Folosește coduri identice; pentru navă păstrează SKU-urile care conectează și viewerul 3D.</p>' + steps([
                'La produsele fizice activează gestionarea stocului și verifică gestiunea aleasă în plugin. Preia URL-ul de sincronizare afișat de plugin și configurează-l în SmartBill → Contul meu → Integrări, conform instrucțiunilor oficiale.',
                'Testează conexiunea. După configurare, stocurile nu se transferă toate automat imediat: se actualizează la mișcări. Verifică opțiunea de preluare manuală pentru stocul inițial.',
                'Dacă sincronizarea eșuează, cere gazdei să verifice serverul și transmiterea antetului Authorization. Nu edita configurații Apache de server din cPanel fără suport.',
            ]) + source('SmartBill — sincronizarea stocurilor WooCommerce', 'https://ajutorgestiune.smartbill.ro/article/822-sincronizarea-stocurilor-cu-magazinul-online') +
            '<p>Nu sincroniza fișierul digital ca și cum ar fi o machetă fizică din depozit. Pentru producție la comandă, termenul și capacitatea atelierului nu sunt echivalente cu stocul de produse finite. Verifică politica separat înainte de a afișa „în stoc”.</p>') +
        block('efactura', '10. Conectează e-Factura în SmartBill',
            '<p>Conectarea WooCommerce → SmartBill și autorizarea SmartBill → SPV sunt două etape separate. Factura PDF trimisă pe email nu dovedește că e-Factura a fost procesată în SPV.</p>' + steps([
                'În SmartBill → Configurare → e-Factura apasă Autorizează. Dacă ai certificat digital cu acces în SPV pentru firma ta, alege ruta cu certificat și urmează pașii.',
                'Dacă accesul este la contabil, alege Obține accesul prin contabil și transmite-i privat linkul generat. El finalizează autorizarea cu certificatul său; nu ai nevoie să primești PIN-ul sau tokenul fizic al lui.',
                'Verifică mesajul de conectare și firma autorizată. Dacă apar erori de certificat, verifică împreună cu contabilul/furnizorul certificatului; ghidul nu instalează sau schimbă certificatul.',
            ]) + source('SmartBill — autorizarea SPV, inclusiv prin contabil', 'https://ajutor.smartbill.ro/article/982-autorizarea-contului-smartbill-pentru-acces-in-s-p-v') +
            '<h3>Stabilește trimiterea după conectare</h3>' + steps([
                'În Configurare → e-Factura verifică trimiterea automată și regulile disponibile. Există și facturi emise prin API care pot intra în acest flux.',
                'Stabilește cu contabilul obligațiile și termenele aplicabile firmei, clienților și operațiunilor tale. Nu deduce scutiri sau termene dintr-un exemplu de magazin.',
                'După prima factură reală, urmărește statusul transmiterii și eventualele erori în SmartBill. Nu te opri la confirmarea emitere/PDF și nu trimite din nou la întâmplare dacă există deja o transmitere.',
                'Verifică notificările de reconectare SPV și procedura de rezolvare. Păstrează documentele și istoricul după regulile firmei.',
            ]) + source('SmartBill — regulile de trimitere e-Factura', 'https://ajutor.smartbill.ro/article/1171-configurare-e-factura')) +
        block('incasari-retur', '11. Încasări, anulări și retururi',
            '<h3>Încasarea se verifică separat</h3><p>În SmartBill poți înregistra încasarea aferentă facturii. Fă această operațiune pe baza dovezii reale: extras, confirmarea procesatorului sau borderoul curierului. Marcarea „încasată” nu mută bani și nu trebuie făcută automat pentru o comandă neplătită.</p>' +
            source('SmartBill — încasări', 'https://ajutor.smartbill.ro/article/89-incasare-prezentare-generala') +
            '<h3>Dacă o comandă este anulată sau returnată</h3>' + steps([
                'Înainte de orice emitere nouă verifică dacă există deja factura și dacă a fost transmisă clientului/SPV. O comandă WooCommerce anulată nu corectează automat documentele SmartBill.',
                'Pentru o factură emisă, folosește procedura de corecție/stornare stabilită cu contabilul. SmartBill are flux de stornare legat de factura inițială; nu crea o factură negativă fără această legătură.',
                'Verifică separat rambursarea efectivă a banilor, stocul fizic revenit și accesul digital, după caz. Statusul Rambursată din WooCommerce nu garantează că toate acestea s-au făcut.',
                'În nota privată a comenzii păstrează referința documentului de corecție și a rambursării. Evită informațiile personale care nu sunt necesare.',
            ]) + source('SmartBill — stornarea facturii', 'https://ajutor.smartbill.ro/article/59-stornare-factura')) +
        block('probleme', '12. Dacă integrarea nu merge',
            table(['Simptom', 'Verifici în ordine'], [
                ['Nu apare API în SmartBill', 'Firma selectată, abonamentul, drepturile contului; confirmare la SmartBill.'],
                ['Autentificare respinsă', 'Emailul contului, tokenul, CUI-ul firmei. Nu posta credențialele în capturi.'],
                ['Factură absentă', 'Notă/eroare în comandă, istoricul și documentele din SmartBill; emiterea manuală înainte de automatizare.'],
                ['Timeout la emitere', 'Caută factura existentă înainte de retry, ca să eviți un duplicat. Cere verificarea conexiunii HTTPS de către gazdă.'],
                ['Total diferit', 'TVA, prețuri cu/fără taxă, transport, cupon, rotunjire; contabil + setările integrării.'],
                ['Factura nu ajunge pe email', 'Trimiterea din SmartBill și destinatarul. Un test WP Mail SMTP nu dovedește livrarea SmartBill Cloud.'],
                ['Pluginul provoacă eroare PHP', 'Versiunile, jurnalul privat al serverului și test pe copie. Revii la facturarea manuală până la remediere.'],
                ['Stoc neactualizat', 'Plan eligibil, coduri, gestiune, preluare inițială și conexiunea de sincronizare.'],
                ['e-Factura are eroare', 'Conectarea SPV, firma, datele documentului și mesajul SmartBill; contabilul verifică tratamentul.'],
            ]) + '<p>Când ceri ajutor, trimite versiuni WordPress/WooCommerce/PHP/SmartBill plugin, pașii și mesajul erorii fără tokenuri, parole sau date complete ale clienților. Pentru plugin folosește canalul indicat în pagina sa oficială; pentru server, suportul firmei de hosting.</p>'))

    append('magazin', 'facturare-smartbill', '10. De la comandă la factura SmartBill',
        '<p>Produsele și comenzile se gestionează în WooCommerce. Facturile se emit în SmartBill, manual sau prin pluginul eligibil. Numărul comenzii WooCommerce nu este numărul facturii.</p>' + steps([
            'Finalizează întâi produsele și checkoutul: date client, cantități, taxare și transport confirmate. Verifică fizic, digital și coș mixt.',
            'Urmează <a href="smartbill.html">SmartBill & facturare</a> pentru abonament, serie, emitere manuală, ciorne, automatizare și e-Factura.',
            'Pentru firme verifică preluarea CUI/CIF și a adresei fiscale în document. Nu adăuga un câmp fără să confirmi maparea lui în integrare.',
            'După emitere, păstrează referința facturii în comanda WooCommerce. Verifică plata și livrarea separat.',
        ]))
    append('lansare', 'publicare-cpanel-smartbill', '8. Publicarea din cPanel și pornirea facturării',
        '<p>Pentru prima lansare, stabilește cu gazda exact ce transferă WP Toolkit / Softaculous: fișiere, pagini, setări și bază de date. Copy Data / Push to Live nu reprezintă o îmbinare inteligentă a comenzilor.</p>' + steps([
            'Imediat înainte de publicare fă un backup nou al site-ului public. Dacă există comenzi, clienți sau solicitări noi, nu înlocui întreaga bază de date cu o copie mai veche.',
            'Pentru un site cu activitate existentă, cere transferul schimbărilor fără pierderea comenzilor. Fișierele temei și pluginului se pot actualiza separat, iar paginile/setările se transferă printr-o procedură care păstrează datele active.',
            'Dacă gazda confirmă transferul complet pentru un site fără date noi, verifică direcția sursă → destinație și opțiunile alese. Nu copia datele locale de exercițiu sau facturile de test.',
        ]) + source('Softaculous — opțiunile Push to Live', 'https://www.softaculous.com/docs/enduser/push-to-live/') + steps([
            'Pe domeniul final verifică HTTPS, paginile, meniurile și checkoutul, apoi configurează credențialele reale direct în panourile private. Nu publica tokenuri în fișierele site-ului.',
            'În SmartBill confirmă firma, seria, regimul fiscal, opțiunea ciornă și automatizarea. Păstrează emiterea manuală pentru început dacă automatizarea nu a fost verificată. Debifarea ciornei se face numai după ce ești pregătit pentru documente reale.',
            'Verifică emailurile WooCommerce/contact prin WP Mail SMTP și factura trimisă din SmartBill separat. Verifică legătura SPV și statusul primei facturi reale.',
            'Elimină protecția cu parolă și descurajarea indexării numai de pe domeniul public, după verificare. Staging rămâne protejat și deconectat de integrările reale.',
            'În primele zile urmărește fiecare comandă: total, plată, factură, email, producție/livrare și, unde este aplicabil, transmitere e-Factura.',
        ]))
    append('depanare', 'cpanel-smartbill-ajutor', '5. Unde rezolvi problemele cPanel și SmartBill',
        '<p><strong>Site/SSL/PHP/server SMTP:</strong> <a href="cpanel.html#suport">suportul găzduirii</a>. <strong>Factură/API/abonament/SPV:</strong> <a href="smartbill.html#probleme">capitolul SmartBill</a>, suportul SmartBill și contabilul pentru tratamentul fiscal. <strong>Produse/comenzi/checkout:</strong> WooCommerce și compatibilitatea extensiilor.</p><p>Când un serviciu nu funcționează, verifică întâi etapa lui: inboxul în webmail, SMTP prin Email Test, factura în SmartBill, e-Factura în statusul SPV. Nu reinstala întregul site pentru o singură setare greșită.</p>')

    # Replace the old five-card map with the user's complete setup path.
    title, subtitle, content = P['index']
    cards = [('cpanel', 'Pregătește cPanel', 'Backup, copie de lucru, HTTPS și PHP.'), ('wordpress', 'Instalează site-ul', 'Tema CR Print, pluginul și paginile.'), ('magazin', 'Configurează WooCommerce', 'Produse, livrare, plată și comenzi.'), ('email', 'Activează emailul', 'hi@crprint.ro și WP Mail SMTP.'), ('smartbill', 'Configurează SmartBill', 'Facturi, încasări și e-Factura.'), ('lansare', 'Verifică și lansează', 'Publicare, SEO și apoi reclame.')]
    roadmap = '<div class="roadmap">' + ''.join(f'<a href="{key}.html"><b>{i+1:02}</b><strong>{label}</strong><span>{desc}</span></a>' for i, (key, label, desc) in enumerate(cards)) + '</div>'
    content = re.sub(r'<div class="roadmap">.*?</div>', lambda _: roadmap, content, count=1, flags=re.S)
    P['index'] = ('Harta de lansare', 'cPanel, WordPress, WooCommerce și SmartBill, explicate de la zero.', content)
    order = ['index', 'cpanel', 'wordpress', 'magazin', 'email', 'smartbill', 'promovare', 'google', 'meta', 'tiktok', 'lansare', 'depanare']
    entries = [(key, P[key]) for key in order]
    P.clear()
    P.update(entries)
