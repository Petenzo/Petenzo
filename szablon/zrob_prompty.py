# Generuje PROMPTY-SEKCJE.md: ogólne prompty + kod do każdej sekcji (na bazie szablon.html)
import re, os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, 'szablon.html'), encoding='utf-8').read()
# neutralne nazwy i jeden ogólny kolor
s = s.replace('var c=document.getElementById("kwCount");c.textContent=cnt;c.hidden=!cnt;', 'var c=document.getElementById("kwCount");if(c){c.textContent=cnt;c.hidden=!cnt;}')
s = re.sub(r'\bkw(?=[-A-Z_])', 'sk', s); s = s.replace('KW_', 'SK_').replace('kwCart2', 'skCart2')
pal = {'--sk-surface:#FFF8F3':'--sk-surface:#F6F8FC','--sk-surface-2:#FCEDE4':'--sk-surface-2:#EAF0FB','--sk-fg:#1F2547':'--sk-fg:#1B2333',
 '--sk-muted:#646A85':'--sk-muted:#5E6878','--sk-border:#F1E4DB':'--sk-border:#E2E8F2','--sk-primary:#E9693F':'--sk-primary:#2F5BD8',
 '--sk-primary-dark:#1F2547':'--sk-primary-dark:#1D3A8A','--sk-primary-soft:#FDEDE5':'--sk-primary-soft:#E8EEFC','--sk-gold:#E9693F':'--sk-gold:#2F5BD8',
 '--sk-gold-soft:#FDEDE5':'--sk-gold-soft:#E8EEFC','linear-gradient(135deg,#F28A5C 0%,#E2572C 100%)':'linear-gradient(135deg,#4A74EC 0%,#2448B8 100%)',
 'linear-gradient(135deg,#2B3266 0%,#1F2547 100%)':'linear-gradient(135deg,#2448B8 0%,#1D3A8A 100%)','rgba(233,105,63,':'rgba(47,91,216,'}
for a, b in pal.items(): s = s.replace(a, b)
L = s.split('\n')
def ln(pat, start=0):
    for i in range(start, len(L)):
        if pat in L[i]: return i
    raise SystemExit('brak: ' + pat)
def rng(a, b): return '\n'.join(L[a:b]).strip('\n')
css0, css1 = ln('<style>') + 1, ln('</style>')
cssL = L[css0:css1]
# podział CSS po komentarzach /* ... */
blocks, cur, name = {}, [], 'base'
for l in cssL:
    m = re.match(r'\s*/\* (.+?) \*/\s*$', l)
    if m: blocks.setdefault(name, []).extend(cur); cur, name = [], m.group(1)
    else: cur.append(l)
blocks.setdefault(name, []).extend(cur)
def tl(*keys): return '\n'.join(l for l in (base_all) if any(k in l for k in keys))
def css(*names): return '\n'.join('\n'.join(blocks.get(n, [])).strip() for n in names if blocks.get(n)).strip()
# końcówka CSS (media, animacje) – w bloku "sticky mobile" po pierwszych regułach sticky
sticky = blocks.get('sticky mobile', [])
k = next((i for i, l in enumerate(sticky) if l.startswith('@media') or l.startswith('@keyframes')), len(sticky))
stickyCSS, tailCSS = '\n'.join(sticky[:k]).strip(), '\n'.join(sticky[k:]).strip()
base_all = cssL
js0, js1 = ln('<script>') + 1, ln('</script>')
JS = L[js0:js1]
def jsr(a, b=None):
    i = next(i for i, l in enumerate(JS) if a in l); j = next(j for j, l in enumerate(JS) if b in l and j > i) if b else len(JS)
    return '\n'.join(JS[i:j]).strip()
H_ = lambda a, b: rng(ln(a), ln(b))
head = rng(0, css0 - 1)
sec = []
def add(title, prompt, html='', c='', js=''):
    sec.append((title, prompt, html, c, js))

INTRO_ALL = jsr('(function(){', '/* BUNDLES */')
INTRO_JS = INTRO_ALL[:INTRO_ALL.index('var gallery=[')].strip().replace('(function(){', '').strip()
ZL = next(l for l in JS if l.startswith('function zl('))
INTRO_JS += '\n' + ZL
GALLERY_JS = INTRO_ALL[INTRO_ALL.index('var gallery=['):]
add('0. FUNDAMENT (wklej jako pierwszy)',
 'Zbuduj jednostronicowy sklep z jednym produktem jako JEDEN plik index.html (HTML + CSS + czysty JS, bez frameworków). '
 'Wszystkie kolory, cienie i zaokrąglenia trzymaj w tokenach CSS w :root (prefiks --sk-), żeby zmiana koloru marki była w jednym miejscu – kolor podam osobno, na razie użyj tego niebieskiego. '
 'Czcionki: Poppins (tekst) + Russo One (nagłówki, logo). Mobile-first, max szerokość treści ok. 1200 px, sekcje z dużym oddechem, karty z miękkim cieniem i zaokrągleniem 20 px, przyciski CTA z gradientem i cieniem. '
 'Strona ma dwa „widoki”: #skHome (strona produktu) i #skPages (podstrony polityk) przełączane funkcją skShow(). '
 'Poniżej: <head>, bazowy CSS (tokeny, reset, przyciski, kontenery, animacje, wersja mobilna) i początek skryptu (zdjęcia, galeria). Kolejne prompty dokładają po jednej sekcji – wstawiaj je w tej kolejności.',
 head, css('base') + '\n\n/* animacje i telefon */\n' + tailCSS, INTRO_JS)
SHOW_JS = jsr('window.skShow=function', None) if False else '\n'.join(l for l in JS[next(i for i,l in enumerate(JS) if l.startswith('window.skShow=function')):] if not l.startswith('})();'))
CART_JS = jsr('/* CART */', '/* TABS */') + '\n\n' + jsr('/* STICKY */', '/* REVIEWS */')
TOP_HTML = rng(ln('<body>') + 1, ln('<main id="skHome"')) + '\n\n<main id="skHome" class="sk-page on">\n\n' + H_('<!-- HERO -->', '<!-- PROBLEM -->') + '\n\n<!-- ...tu kolejne sekcje... -->\n</main>\n<main id="skPages"></main>\n\n' + rng(ln('<!-- CART DRAWER -->'), ln('<!-- CONTACT MODAL -->')) + '\n\n' + rng(ln('<div class="sk-sticky"'), ln('<script>'))
add('1. GÓRA STRONY: PASEK Z NAPISAMI, MENU, KOSZYK, GALERIA, CENA, ZESTAWY, PŁATNOŚCI, PASEK 4 KORZYŚCI',
 'Pierwsza sekcja = wszystko od samej góry do paska 4 korzyści włącznie. '
 'a) Na samej górze cienki pasek w kolorze marki z napisami płynnie przesuwającymi się od prawej do lewej w pętli (np. darmowa dostawa, 14 dni na zwrot, promocja, hasło marki). '
 'b) Pod nim biały, przyklejony nagłówek: po lewej przycisk „trzy kreski” (menu), na środku logo (ikona produktu + nazwa sklepu + mały podpis wersalikami), po prawej ikona koszyka z licznikiem. Kliknięcie „trzech kresek” wysuwa menu na cały ekran z linkami: Jak to działa, Opinie, FAQ, Kontakt z nami itd. + przycisk zamknij. Kliknięcie koszyka otwiera koszyk wysuwany z prawej. '
 'c) Galeria: duże zdjęcie z podpisem + miniatury; na komputerze przyklejona po lewej podczas przewijania, na telefonie przesuwana palcem, bez strzałek. Pierwsze zdjęcie = ludzie używający produktu. '
 'd) Obok/pod galerią: plakietki („Hit…” + „Liczba sztuk ograniczona”), nazwa, gwiazdki + liczba opinii + „X osób ogląda teraz”, cena + przekreślona + % rabatu, 6 korzyści z „✓”, wybór zestawu 1/2/3 szt. jako karty (plakietki „Najczęściej wybierany”, „Najlepsza cena”); po wybraniu zestawu pod nim pojawia się wybór wariantu dla każdej sztuki (dwa małe przyciski). Duży przycisk „Dodaj do koszyka · cena”. '
 'e) Pod przyciskiem logotypy płatności w ich PRAWDZIWYCH kolorach: BLIK czarny z białym napisem, VISA granatowo-niebieski z białym napisem, Mastercard ciemny z czerwono-żółtymi kółkami, Apple Pay czarny, Google Pay ciemny z kolorowym „G”, P24 czerwony z białym napisem; pod nimi linijka „🔒 Bezpieczna płatność · 14 dni na zwrot · …”. '
 'f) Na końcu pełnoszeroki ciemny pasek w kolorze marki z 4 kafelkami: Darmowa wysyłka, 14 dni na zwrot, Bezpieczne płatności, Ocena 4,9/5 – na telefonie 2×2. Tu ta sekcja się kończy. '
 'g) Do tej sekcji należy też: koszyk wysuwany z prawej (pozycje, –/+, kosz, pasek „dodaj jeszcze 1 i zapłać mniej”, podsumowanie z rabatem, „Realizuj zakup”), okno wyboru dostawy („📦 Paczkomat – GRATIS”, „🚚 Kurier – GRATIS”, „Przejdź do płatności” od razu do kasy), przyklejony dolny pasek na telefonie (nazwa, cena, „Do koszyka”) i komunikat „Dodano do koszyka ✓”.',
 TOP_HTML, css('top bar marquee', 'nav', 'hero', 'benefit strip', 'upsell / bundle', 'drawer', 'modal') + '\n' + stickyCSS + '\n' + tl('.sk-flower','.sk-var','.sk-pill','.sk-gallery','.pay-'),
 GALLERY_JS + '\n\n' + jsr('/* BUNDLES */', '/* CART */') + '\n\n' + CART_JS + '\n\n' + SHOW_JS)
add('2. PROBLEM („Brzmi znajomo?”)',
 'Sekcja „ból klienta” na jasnym tle: mały nadtytuł wersalikami w kolorze akcentu (np. „BRZMI ZNAJOMO?”), duży nagłówek nazywający problem (końcówka nagłówka w kolorze marki), 1–2 zdania budujące emocję, a pod spodem 4 białe karty jedna pod drugą, każda z czerwonym „✕” w kółku i jednym zdaniem problemu. Na komputerze obok tekstu zdjęcie.',
 H_('<!-- PROBLEM -->', '<!-- USES -->'), css('two col'))
add('3. KOMU SPRAWISZ RADOŚĆ (KARTY ZE ZDJĘCIAMI)',
 'Wyśrodkowany nadtytuł wersalikami, nagłówek „Komu sprawisz największą radość?” (druga część w kolorze marki), krótki podtytuł. Pod spodem 3 karty: duże zdjęcie u góry, pogrubiony tytuł („Dla dziecka i całej rodziny” itd.) i 1–2 zdania. Na telefonie karty jedna pod drugą, na komputerze obok siebie.',
 H_('<!-- USES -->', '<!-- SOLUTION -->'), css('use cards'))
add('4. ROZWIĄZANIE (ZDJĘCIE + TEKST + LISTA ✓)',
 'Duże zdjęcie z zaokrągleniem i cieniem (ludzie razem korzystający z produktu), pod nim (na komputerze obok) nadtytuł wersalikami, nagłówek z końcówką w kolorze marki, akapit i lista korzyści z zielonymi „✓” w kółkach – każda z pogrubionym początkiem. Na końcu przycisk CTA przewijający do wyboru zestawu.',
 H_('<!-- SOLUTION -->', '<!-- HOW IT WORKS -->'), css('two col'))
add('5. W 3 KROKACH',
 'Wyśrodkowany nadtytuł, nagłówek „… w 3 prostych krokach” (część w kolorze marki), krótki podtytuł. Pod spodem 3 karty: zdjęcie u góry z numerem (01, 02, 03) w zaokrąglonym kwadracie w kolorze marki w lewym górnym rogu, pod zdjęciem pogrubiony tytuł kroku i 1–2 zdania.',
 H_('<!-- HOW IT WORKS -->', '<!-- WHAT YOU GET -->'), css('steps'))
add('6. CO DOKŁADNIE DOSTAJESZ (ZAKŁADKI)',
 'Wyśrodkowany nadtytuł („WSZYSTKO W JEDNYM PUDEŁKU”), nagłówek „Co dokładnie dostajesz”, podtytuł. Pod spodem 3 zakładki-pigułki (aktywna biała z cieniem), a pod nimi biała karta z tytułem, opisem i wewnętrznym jasnym polem „W ZESTAWIE” z listą „✓”. Kliknięcie zakładki zmienia treść bez przeładowania.',
 H_('<!-- WHAT YOU GET -->', '<!-- COMPARE -->'), css('tabs'), jsr('/* TABS */', '/* 48h'))
add('7. TABELA PORÓWNAWCZA',
 'Wyśrodkowany nadtytuł („ZOBACZ RÓŻNICĘ”), nagłówek „Dlaczego [marka], a nie zwykły …?”, podtytuł. Tabela: kolumna „Kryterium”, wyróżniona kolumna marki (nagłówek ciemny w kolorze marki, komórki w jasnym odcieniu, zielone „✓”) i kolumna „zwykły produkt” z „✕”/„–”. Zaokrąglone rogi, cienkie linie między wierszami; na telefonie mieści się bez przewijania w bok.',
 H_('<!-- COMPARE -->', '<!-- REVIEWS -->'), css('compare'))
add('8. OPINIE KLIENTÓW (PASEK PRZEWIJANY W LEWO)',
 'Wyśrodkowany nadtytuł („OPINIE KLIENTÓW”), nagłówek z końcówką w kolorze marki, duża ocena „4,9 ★★★★★” i „Na podstawie X zweryfikowanych zakupów”. Pod spodem JEDEN rząd kart, który sam płynnie przesuwa się w lewo w pętli (start po pokazaniu się sekcji, bez zacięć). Karta: duże zdjęcie od klienta u góry, gwiazdki, tekst opinii (podobnej długości), na dole awatar w kółku (krajobraz) + imię i miasto + „Zweryfikowany zakup”. 12 opinii, polskie imiona, bez dat.',
 H_('<!-- REVIEWS -->', '<!-- ADULT -->'), css('reviews marquee'), jsr('/* REVIEWS */', '/* FAQ */'))
add('9. SEKCJA „NIE TYLKO DLA …” (ZDJĘCIE + 4 PUNKTY)',
 'Ciepłe, jasne tło. Duże zdjęcie z zaokrągleniem (osoba dorosła z produktem w przytulnym wnętrzu), pod nim (na komputerze obok) nadtytuł wersalikami („NIE TYLKO DLA DZIECI”), nagłówek-pytanie z końcówką w kolorze marki, akapit i 4 punkty z ikonami w kółkach (każdy w jednej linijce: pogrubiony początek + dopowiedzenie).',
 H_('<!-- ADULT -->', '<!-- FINAL CTA: 48h -->'), css('adult'))
add('10. KARTA PROMOCJI 48 H + FAQ',
 'Duża karta: u góry na jasnym tle zdjęcie produktu w zaokrąglonej ramce, które delikatnie unosi się i opada, z drobnymi iskierkami; pod spodem na białym tle nazwa produktu w kolorze marki z połyskiem przelatującym co 1,5 s, czerwony dzwoniący budzik + „48h!”, tekst „Nie przegap – cena promocyjna tylko przez 48 godzin!”, czerwone „⚠️ Liczba sztuk ograniczona ♡”, licznik GG:MM:SS w 3 kafelkach (sekundy tykają) i przycisk CTA z lekkim drganiem co 2 s. '
 'Licznik liczony od PIERWSZEJ wizyty na urządzeniu (koniec w localStorage) – przy kolejnej wizycie leci dalej; po 48 h karta znika (ceny bez zmian). '
 'Zaraz pod kartą sekcja FAQ: wyśrodkowany nagłówek, mail kontaktowy, 8 pytań jako akordeon (numer 01, 02… po lewej, plus obracający się w „×” po prawej, jedno otwarte naraz).',
 H_('<!-- FINAL CTA: 48h -->', '</main>'), css('final cta', 'faq') + '\n' + tl('.sk-deal','.sk-float','.sk-shine','.sk-spark','.sk-ring','.sk-nudge','.sk-limit','.sk-beat','@keyframes'),
 jsr('/* PROMO 48h', 'var BUNDLES=[') + '\n\n' + jsr('/* 48h licznik', '/* STICKY */') + '\n\n' + jsr('/* FAQ */', '/* POLICY PAGES */'))
add('11. STOPKA + REGULAMIN, PRYWATNOŚĆ, WYSYŁKA, ZWROTY, KONTAKT',
 'Stopka na jasnym tle, od logo do samego dołu: logo (ikona + nazwa + podpis), 2 zdania o sklepie, mail w ramce z ikoną ✉️, „Odpowiadamy najszybciej, jak to możliwe” z ikoną 🕘; nagłówek „INFORMACJE” i linki: Regulamin, Polityka prywatności, Polityka wysyłki, Zwroty i reklamacje, Kontakt; cienka linia, „[Marka] © rok” i „🔒 Bezpieczne płatności SSL · Dane chronione RODO”. '
 'Kliknięcie linku NIE przeładowuje strony – pokazuje podstronę w tym samym stylu: tytuł, numerowane punkty z tytułem i akapitem, „← Wróć do sklepu”, a pod treścią każdej podstrony formularz „Skontaktuj się z nami” (imię, e-mail, wiadomość → otwiera mail do sklepu). '
 'Teksty ogólne i trochę dłuższe, bez ryzykownych obietnic (bez „wysyłamy w 24 h”, bez godzin odpowiedzi; zwrot pieniędzy i reklamacje „w terminie przewidzianym przepisami prawa”; 14 dni na odstąpienie). Sklep prowadzi [MARKA], kontakt tylko [E-MAIL] – BEZ imienia, nazwiska i adresu.',
 rng(ln('<!-- POLICY PAGES -->'), ln('<!-- CART DRAWER -->')) + '\n\n' + rng(ln('<!-- CONTACT MODAL -->'), ln('<div class="sk-sticky"')), css('footer', 'policy pages', 'modal'), re.sub(r'\}\)\(\);\s*$', '', jsr('/* POLICY PAGES */')).rstrip())

out = ['# Prompty do każdej sekcji sklepu (ogólne)', '',
 'Kolejność: od PROMPTU 0 do PROMPTU 11, po kolei. Każdy prompt to JEDNO pole do skopiowania (opis + kod razem). '
 'Na początku dopisz swoje dane, np.: „Marka: …, produkt: …, kolor przewodni: …, ceny: …, e-mail: …” – Claude podmieni kolor w tokenach :root i teksty w [NAWIASACH]. '
 'Kod w każdym prompcie to WZÓR wyglądu i działania – Claude ma go odtworzyć 1:1 w strukturze i zachowaniu, a treści, zdjęcia i kolor dopasować do mojego produktu.', '',
 'Dopisek do każdego promptu (już jest wliczony): *teksty sprzedażowe po polsku, psychologiczne, bez nawiasów [ ] w wersji końcowej; zdjęcia moje albo wygenerowane; wszystko ma działać na telefonie.*', '']
for n, (t, p, h, c, j) in enumerate(sec):
    body = [p, '', 'Wzoruj się dokładnie na poniższym kodzie. Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści i zdjęcia dopasuj do mojego produktu.']
    if n > 0:
        body += ['', 'WAŻNE: ten prompt jest kompletny. Jeśli plik index.html jeszcze nie istnieje – utwórz go z poniższym <head> i CSS „FUNDAMENT”. Jeśli już istnieje – nie dubluj fundamentu, tylko dopisz sekcję we właściwym miejscu (kolejność sekcji: 1 góra strony, 2 problem, 3 komu, 4 rozwiązanie, 5 trzy kroki, 6 co dostajesz, 7 tabela, 8 opinie, 9 nie tylko dla…, 10 48h + FAQ, 11 stopka + polityki).',
                 '', '=== HEAD (fundament) ===', sec[0][2], '', '=== CSS FUNDAMENT (tokeny, przyciski, animacje, telefon) ===', sec[0][3]]
    if h: body += ['', '=== HTML SEKCJI ===', h]
    if c: body += ['', '=== CSS SEKCJI ===', c]
    if j:
        jj = (sec[0][4] + '\n\n') if n > 0 else ''
        js_all = jj + (j or '')
        body += ['', '=== JS (wszystko w jednym <script> na końcu <body>, owinięte w (function(){ ... })(); – część „pomocnicze” tylko raz) ===', js_all]
    out += ['---', '', '## PROMPT ' + t, '', 'Skopiuj całe pole poniżej jednym kliknięciem i wklej do Claude.', '', '````text', 'PROMPT ' + t, ''] + body + ['````', '']
open(os.path.join(H, 'PROMPTY-SEKCJE.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('OK', len(sec), 'promptów,', sum(len(x) for x in out) // 1024, 'KB')
