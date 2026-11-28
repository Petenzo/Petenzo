import re
p='src.html'; s=open(p,encoding='utf-8').read()
def R(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n>=1, 'BRAK: '+a[:80]
    if cnt==1: assert n==1, 'WIELE(%d): %s'%(n,a[:80])
    s=s.replace(a,b)
def RX(pat,b):
    global s
    s2,n=re.subn(pat,b,s,flags=re.S); assert n>=1,'BRAK RX: '+pat[:60]; s=s2
CHK='<span class="kw-check"><svg viewBox="0 0 12 12"><path d="M2 6.2l2.4 2.3L10 3" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg></span>'
def li(b,t): return '<li>'+CHK+'<span><b>'+b+'</b>'+t+'</span></li>'
def li2(t): return '<li>'+CHK+t+'</li>'
# ---- HEAD ----
R('<title>Kwiatora – Kalendarz adwentowy z kwiatami z klocków</title>','<title>Nostalio – drukarka zdjęć do telefonu</title>')
RX(r'<meta name="description" content="[^"]*">','<meta name="description" content="Drukuj prawdziwe zdjęcia 10×15 cm prosto z telefonu, w domu, w kilka sekund. Drukarka Nostalio: darmowa dostawa, 14 dni na zwrot.">')
RX(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="Nostalio – Twoje wspomnienia w dłoni">')
RX(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="Domowa drukarka zdjęć do telefonu. Postaw telefon, wybierz zdjęcie, odbierz gotową odbitkę.">')
# ---- KOLORY ----
pal={'--kw-surface:#FBF7F0':'--kw-surface:#F8F4FD','--kw-surface-2:#F3EDE2':'--kw-surface-2:#EFE7FA','--kw-fg:#18241D':'--kw-fg:#1E1530',
 '--kw-muted:#5E6B63':'--kw-muted:#655C75','--kw-border:#E8E0D2':'--kw-border:#E6DDF3','--kw-primary:#1E5B3D':'--kw-primary:#6B3FA0',
 '--kw-primary-dark:#123826':'--kw-primary-dark:#3E2163','--kw-primary-soft:#E8F1EA':'--kw-primary-soft:#F1EAFB','--kw-gold:#C9963A':'--kw-gold:#C08A00',
 '--kw-gold-soft:#FBF1DC':'--kw-gold-soft:#FFF4CC','--kw-gradient:linear-gradient(135deg,#2B7A50 0%,#123826 100%)':'--kw-gradient:linear-gradient(135deg,#8A5CC9 0%,#4B2780 100%)',
 '--kw-gradient-gold:linear-gradient(135deg,#E2B866 0%,#B9822A 100%)':'--kw-gradient-gold:linear-gradient(135deg,#FFD54A 0%,#F2B705 100%)',
 'rgba(18,56,38,.22)':'rgba(62,33,99,.20)','rgba(18,56,38,.55)':'rgba(62,33,99,.50)','rgba(18,56,38,.45)':'rgba(62,33,99,.45)',
 'linear-gradient(135deg,#E8F1EA 0%,#FBF1DC 100%)':'linear-gradient(135deg,#F1EAFB 0%,#FFF4CC 100%)'}
for a,b in pal.items(): R(a,b,0)
s=s.replace('#9DB3A6','#B8A6D3')
# mniejsze zdjęcie główne + logo kwadratowe
R('.kw-gallery-main{touch-action:pan-y}','.kw-gallery-main{touch-action:pan-y}\n@media(max-width:959px){.kw-gallery-main{aspect-ratio:5/4}.kw-thumbs{grid-template-columns:repeat(6,1fr);gap:6px}}\n@media(min-width:960px){.kw-hero-grid>div:first-child{max-width:520px;width:100%;justify-self:center}}\n@keyframes kw-blink{0%,100%{opacity:1}50%{opacity:.35}}.kw-blink{animation:kw-blink 1s steps(2,start) infinite;color:var(--kw-sale);font-weight:800;letter-spacing:.06em}')
R('.kw-logo img{height:46px!important;width:auto!important;max-width:none}','.kw-logo img{height:44px!important;width:44px!important;max-width:none}')
s=s.replace('logo-ikona.png" width="26" height="46"','logo-ikona.png" width="44" height="44"')
# ---- TOPBAR / NAV ----
mq='<span>📸 Twoje wspomnienia w dłoni</span><span>🚚 Darmowa dostawa</span><span>↩️ 14 dni na zwrot</span><span>🎁 Idealny prezent na Święta</span>'
RX(r'(<div class="kw-marquee">\n)(    <span>Darmowa wysyłka</span>.*?\n){3}',r'\1'+('    '+mq+'\n')*3)
s=s.replace('<div><span>Kwiatora</span><small>KALENDARZ Z KWIATAMI</small></div>','<div><span>Nostalio</span><small>DRUKARKA ZDJĘĆ</small></div>')
R('onclick="kwMenu(false);kwShow(\'home\')">Kalendarz Kwiatora</a>','onclick="kwMenu(false);kwShow(\'home\')">Drukarka Nostalio</a>')
R('<a href="#jak-dziala" onclick="kwMenu(false);kwShow(\'home\')">Jak to działa</a>','<a href="#zastosowania" onclick="kwMenu(false);kwShow(\'home\')">Dla kogo</a>\n    <a href="#jak-dziala" onclick="kwMenu(false);kwShow(\'home\')">Jak to działa</a>\n    <a href="#zestaw" onclick="kwMenu(false);kwShow(\'home\')">Co dostajesz</a>')
R('<a href="#" onclick="kwMenu(false);kwShow(\'kontakt\');return false">Kontakt</a>','<a href="#" onclick="kwMenu(false);kwShow(\'kontakt\');return false">Kontakt z nami</a>')
# ---- HERO ----
R('alt="Para składa kwiaty z klocków przy stole w świątecznym salonie"','alt="Para drukuje zdjęcia z telefonu na drukarce Nostalio"')
R('<div class="kw-gallery-caption" id="kwCaption">🎁 Prezent, który rozpakowuje się 24 razy</div>','<div class="kw-gallery-caption" id="kwCaption">📸 Z telefonu na papier w kilka sekund</div>')
R('<span class="kw-pill gold">★ Hit Adwentu 2026</span>','<span class="kw-pill gold">★ Hit prezentowy 2026</span>')
RX(r'<h1>Odliczaj do Świąt.*?</h1>','<h1>Zdjęcia z telefonu <span class="kw-accent">w Twoich dłoniach w kilka sekund</span></h1>')
RX(r'<p class="kw-sub">.*?</p>','<p class="kw-sub">Stawiasz telefon w stacji, wybierasz zdjęcie i po chwili trzymasz prawdziwą odbitkę 10×15 cm. Do albumu, ramki, na lodówkę albo w prezencie dla babci. Bez wychodzenia z domu i bez czekania w punkcie foto.</p>')
R('1 248 opinii','2 184 opinii')
R('<span class="kw-price" id="kwPrice">199,99 zł</span>','<span class="kw-price" id="kwPrice">249,99 zł</span>')
R('<span class="kw-old" id="kwOld">299,99 zł</span>','<span class="kw-old" id="kwOld">349,99 zł</span>')
R('<span class="kw-save" id="kwSave">−33%</span>','<span class="kw-save" id="kwSave">−29%</span>')
RX(r'(<div class="kw-price-row">.*?</div>\s*<ul class="kw-list">).*?(</ul>)', r'\1\n        '+'\n        '.join([
 li('Prawdziwe zdjęcia 10×15 cm',' w żywych kolorach, gotowe do albumu i ramki'),
 li('Drukujesz prosto z telefonu',': stawiasz go w stacji i wybierasz zdjęcie'),
 li('Kilka sekund',' od kliknięcia do gotowej odbitki w dłoni'),
 li('Mała i lekka',': zmieści się na półce, biurku i w walizce'),
 li('W zestawie wszystko na start',': drukarka, kaseta i papier'),
 li('Idealny prezent',' dla mamy, babci, pary i przyjaciółki')])+r'\n      \2')
R('<span id="kwCtaPrice">199,99 zł</span>','<span id="kwCtaPrice">249,99 zł</span>')
R('<div class="kw-strip-item"><span style="font-size:22px">⭐</span><div><b>4,9 / 5</b><small>1 200+ zadowolonych rodzin</small></div></div>','<div class="kw-strip-item"><span style="font-size:22px">⭐</span><div><b>4,9 / 5</b><small>2 000+ zadowolonych klientów</small></div></div>')
# ---- PROBLEM ----
RX(r'<!-- PROBLEM -->.*?</section>','''<!-- PROBLEM -->
<section class="kw-section kw-alt" id="problem">
  <div class="kw-container kw-two">
    <div>
      <span class="kw-eyebrow left">Brzmi znajomo?</span>
      <h2 class="kw-h2 left">Masz tysiące zdjęć, a <span class="kw-accent">żadnego nie trzymasz w dłoni</span></h2>
      <p class="kw-lead left">Najpiękniejsze chwile robisz jednym kliknięciem, a potem giną w galerii między zrzutami ekranu. Mijają lata, a album na półce dalej jest pusty.</p>
      <ul class="kw-list kw-pain">
        <li><span class="kw-x">✕</span><span>W telefonie masz ponad 5 000 zdjęć, a i tak nikt ich nie ogląda.</span></li>
        <li><span class="kw-x">✕</span><span>Zdjęcia z wakacji, ślubu i pierwszych kroków dziecka leżą zapomniane w chmurze.</span></li>
        <li><span class="kw-x">✕</span><span>Babcia prosi o zdjęcia wnuków, a Ty znowu zapominasz je wywołać.</span></li>
        <li><span class="kw-x">✕</span><span>Wywoływanie w punkcie to dojazd, kolejka i czekanie kilka dni.</span></li>
        <li><span class="kw-x">✕</span><span>Ramki stoją puste, a na lodówce wiszą tylko magnesy.</span></li>
        <li><span class="kw-x">✕</span><span>Telefon się psuje albo ginie, a razem z nim znikają wspomnienia.</span></li>
      </ul>
      <div class="kw-bridge">A gdyby każde ważne zdjęcie mogło w kilka sekund trafić do Twojej ręki, prosto z telefonu, bez wychodzenia z domu?</div>
    </div>
    <div class="kw-photo" style="aspect-ratio:4/3"><img src="{{IMG}}/06-problem.jpg" width="1200" height="900" loading="lazy" alt="Kobieta przegląda tysiące zdjęć w telefonie, obok pusty album"></div>
  </div>
</section>''')
# ---- USES ----
R('<span class="kw-eyebrow">Jeden kalendarz, wiele okazji</span>','<span class="kw-eyebrow">Jedna drukarka, mnóstwo okazji</span>')
R('<p class="kw-lead">Kwiatora łączy to, czego brakuje w grudniu: wspólny czas, chwilę spokoju i prezent, który ma sens.</p>','<p class="kw-lead">Nostalio zamienia zdjęcia z telefonu w pamiątki, które można dotknąć, podarować i powiesić na ścianie.</p>')
RX(r'<article class="kw-card kw-use"><img src="\{\{IMG\}\}/05-razem.jpg".*?</article>','<article class="kw-card kw-use"><img src="{{IMG}}/05-razem.jpg" width="1200" height="1200" loading="lazy" alt="Przyjaciółki oglądają świeżo wydrukowane zdjęcia"><div><h3>Dla przyjaciółki i na wspólne wieczory</h3><p>Drukujecie zdjęcia od razu po imprezie czy wyjeździe. Każda wychodzi z odbitką, a śmiechu jest więcej niż przy przewijaniu telefonu.</p></div></article>')
RX(r'<article class="kw-card kw-use"><img src="\{\{IMG\}\}/11b-dla-niej.jpg".*?</article>','<article class="kw-card kw-use"><img src="{{IMG}}/11b-dla-niej.jpg" width="1200" height="900" loading="lazy" alt="Para wkłada wydrukowane zdjęcie do ramki"><div><h3>Dla niej, dla niego, dla pary</h3><p>Wasze wspólne chwile w ramkach i na ścianie. Prezent na rocznicę, walentynki albo po prostu bez okazji.</p></div></article>')
RX(r'<article class="kw-card kw-use"><img src="\{\{IMG\}\}/03b-bukiet-szeroki.jpg".*?</article>','<article class="kw-card kw-use"><img src="{{IMG}}/03b-bukiet-szeroki.jpg" width="1200" height="675" loading="lazy" alt="Dziadkowie z wnuczką oglądają wydrukowane zdjęcia"><div><h3>Dla mamy, babci i dziadka</h3><p>Zdjęcia wnuków prosto do rąk, zamiast na ekranie telefonu. Takie prezenty wzruszają najbardziej.</p></div></article>')
# ---- usuń SOLUTION ----
RX(r'<!-- SOLUTION -->.*?</section>\n\n','')
# ---- HOW IT WORKS ----
RX(r'<!-- HOW IT WORKS -->.*?</section>','''<!-- HOW IT WORKS -->
<section class="kw-section" id="jak-dziala">
  <div class="kw-container">
    <span class="kw-eyebrow">Prościej się nie da</span>
    <h2 class="kw-h2">Z telefonu na zdjęcie w <span class="kw-accent">3 prostych krokach</span></h2>
    <p class="kw-lead">Bez kabli do komputera, bez punktu foto i bez czekania.</p>
    <ol class="kw-steps" style="list-style:none;padding:0;margin:0">
      <li class="kw-card kw-step"><span class="num">01</span><img src="{{IMG}}/08-krok1.jpg" width="1200" height="900" loading="lazy" alt="Telefon wkładany do stacji drukarki"><div class="t"><h3>Postaw telefon w stacji</h3><p>Wkładasz telefon w gniazdo na górze drukarki. To wszystko, co trzeba przygotować.</p></div></li>
      <li class="kw-card kw-step"><span class="num">02</span><img src="{{IMG}}/09-krok2.jpg" width="1200" height="900" loading="lazy" alt="Wybieranie zdjęcia na telefonie"><div class="t"><h3>Wybierz zdjęcie</h3><p>Zaznaczasz w aplikacji ulubione zdjęcie, możesz je przyciąć i poprawić kolory.</p></div></li>
      <li class="kw-card kw-step"><span class="num">03</span><img src="{{IMG}}/10-krok3.jpg" width="1200" height="900" loading="lazy" alt="Gotowe zdjęcie wysuwa się z drukarki"><div class="t"><h3>Odbierz gotową odbitkę</h3><p>Po chwili zdjęcie wysuwa się na tackę. Gotowe do albumu, ramki albo w prezencie.</p></div></li>
    </ol>
    <p class="kw-steps-foot">Kilka sekund i wspomnienie, które dotąd było tylko w telefonie, <b>trzymasz w dłoni</b>.</p>
  </div>
</section>''')
# ---- WHAT YOU GET ----
R('<span class="kw-eyebrow">Wszystko w jednym pudełku</span>','<span class="kw-eyebrow">Wszystko w jednym pudełku</span>')
R('<p class="kw-lead">Otwierasz paczkę i możesz zaczynać. Nie trzeba niczego dokupować.</p>','<p class="kw-lead">Otwierasz paczkę, podłączasz zasilanie i drukujesz pierwsze zdjęcia.</p>')
R('<button onclick="kwTab(1)">Kwiaty</button>','<button onclick="kwTab(1)">Zdjęcia</button>')
R('<button onclick="kwTab(2)">Wymiary</button>','<button onclick="kwTab(2)">Specyfikacja</button>')
RX(r'<div class="kw-card kw-tab on">.*?</div>\s*</div>\s*<div class="kw-card kw-tab">.*?</div>\s*</div>\s*<div class="kw-card kw-tab">.*?</div>\s*</div>',
 '<div class="kw-card kw-tab on">\n      <div><h3>Drukarka zdjęć Nostalio</h3><p>Elegancka biała drukarka z żółtą tacką na papier, zapakowana w fioletowe pudełko prezentowe. Pięknie wygląda na półce i od razu nadaje się na prezent.</p></div>\n      <div class="kw-tab-panel"><small>W zestawie</small><ul class="kw-list">'+''.join(li2(t) for t in ['Drukarka zdjęć ze stacją na telefon','Tacka na papier','Zasilacz','Złącze do telefonu','Kaseta z tuszem','10 arkuszy papieru fotograficznego','Instrukcja szybkiego startu'])+'</ul></div>\n    </div>\n    <div class="kw-card kw-tab">\n      <div><h3>Prawdziwe zdjęcia 10×15 cm</h3><p>Klasyczny format odbitek, ten sam co w albumach i ramkach. Żywe kolory i gładki papier fotograficzny.</p></div>\n      <div class="kw-tab-panel"><small>Idealne do</small><ul class="kw-list">'+''.join(li2(t) for t in ['Albumów i ramek','Lodówki, tablicy i girland ze zdjęciami','Kartek i prezentów dla bliskich','Pamiątek z wakacji, ślubu i urodzin'])+'</ul></div>\n    </div>\n    <div class="kw-card kw-tab">\n      <div><h3>Specyfikacja</h3><p>Drukarka ze stacją dokującą na telefon i wysuwaną tacką na papier.</p></div>\n      <div class="kw-tab-panel"><small>Najważniejsze</small><ul class="kw-list">'+''.join(li2(t) for t in ['Format zdjęć: 10×15 cm','Druk prosto z telefonu','Kolor: biała obudowa, żółta tacka','Zasilanie: zasilacz w zestawie'])+'</ul></div>\n    </div>')
# ---- COMPARE ----
RX(r'<!-- COMPARE -->.*?</section>','''<!-- COMPARE -->
<section class="kw-section" id="porownanie">
  <div class="kw-container">
    <span class="kw-eyebrow">Zobacz różnicę</span>
    <h2 class="kw-h2">Dlaczego <span class="kw-accent">Nostalio</span>, a nie punkt foto?</h2>
    <p class="kw-lead">Porównaj, ile wysiłku kosztuje jedno zdjęcie w dłoni.</p>
    <div class="kw-table-wrap">
      <table class="kw-table">
        <thead><tr><th>Kryterium</th><th class="us">Nostalio</th><th>Punkt foto</th><th>Zamawianie online</th><th>Zwykła drukarka</th></tr></thead>
        <tbody>
          <tr><td>Zdjęcie w dłoni po kilku sekundach</td><td class="us"><span class="kw-yes">✓</span></td><td><span class="kw-no">✕</span></td><td><span class="kw-no">✕</span></td><td><span class="kw-mid">–</span></td></tr>
          <tr><td>Bez wychodzenia z domu</td><td class="us"><span class="kw-yes">✓</span></td><td><span class="kw-no">✕</span></td><td><span class="kw-yes" style="color:#B8A6D3">✓</span></td><td><span class="kw-yes" style="color:#B8A6D3">✓</span></td></tr>
          <tr><td>Drukujesz prosto z telefonu</td><td class="us"><span class="kw-yes">✓</span></td><td><span class="kw-mid">–</span></td><td><span class="kw-yes" style="color:#B8A6D3">✓</span></td><td><span class="kw-no">✕</span></td></tr>
          <tr><td>Jakość jak z albumu</td><td class="us"><span class="kw-yes">✓</span></td><td><span class="kw-yes" style="color:#B8A6D3">✓</span></td><td><span class="kw-yes" style="color:#B8A6D3">✓</span></td><td><span class="kw-no">✕</span></td></tr>
          <tr><td>Bez czekania na kuriera</td><td class="us"><span class="kw-yes">✓</span></td><td><span class="kw-mid">–</span></td><td><span class="kw-no">✕</span></td><td><span class="kw-yes" style="color:#B8A6D3">✓</span></td></tr>
          <tr><td>Świetny prezent</td><td class="us"><span class="kw-yes">✓</span></td><td><span class="kw-no">✕</span></td><td><span class="kw-no">✕</span></td><td><span class="kw-no">✕</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>''')
# ---- REVIEWS header ----
R('Zobacz, co mówią <span class="kw-accent">rodziny z całej Polski</span>','Zobacz, co mówią <span class="kw-accent">nasi klienci</span>')
R('Na podstawie 1 248 zweryfikowanych zakupów','Na podstawie 2 184 zweryfikowanych zakupów')
# ---- usuń ADULT ----
RX(r'<!-- ADULT -->.*?</section>\n','')
# ---- DEAL -> WYPRZEDAŻ 1h ----
RX(r'<!-- FINAL CTA: 48h -->.*?</section>','''<!-- FINAL CTA: WYPRZEDAŻ 1h -->
<section class="kw-section kw-alt" id="kwDealSec">
  <div class="kw-container">
    <div class="kw-deal">
      <div class="kw-deal-img">
        <span class="kw-spark s1"></span><span class="kw-spark s2"></span>
        <img class="kw-float" src="{{IMG}}/01-hero.jpg" width="1200" height="1200" loading="lazy" alt="Drukarka zdjęć Nostalio">
      </div>
      <div class="kw-deal-body">
        <h2 class="kw-shine">Drukarka Nostalio</h2>
        <div class="kw-deal-badge"><svg class="kw-ring" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="7"/><path d="M12 10v3l2 2M5 4 2.5 6.5M19 4l2.5 2.5"/></svg><b class="kw-pulse">−29%</b></div>
        <p class="kw-nudge"><span class="kw-blink">🔥 WYPRZEDAŻ KOŃCZY SIĘ ZA</span><br><span class="kw-limit">⚠️ Zostało tylko kilka sztuk w tej cenie</span> <span class="kw-gold kw-beat">♡</span></p>
        <div class="kw-deal-timer">
          <div><b id="kwDM">59</b><small>minut</small></div><i>:</i>
          <div><b id="kwDS">59</b><small>sekund</small></div>
        </div>
        <button class="kw-btn full" onclick="kwScrollBuy()">Kupuję w cenie wyprzedaży →</button>
      </div>
    </div>
  </div>
</section>''')
# ---- FAQ / stopka / kontakt ----
s=s.replace('kontakt@kwiatora.pl','kontakt@nostalio.pl')
R('Kalendarze adwentowe z kwiatami z klocków. Tworzymy prezenty, które łączą rodziny i zostają na dłużej niż jeden sezon.','Domowe drukarki zdjęć do telefonu. Pomagamy zamieniać zdjęcia z galerii w prawdziwe pamiątki, które można dotknąć i podarować.')
R('<span>Kwiatora © 2026</span>','<span>Nostalio © 2026</span>')
R('<div class="kw-dr-bar">🚚 Darmowa dostawa InPost · ↩️ 14 dni na zwrot</div>','<div class="kw-dr-bar">🚚 Darmowa dostawa · ↩️ 14 dni na zwrot</div>')
R('<div class="n">Kalendarz Kwiatora</div><div class="p" id="kwStickyPrice">199,99 zł <s style="color:var(--kw-muted);font-weight:400">299,99 zł</s></div>','<div class="n">Drukarka Nostalio</div><div class="p" id="kwStickyPrice">249,99 zł <s style="color:var(--kw-muted);font-weight:400">349,99 zł</s></div>')
# ---- JS ----
RX(r'var gallery=\[.*?\n\];','''var gallery=[
 ["00-hero-stol.jpg","📸 Z telefonu na papier w kilka sekund"],
 ["02-szufladka.jpg","📱 Postaw telefon i wybierz zdjęcie"],
 ["00-hero-dorosli.jpg","✨ Prawdziwe zdjęcia 10×15 cm"],
 ["04-prezent.jpg","🎁 Elegancko zapakowana, gotowa na prezent"],
 ["03-bukiet.jpg","🖼️ Ściana pełna Waszych wspomnień"],
 ["05-razem.jpg","💜 Wspólne chwile, które zostają"]
];''')
RX(r'/\* PROMO 48h:.*?var KW_EXP=Date\.now\(\)>=KW_END;if\(KW_EXP\)document\.documentElement\.classList\.add\("kw-exp"\);','''/* WYPRZEDAŻ 1h: liczona od pierwszej wizyty na tym urządzeniu */
var KW_END;try{KW_END=+localStorage.getItem("odbSaleEnd")}catch(e){}
if(!KW_END){KW_END=Date.now()+3600*1000;try{localStorage.setItem("odbSaleEnd",KW_END)}catch(e){}}
var KW_EXP=Date.now()>=KW_END;if(KW_EXP)document.documentElement.classList.add("kw-exp");''')
RX(r'var BUNDLES=\[.*?\n\];','''var BUNDLES=[
 {q:1,name:"1 drukarka",desc:"Dla siebie",price:249.99,old:349.99},
 {q:2,name:"2 drukarki",desc:"Dla siebie i na prezent",price:479.99,old:699.99,tag:"Najczęściej wybierany"},
 {q:3,name:"3 drukarki",desc:"Prezenty dla całej rodziny",price:709.99,old:1049.99,tag:"Najlepsza cena",gold:true}
];''')
R('var CH=BUNDLES.map(function(b){var a=[];for(var k=0;k<b.q;k++)a.push("Słonecznik");return a});\n','')
RX(r"\+\n   '<div class=\"kw-variants\">'.*?\.join\(''\)\+'</div>';",';')
R("  el.querySelectorAll('.kw-flower').forEach(function(btn){btn.onclick=function(e){e.stopPropagation();var ii=+btn.dataset.i,kk=+btn.dataset.k;CH[ii][kk]=btn.dataset.f;btn.parentNode.querySelectorAll('.kw-flower').forEach(function(x){x.classList.toggle('on',x===btn)});pick(ii)}});\n",'')
# górna cena zawsze 1 szt.
R('''  document.getElementById("kwPrice").textContent=zl(b.price);document.getElementById("kwOld").textContent=zl(b.old);
  document.getElementById("kwSave").textContent="−"+Math.round((1-b.price/b.old)*100)+"%";
  document.getElementById("kwCtaPrice").textContent=zl(b.price);
  document.getElementById("kwStickyPrice").innerHTML=zl(b.price)+' <s style="color:var(--kw-muted);font-weight:400">'+zl(b.old)+'</s>';''','''  var b1=BUNDLES[0];
  document.getElementById("kwPrice").textContent=zl(b1.price);document.getElementById("kwOld").textContent=zl(b1.old);
  document.getElementById("kwSave").textContent="−"+Math.round((1-b1.price/b1.old)*100)+"%";
  document.getElementById("kwCtaPrice").textContent=zl(b.price);
  document.getElementById("kwStickyPrice").innerHTML=zl(b1.price)+' <s style="color:var(--kw-muted);font-weight:400">'+zl(b1.old)+'</s>';''')
R('localStorage.setItem("kwCart2"','localStorage.setItem("odbCart"'); R('localStorage.getItem("kwCart2"','localStorage.getItem("odbCart"')
R('function unitFor(q){return q>=3?569.99/3:q===2?385.99/2:199.99}','function unitFor(q){return q>=3?709.99/3:q===2?479.99/2:249.99}')
RX(r'window\.kwAddBundle=function\(\)\{.*?kwCart\(true\)\};','window.kwAddBundle=function(){addItem({key:"odb",name:"Drukarka zdjęć Nostalio",variant:"Biała z żółtą tacką · 10×15 cm",img:"01-hero.jpg",qty:BUNDLES[sel].q,old:349.99});kwCart(true)};')
R("Twój koszyk jest pusty 🌷","Twój koszyk jest pusty 📸")
R("""'Dodaj jeszcze <b>'+(n===1?"1 kalendarz":"1 kalendarz")+'</b>""","""'Dodaj jeszcze <b>1 drukarkę</b>""")
R("'🎉 Masz najniższą cenę: <b>ok. 190 zł</b> za kalendarz","'🎉 Masz najniższą cenę: <b>'+zl(unitFor(3))+'</b> za drukarkę")
R('/* 48h licznik w sekcji promocji */','/* licznik wyprzedaży 1h */')
R('''document.getElementById("kwDH").textContent=String(Math.floor(s/3600)).padStart(2,"0");document.getElementById("kwDM").textContent=String(Math.floor(s%3600/60)).padStart(2,"0");''','''document.getElementById("kwDM").textContent=String(Math.floor(s/60)).padStart(2,"0");''')
RX(r'var R=\[.*?\n\];','''var R=[
 ["Amelia","Kraków","13-opinia-slonecznik.jpg","","Cała lodówka jest teraz w naszych zdjęciach. Drukuję po każdym weekendzie i dzieci same wybierają, które idą na drzwi. Najlepszy zakup tego roku."],
 ["Piotr","Wrocław","00-hero-stol.jpg","","Kupiłem żonie na rocznicę i trafiłem idealnie. Wieczorem wydrukowaliśmy zdjęcia z całego roku. Kolory są żywe, a papier wygląda jak z punktu foto."],
 ["Julia","Gdańsk","03-bukiet.jpg","","Zrobiłam girlandę ze zdjęć z wakacji nad łóżkiem. Drukarka jest mała, cicha i bardzo prosta. Telefon kładę w stacji i po chwili zdjęcie jest gotowe."],
 ["Aleksander","Poznań","04-prezent.jpg","","Dałem mamie pod choinkę razem z papierem. Pudełko wygląda bardzo elegancko. Teraz co tydzień dostaję od niej odbitki zdjęć wnuków."],
 ["Natalia","Łódź","15-opinia-biurko.jpg","","Stoi na moim biurku i drukuję zdjęcia z podróży na tablicę korkową. Obsługa jest banalna, a efekt robi wrażenie na każdym, kto wchodzi do pokoju."],
 ["Zofia","Lublin","05-razem.jpg","","Na babskim wieczorze drukarka była gwiazdą. Każda wyszła z kilkoma zdjęciami. Śmiechu było mnóstwo, a pamiątki zostały na długo."],
 ["Kacper","Katowice","00-hero-dorosli.jpg","","Zdjęcie wychodzi naprawdę szybko i ma świetną ostrość. Wydrukowałem rodzinne zdjęcie z plaży i stoi teraz w ramce w salonie. Bardzo polecam."],
 ["Maja","Szczecin","02-szufladka.jpg","","Myślałam, że będzie trudna w obsłudze, a to tylko telefon w stacji i jedno kliknięcie. Nawet moja babcia sobie radzi. Super prezent dla całej rodziny."],
 ["Oliwia","Bydgoszcz","01-hero.jpg","","Wreszcie mam w dłoni zdjęcia, które latami leżały w telefonie. Uzupełniłam album dziecka w jeden wieczór. Żałuję, że nie kupiłam wcześniej."],
 ["Szymon","Rzeszów","13-opinia-slonecznik.jpg","","Syn sam wybiera zdjęcia i drukuje je do szkoły na projekty. Zamiast grać w telefonie, robi albumy. Dla mnie to ogromny plus."],
 ["Hanna","Toruń","03-bukiet.jpg","","Drukuję zdjęcia dla dziadków po każdych odwiedzinach. Płaczą ze wzruszenia, gdy dostają odbitki wnuków. Najpiękniejszy prezent, jaki mogłam im dać."],
 ["Mateusz","Białystok","04-prezent.jpg","","Kupiłem dwie, jedną dla siebie, drugą dla siostry. Paczka przyszła dobrze zapakowana. Zdjęcia wyglądają bardzo profesjonalnie, cena uczciwa."]
];''')
RX(r'var F=\[.*?\n\];','''var F=[
 ["Z jakimi telefonami działa drukarka?","Drukarka współpracuje z popularnymi smartfonami. Przed zakupem możesz napisać do nas na "+EMAIL+", a sprawdzimy zgodność z Twoim modelem."],
 ["Jakiego rozmiaru są zdjęcia?","Drukarka drukuje klasyczne zdjęcia w formacie 10×15 cm, takim samym jak w albumach i ramkach."],
 ["Co jest w zestawie?","Drukarka, tacka na papier, zasilacz, złącze do telefonu, kaseta z tuszem, 10 arkuszy papieru fotograficznego i instrukcja szybkiego startu."],
 ["Czy obsługa jest trudna?","Nie. Stawiasz telefon w stacji, wybierasz zdjęcie i drukujesz. Poradzi sobie każdy, także dziecko i babcia."],
 ["Gdzie kupię papier i kasety na kolejne zdjęcia?","Wkłady z papierem i tuszem są dostępne jako materiały eksploatacyjne. Napisz do nas, a podpowiemy, jaki zestaw wybrać."],
 ["Ile trwa dostawa?","Dostawa do paczkomatu lub kurierem pod adres jest darmowa i trwa zwykle kilka dni roboczych. W okresach wzmożonych zamówień czas ten może się wydłużyć."],
 ["Czy mogę zwrócić produkt?","Tak. Masz 14 dni od otrzymania paczki na zwrot bez podawania przyczyny. Wystarczy napisać na "+EMAIL+"."],
 ["Czy to dobry prezent?","Zdecydowanie. Drukarka przychodzi w eleganckim pudełku i sprawdza się jako prezent dla mamy, babci, pary, przyjaciółki i każdego, kto kocha zdjęcia."]
];''')
s=s.replace('var SELLER="Kwiatora";','var SELLER="Nostalio";')
s=s.replace('<b>Kwiatora</b>','<b>Nostalio</b>').replace('"Wiadomość ze sklepu Kwiatora"','"Wiadomość ze sklepu Nostalio"')
s=s.replace('Czas dostawy wynosi zwykle <b>6–10 dni roboczych</b>','Czas dostawy wynosi zwykle <b>kilka dni roboczych</b>')
s=s.replace('do paczkomatów InPost oraz kurierem','do paczkomatów oraz kurierem')
s=s.replace('<span>📦 Paczkomat InPost</span>','<span>📦 Paczkomat</span>').replace('"Paczkomat InPost · GRATIS"','"Paczkomat · GRATIS"')
open(p,'w',encoding='utf-8').write(s)
left=re.findall(r'[^\n]{0,40}(?:Kwiat|kwiat|klock|bukiet|Bukiet|Kalendarz|kalendarz|Wigili|InPost)[^\n]{0,40}',s)
print('OK; zostało:',len(left)); [print(' >',l) for l in left[:20]]
