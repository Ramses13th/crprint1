# CR Print 3D

Site cu pagini separate, temă întunecată/luminoasă, magazin demonstrativ și pachet WordPress cu WooCommerce și WP Mail SMTP.

Interfața pentru vizitatori are aspectul unui site public: nu afișează etichete de demonstrație. Protecțiile locale rămân active în backend. Contact are acces direct la telefon/email/WhatsApp, câmpuri opționale extensibile și o hartă încărcată la cerere.

Manualul separat din `ghid/` are 10 capitole, peste 12.000 de cuvinte, căutare, calculator de buget și progres salvat în browser. Include instrucțiuni de la identificarea găzduirii până la instalarea ZIP-urilor, editarea produselor, SMTP, livrare, publicare și campanii Google/Meta/TikTok pentru 300–600 lei lunar.

**Începe aici: [ghidul scurt pentru pornirea magazinului](PORNIRE-MAGAZIN.md).**

## Pornire pe Windows

1. Dublu-click pe **Start-Demo.cmd**. Păstrează fereastra deschisă.
2. Deschide **http://127.0.0.1:4173/**. Portul 4174 rămâne disponibil ca alternativă.
3. Produse, comenzi și mesaje: **http://127.0.0.1:4173/admin.html**.
4. Ghidul separat: **http://127.0.0.1:4173/ghid/**.
5. Pentru WordPress real, dublu-click pe **Start-WordPress.cmd**, apoi deschide **http://127.0.0.1:9400/wp-admin/**.

Demo-ul rapid necesită Node.js 22+. WordPress Playground necesită Node.js 24.18+ și internet la instalarea inițială. Scriptul folosește runtime-ul Codex disponibil pe acest computer; pe alte computere instalează Node.js LTS de pe site-ul oficial. Nu trebuie instalat PHP/MySQL pentru Playground.

Oprește serverele cu Ctrl+C în ferestrele lor. Dacă portul este ocupat, oprește serverul anterior sau folosește `Start-Demo.ps1 -Port 4180` / `Start-WordPress.ps1 -Port 9401`.

## Cele două medii

| Funcție | Demo rapid | WordPress local |
|---|---|---|
| Administrare produse | `/admin.html`, catalog JSON | Produse în WooCommerce |
| Comenzi | Salvate pe acest computer | Comenzi native WooCommerce |
| Coș | Browser + preț recalculat pe server | Sesiune WooCommerce |
| Contact | Solicitări salvate local | Solicitări 3D + integrare `wp_mail` |
| Email extern | Oprit | Oprit explicit în mediul local |
| Plăți | Nu se încasează bani | Metodă demonstrativă, fără încasare |

**Prețurile 149/49 lei și transportul de 19 lei sunt exemple.** Confirmă prețurile, scara, materialul, finisajul și licența înainte de producție.

Catalogul demo este în `data/catalog.json`. Comenzile și mesajele sunt în `%TEMP%/crprint-local-demo`, în afara fișierelor servite public. În WordPress, datele persistă în `%LOCALAPPDATA%/CRPrint/wordpress-demo`; fă backup înainte de experimente. Cele două cataloage sunt independente. Exportul CSV din demo ajută transferul în WooCommerce; verifică fișierele digitale și imaginile separat.

Serverele sunt limitate la acest computer. Administrarea demo nu este un sistem de autentificare pentru producție. În browserul deschis direct din fișiere sau printr-un server static, coșul poate funcționa ca simulare, dar salvarea comenzilor/formularului necesită serverul Node.

Lansatorul WordPress verifică fișierele editorului WooCommerce și poate reface o instalare locală incompletă din arhiva oficială a aceleiași versiuni. Pentru instalări noi, blueprintul folosește arhiva completă oficială WooCommerce.

Formularul expune evenimentul `crprint_contact_success` numai după înregistrarea solicitării. În WordPress, confirmarea pentru acest eveniment este verificată pe server și evită repetarea în aceeași sesiune. Nu transmite date de contact. Site-ul nu încarcă singur Analytics, pixeli sau alte instrumente publicitare; configurarea cu consimțământ este explicată în ghid.

## Instalare pe WordPress public

Pachete pentru staging:

- `wordpress/crprint-studio.zip`: tema CR Print Studio.
- `wordpress/crprint-core.zip`: import în ciornă și formular de contact.
- WooCommerce și WP Mail SMTP: pluginurile oficiale din directorul WordPress.

Nu încărca întregul proiect ca temă. Ghidul în `ghid/wordpress.html` explică instalarea, păstrarea site-ului existent, importul și editarea. `ghid/email.html` explică SMTP/DNS; `ghid/magazin.html` explică produsele fizice/digitale, plata și livrarea. Blueprintul și produsul digital demo sunt numai pentru mediul local.

Emailul real se activează după alegerea furnizorului și configurarea WP Mail SMTP. Este necesar un test real de livrare; salvarea unei solicitări sau acceptarea de către `wp_mail` nu garantează primirea în inbox. Pluginul salvează solicitările și când expedierea eșuează.

Paginile juridice sunt modele demonstrative. Completează datele firmei, condițiile comerciale și textele reale înainte de lansare. Fișierul FBX din demo este public; produsul comercial trebuie livrat prin descărcări protejate WooCommerce, cu un fișier separat de previzualizare.

## Conținut și construcție

- `tools/build-site.py`: paginile HTML, metadatele, sitemapul și componentele comune.
- `design.css`: designul, temele și adaptarea la ecrane mici.
- `tools/shared-ui.js`: animațiile, meniul, tema și încărcarea viewerului la cerere.
- `tools/commerce.js`: magazinul demonstrativ; `dev-server.mjs`: API local.
- `tools/build-wordpress.py`: resursele temei și ZIP-urile.
- `tools/build-guide.py`: cele 10 capitole ale ghidului.

Reconstrucție: `npm run build` cu Python disponibil în PATH. Pe acest computer se poate folosi Python din runtime-ul Codex. Paginile generate se suprascriu la reconstrucție; modifică generatorul pentru schimbări permanente. În WordPress, produsele se editează în WooCommerce, iar paginile importate într-un bloc HTML personalizat.

Logo-ul original este păstrat. Imaginile noi generate au prompturi în `images/IMAGE-PROMPTS.md`. Randările navei provin din geometria modelului furnizat. Three.js este servit local, cu licența inclusă. Modelul FBX folosește o cale relativă; versiunea WordPress folosește un GLB simplificat pentru previzualizare.

## Verificări

Au fost verificate catalogul, editarea și restaurarea prețului, coșul, prețurile calculate pe server, prevenirea comenzilor duplicate în cereri concurente, stocurile, liniile duplicate, anti-spam/honeypot, accesul la administrare, viewerul 3D și meniul mobil. În administrare pot apărea înregistrări fictive marcate „QA Demo”.

SEO: titluri/descriptori individuali, structură semantică, imagini responsive, schema LocalBusiness și sitemap. Mediile locale au noindex. Pentru producție folosește sitemapul WordPress/pluginului SEO și verifică Search Console. Nu există promisiuni de poziționare sau de rentabilitate a reclamelor.

Playground folosește SQLite. Interogarea MySQL pentru rezervarea temporară a stocului este dezactivată exclusiv în demo-ul local; validarea și reducerea stocului rămân active. Pe găzduirea de producție MySQL/MariaDB, rezervarea WooCommerce este păstrată.
