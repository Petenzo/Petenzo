# PROMPT: Postaw nowy sklep Shopify krok po kroku (home.pl + ImprovMX + Google Search Console)

> Skopiuj całość do nowego czatu z Claude. Na początku napisz: **„Prowadź mnie krok po kroku według tej instrukcji. Po każdym kroku czekaj, aż napiszę »dalej«. Odpowiadaj po polsku, krótko, konkretnie co kliknąć.”**
>
> Wszędzie, gdzie jest **TWOJADOMENA.pl**, wpisz swoją domenę, a zamiast **NAZWA** nazwę sklepu.

---

## KROK 0: Zanim zaczniesz

- Przygotuj: **nazwę sklepu**, **domenę .pl**, **Gmaila**, na który ma przychodzić poczta, oraz dane do płatności (konto bankowe, dowód).
- Jeśli Claude ma podłączony konektor **Shopify**, sprawdź, **do którego sklepu** jest podłączony. Na claude.ai: **Ustawienia → Konektory → Shopify → Rozłącz → Połącz → wybierz NOWY sklep**. Łatwo się pomylić i pracować na starym sklepie.
- Pracujesz w **Safari na MacBooku** i wyskakuje „Okno wyskakujące zablokowane”? Masz dwie opcje:
  - **Szybko:** kliknij ikonkę okienka w pasku adresu, obok ikony głośnika.
  - **Na stałe:** **Safari → Ustawienia dla witryny admin.shopify.com → Okna wyskakujące: Zezwalaj**. Ewentualnie **Safari → Ustawienia (⌘ + ,) → Witryny → Okna wyskakujące → admin.shopify.com → Zezwalaj**.
  - Potem odśwież stronę: **⌘ + R**.
  - Dalej nie działa? Otwórz Shopify w **Chrome**.

---

## KROK 1: Sklep w Shopify

1. Wejdź na **shopify.com/pl** i kliknij **„Rozpocznij bezpłatny okres próbny”**.
2. Zarejestruj się na Gmaila. Pytania na start możesz **pominąć**.
3. Sklep dostanie adres `xxxx.myshopify.com` i będzie **zamknięty hasłem**. Tak ma być, otworzysz go na końcu.

---

## KROK 2: Domena w home.pl

1. Wejdź na **home.pl**, wyszukaj **TWOJADOMENA.pl** i dodaj ją do koszyka.
2. **Odznacz wszystkie dodatki**: hosting, pocztę, kreator stron i SSL. Nie są potrzebne.
3. Zapłać i poczekaj na maila, że domena jest aktywna.

---

## KROK 3: DNS w home.pl (sklep)

Wejdź w **panel.home.pl → Domeny → TWOJADOMENA.pl → DNS (Strefa DNS / Rekordy DNS)**.

Jeśli są stare rekordy **A** z pustym hostem albo stary rekord dla **www**, usuń je. **Rekordów NS nie ruszaj.**

### Rekord A
Kliknij **„Dodaj nowy rekord”**:

| Pole w home.pl | Co wpisać |
|---|---|
| **Typ rekordu** | `A` |
| **Adres IPv4** | `23.227.38.65` |
| **Host (Opcjonalne)** | **ZOSTAW PUSTE** |
| **TTL (Opcjonalne)** | puste (domyślnie 3600) |

> ⚠️ Częsty błąd: IP wpisane w pole **Host**. Ma iść do **Adres IPv4**, a Host zostaje pusty.

Kliknij **OK**.

### Rekord CNAME
Kliknij **„Dodaj nowy rekord”**:

| Pole w home.pl | Co wpisać |
|---|---|
| **Typ rekordu** | `CNAME` |
| **Nazwa kanoniczna** | `shops.myshopify.com.` (z kropką na końcu) |
| **Host** | `www` |
| **TTL** | puste |

Kliknij **OK**.

---

## KROK 4: Podłączenie domeny w Shopify

1. W Shopify kliknij **Ustawienia** (lewy dolny róg), potem **Domeny**.
2. Kliknij **„Połącz istniejącą domenę”**, wpisz **TWOJADOMENA.pl** i kliknij **„Zweryfikuj połączenie”**.
   - Jeśli wyskoczy błąd, odczekaj 30–60 minut i kliknij jeszcze raz. Często łapie od razu.
3. Przy **TWOJADOMENA.pl** kliknij **„Ustaw jako główną”**.

**Gotowe, gdy widzisz:**

| Domena | Status |
|---|---|
| TWOJADOMENA.pl | **Główna · Połączona** |
| xxxx.myshopify.com | Połączona. Zostaw, tej domeny nie da się usunąć i nie przeszkadza |
| www.TWOJADOMENA.pl | przekierowuje na główną |

SSL (kłódka 🔒) Shopify zrobi sam, czasem po kilku godzinach.

---

## KROK 5: Poczta kontakt@TWOJADOMENA.pl (ImprovMX, za darmo)

### 5A. ImprovMX
1. Wejdź na **improvmx.com**. Na stronie głównej wpisz **TWOJADOMENA.pl** i swojego **Gmaila**, potem kliknij **„Create a free alias”**.
2. Potwierdź link, który przyjdzie na Gmaila.
3. Domena będzie na **czerwono**, dopóki nie ustawisz DNS. Tak ma być.
4. Alias `*` przekierowuje **wszystkie** adresy z domeny, w tym `kontakt@`. Możesz dodać osobny alias **kontakt → Gmail**.

### 5B. Rekordy w home.pl
Wejdź w **panel.home.pl → Domeny → TWOJADOMENA.pl → DNS**. Najpierw **usuń stare rekordy MX** i stary TXT zaczynający się od `v=spf1`, jeśli są. Potem dodaj:

| Typ | Host | Wartość / Serwer | Priorytet |
|---|---|---|---|
| **MX** | **puste** | `mx1.improvmx.com.` | `10` |
| **MX** | **puste** | `mx2.improvmx.com.` | `20` |
| **TXT** | **puste** | `v=spf1 include:spf.improvmx.com ~all` | – |

### ✅ Tak ma wyglądać cała lista DNS po krokach 3 i 5

| Typ rekordu | Host | Dane |
|---|---|---|
| TXT | TWOJADOMENA.pl. | `v=spf1 include:spf.improvmx.com ~all` |
| MX | TWOJADOMENA.pl. | `20 mx2.improvmx.com.` |
| MX | TWOJADOMENA.pl. | `10 mx1.improvmx.com.` |
| CNAME | www.TWOJADOMENA.pl. | `shops.myshopify.com.` |
| A | TWOJADOMENA.pl. | `23.227.38.65` |

### 5C. Test poczty
1. W ImprovMX kliknij **Check again / Refresh**. Ma być **zielono**. Trwa to od kilku minut do 1–2 godzin.
2. Wyślij maila na **kontakt@TWOJADOMENA.pl** z **innego** konta niż ten Gmail, bo Gmail ukrywa maile wysłane do samego siebie.
3. Mail ma przyjść na Gmaila. Sprawdź też **Spam**.

> Darmowy ImprovMX tylko **odbiera** pocztę. Klientom odpowiadasz z Gmaila. Maile o zamówieniach i tak wysyła Shopify.

---

## KROK 6: Dane sklepu

> W nowym panelu Shopify **nie ma zakładki „Ogólne”**. Dane sklepu są w **pierwszym kafelku na górze menu Ustawień**, tym z nazwą sklepu i domeną.

1. Kliknij **Ustawienia → kafelek z nazwą sklepu**.
2. Uzupełnij:
   - **Nazwa sklepu:** `NAZWA` (z dużej litery)
   - **E-mail sklepu / kontaktowy:** `kontakt@TWOJADOMENA.pl`
   - **E-mail nadawcy:** `kontakt@TWOJADOMENA.pl`
   - **Waluta:** **PLN**. Ustaw ją **przed pierwszą sprzedażą**, bo potem nie da się jej zmienić.
   - **Strefa czasowa:** `(GMT+01:00) Warszawa`
   - **Jednostki:** metryczne, **kg**
3. Kliknij **Zapisz**.
4. Jeśli pojawi się **„Uwierzytelnij domenę”** (dla maili), dodaj w home.pl rekordy CNAME, które poda Shopify, tak samo jak w kroku 3.
5. **Ustawienia → Języki:** ustaw **polski jako domyślny**.
6. **Ustawienia → Rynki:** zostaw tylko **Polskę**.

---

## KROK 7: Produkt i dostawca (KungfuBuy)

### 7A. KungfuBuy
- **Nowego konta nie zakładasz.** Logujesz się na **istniejące** konto KungfuBuy.
- Upewnij się, że w Shopify jesteś w **nowym sklepie**. Przełączasz w lewym górnym rogu, na nazwie sklepu.
- Podpięcie sklepu, do wyboru:
  - **Aplikacje → Shopify App Store → „KungfuBuy” → Zainstaluj → zaloguj się istniejącym kontem**,
  - albo w panelu KungfuBuy: **Stores → Add store** i wpisz `xxxx.myshopify.com`.
- W KungfuBuy mają być widoczne **wszystkie Twoje sklepy**.
- Produkt: wyślij agentowi **link do produktu** (AliExpress lub 1688) i napisz: *„chcę ten produkt do sklepu NAZWA, warianty …, wtyczka EU, wysyłka do Polski”*. Agent poda cenę i **zmapuje** produkt z Shopify.
- Nie widzisz, gdzie dodać drugi sklep? Napisz agentowi: *„chcę podpiąć drugi sklep Shopify do mojego konta”*.

### 7B. Produkt w Shopify (Produkty → produkt)
- **Tytuł**, **opis**, **zdjęcia własne**. Zdjęcia z AliExpress usuń.
- **Warianty**, np. kolory, i **ceny**.
- **Śledzenie stanu magazynowego: odznacz** albo zaznacz **„Kontynuuj sprzedaż, gdy brak w magazynie”**. Inaczej sklep pokaże „wyprzedane”.
- **Waga**, np. `0,3 kg`.
- Na dole **„Strona w wyszukiwarce” → Edytuj → Uchwyt URL**: krótki adres, np. `nazwa-produktu`.
- **Status: Aktywny** i zaznaczony **kanał „Sklep online”**. Bez tego koszyk nie działa.

---

## KROK 8: Płatności (Ustawienia → Płatności)

1. Kliknij **Aktywuj Shopify Payments**. Podaj typ działalności, dane, **IBAN** i nazwę na wyciągu `NAZWA`. Dowód wgrasz, jeśli Shopify poprosi.
2. Przy **Shopify Payments → Zarządzaj** włącz: ✅ **Visa/Mastercard**, ✅ **BLIK**, ✅ **Apple Pay**, ✅ **Google Pay**.
3. ❌ **Shop Pay → WYŁĄCZ.**
4. Kliknij **Zapisz**.
5. **PayPal → Aktywuj PayPal** i zaloguj się na konto **PayPal Business**.
6. Nie widzisz BLIK-a? Dodaj **Przelewy24** jako dodatkową bramkę.

> Wypłaty ruszą dopiero po wybraniu **płatnego planu**.

---

## KROK 9: Dostawa

> W nowym panelu **wysyłka jest w „Rynkach”**: **Ustawienia → Wysyłka i dostawa → Opcje wysyłki → Polska**, ewentualnie **Ustawienia → Rynki → Polska → Wysyłka**.

1. Shopify tworzy domyślnie **„Standardowa”** i **„Ekspresowa”**. Przerób je, nie dodawaj nowych:

| Było | Zmień nazwę na | Cena |
|---|---|---|
| Standardowa | `Paczkomat InPost` | **0,00 zł** |
| Ekspresowa | `Kurier pod adres` | **0,00 zł** |

2. ⚠️ Shopify potrafi mieć **dwie „Standardowe”**, np. 20 zł oraz 0 zł od 200 zł. **Usuń** tę płatną i warunkową, zostaw tylko dwie stawki po 0 zł **bez warunków**.
3. **Dostawa lokalna:** wyłączona. **Odbiór w sklepie:** wyłączony.
4. **Szacowane daty dostawy:** wyłącz albo ustaw ręcznie. Automatyczne pokazują „dostawa jutro”.
5. **Aplikacja InPost:** **Aplikacje → App Store → „InPost paczkomaty”**. Wybierz aplikację z **mapą paczkomatów w kasie** (najlepiej tę samą co w poprzednim sklepie) i sprawdź w jej ustawieniach, jak ma się nazywać stawka.

---

## KROK 10: Kasa (Ustawienia → Realizacja zakupu)

1. **Informacje kontaktowe klienta:** E-mail.
2. **Pola formularza:**
   - Imię i nazwisko: **wymagane**
   - Nazwa firmy: **ukryte**
   - Linia adresu 2: **opcjonalna**
   - **Numer telefonu: WYMAGANY.** InPost wysyła SMS z kodem.
3. **Dostosuj** (tutaj wolno, to kasa, a nie motyw) → ikona **pędzla**:
   - **Logo:** napis logo na przezroczystym tle (PNG)
   - **Kolor przycisków / akcentu:** kolor marki
4. Kliknij **Zapisz**.

---

## KROK 11: Rabaty na zestawy (Rabaty → Utwórz rabat → „Kwota rabatu od produktów”)

| Pole | Kup 2 | Kup 3 |
|---|---|---|
| Metoda | **Rabat automatyczny** | **Rabat automatyczny** |
| Tytuł (widzi klient) | `Zestaw 2 – rabat` | `Zestaw 3 – rabat` |
| Wartość | Stała kwota, rabat na zamówienie | Stała kwota, rabat na zamówienie |
| Dotyczy | wybrany produkt | wybrany produkt |
| Minimalna liczba produktów | `2` | `3` |
| Kombinacje | brak | brak |
| Daty | od dziś, bez końca | od dziś, bez końca |

- Kwota = **(cena × liczba sztuk) − cena zestawu**.
- Przy 3 sztukach Shopify sam wybierze **lepszy** rabat.
- Cena za sztukę **co do grosza**? Zaznacz rabat **od każdej sztuki**. To działa tylko, gdy w polu „Dotyczy” wybrany jest konkretny produkt.

---

## KROK 12: Motyw (strona sklepu)

1. **Sklep online → Motywy → Dodaj motyw → Prześlij plik zip** i wybierz plik zip motywu.
2. Przy nowym motywie kliknij **Opublikuj**.
3. ⚠️ Przy motywie **NIGDY nie klikaj „Dostosuj” ani „Zaktualizuj”**, bo to rozwala stronę.
4. Kolejne wersje wgrywasz tak samo jako **nowy motyw** i publikujesz. Stare możesz usunąć.

> Ceny na stronie są wpisane w motyw. Gdy zmienisz cenę w Shopify, zmień ją też w motywie, żeby strona i kasa pokazywały to samo.

---

## KROK 13: Polityki (Ustawienia → Polityki)

1. **„Zasady zwrotów i anulowania” → Domyślne zasady:** **zwroty w ciągu 14 dni**, koszt odesłania pokrywa klient. Kliknij **Zapisz**.
2. **Polityki pisemne.** Kliknij w każdy wiersz, wklej tekst i kliknij **Zapisz**. Ma się pojawić status **Opublikowano**:

| Wiersz w Shopify | Co wkleić |
|---|---|
| Polityka zwrotów („Do przeglądu”) | Zwroty i reklamacje. Usuń tekst wstawiony przez Shopify |
| Polityka prywatności („Automatyczne”) | Możesz zostawić automatyczną albo przełączyć na własną |
| Warunki świadczenia usług | Regulamin |
| Polityka wysyłki | Polityka wysyłki |
| Dane kontaktowe („Wymagane”) | Kontakt |
| Nota prawna | opcjonalnie |

**Zasady treści:** pisz ogólnie, **14 dni na zwrot**, dostawa **zwykle 6–10 dni roboczych**, kontakt `kontakt@TWOJADOMENA.pl`. Prawo i tak wymaga, żeby klient mógł poznać sprzedawcę, a Shopify pokazuje dane z ustawień sklepu w kasie i na dokumentach.

---

## KROK 14: Google Search Console

1. Wejdź na **search.google.com/search-console → Dodaj usługę**.
2. Wybierz **PRAWĄ** stronę, **„Prefiks adresu URL”**, i wpisz dokładnie:
   ```
   https://TWOJADOMENA.pl
   ```
   **Bez kropki na końcu.** Kropkę wpisuje się tylko w rekordach DNS w home.pl.
3. Kliknij **DALEJ**.
4. ⚠️ **NIE wybieraj „Plik HTML”**, bo Shopify nie pozwala wgrać takiego pliku. **Przewiń w dół** pod „Menedżer tagów Google” i kliknij **„Dostawca nazwy domeny”**, potem **KOPIUJ**. Dostaniesz `google-site-verification=...`.
5. W **home.pl → DNS → Dodaj nowy rekord**:

| Pole | Co wpisać |
|---|---|
| **Typ rekordu** | `TXT` |
| **Host** | **puste** |
| **Wartość** | `google-site-verification=...` (wklej cały skopiowany tekst) |
| **TTL** | puste |

   > Rekordu poczty `v=spf1 include:spf.improvmx.com ~all` **nie ruszaj**. To mają być **dwa osobne** rekordy TXT.

6. Wróć do Google i kliknij **WERYFIKUJ**. Błąd? Spróbuj ponownie za 10–30 minut.
7. Ma się pokazać **„Własność zweryfikowana automatycznie · Metoda: Dostawca nazwy domeny”**.
8. **Nie musisz dodawać** wersji `http://` ani `www`, bo Shopify przekierowuje je na `https://TWOJADOMENA.pl`. Lewej strony („Domena”) też nie trzeba.
9. **Rekordu TXT nigdy nie usuwaj**, bo weryfikacja przepadnie.
10. **Dopiero po zdjęciu hasła ze sklepu:**
    - **Mapy witryn** → wpisz `sitemap.xml` → **PRZEŚLIJ**
    - górny pasek → `https://TWOJADOMENA.pl` → **POPROŚ O ZINDEKSOWANIE**
    - to samo dla `https://TWOJADOMENA.pl/products/adres-produktu`

---

## KROK 15: Social media

1. **Instagram @NAZWA:** profilówka z logo, bio, przełącz na **konto firmowe**.
2. **Strona na Facebooku „NAZWA”:** to samo logo, bio i link do sklepu.
3. Połącz IG z FB: **ustawienia strony FB → Konta połączone → Instagram**.
4. **ManyChat** (manychat.com): zaloguj się przez Facebooka, podłącz FB i IG i ustaw automat, np. słowo w komentarzu lub DM → wiadomość z linkiem do sklepu.
5. Dodaj wszystko do tego samego **Business Managera**, co w poprzednim sklepie.
6. **Judge.me** (App Store): automatyczne prośby o opinie. Opinie kupujących dostają znaczek weryfikacji.

---

## KROK 16: Start i test (przed reklamami)

1. **Ustawienia → Plan:** wybierz plan.
2. **Sklep online → Preferencje → Ochrona hasłem: WYŁĄCZ.**
3. **Shopify Payments → Zarządzaj → Tryb testowy: WŁĄCZ.**
4. **Zamówienie testowe nr 1:** zestaw 2 szt. + **Paczkomat**. Sprawdź cenę w kasie, wybierz paczkomat na mapie, wpisz telefon i zapłać kartą testową `4242 4242 4242 4242`, data w przyszłości, CVC `123`.
5. **Zamówienie testowe nr 2:** zestaw 3 szt. + **Kurier**. Sprawdź cenę.
6. Sprawdź, czy:
   - przyszedł mail z potwierdzeniem,
   - zamówienie jest w Shopify i w **KungfuBuy**,
   - paczkomat zapisał się w zamówieniu,
   - mail na `kontakt@` dochodzi na Gmaila.
7. **Wyłącz tryb testowy.** Testowe zamówienia **anuluj**, a agentowi napisz, żeby ich **nie wysyłał**.
8. Zrób kroki z **Google Search Console (punkt 10)**.
9. Dopiero teraz włącz **reklamy** 🚀

---

## Najczęstsze pułapki (ściąga)

| Problem | Rozwiązanie |
|---|---|
| IP w polu „Host” w home.pl | IP do **Adres IPv4**, Host **pusty** |
| CNAME bez wartości | **Nazwa kanoniczna** = `shops.myshopify.com.`, Host = `www` |
| Shopify nie weryfikuje domeny | odczekaj 30–60 minut i kliknij jeszcze raz |
| Brak zakładki „Ogólne” | dane sklepu są w **kafelku na górze Ustawień** |
| Wysyłka „przeniesiona do Rynków” | **Opcje wysyłki → Polska**, przerób Standardowa/Ekspresowa |
| Dwie stawki „Standardowa” (20 zł i 0 zł) | usuń płatną, zostaw 0 zł bez warunków |
| Safari blokuje okienko | ikonka w pasku adresu albo **Zezwalaj** dla admin.shopify.com |
| Google: „Plik HTML” | przewiń w dół → **„Dostawca nazwy domeny”** (TXT w home.pl) |
| Kropka w adresie w Google | **bez kropki**: `https://TWOJADOMENA.pl` |
| Mail testowy nie dochodzi | wyślij z **innego** konta i sprawdź **Spam** |
| Claude zmienia nie ten sklep | sprawdź konektor Shopify i zaloguj go na **właściwy** sklep |
| Strona pokazuje inną cenę niż kasa | zmień cenę też w motywie |
| Kliknąłem „Dostosuj” przy motywie | wgraj zip jeszcze raz jako nowy motyw i **Opublikuj** |
