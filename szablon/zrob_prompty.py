# Generuje PROMPTY-SEKCJE.md: ogólne prompty + kod do każdej sekcji (na bazie szablon.html)
import re, os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, 'szablon.html'), encoding='utf-8').read()
# neutralne nazwy i jeden ogólny kolor
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

INTRO_JS = jsr('(function(){', '/* BUNDLES */')
add('0. FUNDAMENT (wklej jako pierwszy)',
 'Zbuduj jednostronicowy sklep z jednym produktem jako JEDEN plik index.html (HTML + CSS + czysty JS, bez frameworków). '
 'Wszystkie kolory, cienie i zaokrąglenia trzymaj w tokenach CSS w :root (prefiks --sk-), żeby zmiana koloru marki była w jednym miejscu – kolor podam osobno, na razie użyj tego niebieskiego. '
 'Czcionki: Poppins (tekst) + Russo One (nagłówki, logo). Mobile-first, max szerokość treści ok. 1200 px, sekcje z dużym oddechem, karty z miękkim cieniem i zaokrągleniem 20 px, przyciski CTA z gradientem i cieniem. '
 'Strona ma dwa „widoki”: #skHome (strona produktu) i #skPages (podstrony polityk) przełączane funkcją skShow(). '
 'Poniżej: <head>, bazowy CSS (tokeny, reset, przyciski, kontenery, animacje, wersja mobilna) i początek skryptu (zdjęcia, galeria). Kolejne prompty dokładają po jednej sekcji – wstawiaj je w tej kolejności.',
 head, css('base') + '\n\n/* animacje i telefon */\n' + tailCSS, INTRO_JS)
add('1. PASEK PROMOCJI + MENU Z LOGO',
 'Na samej górze cienki pasek w kolorze marki z napisami przesuwającymi się płynnie od prawej do lewej w nieskończoność (np. darmowa dostawa, zwroty, promocja, hasło marki – teksty powielone 3×, żeby nie było przerwy). '
 'Pod nim biały, przyklejony nagłówek: po lewej logo (mała ikona produktu ok. 46 px + nazwa sklepu i mały podpis wersalikami), na środku menu z kotwicami do sekcji, po prawej ikona koszyka z licznikiem. Na telefonie menu chowa się pod „hamburgerem” i wysuwa na pełny ekran.',
 rng(ln('<body>') + 1, ln('<main id="skHome"')), css('top bar marquee', 'nav'))
add('2. HERO: GALERIA, CENA, ZESTAWY + PASEK KORZYŚCI',
 'Pierwszy ekran sprzedażowy w dwóch kolumnach. Lewa: galeria (duże zdjęcie z podpisem na dole + miniatury), na komputerze przyklejona (sticky) podczas przewijania, na telefonie przesuwana palcem (swipe), bez strzałek. Pierwsze zdjęcie = ludzie używający produktu. '
 'Prawa: plakietki („Hit…” + „Liczba sztuk ograniczona”), nazwa, gwiazdki z liczbą opinii i „X osób ogląda teraz”, cena + cena przekreślona + procent rabatu, lista 6 korzyści z ikonami „✓”, wybór zestawu 1/2/3 sztuki jako karty z radiem (plakietki „Najczęściej wybierany”, „Najlepsza cena”) – po kliknięciu zestawu pod nim pojawia się wybór wariantu dla każdej sztuki (dwa małe przyciski A/B na każdą sztukę), duży przycisk „Dodaj do koszyka · cena”, linijka zaufania i kolorowe logotypy płatności. '
 'Cena w nagłówku, przycisku i pasku na dole zmienia się po wyborze zestawu. Pod hero pełnoszeroki pasek w kolorze marki z 4 kafelkami (dostawa, zwroty, płatności, ocena) – na telefonie 2×2.',
 H_('<!-- HERO -->', '<!-- PROBLEM -->'), css('hero', 'benefit strip', 'upsell / bundle') + '\n' + tl('.sk-flower','.sk-var','.sk-pill','.sk-gallery'), jsr('/* BUNDLES */', '/* CART */').split('/* CART */')[0])
add('3. PROBLEM',
 'Sekcja „ból klienta”: dwie kolumny – zdjęcie (na telefonie nad tekstem) i tekst: mały nadtytuł wersalikami, mocny nagłówek nazywający problem, 2 krótkie akapity budujące emocję i lista 3–4 punktów z czerwonym „✕”. Tło jasne, zdjęcie z zaokrągleniem i cieniem.',
 H_('<!-- PROBLEM -->', '<!-- USES -->'), css('two col'))
add('4. KOMU SPRAWISZ RADOŚĆ (3 KARTY)',
 'Wyśrodkowany nagłówek + podtytuł, pod spodem 3 karty obok siebie (na telefonie jedna pod drugą): zdjęcie u góry, krótki tytuł i 1–2 zdania. Karty lekko unoszą się po najechaniu.',
 H_('<!-- USES -->', '<!-- SOLUTION -->'), css('use cards'))
add('5. ROZWIĄZANIE',
 'Lustrzane odbicie sekcji „Problem”: tekst po lewej, zdjęcie po prawej. Nadtytuł, nagłówek przedstawiający produkt jako rozwiązanie, akapit i lista korzyści z zielonym „✓”, na końcu przycisk CTA przewijający do wyboru zestawu.',
 H_('<!-- SOLUTION -->', '<!-- HOW IT WORKS -->'), css('two col'))
add('6. W 3 KROKACH',
 'Nagłówek „Jak to działa” + 3 kroki w rzędzie (na telefonie w kolumnie): duży numer w kółku w kolorze marki, zdjęcie, tytuł kroku i jedno zdanie. Między krokami subtelna linia/strzałka.',
 H_('<!-- HOW IT WORKS -->', '<!-- WHAT YOU GET -->'), css('steps'))
add('7. CO DOSTAJESZ (ZAKŁADKI)',
 'Sekcja z 3 zakładkami (np. „W zestawie”, „Specyfikacja”, „Dla kogo”): przyciski-pigułki u góry, aktywna wypełniona kolorem marki; treść zakładki to lista lub krótki tekst obok zdjęcia. Przełączanie bez przeładowania.',
 H_('<!-- WHAT YOU GET -->', '<!-- COMPARE -->'), css('tabs'), jsr('/* TABS */', '/* 48h'))
add('8. TABELA PORÓWNAWCZA (MY vs INNI)',
 'Tabela 3 kolumny: cecha | nasz produkt (kolumna wyróżniona kolorem marki, z logo) | „zwykłe rozwiązanie”. Wiersze z „✓” i „✕”/„–”, pod tabelą krótka legenda co znaczy „–”. Na telefonie tabela mieści się bez przewijania w bok.',
 H_('<!-- COMPARE -->', '<!-- REVIEWS -->'), css('compare'))
add('9. OPINIE (JEDEN PASEK PRZEWIJANY W LEWO)',
 'Nagłówek z oceną (np. 4,9/5 i liczba opinii). Pod spodem JEDEN rząd kart opinii, który sam płynnie przesuwa się w lewo w pętli (animacja startuje, gdy sekcja pojawi się na ekranie, translate3d, bez zacięć; pauza po najechaniu tylko na komputerze). '
 'Karta: awatar w kółku (zdjęcie krajobrazu, nie twarz), imię + miasto, 5 gwiazdek, „Zweryfikowany zakup”, tekst opinii – wszystkie opinie podobnej długości, bez dat. 12 opinii z polskimi imionami.',
 H_('<!-- REVIEWS -->', '<!-- ADULT -->'), css('reviews marquee'), jsr('/* REVIEWS */', '/* FAQ */'))
add('10. SEKCJA Z 4 PUNKTAMI (DLA KOGO / DLACZEGO)',
 'Dwie kolumny: duże zdjęcie i blok tekstu z nagłówkiem oraz 4 punktami z ikonami w kółkach (każdy punkt w jednej linijce: pogrubiony początek + dopowiedzenie). Na końcu przycisk CTA.',
 H_('<!-- ADULT -->', '<!-- FINAL CTA: 48h -->'), css('adult'))
add('11. KARTA PROMOCJI 48 H Z ANIMACJAMI',
 'Duża karta w kolorze marki: po lewej zdjęcie produktu, które delikatnie unosi się w górę i w dół (float) z iskierkami; po prawej nazwa z przelatującym połyskiem co 1,5 s, plakietka z dzwoniącym zegarem, tekst „cena promocyjna tylko przez 48 godzin” + „Liczba sztuk ograniczona”, licznik GG:MM:SS (sekundy „tykają”) i przycisk CTA z lekkim drganiem co 2 s. '
 'Licznik liczony od PIERWSZEJ wizyty na danym urządzeniu (koniec zapisany w localStorage) – przy kolejnej wizycie czas leci dalej. Po upływie 48 h cała ta sekcja znika (ceny zostają bez zmian).',
 H_('<!-- FINAL CTA: 48h -->', '<!-- FAQ -->'), css('final cta') + '\n' + tl('.sk-deal','.sk-float','.sk-shine','.sk-spark','.sk-ring','.sk-nudge','.sk-limit','.sk-beat','@keyframes'), jsr('/* PROMO 48h', 'var BUNDLES=[') + '\n\n' + jsr('/* 48h licznik', '/* STICKY */'))
add('12. FAQ (NAJCZĘŚCIEJ ZADAWANE PYTANIA)',
 'Wyśrodkowany nagłówek + mail kontaktowy pod spodem. Lista 8 pytań jako akordeon, wyśrodkowana, wąska kolumna: każde pytanie w jednej linijce z numerem (01, 02…) po lewej i plusem po prawej, który obraca się w „×”; odpowiedź rozwija się płynnie. Otwarte jest jedno pytanie naraz.',
 H_('<!-- FAQ -->', '</main>'), css('faq'), jsr('/* FAQ */', '/* POLICY PAGES */'))
add('13. STOPKA + WSZYSTKIE POLITYKI (REGULAMIN, PRYWATNOŚĆ, WYSYŁKA, ZWROTY, KONTAKT)',
 'Stopka od logo do samego dołu: po lewej logo + nazwa, krótki opis sklepu, mail i informacja o kontakcie; po prawej kolumna „Informacje” z linkami: Regulamin, Polityka prywatności, Polityka wysyłki, Zwroty i reklamacje, Kontakt. Na dole pasek z „© rok” i skrótem zaufania. '
 'Kliknięcie linku NIE przeładowuje strony – pokazuje podstronę (widok #skPages) w tym samym stylu: nagłówek, punkty numerowane z tytułem i akapitem, przycisk „← Wróć do sklepu”, a pod treścią każdej polityki formularz „Skontaktuj się z nami” (imię, e-mail, wiadomość → otwiera mail do sklepu). '
 'Teksty polityk ogólne, trochę dłuższe, bez ryzykownych obietnic (bez „wysyłamy w 24 h”, bez konkretnych godzin odpowiedzi; terminy reklamacji/zwrotu pieniędzy „w terminie przewidzianym przepisami prawa”, 14 dni na odstąpienie). Sklep prowadzi [NAZWA SKLEPU], kontakt tylko przez [E-MAIL], BEZ imienia, nazwiska i adresu.',
 rng(ln('<!-- POLICY PAGES -->'), ln('<!-- CART DRAWER -->')) + '\n\n' + rng(ln('<!-- CONTACT MODAL -->'), ln('<div class="sk-sticky"')), css('footer', 'policy pages', 'modal'), jsr('/* POLICY PAGES */'))
add('14. KOSZYK, OKNO DOSTAWY, PASEK NA DOLE TELEFONU',
 'Koszyk jako panel wysuwany z prawej (z przyciemnieniem tła): pozycje ze zdjęciem, nazwą, wybranym wariantem, licznikiem –/+ i koszem; pasek postępu „Dodaj jeszcze 1 szt. i zapłać mniej”; podsumowanie (cena regularna, łączny rabat, razem); przycisk „Realizuj zakup” i logotypy płatności. Koszyk zapisuje się w localStorage. '
 '„Realizuj zakup” otwiera małe okno wyboru dostawy (np. „📦 Paczkomat – GRATIS”, „🚚 Kurier pod adres – GRATIS”, dopisek, że adres poda się w kasie) i przycisk „Przejdź do płatności”, który od razu przenosi do kasy (w Shopify: link /cart/IDwariantu:ilość,… – bez czekania). '
 'Na telefonie przy przewijaniu pojawia się przyklejony dolny pasek z nazwą, ceną i przyciskiem „Do koszyka”; po dodaniu wyskakuje mały komunikat „Dodano do koszyka ✓”.',
 rng(ln('<!-- CART DRAWER -->'), ln('<!-- CONTACT MODAL -->')) + '\n\n' + rng(ln('<div class="sk-sticky"'), ln('<script>')), css('drawer', 'modal') + '\n' + stickyCSS, jsr('/* CART */', '/* TABS */') + '\n\n' + jsr('/* STICKY */', '/* REVIEWS */'))

out = ['# Prompty do każdej sekcji sklepu (ogólne)', '',
 'Kolejność: od PROMPTU 0 do PROMPTU 14, po kolei. Każdy prompt to JEDNO pole do skopiowania (opis + kod razem). '
 'Na początku dopisz swoje dane, np.: „Marka: …, produkt: …, kolor przewodni: …, ceny: …, e-mail: …” – Claude podmieni kolor w tokenach :root i teksty w [NAWIASACH]. '
 'Kod w każdym prompcie to WZÓR wyglądu i działania – Claude ma go odtworzyć 1:1 w strukturze i zachowaniu, a treści, zdjęcia i kolor dopasować do mojego produktu.', '',
 'Dopisek do każdego promptu (już jest wliczony): *teksty sprzedażowe po polsku, psychologiczne, bez nawiasów [ ] w wersji końcowej; zdjęcia moje albo wygenerowane; wszystko ma działać na telefonie.*', '']
for n, (t, p, h, c, j) in enumerate(sec):
    body = [p, '', 'Wzoruj się dokładnie na poniższym kodzie. Zachowaj klasy z prefiksem sk- i tokeny --sk-, treści i zdjęcia dopasuj do mojego produktu.']
    if n > 0:
        body += ['', 'WAŻNE: ten prompt jest kompletny. Jeśli plik index.html jeszcze nie istnieje – utwórz go z poniższym <head> i CSS „FUNDAMENT”. Jeśli już istnieje – nie dubluj fundamentu, tylko dopisz sekcję we właściwym miejscu (kolejność sekcji: pasek+menu, hero, problem, komu, rozwiązanie, 3 kroki, zakładki, tabela, opinie, 4 punkty, 48h, FAQ, stopka+polityki, koszyk).',
                 '', '=== HEAD (fundament) ===', sec[0][2], '', '=== CSS FUNDAMENT (tokeny, przyciski, animacje, telefon) ===', sec[0][3]]
    if h: body += ['', '=== HTML SEKCJI ===', h]
    if c: body += ['', '=== CSS SEKCJI ===', c]
    if j or n == 2:
        jj = (sec[0][4] + '\n\n') if n > 0 else ''
        if n == 2: jj += sec[14][4] + '\n\n'
        body += ['', '=== JS (wstaw do jednego <script> na końcu <body>, w środku (function(){ ... })();) ===', jj + (j or '')]
    out += ['---', '', '## PROMPT ' + t, '', 'Skopiuj całe pole poniżej jednym kliknięciem i wklej do Claude.', '', '````text', 'PROMPT ' + t, ''] + body + ['````', '']
open(os.path.join(H, 'PROMPTY-SEKCJE.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('OK', len(sec), 'promptów,', sum(len(x) for x in out) // 1024, 'KB')
