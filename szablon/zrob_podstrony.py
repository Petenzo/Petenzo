# Ogólne szablony podstron (regulamin, polityki, kontakt, koszyk) z nawiasami – na bazie podstron Lulavi
import re
R='/home/user/Petenzo/'
base=open(R+'szablon/szablon-sklepu.html').read()
pod=open(R+'shopify-motyw/src/podstrona.html').read()
css=pod[:pod.index('</style>')+8]
head=base[:base.index('<main>')]
foot=base[base.index('</main>')+7:base.index('<script>')]
end='</body>\n</html>\n'
def form():
    return '''<section class="pod-kontakt"><div class="wrap pod-wrap"><h2>Skontaktuj się <span class="hl">z nami</span></h2>
<form class="pod-form" onsubmit="return false"><input type="text" placeholder="Imię"><input type="email" placeholder="E-mail"><input type="tel" placeholder="Numer telefonu"><textarea placeholder="Wiadomość"></textarea><button class="btn" type="button">Wyślij</button></form></div></section>'''
def strona(tytul, tresc):
    return f'<main class="podstrona"><div class="wrap pod-wrap"><h1>{tytul}</h1><div class="pod-tresc">{tresc}</div></div>{form()}</main>'
S='[NAZWA SKLEPU]'; E='[E-MAIL KONTAKTOWY]'
strony={
'5-regulamin':strona('Regulamin',f'''<h2>1. Informacje ogólne</h2><p>Sklep internetowy <b>{S}</b> prowadzi sprzedaż na odległość za pośrednictwem strony [ADRES STRONY]. Kontakt ze sprzedawcą: <b>{E}</b>.</p>
<h2>2. Składanie zamówień</h2><p>Zamówienie składasz przez stronę sklepu. Umowa zostaje zawarta w chwili otrzymania e-maila z potwierdzeniem zamówienia. Ceny są podane w złotych i zawierają podatki.</p>
<h2>3. Płatności</h2><p>Dostępne metody płatności (m.in. <b>[METODY PŁATNOŚCI]</b>) wyświetlają się w kasie. Zamówienie realizujemy po zaksięgowaniu płatności.</p>
<h2>4. Dostawa</h2><p>Dostawa jest <b>[CENA DOSTAWY – np. bezpłatna]</b>, a czas realizacji wynosi zwykle <b>[CZAS DOSTAWY]</b>. Szczegóły w <a href="#">Polityce wysyłki</a>.</p>
<h2>5. Zwroty</h2><p>Masz <b>[LICZBA DNI] dni od otrzymania produktu</b> na odstąpienie od umowy bez podawania przyczyny. Szczegóły w <a href="#">Zwrotach i reklamacjach</a>.</p>
<h2>6. Reklamacje</h2><p>Odpowiadamy za zgodność produktu z umową. Reklamację zgłoś na <b>{E}</b> – odpowiemy w ciągu <b>14 dni</b>.</p>
<h2>7. Spory</h2><p>Możesz skorzystać z pomocy miejskiego lub powiatowego rzecznika konsumentów albo Inspekcji Handlowej.</p>
<h2>8. Postanowienia końcowe</h2><p>W sprawach nieuregulowanych stosuje się prawo polskie, w szczególności Kodeks cywilny i ustawę o prawach konsumenta. Zasady przetwarzania danych opisuje <a href="#">Polityka prywatności</a>.</p>'''),
'6-polityka-prywatnosci':strona('Polityka prywatności',f'''<h2>1. Administrator danych</h2><p>Administratorem danych osobowych jest <b>{S}</b>. Kontakt w sprawach danych: <b>{E}</b>.</p>
<h2>2. Jakie dane zbieramy?</h2><ul><li>imię i nazwisko,</li><li>adres dostawy,</li><li>adres e-mail,</li><li>numer telefonu (jeśli go podasz),</li><li>dane potrzebne do płatności i realizacji zamówienia.</li></ul>
<h2>3. Po co je zbieramy?</h2><ul><li>realizacja zamówień,</li><li>kontakt z Tobą,</li><li>obsługa zwrotów i reklamacji,</li><li>obowiązki wynikające z przepisów prawa,</li><li>statystyki i reklama – tylko za Twoją zgodą.</li></ul>
<h2>4. Komu je przekazujemy?</h2><p>Tylko firmom potrzebnym do realizacji zamówienia: firmom kurierskim, operatorom płatności, dostawcy towaru oraz platformie sklepu <b>[PLATFORMA – np. Shopify]</b>.</p>
<h2>5. Jak długo je przechowujemy?</h2><p>Przez czas realizacji zamówienia oraz tak długo, jak wymagają tego przepisy, np. podatkowe.</p>
<h2>6. Twoje prawa</h2><ul><li>dostęp do danych i ich poprawienie,</li><li>usunięcie lub ograniczenie przetwarzania,</li><li>sprzeciw i przeniesienie danych,</li><li>skarga do Prezesa UODO.</li></ul>
<h2>7. Pliki cookies</h2><p>Używamy cookies, żeby sklep działał poprawnie, oraz do statystyk i reklam. Zgodą zarządzasz w banerze cookies i w przeglądarce.</p>'''),
'7-polityka-wysylki':strona('Polityka wysyłki',f'''<h2>1. Obszar dostawy</h2><p>Wysyłamy na terenie <b>[KRAJ]</b>: <b>[DOSTAWA 1 – np. do paczkomatów]</b> albo <b>[DOSTAWA 2 – np. kurierem pod adres]</b>.</p>
<h2>2. Koszt dostawy</h2><p>Dostawa jest <b>[CENA DOSTAWY – np. bezpłatna]</b> przy każdym zamówieniu.</p>
<h2>3. Czas dostawy</h2><p>Zwykle <b>[CZAS DOSTAWY]</b> od zaksięgowania płatności. W wyjątkowych sytuacjach, np. opóźnień przewoźnika, dostawa może potrwać dłużej – wtedy damy Ci znać.</p>
<h2>4. Śledzenie paczki</h2><p>Po wysłaniu dostaniesz e-mail z numerem do śledzenia przesyłki.</p>
<h2>5. Uszkodzona paczka</h2><p>Sprawdź paczkę przy odbiorze. Jeśli jest uszkodzona, napisz do nas na <b>{E}</b> i dołącz zdjęcie.</p>
<h2>6. Kontakt</h2><p>Pytania o wysyłkę? Napisz: <b>{E}</b></p>'''),
'8-zwroty-i-reklamacje':strona('Zwroty i reklamacje',f'''<h2>1. [LICZBA DNI] dni na zwrot</h2><p>Masz <b>[LICZBA DNI] dni od otrzymania produktu</b> na odstąpienie od umowy, bez podawania przyczyny.</p>
<h2>2. Jak zwrócić?</h2><ol><li>Napisz na <b>{E}</b> – podaj numer zamówienia i że chcesz zwrócić produkt.</li><li>W odpowiedzi dostaniesz adres do odesłania paczki.</li><li>Odeślij produkt w ciągu <b>14 dni</b> od zgłoszenia.</li></ol>
<h2>3. Zwrot pieniędzy</h2><p>Oddamy pieniądze w ciągu <b>14 dni</b> od zgłoszenia, tą samą metodą płatności. Możemy wstrzymać zwrot do czasu otrzymania produktu lub dowodu jego nadania. Koszt odesłania pokrywa kupujący.</p>
<h2>4. Anulowanie zamówienia</h2><p>Zamówienie możesz anulować, dopóki nie zostało wysłane – napisz do nas jak najszybciej z numerem zamówienia.</p>
<h2>5. Reklamacje</h2><p>Jeśli produkt jest wadliwy, napisz na <b>{E}</b>, opisz problem i dołącz zdjęcie. Odpowiemy w ciągu <b>14 dni</b>. Przy uznanej reklamacji wszystkie koszty, także wysyłki, pokrywamy my.</p>'''),
'9-kontakt':strona('Kontakt',f'''<h2>Napisz do nas</h2><p>Masz pytanie o zamówienie, wysyłkę albo zwrot? Napisz na <b>{E}</b> albo skorzystaj z formularza poniżej.</p><p>Odpowiadamy zwykle w ciągu <b>[CZAS ODPOWIEDZI – np. 24 godzin]</b>, [DNI – np. od poniedziałku do piątku].</p>'''),
}
poz=lambda n:f'''<div class="kp-poz"><img src="{re.search(r'data:image/svg\+xml;base64,[^"]+',base).group(0)}" alt=""><div><div class="kp-nazwa">[NAZWA PRODUKTU]</div><div class="kp-wzor">[WARIANT {n}]</div><div class="kp-szt">[CENA] / szt.</div><a class="kp-usun" href="#">× Usuń</a></div>
<div class="kp-dol"><span class="kp-ilosc"><a href="#">−</a><span>1</span><a href="#">+</a></span><div class="kp-cena"><s>[STARA CENA]</s>[CENA]</div></div></div>'''
strony['10-strona-koszyka']=f'''<main class="kp"><div class="wrap"><div class="kp-head"><h1>Twój koszyk <span class="kp-ile">[LICZBA] produkty</span></h1><a class="kp-wroc" href="#">← Kontynuuj zakupy</a></div>
<form class="kp-grid" onsubmit="return false"><div class="kp-lewa"><div class="kp-box">{poz(1)}{poz(2)}</div></div>
<div class="kp-prawa"><div class="kp-box kp-pods"><h2>Podsumowanie</h2><div class="kp-wiersz"><span>Produkty ([LICZBA])</span><span>[KWOTA]</span></div><div class="kp-wiersz rabat"><span>Rabat za zestaw</span><span>−[KWOTA]</span></div>
<div class="kp-wiersz dost"><span>🚚 Dostawa</span><b>[CENA DOSTAWY]</b></div><div class="kp-razem"><span>Razem</span><span>[KWOTA]</span></div></div>
<div class="kp-punkt"><b>📦 [DOSTAWA – np. Darmowa dostawa]</b>[DOSTAWA 1] albo [DOSTAWA 2]. [INFORMACJA – jak klient wybiera dostawę w kasie]</div>
<button class="btn" type="button"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></svg>Realizuj zamówienie</button><div class="kp-ssl">🔒 Bezpieczna płatność · Szyfrowanie SSL</div></div></form></div></main>'''
for k,v in strony.items():
    open(R+f'szablon/{k}.html','w').write(head.replace('<title>Szablon sklepu</title>','<title>Szablon – '+k+'</title>')+css+v+foot+end)
print(list(strony))
