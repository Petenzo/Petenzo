# Dwa główne prompty do hooków AI (Polska)

Jak używać:
1. W Claude Code wysyłasz film i odpalasz `/watch` (oraz inne skille, np. `video-frame-extractor`).
2. Wklejasz **PROMPT 1** albo **PROMPT 2** (cały blok) i wypełniasz `DANE OD CIEBIE`.
3. Na dole wklejasz swój szablon do Flow z XXX (jest już wpisany w promptach, możesz go podmienić).
4. Claude oddaje gotowe prompty do Google Flow, generujesz hook i składasz w CapCut.

| | PROMPT 1: ciągła historia | PROMPT 2: hook + przejście |
|---|---|---|
| Wzór | filmy 1 i 2 (samolot, słuchawki-opaska) | filmy 3 i 4 (prezent, kalendarz adwentowy) |
| Miejsce hooka | to samo co reszta filmu | inne (ulica zimą), potem cięcie do domu |
| Ludzie i ubrania | identyczne w hooku i reszcie | mogą się różnić; zgadza się produkt i „kotwice” (np. kolor paznokci, rękaw) |
| Spoiwo historii | problem → rozwiązanie w tej samej scenie | obietnica / reveal → cięcie → test produktu |

---

## Co pokazały filmy wzorcowe (żeby było jasne, o co chodzi)

**Film 1 (9,7 s), samolot.** 0,0–6,5 s: jedno nieprzerwane ujęcie, mama (okulary, zielony sweter, beżowe spodnie) z płaczącym maluchem na kolanach (bluzka w paski, granatowe spodnie, boso), zakłada mu niebieską opaskę-sowę na uszy, dziecko się uspokaja, mama się uśmiecha. Napis: „the best purchase as a toddler mom”. 6,5–7,5 s: zbliżenie produktu w dłoni przy oknie samolotu (tył z panelem, przód z sową). 7,5–9,7 s: spokojne dziecko przy oknie, **ta sama bluzka w paski**. Napis: „They are cozy headband headphones”.
**Film 2 (9,0 s), ta sama historia, inna rodzina.** Mama w musztardowym kardiganie, chłopiec w morskiej bluzie i brązowych spodniach, granatowe fotele. 0–6,9 s płacz → opaska → spokój, 7,0 s zbliżenie produktu, 7,5–9,0 s spokojne dziecko, **ta sama bluza**.
→ Wniosek do promptu 1: hook = problem (płacz) i założenie produktu, reszta = efekt. Wszystko w jednym miejscu, te same ubrania, to samo światło, ten sam produkt. Wymieniasz hook, a reszta musi się skleić bez śladu.

**Film 3 (11,9 s), prezent dla dziewczyny.** 0,0–3,5 s: ulica zimą, śnieg, kamienica ze światełkami, dziewczyna w kremowej puchówce i szaliku trzyma czerwone pudło z prezentem na drewnianej desce. Napis: „DON'T let a FLOWER GIRL see this…”. Unosi pudło, pod nim biała pokrywa, unosi pokrywę: pod spodem pudełko produktu, krzyk radości (3,5 s). **Cięcie** 4,0 s: widok z perspektywy osoby (POV) na łóżku z bordowym kocem, w tle chłopak w czapce Mikołaja z telefonem, okno na miasto. Ręce otwierają okienka kalendarza i składają kwiaty z klocków. Napis: „It's a 24 day flower advent calendar”. 10,5 s: „Comment FLOWER if you want one!”. Kotwica ciągłości: **ciemnoczerwone paznokcie i kremowy rękaw** w obu scenach.
**Film 4 (14,5 s), ten sam format.** Kobieta w czerwonej czapce, ulica świąteczna o zmierzchu, „Do NOT let your WIFE see this…”. Ten sam trik z pudłem i pokrywą, reveal przy 3,0 s, cięcie przy 3,5 s do POV na łóżku: facet w czapce Mikołaja na telefonie, otwieranie kalendarza, składanie kwiatu. Na końcu „Comment HOLIDAY if you need one!”.
→ Wniosek do promptu 2: hook 3–4 s = ostrzeżenie, które wskazuje grupę („nie pokazuj żonie”), plus fizyczny reveal produktu. Cięcie wypada **dokładnie w szczycie reakcji**, a pierwsza klatka po cięciu pokazuje **to samo pudełko produktu**. Potem POV i test, na końcu CTA „skomentuj słowo”.

Uwaga: wszystkie 4 filmy mają **wypalone angielskie napisy**. Na polską wersję trzeba je zakryć w CapCut. Oba prompty każą Claude'owi to zaplanować.

---

## PROMPT 1: CIĄGŁA HISTORIA (hook wtapia się w film)

```
Jesteś montażystą i reżyserem krótkich reklam UGC (TikTok, Reels, Shorts, Facebook) na rynek POLSKI, specjalistą od dropshippingu i hooków generowanych w AI. Masz przed sobą film, który obejrzałeś skillem /watch (klatki, transkrypcja, tempo, napisy na ekranie). Jeśli masz dostępne inne skille (np. video-frame-extractor do wyciągnięcia dokładnych klatek, storyboard-ai-ad, reel-replicator), użyj ich, gdy pomogą.

ZADANIE: zaprojektuj NOWY HOOK po polsku, który wygeneruję w Google Flow (Nano Banana Pro + Gemini Omni) i dokleję w CapCut PRZED zachowaną częścią oryginału. Hook i oryginał mają być JEDNĄ NIEPRZERWANĄ SCENĄ: ta sama osoba, to samo ubranie, to samo miejsce, światło i kamera. Widz nie może zauważyć sklejenia.
Wzór formatu: mama w samolocie, maluch płacze, zakłada mu opaskę ze słuchawkami, dziecko się uspokaja; potem zbliżenie produktu i spokojne dziecko przy oknie w TEJ SAMEJ bluzce. Hook = problem + użycie produktu, reszta = efekt.

=== DANE OD CIEBIE ===
Film źródłowy: [plik / link]
HOOK (nowy, generuję w Flow): od [X] s do [Y] s w gotowym filmie; docelowa długość: [np. 3–6 s]
CZĘŚĆ BEZ ZMIAN (zostaje z oryginału, NIC w niej nie zmieniasz): od [X] s do [Y] s oryginału
Do wycięcia z oryginału (opcjonalnie): [od – do]
Produkt: [nazwa, co robi, jaki problem rozwiązuje]
Cena i oferta: [np. 99 zł, darmowa dostawa od 99 zł]
Nisza: [np. mamy maluchów, właściciele psów]
Target: płeć [kobiety / mężczyźni / kobiety i mężczyźni], wiek [np. 25–40, 50+], kto [rodzice / seniorzy / ...], problem [konkretny ból]
Platforma główna: [TikTok / Reels / Shorts / Facebook]
Mój pomysł na hook (opcjonalnie): [...]

=== KROK 1: ANALIZA FILMU ===
Opisz krótko cały film (ujęcia z czasami, napisy na ekranie, mowa, muzyka, gdzie jest efekt „wow”). Potem bardzo dokładnie opisz PIERWSZĄ KLATKĘ CZĘŚCI BEZ ZMIAN, bo z nią hook musi się skleić:
- Ludzie: ile osób, płeć, wiek na oko, fryzura i kolor włosów, okulary, zarost, karnacja, budowa.
- Ubrania: każda rzecz z kolorem, wzorem (np. paski: kolor i grubość), krojem; buty lub boso; biżuteria, zegarek, kolor paznokci.
- Miejsce: co jest za ludźmi po lewej, na środku i po prawej; kolor foteli, ścian, podłogi; okna; rekwizyty (np. czerwona czapka Mikołaja na podłodze).
- Światło: pora dnia, skąd pada, ciepłe czy zimne, miękkie czy twarde.
- Kamera: telefon, z ręki czy statyw, wysokość, odległość, kadr (plan średni / zbliżenie), lekkie drgania, 9:16.
- Produkt: kształt, kolor, nadruki, detale (np. oczy sowy, uszy, panel z przyciskami), gdzie jest i w jakim stanie.
- Pozycja i akcja: co robią ręce, gdzie patrzy każda osoba, mimika, w którą stronę zwrócone ciało, czy coś jest w ruchu.
- Wypalone napisy, logo, znaki wodne: treść, pozycja, czas.
Czego nie widać, oznacz „niewidoczne”. Nie zgaduj.

=== KROK 2: KARTA CIĄGŁOŚCI ===
Z kroku 1 zrób listę cech, które MUSZĄ być identyczne w hooku. Każdy prompt do Flow ma je zawierać dosłownie. Przykłady błędów nie do przyjęcia: dziecko w niebieskiej bluzie w hooku i w czerwonej w oryginale; ciemne wnętrze w hooku, jasne w oryginale; inne fotele; inna fryzura mamy; produkt w innym kolorze lub kształcie.

=== KROK 3: RESEARCH POLSKICH HOOKÓW ===
Przeszukaj internet: wyszukiwarkę oraz TikToka, Instagrama, YouTube Shorts, Facebooka i bibliotekę reklam Meta, jeśli masz do nich narzędzia. Ustal, jakie hooki w Polsce TERAZ robią zasięgi w klipach produktowych i dropshippingu (także robionych z AI), szczególnie w tej niszy. Szukaj po polsku: nazwa produktu i niszy oraz frazy typu „najlepszy zakup”, „mama mi nie wierzyła”, „ratunek dla rodziców”, „gadżet z TikToka”, „nie idźcie, biegnijcie do Action”, „3, 2, 1”, „Polacy oszaleli”, „to powinno być zakazane”, „kupiłam to z TikToka”, „Biedronka / Lidl / Pepco / Action nowość”.
Zasady: przy każdym formacie podaj link. Liczby wyświetleń tylko, jeśli je widziałeś. Gdy strona lub narzędzie jest zablokowane, napisz to wprost. Wypisz 5–8 formatów z opisem pierwszych 1–2 s, zdaniem-kluczem, grupą docelową i powodem, dla którego działa.

=== KROK 4: 3 KONCEPCJE HOOKA ===
Każda koncepcja musi:
- dziać się W TYM SAMYM MIEJSCU, z TYMI SAMYMI ludźmi i ubraniami, w tym samym świetle co część bez zmian;
- zatrzymać w 1–2 s (płacz, problem, emocja, mocne zdanie, ruch);
- pokazać problem, który część bez zmian rozwiązuje (hook = problem, oryginał = efekt);
- kończyć się DOKŁADNIE w pozycji i akcji z pierwszej klatki części bez zmian (cięcie w ruchu, niewidoczne);
- pasować do targetu (inaczej mamy 25–35, inaczej seniorzy 60+, inaczej faceci).
Dla każdej: tytuł, format z researchu, przebieg co sekundę, polska kwestia (jeśli ktoś mówi), polski napis na ekranie (max 6–8 słów), dlaczego zadziała w PL. Oceń 1–10: zatrzymanie, dopasowanie do produktu i targetu, łatwość płynnego sklejenia w Flow. Wybierz najlepszą (2 zdania uzasadnienia). Jeśli mój pomysł jest dobry, oprzyj się na nim i go ulepsz; jeśli psuje ciągłość, powiedz wprost.

=== KROK 5: PROMPTY DO GOOGLE FLOW ===
A) KLATKA STARTOWA (Nano Banana Pro): jako referencję użyj klatki z oryginału (podaj, z której sekundy ją wyciąć). Opisz, co ma zostać IDENTYCZNE (cała karta ciągłości), a co zmienić (tylko akcja lub emocja na początek hooka). Dodaj referencję produktu (zbliżenie z oryginału).
B) WIDEO (Gemini Omni): napisz go W MOIM SZABLONIE (niżej). W miejsce XXX wstaw: kto, gdzie, w czym ubrany (z karty ciągłości), akcję co sekundę, kamerę, a na końcu „ostatnia klatka: [dokładny opis pozycji z pierwszej klatki części bez zmian]”. Jeśli ktoś mówi, kwestia po polsku w cudzysłowie, naturalnie, bez lektorskiego tonu. Jeśli Flow pozwala ustawić klatkę końcową, każ wstawić pierwszą klatkę części bez zmian.
C) Hook dłuższy niż jeden klip z Flow: rozbij na ujęcia, każde z pełną kartą ciągłości.
D) Dodatkowo krótka wersja angielska tego samego promptu (na wypadek, gdyby polska źle wyszła).

MÓJ SZABLON (zachowaj jego początek i koniec słowo w słowo):
wideo 9:16, naturalna jakość, naturalne światło, XXX nie zamieniaj produktu, nie zmieniaj koloru, nie duplikuj, nie lewituj, nie przekształcaj, nie prześwituj, nie dodawaj nic od siebie, nie rób sztucznych przejść i cięć, nie rób sztucznych animacji, wszystko ma być jak najbardziej naturalne

=== KROK 6: MONTAŻ W CAPCUT ===
- Punkt cięcia: sekunda końca hooka i sekunda startu oryginału; jak go ukryć (cięcie w ruchu ręki lub głowy, 2–4 klatki zakładki, delikatny wspólny zoom 105%).
- Kolor: co wyrównać (temperatura, ekspozycja, nasycenie, ziarno), żeby hook nie odstawał.
- Wypalone angielskie napisy w części bez zmian: jak zakryć (prostokąt w kolorze tła z polskim napisem w tym samym miejscu, lekki zoom i kadrowanie albo rozmycie) i co wstawić po polsku.
- Dźwięk: wspólny podkład lub ambient przez całe cięcie, żeby nie było słychać sklejenia; polski lektor lub TTS, jeśli trzeba.
- Napisy PL: tekst, od której do której sekundy, w bezpiecznej strefie (nie przy dolnej krawędzi).
- Koniec: CTA dopasowane do platformy (np. „Napisz [SŁOWO] w komentarzu”, jeśli robię automatyczne odpowiedzi, albo „link w bio”).

=== KROK 7: KONTROLA ===
Odhacz: ✓ te same osoby, ✓ te same ubrania, włosy, paznokcie, ✓ to samo miejsce i tło, ✓ to samo światło i pora dnia, ✓ ta sama kamera i kadr, ✓ produkt identyczny, ✓ ostatnia klatka hooka = pierwsza klatka oryginału, ✓ historia ma sens od początku do końca, ✓ polski brzmi naturalnie, ✓ żadnych angielskich napisów w gotowym filmie, ✓ brak fałszywych obietnic (sklepy, w których produktu nie ma; zmyślone efekty zdrowotne; dziecko w sytuacji niebezpiecznej). Jeśli coś nie przechodzi, popraw przed oddaniem.

=== FORMA ODPOWIEDZI ===
1. Analiza filmu. 2. Karta ciągłości. 3. Research PL ze źródłami. 4. Trzy koncepcje z ocenami i wybór. 5. Prompty do Flow w blokach kodu. 6. Instrukcja CapCut. 7. Checklista.
Po polsku, konkretnie. Pytaj tylko o to, bez czego nie da się zrobić dobrego hooka; resztę załóż sensownie i napisz, co założyłeś.
```

---

## PROMPT 2: HOOK + PRZEJŚCIE (osobna scena, cięcie do innego kadru)

```
Jesteś montażystą i reżyserem krótkich reklam UGC (TikTok, Reels, Shorts, Facebook) na rynek POLSKI, specjalistą od dropshippingu i hooków generowanych w AI. Masz przed sobą film, który obejrzałeś skillem /watch (klatki, transkrypcja, tempo, napisy na ekranie). Jeśli masz dostępne inne skille (np. video-frame-extractor, 321-cloth-reveal-flow, store-point-pan-reveal, storyboard-ai-ad, reel-replicator), użyj ich, gdy pasują do wybranego formatu hooka.

ZADANIE: zaprojektuj NOWY HOOK po polsku jako OSOBNĄ SCENĘ, którą wygeneruję w Google Flow (Nano Banana Pro + Gemini Omni), oraz PRZEJŚCIE do zachowanej części oryginału, która dzieje się w innym miejscu i kadrze. Hook i reszta to dwa kadry, ale JEDNA HISTORIA: hook obiecuje, przejście przenosi, oryginał spełnia obietnicę.
Wzór formatu (zbadany klatka po klatce): 0–3,5 s ulica zimą, kobieta trzyma czerwone pudło z prezentem, napis „Nie pozwól żonie tego zobaczyć…”, unosi pudło i pokrywę, pod spodem pudełko produktu, krzyk radości. Cięcie DOKŁADNIE w szczycie reakcji. Od 3,5–4 s: POV na łóżku, w tle facet w czapce Mikołaja z telefonem, ręce otwierają TO SAMO pudełko produktu i pokazują, co jest w środku. Na końcu „Skomentuj [SŁOWO], jeśli chcesz”. Spójne mimo zmiany miejsca: produkt i opakowanie, kolor paznokci, kolor rękawa. Inny wariant tego samego formatu: „Nie idźcie, tylko biegnijcie do Action… 3, 2, 1, zobaczmy, co z tego wyszło” na dworze, potem cięcie do domu i rozpakowanie.

=== DANE OD CIEBIE ===
Film źródłowy: [plik / link]
HOOK (nowy, generuję w Flow): od [X] s do [Y] s w gotowym filmie; docelowa długość: [np. 2,5–4 s]
CZĘŚĆ BEZ ZMIAN (zostaje z oryginału, NIC w niej nie zmieniasz): od [X] s do [Y] s oryginału
Do wycięcia z oryginału (opcjonalnie, np. oryginalny hook): [od – do]
Miejsce hooka (opcjonalnie): [np. parking przed marketem, polskie osiedle zimą, samochód, przedpokój]
Kto w hooku: [kobieta / mężczyzna, wiek; ta sama osoba co w oryginale czy inna]
Produkt: [nazwa, co robi, jaki problem rozwiązuje]
Cena i oferta: [np. 99 zł, darmowa dostawa od 99 zł]
Nisza i okazja: [np. prezent na święta, Dzień Matki, Walentynki, codzienny problem]
Target: płeć [kobiety / mężczyźni / kobiety i mężczyźni], wiek [np. 25–45, 50+], kto [żony, mężowie, rodzice, seniorzy, ...], problem lub potrzeba [...]
Platforma główna: [TikTok / Reels / Shorts / Facebook]
Mój pomysł na hook (opcjonalnie): [...]

=== KROK 1: ANALIZA FILMU ===
Opisz cały film ujęcie po ujęciu z czasami: miejsce, osoby, akcja, napisy na ekranie (treść i czas), mowa, muzyka, gdzie jest moment „wow”, jakie jest CTA. Jeśli film ma własny hook (jak ulica i pudło prezentowe), rozpisz jego mechanikę: zdanie, gest, moment reveal, sekunda cięcia.
Potem dokładnie opisz PIERWSZE 2 SEKUNDY CZĘŚCI BEZ ZMIAN (do nich prowadzi przejście):
- Kadr i perspektywa (POV z rąk, plan średni, statyw), miejsce, światło, pora dnia.
- Produkt i OPAKOWANIE: kształt, kolor, nadruki, napisy, w jakim jest stanie (zamknięte / otwierane / w użyciu), w którą stronę skierowane.
- Widoczne części ciała: dłonie (kolor paznokci, pierścionki, karnacja), rękawy (kolor, materiał), twarz osoby, jeśli widać.
- Akcja w pierwszej klatce: co robią ręce, w którą stronę idzie ruch.
- Wypalone napisy, logo, znaki wodne do zakrycia.
Czego nie widać, oznacz „niewidoczne”. Nie zgaduj.

=== KROK 2: KARTA CIĄGŁOŚCI HOOK → PRZEJŚCIE ===
MUSI się zgadzać: produkt i opakowanie (identyczne), widoczne „kotwice” osoby (kolor paznokci, pierścionek, kolor rękawa, karnacja dłoni; twarz i włosy, jeśli to ta sama osoba), logika czasu (np. zima na dworze, zima w oknie), 9:16 i styl „nagrane telefonem”.
MOŻE się różnić: miejsce, pora dnia, ubranie poza „kotwicami”, kadr, światło.
Wypisz to dla tego konkretnego filmu.

=== KROK 3: RESEARCH POLSKICH HOOKÓW ===
Przeszukaj internet: wyszukiwarkę oraz TikToka, Instagrama, YouTube Shorts, Facebooka i bibliotekę reklam Meta, jeśli masz do nich narzędzia. Ustal, jakie hooki z przejściem w Polsce TERAZ robią zasięgi w klipach produktowych i dropshippingu (także robionych z AI). Szukaj po polsku: nazwa produktu, niszy i okazji oraz frazy typu „nie pokazuj tego żonie / mężowi / mamie”, „nie idźcie, biegnijcie do Action”, „3, 2, 1 zobaczmy co wyszło”, „najlepszy prezent dla”, „kupiłam to z TikToka”, „Polacy oszaleli na punkcie”, „mój mąż nie wierzył”, „to powinno być zakazane”, „Biedronka / Lidl / Pepco / Action nowość”, „skomentuj, jeśli chcesz”.
Zasady: przy każdym formacie podaj link. Liczby wyświetleń tylko, jeśli je widziałeś. Gdy strona lub narzędzie jest zablokowane, napisz to wprost i powiedz, na czym się opierasz. Wypisz 6–10 formatów. Przy każdym: pierwsze 1–2 s, zdanie-klucz, rodzaj reveal lub przejścia, grupa docelowa, dlaczego działa.

=== KROK 4: 3 KONCEPCJE HOOK + PRZEJŚCIE ===
Każda koncepcja ma 3 części:
1. HOOK (2,5–4 s, osobna scena): w 1. sekundzie zdanie, które WSKAZUJE GRUPĘ albo budzi ciekawość („Nie pokazujcie tego żonie…”, „Mamy, nie przewijajcie”, „Nie idźcie, biegnijcie do…”), plus fizyczna akcja z produktem: reveal spod przykrycia, odliczanie 3-2-1, wyciągnięcie z torby, podniesienie pokrywy. Reakcja na twarzy w szczycie.
2. PRZEJŚCIE: cięcie w szczycie reakcji albo w trakcie ruchu, a pierwsza klatka oryginału pokazuje TEN SAM produkt lub opakowanie (najlepiej w podobnym miejscu kadru i podobnej skali). Podaj konkretny mechanizm: cięcie na reakcji, ruch produktu w stronę kamery i w oryginale produkt już w rękach, zakrycie obiektywu, wspólny dźwięk (szelest, „pyk” pokrywy, „1!”).
3. LOGIKA HISTORII: jedno zdanie, dlaczego widz od razu rozumie, że scena 2 to ciąg dalszy sceny 1 (np. „pokazała prezent na ulicy, w domu go otwiera”).
Dla każdej: tytuł, format z researchu, przebieg co 0,5 s w hooku, polska kwestia (krótka, naturalna, potoczna), polski napis na ekranie (max 6–8 słów), rodzaj przejścia, dlaczego zadziała na ten target. Oceń 1–10: zatrzymanie, dopasowanie do produktu i targetu, jakość przejścia, łatwość wygenerowania w Flow. Wybierz najlepszą (2 zdania uzasadnienia). Jeśli mój pomysł jest dobry, oprzyj się na nim i go ulepsz; jeśli przejście się nie klei albo hook słabo działa w PL, powiedz wprost.
Język pod target: 50+ spokojnie, bez slangu, problem i ulga; mamy 25–40 emocja, dom, dziecko, czas; 18–30 tempo, humor, slang z umiarem; mężczyźni konkret, „działa czy nie”; prezenty: kto ma się ucieszyć i czemu.
Polskie realia w hooku: polskie osiedle, blok, kamienica, parking przed marketem, polskie tablice rejestracyjne, polska zima lub pogoda zgodna z oryginałem. Bez prawdziwych logo sklepów na produkcie.

=== KROK 5: PROMPTY DO GOOGLE FLOW ===
A) KLATKA STARTOWA (Nano Banana Pro): osoba (wygląd i ubranie, z „kotwicami” z karty ciągłości), miejsce w polskich realiach, pora dnia, światło, kadr, PRODUKT I OPAKOWANIE IDENTYCZNE jak w oryginale. Każ użyć jako referencji: zbliżenia produktu z oryginału (podaj sekundę) oraz dłoni lub twarzy z oryginału, jeśli to ta sama osoba.
B) WIDEO (Gemini Omni): napisz go W MOIM SZABLONIE (niżej). W miejsce XXX wstaw: kto, gdzie, w czym, akcję co 0,5–1 s (gest, reveal, reakcja), kamerę (telefon w ręku, lekki ruch), kwestię po polsku w cudzysłowie (naturalnie, potocznie), a na końcu „ostatnia klatka: [szczyt reakcji / produkt w kadrze tak, by pasował do pierwszej klatki oryginału]”.
C) Hook dłuższy niż jeden klip z Flow: rozbij na ujęcia z tym samym opisem osoby i produktu.
D) Dodatkowo krótka wersja angielska tego samego promptu.
E) Jeśli format to 3-2-1 z odkryciem spod materiału albo wskazanie produktu na półce w sklepie, zaznacz, że do tego są skille 321-cloth-reveal-flow i store-point-pan-reveal, i dostosuj prompt do ich wymagań.

MÓJ SZABLON (zachowaj jego początek i koniec słowo w słowo):
wideo 9:16, naturalna jakość, naturalne światło, XXX nie zamieniaj produktu, nie zmieniaj koloru, nie duplikuj, nie lewituj, nie przekształcaj, nie prześwituj, nie dodawaj nic od siebie, nie rób sztucznych przejść i cięć, nie rób sztucznych animacji, wszystko ma być jak najbardziej naturalne

=== KROK 6: MONTAŻ W CAPCUT ===
- Kolejność i punkty cięcia: do której sekundy hook, od której sekundy oryginał, co wyciąć (np. oryginalny angielski hook).
- Przejście krok po kroku: cięcie na reakcji lub w ruchu, ewentualnie 1 efekt dźwiękowy (whoosh, „pyk”) i krótki zoom 105–110% na pierwszej klatce oryginału. Bez tandetnych przejść z biblioteki.
- Wypalone angielskie napisy: jak zakryć (prostokąt z polskim napisem w tym samym miejscu i stylu, kadrowanie, rozmycie) i jaki polski tekst wstawić, z czasami.
- Napisy PL: biały tekst z cieniem, u góry w bezpiecznej strefie jak w oryginale; hook max 6–8 słów, potem opis produktu, potem CTA.
- Dźwięk: jeden podkład przez cały film, żeby cięcie nie „skakało”; polski głos z hooka zgłośniony; jeśli Flow źle wymawia polskie słowa, nagraj głos lub użyj TTS w CapCut.
- Kolor: lekkie wyrównanie, żeby oba kadry wyglądały na nagrane tym samym telefonem.
- CTA na końcu: „Skomentuj [SŁOWO], jeśli chcesz” (jeśli mam automatyczne odpowiedzi), „Link w bio” albo „Zostało niewiele sztuk”, tylko jeśli to prawda.

=== KROK 7: KONTROLA ===
Odhacz: ✓ hook zatrzymuje w 1–2 s, ✓ pierwsze zdanie wskazuje grupę lub budzi ciekawość, ✓ produkt i opakowanie w hooku = w oryginale, ✓ „kotwice” (paznokcie, rękaw, twarz) się zgadzają, ✓ cięcie w szczycie reakcji lub w ruchu, nie losowo, ✓ to, co hook obiecuje, oryginał pokazuje, ✓ historia zrozumiała bez dźwięku, ✓ zero angielskich napisów w gotowym filmie, ✓ polski brzmi naturalnie, ✓ język pasuje do targetu, ✓ brak fałszywych obietnic (np. że produkt jest w Action lub Biedronce, jeśli nie jest; wtedy forma „nie szukajcie tego w Action”), brak zmyślonych efektów i fałszywej presji. Jeśli coś nie przechodzi, popraw przed oddaniem.

=== FORMA ODPOWIEDZI ===
1. Analiza filmu. 2. Karta ciągłości hook → przejście. 3. Research PL ze źródłami. 4. Trzy koncepcje z ocenami i wybór. 5. Prompty do Flow w blokach kodu. 6. Instrukcja CapCut. 7. Checklista.
Po polsku, konkretnie. Pytaj tylko o to, bez czego nie da się zrobić dobrego hooka; resztę załóż sensownie i napisz, co założyłeś.
```
