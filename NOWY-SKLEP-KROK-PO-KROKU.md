# Nowy sklep – krok po kroku

## 1. Konto i domena
1. Załóż nowy sklep w Shopify (nowe konto/sklep) i wybierz plan.
2. Kup domenę w home.pl (np. nazwa.pl).
3. Shopify → **Ustawienia → Domeny → Połącz istniejącą domenę** → wpisz domenę.
4. home.pl → **Domeny → domena → Strefa DNS**:
   - **A**, nazwa pusta (@) → `23.227.38.65`
   - **CNAME**, nazwa `www` → `shops.myshopify.com`
5. Shopify → **Zweryfikuj** → ustaw domenę jako **główną**.

## 2. Poczta kontakt@domena (ImprovMX)
1. improvmx.com → dodaj domenę + swój Gmail, alias `*` lub `kontakt` → Gmail.
2. home.pl → Strefa DNS (stare MX usuń, A i CNAME zostaw):
   - **MX** 10 → `mx1.improvmx.com.`
   - **MX** 20 → `mx2.improvmx.com.`
   - **TXT** → `v=spf1 include:spf.improvmx.com ~all`
3. ImprovMX → **Check again**, aż będzie zielono. Test: wyślij maila na kontakt@.
4. Shopify → **Ustawienia → Szczegóły sklepu** → e-mail sklepu = kontakt@domena.

## 3. Dane sklepu
1. **Ustawienia → Szczegóły sklepu**: nazwa sklepu, kraj Polska, waluta PLN, strefa czasowa.
2. **Ustawienia → Języki**: polski jako główny.
3. Wyłącz hasło na sklepie (Sklep online → Preferencje), gdy wszystko gotowe.

## 4. Produkt i dostawca
1. Zainstaluj aplikację dostawcy (np. Kungfubuy) i zaimportuj produkt.
2. Uzupełnij warianty, zdjęcia, cenę i cenę przed obniżką.
3. Ustaw krótki adres produktu (Uchwyt URL), np. `/products/nazwa`.
4. Sprawdź, czy produkt jest **Aktywny** i dostępny w kanale Sklep online.

## 5. Płatności
1. **Ustawienia → Płatności → Shopify Payments**: włącz BLIK, karty, Apple Pay, Google Pay.
2. Dodaj PayPal.
3. Shop Pay – wyłącz, jeśli nie chcesz pola z telefonem w kasie.

## 6. Dostawa
1. **Ustawienia → Wysyłka i dostawa → Profil ogólny → Polska**:
   - Paczkomaty InPost – 0 zł
   - Kurier pod adres – 0 zł
2. Wyłącz niepotrzebne (Orlen, DPD, Ekspresowa, International).
3. Zainstaluj aplikację InPost (wybór paczkomatu).
4. **Ustawienia → Realizacja zakupu**: telefon do wysyłki = **Wymagany**.

## 7. Rabaty za zestawy
1. **Rabaty → Utwórz → Automatyczny**:
   - Kup 2 → kwota rabatu (np. −49,99 zł), min. 2 sztuki
   - Kup 3 → kwota rabatu (np. −119,98 zł), min. 3 sztuki

## 8. Strona (motyw)
1. Daj mi zdjęcia produktu, ceny i opis – robię stronę na naszym szablonie (kolory pod produkt).
2. Wgrywam motyw do Shopify, Ty klikasz tylko **Opublikuj**.
3. **Nigdy nie klikaj „Dostosuj” ani „Zaktualizuj”** przy motywie.
4. Sprawdzasz w Chrome / oknie prywatnym: wybór wariantów, koszyk, dostawa, kasa.

## 9. Polityki
1. **Ustawienia → Zasady**: regulamin, prywatność, wysyłka, zwroty, kontakt (wklejasz gotowe teksty ode mnie).
2. Te same podstrony są w motywie.

## 10. Kasa (wygląd)
1. **Ustawienia → Realizacja zakupu → Dostosuj**: logo, kolory strony, Zapisz.

## 11. Google Search Console
1. search.google.com/search-console → **Dodaj usługę → Prefiks URL** → `https://domena`.
2. Metoda **Tag HTML** → wklejasz mi kod → wstawiam do motywu → Opublikuj → **Weryfikuj**.
3. **Mapy witryn** → `sitemap.xml` → Prześlij.
4. Wklej link produktu u góry → **Poproś o zindeksowanie**.

## 12. Social media
1. Shopify → kanał **Facebook i Instagram** (katalog) i **Shop**.
2. Strona na Facebooku + Instagram firmowy: logo, zdjęcie w tle, bio z linkiem do sklepu.
3. ManyChat: połącz Instagram (przez stronę FB), automatyczne odpowiedzi.

## 13. Test końcowy
1. Zrób testowe zamówienie (paczkomat i kurier) – dostawa 0 zł, rabaty się liczą.
2. Sprawdź maila z potwierdzeniem i czy kontakt@ dochodzi na Gmaila.
3. Dopiero potem reklamy.
