"""Robi OGÓLNY szablon (placeholdery [ ... ] jak w Lulavi) z gotowej strony Kwiatora.
Użycie: python3 zrob_ogolny.py   → szablon/szablon.html + szablon/img/ (zdjęcia-zaślepki)
"""
import os, re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, '../kwiatora/src.html'), encoding='utf-8').read()

def R(a, b, n=1):
    global s
    if a not in s:
        raise SystemExit('Nie znaleziono: ' + a[:70])
    s = s.replace(a, b) if n == 0 else s.replace(a, b, n)

def RX(p, b, n=1):
    global s
    s, k = re.subn(p, b, s, count=n, flags=re.S)
    if not k:
        raise SystemExit('Regex bez trafienia: ' + p[:70])

# ---------- KOLORY (pomarańcz + granat jak w szablonie) ----------
for a, b in [('--kw-surface:#FBF7F0', '--kw-surface:#FFF8F3'), ('--kw-surface-2:#F3EDE2', '--kw-surface-2:#FCEDE4'),
             ('--kw-fg:#18241D', '--kw-fg:#1F2547'), ('--kw-muted:#5E6B63', '--kw-muted:#646A85'),
             ('--kw-border:#E8E0D2', '--kw-border:#F1E4DB'), ('--kw-primary:#1E5B3D', '--kw-primary:#E9693F'),
             ('--kw-primary-dark:#123826', '--kw-primary-dark:#1F2547'), ('--kw-primary-soft:#E8F1EA', '--kw-primary-soft:#FDEDE5'),
             ('--kw-gold:#C9963A', '--kw-gold:#E9693F'), ('--kw-gold-soft:#FBF1DC', '--kw-gold-soft:#FDEDE5'),
             ('--kw-gradient:linear-gradient(135deg,#2B7A50 0%,#123826 100%)', '--kw-gradient:linear-gradient(135deg,#F28A5C 0%,#E2572C 100%)'),
             ('--kw-gradient-gold:linear-gradient(135deg,#E2B866 0%,#B9822A 100%)', '--kw-gradient-gold:linear-gradient(135deg,#2B3266 0%,#1F2547 100%)'),
             ('rgba(18,56,38,.22)', 'rgba(233,105,63,.18)'), ('rgba(18,56,38,.55)', 'rgba(233,105,63,.45)')]:
    R(a, b)
R('<title>Kwiatora – Kalendarz adwentowy z kwiatami z klocków</title>', '<title>[NAZWA SKLEPU] – [NAZWA PRODUKTU]</title>')
RX(r'<meta name="description" content="[^"]*">', '<meta name="description" content="[OPIS SEO – 1–2 zdania z korzyścią]">')
RX(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="[NAZWA SKLEPU] – [OBIETNICA]">')
RX(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="[OPIS DO UDOSTĘPNIEŃ]">')

# ---------- ZDJĘCIA: nazwy ogólne ----------
IMGS = {'logo-ikona.png': ('logo.png', 'LOGO'),
        '00-hero-stol.jpg': ('foto-1.jpg', 'ZDJĘCIE 1 – produkt w użyciu'), '02-szufladka.jpg': ('foto-2.jpg', 'ZDJĘCIE 2 – detal'),
        '00-hero-dorosli.jpg': ('foto-3.jpg', 'ZDJĘCIE 3 – emocja'), '04-prezent.jpg': ('foto-4.jpg', 'ZDJĘCIE 4 – opakowanie'),
        '03-bukiet.jpg': ('foto-5.jpg', 'ZDJĘCIE 5 – efekt'), '05-razem.jpg': ('foto-6.jpg', 'ZDJĘCIE 6 – razem'),
        '06-problem.jpg': ('problem.jpg', 'ZDJĘCIE – problem klienta'), '11b-dla-niej.jpg': ('zastosowanie-2.jpg', 'ZASTOSOWANIE 2'),
        '03b-bukiet-szeroki.jpg': ('zastosowanie-3.jpg', 'ZASTOSOWANIE 3'), '07-rozwiazanie.jpg': ('rozwiazanie.jpg', 'ZDJĘCIE – rozwiązanie'),
        '08-krok1.jpg': ('krok-1.jpg', 'KROK 1'), '09-krok2.jpg': ('krok-2.jpg', 'KROK 2'), '10-krok3.jpg': ('krok-3.jpg', 'KROK 3'),
        '11-dla-doroslych.jpg': ('sekcja-4.jpg', 'ZDJĘCIE – sekcja z 4 punktami'),
        '13-opinia-slonecznik.jpg': ('opinia-1.jpg', 'ZDJĘCIE OD KLIENTA'), '14-opinia-kuchnia.jpg': ('opinia-2.jpg', 'ZDJĘCIE OD KLIENTA'),
        '15-opinia-biurko.jpg': ('opinia-3.jpg', 'ZDJĘCIE OD KLIENTA'), '16-opinia-roza.jpg': ('opinia-4.jpg', 'ZDJĘCIE OD KLIENTA'),
        '01-hero.jpg': ('opinia-5.jpg', 'ZDJĘCIE OD KLIENTA')}
s = s.replace('"05-razem.jpg","Różany', '"opinia-6.jpg","Różany')  # 05 w opiniach nie występuje, bezpiecznik
for old, (new, _) in IMGS.items():
    s = s.replace(old, new)
IMGS['_rev6'] = ('opinia-6.jpg', 'ZDJĘCIE OD KLIENTA')
for i in range(1, 13):
    IMGS['av%d' % i] = ('av%d.jpg' % i, 'KRAJOBRAZ')

# ---------- GÓRA ----------
RX(r'(<div class="kw-marquee">).*?(\n  </div>)', r'\1\n' + ('    <span>[KORZYŚĆ 1 – np. Darmowa wysyłka]</span><span>[KORZYŚĆ 2 – np. 14 dni na zwrot]</span><span>[PROMOCJA]</span><span>[HASŁO MARKI]</span>\n' * 3).rstrip('\n') + r'\2')
R('<div><span>Kwiatora</span><small>KALENDARZ Z KWIATAMI</small></div>', '<div><span>[NAZWA]</span><small>[PODPIS POD LOGO]</small></div>', 0)
for a, b in [('>Dla kogo</a>', '>[MENU 1 – zastosowania]</a>'), ('>Jak to działa</a>\n      <a href="#zestaw"', '>[MENU 2 – jak działa]</a>\n      <a href="#zestaw"'),
             ('>Co dostajesz</a>', '>[MENU 3 – zestaw]</a>'), ('>Porównanie</a>', '>[MENU 4 – porównanie]</a>'),
             ('onclick="kwShow(\'home\')">Opinie</a>', 'onclick="kwShow(\'home\')">[MENU 5 – opinie]</a>'), ('onclick="kwShow(\'home\')">FAQ</a>\n    </nav>', 'onclick="kwShow(\'home\')">[MENU 6 – FAQ]</a>\n    </nav>'),
             ('>Kalendarz Kwiatora</a>', '>[NAZWA PRODUKTU]</a>')]:
    R(a, b)

# ---------- HERO ----------
RX(r'(<img id="kwMain" [^>]*alt=")[^"]*"', r'\1[OPIS ZDJĘCIA 1]"')
RX(r'(<div class="kw-gallery-caption" id="kwCaption">)[^<]*', r'\1⭐ [PODPIS ZDJĘCIA 1 – korzyść]')
R('<span class="kw-pill gold">★ Hit Adwentu 2026</span><span class="kw-pill sale">⚠️ Liczba sztuk ograniczona</span>',
  '<span class="kw-pill gold">★ [PLAKIETKA – np. Bestseller 2026]</span><span class="kw-pill sale">⚠️ [PILNOŚĆ – np. Liczba sztuk ograniczona]</span>')
RX(r'<h1>.*?</h1>', '<h1>[NAGŁÓWEK GŁÓWNY – problem klienta + obietnica] <span class="kw-accent">[EFEKT KOŃCOWY]</span></h1>')
RX(r'<p class="kw-sub">.*?</p>', '<p class="kw-sub">[PODTYTUŁ – jak produkt zmienia dzień klienta, 1–2 zdania]</p>')
R('<b>4,9</b> · 1 248 opinii · <span style="color:var(--kw-ok);font-weight:600">● 37 osób ogląda teraz</span>',
  '<b>[OCENA]</b> · [LICZBA] opinii · <span style="color:var(--kw-ok);font-weight:600">● [LICZBA] osób ogląda teraz</span>')
chk = re.search(r'<span class="kw-check">.*?</span>', s).group(0)
RX(r'(<div class="kw-price-row">.*?</div>\s*<ul class="kw-list">).*?(</ul>)', r'\1\n' + ''.join(
    '        <li>%s<span><b>[KORZYŚĆ %d]</b> [dopowiedzenie]</span></li>\n' % (chk.replace('\\', '\\\\'), i) for i in range(1, 7)) + r'      \2')
R('<div class="kw-bundles-title">Wybierz zestaw</div>', '<div class="kw-bundles-title">[WYBIERZ ZESTAW]</div>')
R('<p class="kw-micro">🔒 Bezpieczna płatność · 14 dni na zwrot · Odpowiadamy w 24 h</p>', '<p class="kw-micro">🔒 [MIKROZAUFANIE – płatność · zwroty · kontakt]</p>')
RX(r'(<div class="kw-container kw-strip-in">).*?(\n  </div>\n</div>)', r'''\1
    <div class="kw-strip-item"><span style="font-size:22px">🚚</span><div><b>[DOSTAWA]</b><small>[sposób dostawy]</small></div></div>
    <div class="kw-strip-item"><span style="font-size:22px">↩️</span><div><b>[ZWROTY]</b><small>[krótki dopisek]</small></div></div>
    <div class="kw-strip-item"><span style="font-size:22px">🔒</span><div><b>[PŁATNOŚCI]</b><small>[metody płatności]</small></div></div>
    <div class="kw-strip-item"><span style="font-size:22px">⭐</span><div><b>[OCENA]</b><small>[liczba zadowolonych]</small></div></div>\2''')

# ---------- SEKCJE: nadtytuł / nagłówek / lead ----------
def head(sec_id_or_marker, eyebrow, h2, lead):
    RX(r'(' + sec_id_or_marker + r'.*?<span class="kw-eyebrow[^"]*">)[^<]*(</span>\s*<h2 class="kw-h2[^"]*">).*?(</h2>\s*<p class="kw-lead[^"]*"[^>]*>)[^<]*(</p>)',
       r'\1' + eyebrow + r'\2' + h2 + r'\3' + lead + r'\4')

head(r'<!-- PROBLEM -->', '[NADTYTUŁ – np. Brzmi znajomo?]', '[NAGŁÓWEK PROBLEMU – frustracja klienta] <span class="kw-accent">[SŁOWO KLUCZ]</span>', '[ZDANIE WYJAŚNIAJĄCE PROBLEM]')
RX(r'(<ul class="kw-list kw-pain">).*?(</ul>)', r'\1\n' + ''.join('        <li><span class="kw-x">✕</span><span>[PROBLEM %d]</span></li>\n' % i for i in range(1, 7)) + r'      \2')
RX(r'<div class="kw-bridge">.*?</div>', '<div class="kw-bridge">[PODSUMOWANIE – skutek problemów w 1 zdaniu, pytanie „a gdyby…”]</div>')
head(r'<!-- USES -->', '[NADTYTUŁ – np. Gdzie się przydaje]', '[NAGŁÓWEK ZASTOSOWAŃ] <span class="kw-accent">[SŁOWO KLUCZ]</span>', '[PODTYTUŁ ZASTOSOWAŃ]')
RX(r'(<div class="kw-uses">).*?(\n    </div>)', r'''\1
      <article class="kw-card kw-use"><img src="{{IMG}}/foto-6.jpg" width="1200" height="1200" loading="lazy" alt="[ZASTOSOWANIE 1]"><div><h3>[ZASTOSOWANIE 1]</h3><p>[OPIS – 1 zdanie]</p></div></article>
      <article class="kw-card kw-use"><img src="{{IMG}}/zastosowanie-2.jpg" width="1200" height="900" loading="lazy" alt="[ZASTOSOWANIE 2]"><div><h3>[ZASTOSOWANIE 2]</h3><p>[OPIS – 1 zdanie]</p></div></article>
      <article class="kw-card kw-use"><img src="{{IMG}}/zastosowanie-3.jpg" width="1200" height="675" loading="lazy" alt="[ZASTOSOWANIE 3]"><div><h3>[ZASTOSOWANIE 3]</h3><p>[OPIS – 1 zdanie]</p></div></article>\2''')
head(r'<!-- SOLUTION -->', '[NADTYTUŁ – np. Dlatego powstał produkt]', '[NAGŁÓWEK ROZWIĄZANIA – jak produkt rozwiązuje problem] <span class="kw-accent">[SŁOWO KLUCZ]</span>', '[ZDANIE O ROZWIĄZANIU]')
RX(r'(<!-- SOLUTION -->.*?<ul class="kw-list">).*?(</ul>)', r'\1\n' + ''.join('        <li>%s<span><b>[ULGA %d]</b> [dopowiedzenie]</span></li>\n' % (chk.replace('\\', '\\\\'), i) for i in range(1, 7)) + r'      \2')
head(r'<!-- HOW IT WORKS -->', '[NADTYTUŁ – np. Proste jak 1-2-3]', '[EFEKT] <span class="kw-accent">w 3 krokach</span>', '[PODTYTUŁ – co jest proste]')
for i in (1, 2, 3):
    RX(r'(<span class="num">0%d</span><img [^>]*alt=")[^"]*("><div class="t"><h3>)[^<]*(</h3><p>)[^<]*' % i, r'\1[KROK %d]\2[KROK %d]\3[OPIS KROKU %d]' % (i, i, i))
RX(r'<p class="kw-steps-foot">.*?</p>', '<p class="kw-steps-foot">[ZDANIE PODSUMOWANIA KROKÓW]</p>')
head(r'<!-- WHAT YOU GET -->', '[NADTYTUŁ – np. W paczce]', 'Co dokładnie <span class="kw-accent">dostajesz</span>', '[PODTYTUŁ ZESTAWU]')
R('<button class="on" onclick="kwTab(0)">W pudełku</button>', '<button class="on" onclick="kwTab(0)">[ZAKŁADKA 1]</button>')
R('<button onclick="kwTab(1)">Kwiaty</button>', '<button onclick="kwTab(1)">[ZAKŁADKA 2]</button>')
R('<button onclick="kwTab(2)">Wymiary</button>', '<button onclick="kwTab(2)">[ZAKŁADKA 3]</button>')
tabs = re.findall(r'<div class="kw-card kw-tab[^"]*">.*?</div>\s*</div>', s, re.S)
for i, t in enumerate(tabs, 1):
    on = ' on' if i == 1 else ''
    s = s.replace(t, '<div class="kw-card kw-tab%s">\n      <div><h3>[NAZWA PRODUKTU / ZAKŁADKA %d]</h3><p>[OPIS ZESTAWU – 1–2 zdania]</p></div>\n      <div class="kw-tab-panel"><small>[ZAWARTOŚĆ]</small><ul class="kw-list">%s</ul></div>\n    </div>' % (on, i, ''.join('<li>%s[ELEMENT %d]</li>' % (chk, j) for j in range(1, 5))), 1)
head(r'<!-- COMPARE -->', '[NADTYTUŁ – np. Porównanie]', 'Dlaczego <span class="kw-accent">[TWÓJ PRODUKT]</span>, a nie [ALTERNATYWA]?', '[PODTYTUŁ PORÓWNANIA]')
R('<th>Kryterium</th><th class="us">Kwiatora</th><th>Kalendarz ze słodyczami</th><th>Zwykłe klocki</th><th>Żywe kwiaty</th>',
  '<th>Cecha</th><th class="us">[TWÓJ PRODUKT]</th><th>[ALTERNATYWA 1]</th><th>[ALTERNATYWA 2]</th><th>[ALTERNATYWA 3]</th>')
for i, txt in enumerate(['Codzienna niespodzianka przez 24 dni', 'Wspólny czas bez ekranu', 'Zero cukru', 'Zostaje coś na lata', 'Ozdoba domu na Święta i cały rok', 'Dla dzieci i dorosłych'], 1):
    R('<td>%s</td>' % txt, '<td>[CECHA %d]</td>' % i)
head(r'<!-- REVIEWS -->', '[NADTYTUŁ – np. Opinie]', 'Zobacz, co mówią <span class="kw-accent">[KLIENCI]</span>', '')  if False else None
RX(r'(<!-- REVIEWS -->.*?<span class="kw-eyebrow">)[^<]*(</span>\s*<h2 class="kw-h2">).*?(</h2>)', r'\1[NADTYTUŁ – np. Opinie klientów]\2Zobacz, co mówią <span class="kw-accent">[KLIENCI]</span>\3')
R('<div class="kw-rev-score"><b>4,9</b>', '<div class="kw-rev-score"><b>[OCENA]</b>')
R('Na podstawie 1 248 zweryfikowanych zakupów', 'Na podstawie [LICZBA] zweryfikowanych zakupów')
head(r'<!-- ADULT -->', '[NADTYTUŁ – np. Nie tylko dla…]', '[NAGŁÓWEK – obalenie obiekcji] <span class="kw-accent">[SŁOWO KLUCZ]</span>', '[ZDANIE ROZWIJAJĄCE]')
RX(r'(<!-- ADULT -->.*?<ul class="kw-list">).*?(</ul>)', r'\1\n' + ''.join('        <li>%s<span><b>[PUNKT %d]</b> [dopowiedzenie]</span></li>\n' % (chk.replace('\\', '\\\\'), i) for i in range(1, 5)) + r'      \2')
RX(r'(<!-- ADULT -->.*?<img [^>]*alt=")[^"]*"', r'\1[OPIS ZDJĘCIA]"')
R('<h2 class="kw-shine">Kalendarz Kwiatora</h2>', '<h2 class="kw-shine">[NAZWA PRODUKTU]</h2>')
R('Nie przegap – cena promocyjna tylko przez 48 godzin!', 'Nie przegap – [CENA PROMOCYJNA tylko przez 48 godzin]!')
R('⚠️ Liczba sztuk ograniczona</span> <span', '⚠️ [PILNOŚĆ – np. Liczba sztuk ograniczona]</span> <span')
R('Kup teraz i skorzystaj z rabatu! →', '[CTA – np. Kup teraz i skorzystaj z rabatu!] →')
RX(r'(class="kw-float" [^>]*alt=")[^"]*"', r'\1[NAZWA PRODUKTU]"')

# ---------- STOPKA / KOSZYK / STICKY ----------
RX(r'(<p style="color:var\(--kw-muted\);font-size:14px;max-width:360px">)[^<]*', r'\1[OPIS SKLEPU – 1–2 zdania]')
R('<span>Kwiatora © 2026</span>', '<span>[NAZWA SKLEPU] © [ROK]</span>')
R('🚚 Darmowa dostawa InPost · ↩️ 14 dni na zwrot', '🚚 [DOSTAWA] · ↩️ [ZWROTY]')
R('<div class="n">Kalendarz Kwiatora</div>', '<div class="n">[NAZWA PRODUKTU]</div>')
R('Odpowiadamy pon.–pt. w 24 h', '[GODZINY ODPOWIEDZI]')

# ---------- JS: galeria, zestawy, opinie, FAQ ----------
RX(r'var gallery=\[.*?\n\];', 'var gallery=[\n' + ',\n'.join(' ["foto-%d.jpg","⭐ [PODPIS ZDJĘCIA %d – korzyść]"]' % (i, i) for i in range(1, 7)) + '\n];')
RX(r'var BUNDLES=\[.*?\n\];', '''var BUNDLES=[
 {q:1,name:"[Kup 1]",desc:"[Pakiet startowy]",price:99.99,old:149.99},
 {q:2,name:"[Kup 2]",desc:"[Oszczędzasz X zł · cena za szt.]",price:179.98,old:299.98,tag:"[NAJCZĘŚCIEJ WYBIERANY]"},
 {q:3,name:"[Kup 3]",desc:"[Najlepsza cena za szt.]",price:239.97,old:449.97,tag:"[NAJLEPSZA CENA]",gold:true}
];''')
R('name:"Kalendarz adwentowy Kwiatora",variant:"24 kwiaty z klocków",img:"foto-4.jpg"', 'name:"[NAZWA PRODUKTU]",variant:"[KRÓTKI OPIS]",img:"foto-1.jpg"')
RX(r'function unitFor\(q\)\{[^}]*\}', 'function unitFor(q){return q>=3?BUNDLES[2].price/3:q===2?BUNDLES[1].price/2:BUNDLES[0].price}')
s = s.replace('old:249.99});kwCart(true)', 'old:BUNDLES[0].old});kwCart(true)')
RX(r"if\(n===0\)pr\.innerHTML=\"\";.*?\n", '''if(n===0)pr.innerHTML="";else if(n<3)pr.innerHTML='Dodaj jeszcze <b>1 szt.</b> i zapłać tylko <b>'+zl(unitFor(n+1))+'</b> za sztukę<div class="bar"><i style="width:'+(n/3*100)+'%"></i></div>';else pr.innerHTML='🎉 Masz najniższą cenę: <b>'+zl(unitFor(3))+'</b> za sztukę<div class="bar"><i style="width:100%"></i></div>';\n''')
names = [('Amelia', 'Kraków'), ('Piotr', 'Wrocław'), ('Julia', 'Gdańsk'), ('Aleksander', 'Poznań'), ('Natalia', 'Łódź'), ('Zofia', 'Lublin'),
         ('Kacper', 'Katowice'), ('Maja', 'Szczecin'), ('Oliwia', 'Bydgoszcz'), ('Szymon', 'Rzeszów'), ('Hanna', 'Toruń'), ('Mateusz', 'Białystok')]
RX(r'var R=\[.*?\n\];', 'var R=[\n' + ',\n'.join(' ["%s","%s","opinia-%d.jpg","","[TREŚĆ OPINII %d – 2–3 zdania, konkretna korzyść, ok. 25 słów]"]' % (n, c, i % 6 + 1, i + 1) for i, (n, c) in enumerate(names)) + '\n];')
RX(r'var F=\[.*?\n\];', 'var F=[\n' + ',\n'.join(' ["[PYTANIE %d]","[ODPOWIEDŹ %d]"]' % (i, i) for i in range(1, 9)) + '\n];')

# ---------- POLITYKI ----------
s = s.replace('<b>Kwiatora</b>', '<b>[NAZWA SKLEPU]</b>').replace('"Wiadomość ze sklepu Kwiatora"', '"Wiadomość ze sklepu [NAZWA SKLEPU]"')
s = s.replace('Kwiatora', '[NAZWA SKLEPU]').replace('kontakt@kwiatora.pl', '[E-MAIL KONTAKTOWY]')
s = re.sub(r'alt="(?!\[|Zdjęcie od klienta)[^"]+"', 'alt="[OPIS ZDJĘCIA]"', s)
s = s.replace('</style>', '.kw-hero-grid>*{min-width:0}\n.kw-pills{flex-wrap:wrap!important;white-space:normal!important}\n</style>', 1)
leftover = re.findall(r'[^\n]*(?:klock|kwiat|Kalendarz|bukiet|Wigili)[^\n]*', s, re.I)
open(os.path.join(HERE, 'szablon.html'), 'w', encoding='utf-8').write(s)
print('OK szablon.html; zostało linii z Kwiatora-słowami:', len(leftover))
for l in leftover[:15]:
    print('  >', l.strip()[:120])

# ---------- ZDJĘCIA-ZAŚLEPKI ----------
os.makedirs(os.path.join(HERE, 'img'), exist_ok=True)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 34)
except Exception:
    font = ImageFont.load_default()
for _, (fn, label) in IMGS.items():
    path = os.path.join(HERE, 'img', fn)
    if fn.startswith('av'):
        im = Image.new('RGB', (120, 120), (253, 237, 229)); ImageDraw.Draw(im).ellipse((30, 30, 90, 90), outline=(233, 105, 63), width=4)
        im.save(path, quality=80); continue
    if fn == 'logo.png':
        im = Image.new('RGBA', (120, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((4, 50, 116, 160), 20, outline=(233, 105, 63), width=5); d.text((60, 105), 'LOGO', fill=(233, 105, 63), font=font, anchor='mm')
        im.save(path); continue
    w, h = (1200, 900) if fn in ('problem.jpg', 'rozwiazanie.jpg', 'zastosowanie-2.jpg', 'krok-1.jpg', 'krok-2.jpg', 'krok-3.jpg', 'sekcja-4.jpg') else ((1200, 675) if fn == 'zastosowanie-3.jpg' else (1200, 1200))
    im = Image.new('RGB', (w, h), (253, 237, 229)); d = ImageDraw.Draw(im)
    for x in range(30, w - 30, 40):
        d.line((x, 30, x + 20, 30), fill=(239, 150, 120), width=4); d.line((x, h - 30, x + 20, h - 30), fill=(239, 150, 120), width=4)
    for y in range(30, h - 30, 40):
        d.line((30, y, 30, y + 20), fill=(239, 150, 120), width=4); d.line((w - 30, y, w - 30, y + 20), fill=(239, 150, 120), width=4)
    d.text((w // 2, h // 2 - 24), '[ZDJĘCIE]', fill=(226, 87, 44), font=font, anchor='mm')
    d.text((w // 2, h // 2 + 30), label, fill=(150, 110, 100), font=font, anchor='mm')
    im.save(path, quality=80)
print('OK img/:', len(os.listdir(os.path.join(HERE, 'img'))), 'plików')
