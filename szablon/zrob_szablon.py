# Buduje ogólny szablon sklepu (placeholdery w nawiasach) z lulavi-strona.html + koszyk.html
import re, base64, html
R='/home/user/Petenzo/'
src=open(R+'lulavi-strona.html').read()
kosz=open(R+'shopify-motyw/src/koszyk.html').read()

def ph(label, w=800, h=600, kolo=False):
    t=html.escape(label)
    if kolo:
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="#fff1ea"/><text x="50" y="56" font-family="Arial" font-size="13" font-weight="700" fill="#e8532a" text-anchor="middle">{t}</text></svg>'
    else:
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#fff1ea"/>'
             f'<rect x="12" y="12" width="{w-24}" height="{h-24}" rx="18" fill="none" stroke="#ffb59a" stroke-width="4" stroke-dasharray="14 10"/>'
             f'<text x="{w/2}" y="{h/2-10}" font-family="Arial" font-size="{int(w/22)}" font-weight="700" fill="#e8532a" text-anchor="middle">[ZDJĘCIE]</text>'
             f'<text x="{w/2}" y="{h/2+int(w/22)+6}" font-family="Arial" font-size="{int(w/32)}" fill="#66708a" text-anchor="middle">{t}</text></svg>')
    return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()

# --- zdjęcia -> ramki z opisem
opisy={'dom-panda':'produkt w użyciu – zdjęcie główne','samolot-lisek':'sytuacja 1 (np. podróż)','auto-zabka':'sytuacja 2','kuchnia-hipcio':'sytuacja 3',
 'dziadek-mis':'sytuacja 4','drzemka-kotek':'sytuacja 5','placz-dom-v2':'problem klienta','pociag-sowka':'zastosowanie 1','restauracja-hipcio':'zastosowanie 2',
 'placz-mis':'zastosowanie 3','relaks-sowka':'rozwiązanie / efekt','zaloz-lisek':'jak używać','rodzenstwo-pingwin-misio':'produkt + zadowolony klient'}
def img(m):
    k=m.group(1).split('/')[-1]
    if 'opinie' in m.group(1): return 'src="'+ph('',kolo=True)+'"'
    return 'src="'+ph(opisy.get(k,'zdjęcie produktu'))+'"'
src=re.sub(r'src="(zdjecia/[\w/-]+)\.jpg"',img,src)

def sub(a,b,cnt=1):
    global src
    assert src.count(a)>=1, a[:80]
    src=src.replace(a,b) if cnt==0 else src.replace(a,b,cnt)

# --- head
sub('<title>Lulavi</title>','<title>Szablon sklepu</title>')
src=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="[OPIS STRONY DLA GOOGLE – 1 zdanie: produkt + główna korzyść]">',src)
# --- pasek
src=re.sub(r'<div class="topbar"[^>]*>\s*<div class="ticker"[^>]*>.*?</div>',
 '<div class="topbar" aria-label="Pasek z korzyściami">\n  <div class="ticker" aria-hidden="true">'+('<span>[KORZYŚĆ 1 – np. darmowa wysyłka]</span><span>[KORZYŚĆ 2 – np. 14 dni na zwrot]</span><span>[PROMOCJA – np. −50 zł]</span><span>[HASŁO MARKI]</span>'*4)+'</div>',src,1,re.S)
# --- logo / menu
src=re.sub(r'(<a class="logo" href="#" aria-label=")[^"]*(">\s*<svg).*?</svg>\s*lulavi',
 r'\1[LOGO] – strona główna\2'[:0]+'<a class="logo" href="#" aria-label="Logo – strona główna"><span class="logo-ph">LOGO</span>\n      [NAZWA]',src,1,re.S)
for a,b in [('Gdzie się przydaje</a>','[MENU 1 – zastosowania]</a>'),('Jak to działa</a>','[MENU 2 – jak działa]</a>'),('Co dostajesz</a>','[MENU 3 – zestaw]</a>'),
            ('Dlaczego Lulavi</a>','[MENU 4 – porównanie]</a>'),('>Opinie</a>','>[MENU 5 – opinie]</a>'),('>Pytania</a>','>[MENU 6 – FAQ]</a>')]: sub(a,b)
# --- galeria
src=re.sub(r'aria-label="Zdjęcia Lulavi[^"]*"','aria-label="Zdjęcia produktu"',src)
for a,b in [('<span>🧸</span>Zakładasz w sekundę','<span>⭐</span>[PODPIS ZDJĘCIA 1 – korzyść]'),('<span>✈️</span>Cały lot bez płaczu','<span>⭐</span>[PODPIS ZDJĘCIA 2]'),
            ('<span>🚗</span>Spokojna jazda autem','<span>⭐</span>[PODPIS ZDJĘCIA 3]'),('<span>🍳</span>Gotujesz, a dziecko słucha bajki','<span>⭐</span>[PODPIS ZDJĘCIA 4]'),
            ('<span>☕</span>Dziadkowie mają chwilę oddechu','<span>⭐</span>[PODPIS ZDJĘCIA 5]'),('<span>😴</span>Łatwiej zasnąć przy ulubionej bajce','<span>⭐</span>[PODPIS ZDJĘCIA 6]')]: sub(a,b)
src=re.sub(r'(<figure class="slide"><img src="[^"]*") alt="[^"]*"',r'\1 alt="[OPIS ZDJĘCIA]"',src)
sub('<li><span>🚚</span><b>Darmowa wysyłka</b>Paczkomat InPost albo kurier pod adres · 6–9 dni roboczych</li>','<li><span>🚚</span><b>[DOSTAWA – np. Darmowa wysyłka]</b>[SPOSÓB DOSTAWY · CZAS DOSTAWY]</li>')
sub('<li><span>↩️</span><b>14 dni na zwrot</b>bez podawania przyczyny</li>','<li><span>↩️</span><b>[ZWROTY – np. 14 dni na zwrot]</b>[KRÓTKI DOPISEK]</li>')
sub('<li><span>🔒</span><b>Bezpieczne płatności</b>BLIK, karta, przelew</li>','<li><span>🔒</span><b>[PŁATNOŚCI]</b>[METODY PŁATNOŚCI]</li>')
sub('<li><span>🧸</span><b>Miękki polar</b>bez twardych nauszników</li>','<li><span>⭐</span><b>[CECHA PRODUKTU]</b>[KRÓTKI DOPISEK]</li>')
# --- buy box
sub('<span class="pill">🎧 Opaska ze słuchawkami · dla dzieci 3–12 lat</span>','<span class="pill">⭐ [KATEGORIA PRODUKTU · DLA KOGO]</span>')
sub('<h1>Płacz w samolocie? Marudzenie w aucie? Załóż Lulavi i miej <span class="hl">święty spokój</span></h1>',
    '<h1>[NAGŁÓWEK GŁÓWNY – problem klienta + obietnica] <span class="hl">[EFEKT KOŃCOWY]</span></h1>')
src=re.sub(r'<p class="lead">Miękka opaska z wbudowanymi.*?</p>','<p class="lead">[PODTYTUŁ – czym jest produkt i co zyskuje klient, 1–2 zdania]</p>',src,1,re.S)
sub('<div class="rating">🚚 Darmowa wysyłka · ↩️ 14 dni na zwrot · 🦊 9 zwierzaków do wyboru</div>','<div class="rating">🚚 [DOSTAWA] · ↩️ [ZWROTY] · ⭐ [LICZBA WARIANTÓW]</div>')
sub('<span class="price">149,99 zł</span>','<span class="price">[CENA]</span>')
sub('<span class="old">199,99 zł</span>','<span class="old">[STARA CENA]</span>')
sub('<span class="save">−50 zł</span>','<span class="save">[−ZNIŻKA]</span>')
src=re.sub(r'(<div class="price-row">.*?</div>\s*<ul class="ticks">).*?(</ul>)',
 r'\1\n        <li>[KORZYŚĆ 1]</li>\n        <li>[KORZYŚĆ 2]</li>\n        <li>[KORZYŚĆ 3]</li>\n        <li>[KORZYŚĆ 4]</li>\n        <li>[KORZYŚĆ 5]</li>\n      \2',src,1,re.S)
sub('<span>Kup więcej, zapłać mniej</span>','<span>[HASŁO ZESTAWÓW – np. Kup więcej, zapłać mniej]</span>')
sub('<b>Kup 1</b><small class="green">Darmowa wysyłka</small></div>\n            <div class="offer-price"><b>149,99 zł</b><s>199,99 zł</s>',
    '<b>[Kup 1]</b><small class="green">[DOPISEK – np. darmowa wysyłka]</small></div>\n            <div class="offer-price"><b>[CENA 1 SZT.]</b><s>[STARA CENA]</s>')
sub('<span class="offer-badge">Najczęściej wybierane</span>','<span class="offer-badge">[ETYKIETA – np. Najczęściej wybierane]</span>')
sub('<b>Kup 2</b><small class="green">Oszczędzasz 50 zł · darmowa wysyłka</small></div>\n            <div class="offer-price"><b>249,99 zł</b><s>299,98 zł</s>',
    '<b>[Kup 2]</b><small class="green">[Oszczędzasz X zł · dostawa]</small></div>\n            <div class="offer-price"><b>[CENA 2 SZT.]</b><s>[STARA CENA]</s>')
sub('<span class="offer-badge">Najlepsza cena</span>','<span class="offer-badge">[ETYKIETA – np. Najlepsza cena]</span>')
sub('<b>Kup 3</b><small class="green">Oszczędzasz 120 zł · darmowa wysyłka</small></div>\n            <div class="offer-price"><b>329,99 zł</b><s>449,97 zł</s>',
    '<b>[Kup 3]</b><small class="green">[Oszczędzasz X zł · dostawa]</small></div>\n            <div class="offer-price"><b>[CENA 3 SZT.]</b><s>[STARA CENA]</s>')
sub('data-price="149,99"','data-price="[CENA 1 SZT.]"'); sub('data-price="249,99"','data-price="[CENA 2 SZT.]"'); sub('data-price="329,99"','data-price="[CENA 3 SZT.]"')
sub('<b>14 dni na zwrot</b>\n          <span>Jeśli dziecko nie polubi Lulavi, oddasz ją bez podawania przyczyny i odzyskasz pieniądze.</span>',
    '<b>[GWARANCJA – np. 14 dni na zwrot]</b>\n          <span>[ZDANIE O GWARANCJI – co klient może zrobić, jeśli produkt mu nie podpasuje]</span>')
sub('Dodaj do koszyka: 249,99 zł</button>','Dodaj do koszyka: [CENA]</button>')
sub('<p class="under-btn">🚚 Darmowa wysyłka: Paczkomat InPost albo kurier · 14 dni na zwrot · BLIK, karta, przelew</p>','<p class="under-btn">🚚 [DOSTAWA] · [ZWROTY] · [METODY PŁATNOŚCI]</p>')
# --- problem
sub('<span class="eyebrow">Brzmi znajomo?</span>','<span class="eyebrow">[NADTYTUŁ – np. Brzmi znajomo?]</span>')
sub('<h2>Dziecko płacze, a Ty potrzebujesz <span class="hl">chwili spokoju</span></h2>','<h2>[NAGŁÓWEK PROBLEMU – frustracja klienta] <span class="hl">[SŁOWO KLUCZ]</span></h2>')
sub('<p class="lead">To nie wina dziecka. Nudzi się, jest zmęczone i nie ma czym zająć głowy.</p>','<p class="lead">[ZDANIE WYJAŚNIAJĄCE PROBLEM]</p>')
src=re.sub(r'<ul class="xlist">.*?</ul>','<ul class="xlist">\n'+''.join(f'        <li>[PROBLEM {i}]</li>\n' for i in range(1,7))+'      </ul>',src,1,re.S)
sub('<div class="summary">Efekt? Zmęczone dziecko, zestresowany rodzic i zero chwili dla siebie.</div>','<div class="summary">[PODSUMOWANIE – skutek problemu w 1 zdaniu]</div>')
# --- gdzie
sub('<span class="eyebrow">Gdzie się przydaje</span>','<span class="eyebrow">[NADTYTUŁ – np. Gdzie się przydaje]</span>')
sub('<h2>Wszędzie tam, gdzie potrzebujesz <span class="hl">chwili spokoju</span></h2>','<h2>[NAGŁÓWEK ZASTOSOWAŃ] <span class="hl">[SŁOWO KLUCZ]</span></h2>')
sub('<p>Jedna opaska na podróże, wyjścia i domowe kryzysy.</p>','<p>[PODTYTUŁ ZASTOSOWAŃ]</p>')
src=re.sub(r'<h3>W podróży</h3><p>[^<]*</p>','<h3>[ZASTOSOWANIE 1]</h3><p>[OPIS 1 ZDANIE]</p>',src)
src=re.sub(r'<h3>W restauracji</h3><p>[^<]*</p>','<h3>[ZASTOSOWANIE 2]</h3><p>[OPIS 1 ZDANIE]</p>',src)
src=re.sub(r'<h3>Gdy jest płacz</h3><p>[^<]*</p>','<h3>[ZASTOSOWANIE 3]</h3><p>[OPIS 1 ZDANIE]</p>',src)
# --- rozwiązanie
sub('<span class="eyebrow">Poznaj Lulavi</span>','<span class="eyebrow">[NADTYTUŁ – np. Poznaj (NAZWA PRODUKTU)]</span>')
sub('<h2>Ulubiona bajka w <span class="hl">miękkiej opasce</span>, która nie spada</h2>','<h2>[NAGŁÓWEK ROZWIĄZANIA – jak produkt rozwiązuje problem] <span class="hl">[SŁOWO KLUCZ]</span></h2>')
src=re.sub(r'(<span class="hl">\[SŁOWO KLUCZ\]</span></h2>\s*<ul class="ticks">).*?(</ul>)',r'\1\n'+''.join(f'        <li>[ZALETA {i}]</li>\n' for i in range(1,7))+r'      \2',src,1,re.S)
# --- kroki
sub('<span class="eyebrow">Proste jak klik</span>','<span class="eyebrow">[NADTYTUŁ – np. Proste jak klik]</span>')
sub('<h2>Spokój w <span class="hl">3 krokach</span></h2>','<h2>[EFEKT] w <span class="hl">3 krokach</span></h2>')
sub('<p>Bez aplikacji i bez plątających się kabli.</p>','<p>[PODTYTUŁ – co jest proste]</p>')
for i,(a,b) in enumerate([('Włącz i połącz','Przytrzymaj przycisk i wybierz opaskę na liście Bluetooth w telefonie.'),('Włącz bajkę lub muzykę','Audiobook, piosenki, biały szum: cokolwiek dziecko lubi.'),('Załóż i odpocznij','Rzep dopasujesz w sekundę. Dziecko słucha, Ty masz chwilę dla siebie.')],1):
    sub(f'<b>{a}</b>{b}',f'<b>[KROK {i}]</b>[OPIS KROKU {i}]')
# --- w paczce
sub('<span class="eyebrow">W paczce</span>','<span class="eyebrow">[NADTYTUŁ – np. W paczce]</span>')
sub('<h2>Co dokładnie <span class="hl">dostajesz</span></h2>','<h2>Co dokładnie <span class="hl">dostajesz</span></h2>')
sub('<h3>Lulavi: gotowa od pierwszego dnia</h3>','<h3>[NAZWA PRODUKTU]: [HASŁO]</h3>')
sub('<p>Wszystko w jednym pudełku. Wyjmij, naładuj i włącz pierwszą bajkę jeszcze dziś.</p>','<p>[OPIS ZESTAWU – 1–2 zdania]</p>')
for tid,pref,n in [('tab-zawartosc','ELEMENT ZESTAWU',4),('tab-parametry','PARAMETR',4),('tab-pielegnacja','WSKAZÓWKA',3)]:
    src=re.sub(r'(<div role="tabpanel" id="'+tid+r'"[^>]*>\s*<div class="panel-title">[^<]*</div>\s*<ul class="ticks">).*?(</ul>)',
               r'\1\n'+''.join(f'            <li>[{pref} {i}]</li>\n' for i in range(1,n+1))+r'          \2',src,1,re.S)
# --- porównanie
sub('<span class="eyebrow">Porównanie</span>','<span class="eyebrow">[NADTYTUŁ – np. Porównanie]</span>')
sub('<h2>Dlaczego <span class="hl">Lulavi</span>, a nie zwykłe słuchawki?</h2>','<h2>Dlaczego <span class="hl">[TWÓJ PRODUKT]</span>, a nie [ALTERNATYWA]?</h2>')
sub('<tr><th>Cecha</th><th class="us">Lulavi</th><th>Zwykłe słuchawki</th><th>Bajka na głos z telefonu</th></tr>','<tr><th>Cecha</th><th class="us">[TWÓJ PRODUKT]</th><th>[ALTERNATYWA 1]</th><th>[ALTERNATYWA 2]</th></tr>')
for i,t in enumerate(['Miękka, nie uciska uszu','Nie spada przy zabawie','Nie przeszkadza innym','Sprawdza się w samolocie','Wygodna do drzemki','Dziecko chce ją nosić'],1):
    sub(f'<td>{t}</td>',f'<td>[CECHA {i}]</td>')
# --- opinie
sub('<span class="eyebrow">Opinie kupujących</span>','<span class="eyebrow">[NADTYTUŁ – np. Opinie kupujących]</span>')
sub('<h2>Zobacz, co mówią <span class="hl">rodzice</span></h2>','<h2>Zobacz, co mówią <span class="hl">[KLIENCI]</span></h2>')
sub('<p class="zrodlo">Opinie tego modelu opaski od kupujących na Amazon w Europie, przetłumaczone na polski.</p>','<p class="zrodlo">[ŹRÓDŁO OPINII – skąd pochodzą]</p>')
src=re.sub(r'<b class="tytul">[^<]*</b>','<b class="tytul">[TYTUŁ OPINII]</b>',src)
src=re.sub(r'<blockquote>[^<]*</blockquote>','<blockquote>„[TREŚĆ OPINII – prawdziwa opinia klienta]”</blockquote>',src)
src=re.sub(r'<b>[^<]*<i class="ok">✔</i></b>Zweryfikowany zakup · wzór [^<]*','<b>[IMIĘ] <i class="ok">✔</i></b>Zweryfikowany zakup · [WARIANT]',src)
# --- CTA
src=re.sub(r'(<div class="card cta">\s*<img src="[^"]*") alt="[^"]*"',r'\1 alt="[OPIS ZDJĘCIA]"',src)
sub('<h2>Chwila spokoju jest <span class="hl">bliżej, niż myślisz</span></h2>','<h2>[NAGŁÓWEK KOŃCOWY – powtórzenie obietnicy] <span class="hl">[SŁOWO KLUCZ]</span></h2>')
sub('<p>Daj dziecku jego bajkę, a sobie święty spokój. Masz 14 dni na zwrot, więc nic nie ryzykujesz.</p>','<p>[ZDANIE ZACHĘTY + GWARANCJA]</p>')
sub('Zamawiam Lulavi: 149,99 zł</a>','Zamawiam [NAZWA PRODUKTU]: [CENA]</a>')
sub('<p class="under-btn" style="text-align:left">Darmowa wysyłka · 14 dni na zwrot</p>','<p class="under-btn" style="text-align:left">[DOSTAWA] · [ZWROTY]</p>')
# --- FAQ
sub('<b>kontakt@mivro.pl</b></p>','<b>[E-MAIL KONTAKTOWY]</b></p>')
src=re.sub(r'<div class="faq-list">.*?</div>\s*</div>\s*</section>','<div class="faq-list">\n'+''.join(
 f'      <details>\n        <summary>[PYTANIE {i}{" – np. Jak wygląda dostawa?" if i==7 else ""}]</summary>\n        <p>[ODPOWIEDŹ {i}]</p>\n      </details>\n' for i in range(1,9))+'    </div>\n  </div>\n</section>',src,1,re.S)
# --- stopka
sub('<a class="logo" href="/">lulavi</a>','<a class="logo" href="/">[NAZWA SKLEPU]</a>')
src=re.sub(r'(<div class="f-brand">\s*<a class="logo" href="/">\[NAZWA SKLEPU\]</a>\s*)<p>[^<]*</p>',r'\1<p>[OPIS SKLEPU – 1–2 zdania]</p>',src)
sub('href="mailto:kontakt@mivro.pl"','href="#"'); sub('</svg></span>kontakt@mivro.pl</a>','</svg></span>[E-MAIL KONTAKTOWY]</a>')
sub('Odpowiadamy w 24 h · Pon–Pt','[GODZINY ODPOWIEDZI]')
sub('<span>LULAVI.PL © 2026</span>','<span>[NAZWA SKLEPU] © [ROK]</span>')
# --- warianty (kółka)
src=re.sub(r"var WZORY = \[.*?\];","var WZORY = ["+",".join(f"{{ id: 'w{i}', nazwa: '[WARIANT {i}]' }}" for i in range(1,7))+"];",src,1,re.S)
minis={f'zdjecia/warianty/mini-w{i}.jpg':ph(f'W{i}',kolo=True) for i in range(1,7)}
import json
src=src.replace("<script>\n  function obraz","<script>window.OBRAZY="+json.dumps(minis)+";</script>\n<script>\n  function obraz",1)
sub("label.innerHTML = (n > 1 ? 'Opaska ' + i + ': ' : 'Wzór: ')","label.innerHTML = (n > 1 ? '[Sztuka] ' + i + ': ' : '[Wariant]: ')",0)
sub("grid.setAttribute('aria-label', 'Wzór opaski nr ' + i);","grid.setAttribute('aria-label', 'Wariant nr ' + i);")
src=src.replace('Jeśli dziecko nie polubi','')
# logo placeholder style
sub('</style>','  .logo-ph { display:inline-grid; place-items:center; width:46px; height:34px; border:2px dashed var(--coral); border-radius:10px; font-size:10px; font-weight:800; color:var(--coral); letter-spacing:.04em; }\n</style>')

# --- koszyk ogólny
k=kosz
k=k.replace("function zl(gr) { return (gr / 100).toFixed(2).replace('.', ',') + ' zł'; }","function zl(gr) { return '[KWOTA]'; }")
k=k.replace('🚚 Darmowa dostawa · ↩️ 14 dni na zwrot','🚚 [DOSTAWA] · ↩️ [ZWROTY]')
k=k.replace('📦 Paczkomat InPost<small>GRATIS</small>','📦 [DOSTAWA 1 – np. Paczkomat]<small>[CENA DOSTAWY]</small>')
k=k.replace('🚚 Kurier pod adres<small>GRATIS</small>','🚚 [DOSTAWA 2 – np. Kurier]<small>[CENA DOSTAWY]</small>')
k=k.replace('W kasie zaznacz wybraną dostawę. Paczkomat wybierzesz z listy lub mapy zaraz po zapłacie.','[INFORMACJA – jak klient wybiera dostawę w kasie]')
k=k.replace('Lulavi – opaska ze słuchawkami','[NAZWA PRODUKTU]')
k=k.replace("'Dobierz drugą opaskę za <span>100 zł</span> (zamiast 149,99 zł)' : 'Dobierz trzecią opaskę za <span>80 zł</span> (zamiast 149,99 zł)'","'Dobierz drugą sztukę za <span>[CENA]</span> (zamiast [CENA])' : 'Dobierz trzecią sztukę za <span>[CENA]</span> (zamiast [CENA])'")
k=k.replace("', np. dla rodzeństwa:</p>","', [DOPISEK – np. dla kogo]:</p>")
k=k.replace('Twój koszyk jest pusty.<br>Wybierz swojego zwierzaka 🦊🐼🐸','Twój koszyk jest pusty.<br>[ZACHĘTA DO WYBORU PRODUKTU]')
k=k.replace('>Wybierz opaskę</button>','>[Wybierz produkt]</button>')
k=k.replace("'<div class=\"linia dost\"><span>Dostawa</span><span>GRATIS</span></div>'","'<div class=\"linia dost\"><span>Dostawa</span><span>[CENA DOSTAWY]</span></div>'")
k=k.replace('class="glowna" href="/checkout"','class="glowna" href="/checkout" onclick="alert(&quot;Tu klient przechodzi do kasy&quot;);return false"')
k=k.replace('<a href="/checkout">🚚','<a href="/checkout" onclick="alert(&quot;Tu klient przechodzi do kasy&quot;);return false">🚚')
shim="""<script>
  (function () {
    var poz = [];
    function stan() {
      var n = poz.reduce(function (a, p) { return a + p.quantity; }, 0);
      return { item_count: n, original_total_price: n * 10000, total_price: n * 10000, total_discount: 0,
        items: poz.map(function (p) { var w = WZORY[p.variant_id - 100]; return { key: 'k' + p.variant_id, quantity: p.quantity, variant_title: w.nazwa, image: w.img, original_line_price: p.quantity * 10000 }; }) };
    }
    window.fetch = function (url, o) {
      var d = o && o.body ? JSON.parse(o.body) : {};
      if (url.indexOf('/cart/add.js') === 0) d.items.forEach(function (x) { var f = poz.filter(function (p) { return p.variant_id === x.id; })[0]; if (f) f.quantity += x.quantity; else poz.push({ variant_id: x.id, quantity: x.quantity }); });
      if (url.indexOf('/cart/change.js') === 0) { poz.forEach(function (p) { if ('k' + p.variant_id === d.id) p.quantity = d.quantity; }); poz = poz.filter(function (p) { return p.quantity > 0; }); }
      return Promise.resolve({ ok: true, json: function () { return Promise.resolve(stan()); } });
    };
  })();
</script>
"""
src=src.replace("[WARIANT 6]' }];","[WARIANT 6]' }];\n  WZORY.forEach(function (w, i) { w.vid = 100 + i; w.img = obraz('zdjecia/warianty/mini-'+w.id+'.jpg'); });",1)
src=src.replace("b.setAttribute('aria-label', w.nazwa);","b.setAttribute('aria-label', w.nazwa);\n          b.dataset.vid = w.vid;",1)
src=src.replace("obraz('zdjecia/warianty/mini-' + w.id + '.jpg')","w.img",1)
i=src.index('</script>',src.index('function obraz'))+9
src=src[:i]+'\n'+shim+k+src[i:]
import collections; print([src[m.start()-60:m.start()+40] for m in re.finditer("Lulavi|lulavi|opask|Opask|dzieck|InPost",src)])
src=src.replace("cta.textContent = 'Dodaj do koszyka: ' + wybrany.dataset.price + ' zł';","cta.textContent = 'Dodaj do koszyka: ' + wybrany.dataset.price;")
src=re.sub(r' alt="[^"]+"',' alt="[OPIS ZDJĘCIA]"',src)
open(R+'szablon/szablon-sklepu.html','w').write(src)
print('ok', len(src)//1024,'KB')
