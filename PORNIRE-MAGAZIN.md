# Cum pornești magazinul pe computer

## Varianta simplă: site, magazin și administrare

Un singur server pornește întregul site, inclusiv magazinul. Nu trebuie să instalezi WordPress pentru această variantă.

1. Deschide folderul **CRPRINT**, unde sunt fișierele site-ului.
2. Găsește **Start-Demo.cmd** și fă **dublu clic** pe el. Dacă Windows ascunde extensiile, îl poți vedea ca „Start-Demo”, de tip „Windows Command Script”.
3. Se deschide o fereastră cu text. Așteaptă să apară adresa **http://127.0.0.1:4173/**. **Lasă fereastra deschisă.**
4. Deschide browserul și introdu una dintre adresele de mai jos în bara de adrese, apoi apasă Enter.

| Ce vrei să deschizi | Adresa |
|---|---|
| Site-ul | http://127.0.0.1:4173/ |
| Magazinul | http://127.0.0.1:4173/magazin.html |
| Administrarea produselor, comenzilor și mesajelor | http://127.0.0.1:4173/admin.html |
| Manualul complet | http://127.0.0.1:4173/ghid/ |

Adresele funcționează pe acest computer, cât timp serverul este pornit. Nu deschide fișierele HTML direct prin dublu clic: magazinul are nevoie de server.

## Cum modifici produsele

1. Deschide adresa de administrare din tabel.
2. Intră în secțiunea cu produse și selectează produsul pe care vrei să îl modifici.
3. Modifică numele, descrierea, prețul sau stocul, apoi apasă butonul de salvare.
4. Reîncarcă pagina magazinului ca să vezi schimbările.

Comenzile și solicitările de contact se păstrează local pe computer. Acest mediu nu încasează bani și nu trimite emailuri externe. Administrarea locală este destinată lucrului pe computer, nu publicării directe pe internet.

## Oprire și repornire

Pentru oprire, selectează fereastra serverului și apasă **Ctrl+C**. Pentru repornire, fă din nou dublu clic pe **Start-Demo.cmd**. Oprirea serverului nu șterge produsele sau comenzile.

## Dacă ceva nu funcționează

### Site-ul se deschide deja

Serverul este deja pornit. Folosește site-ul; nu mai porni încă o copie.

### Apare „EADDRINUSE” sau „port already in use”

Portul este ocupat. Încearcă mai întâi să deschizi http://127.0.0.1:4173/. Dacă apare site-ul, folosește serverul care rulează deja. Închide doar fereastra nouă care afișează eroarea.

### Apare un mesaj că trebuie instalat Node.js

Pe acest computer, scriptul poate folosi Node.js inclus în mediul Codex. Pe un computer fără acest runtime:

1. Deschide https://nodejs.org/ și descarcă versiunea **LTS**.
2. Rulează instalarea și păstrează opțiunile implicite.
3. Închide fereastra serverului, apoi pornește din nou **Start-Demo.cmd**.

### „Catalogul nu se poate încărca”

1. Verifică dacă fereastra serverului este încă deschisă.
2. Verifică adresa: trebuie să înceapă cu **http://127.0.0.1:4173/**, nu cu `file:///`.
3. Oprește serverul cu Ctrl+C, pornește din nou Start-Demo.cmd și reîncarcă magazinul cu **Ctrl+F5**.
4. Dacă eroarea persistă, păstrează mesajul din fereastra serverului și o captură a erorii pentru depanare.

## Varianta WordPress: administrare cu WooCommerce

Aceasta este o a doua variantă, separată de magazinul de la portul 4173. Produsele și comenzile celor două variante nu se sincronizează automat.

1. În același folder CRPRINT, fă dublu clic pe **Start-WordPress.cmd**.
2. Lasă fereastra deschisă. La prima pornire se descarcă WordPress și pluginurile; ai nevoie de internet. Așteaptă mesajul de confirmare înainte să deschizi site-ul.
3. Deschide **http://127.0.0.1:9400/wp-admin/**. Dacă ți se cere autentificare, folosește linkul de conectare afișat în fereastra serverului.
4. Pentru editare, intră în **Produse → Toate produsele**, selectează produsul și apasă **Editează**. După modificări, apasă **Actualizează**.
5. Comenzile sunt în **WooCommerce → Comenzi**. Magazinul WordPress se vede la **http://127.0.0.1:9400/**.

WordPress local necesită Node.js 24.18 sau mai nou. Nu trebuie să instalezi separat PHP sau MySQL pentru această variantă. Pentru oprire, apasă Ctrl+C în fereastra sa.

Pentru instalarea pe găzduire, emailuri reale, plăți, livrare și publicare, urmează manualul de la **http://127.0.0.1:4173/ghid/**, începând cu capitolul **WordPress de la zero**.
