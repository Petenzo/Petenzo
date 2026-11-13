# Przekazanie projektu: sklep LUMORKA (lumorka.pl)

## Co to jest
Sklep Shopify z jednym produktem: **Lumorka – świecąca kula wspomnień** (szklana kula/bombka wyświetlająca zdjęcia i filmy klienta). Rynek: Polska, waluta PLN, język polski. Dropshipping przez agenta **KungfuBuy**. Drugi sklep właściciela to **Kwiatora** (kwiatora.pl) – NIE mylić sklepów przy połączeniu Shopify.

## Pliki (repo GitHub `petenzo/petenzo`, gałąź `claude/clever-edison-2o14qw`, folder `memora-strona/`)
- `index.html` – cała strona (HTML/CSS/JS w jednym pliku). Ustawienia w obiekcie `CONFIG` (zdjęcia, pakiety, filmy, FAQ, porównanie, data końca promocji `promoKoniec`).
- `zbuduj-podglad.py` – robi `podglad.html` (wszystko wbudowane, do podglądu).
- `zbuduj-motyw.py` – robi motyw Shopify: folder `motyw-shopify/` + `lumorka-motyw.zip`. Zamienia demo-koszyk na prawdziwy (`/cart/add.js` → `/checkout`). ID wariantów są w skrypcie (`VARIANTS`).
- `polityki-do-wklejenia.txt` – teksty polityk do Shopify (Ustawienia → Polityki).
- `logo/` – logo: `LUMORKA-LOGO.pdf`, `LUMORKA-LOGO-kolo.png`, `LUMORKA-LOGO-PROFILOWE-krem.png`, `LUMORKA-LOGO-PROFILOWE-granat.png`, `LUMORKA-NAPIS-granat-przezroczysty.png` (do kasy), `LUMORKA-NAPIS-bialy-przezroczysty.png`.
- `zdjecia/`, `filmy/` – zdjęcia i filmy strony.
- Podgląd online: https://claude.ai/artifact/3K5xzTPRABkkHGZRJi6PGH

Po każdej zmianie w `index.html`: `python3 zbuduj-podglad.py && python3 zbuduj-motyw.py`, commit i push.

## Wygląd / marka
- Logo: napis „Lumorka” krojem **Playfair Display 600**, granat `#1d3461` / `#14325f`, krem `#f1eee6`. Bez bombki w logo.
- Kolory strony: granat + złoto `#c9a24e` + krem; czerwony tylko do pilności („48h!”).
- Ikony płatności: blik, VISA, mastercard, Apple Pay (logo jabłka), Google Pay (kolorowe G), P24.

## Ceny i rabaty
- 1 szt. **249,99 zł** (przekreślona 349,99 zł) · 2 szt. **489,99 zł** (przekreślona 699,99 zł, „Najczęściej wybierane”) · 3 szt. **719,99 zł** (przekreślona 1 049,99 zł, „Najlepsza cena”). Warianty: Biały, Czarny.
- Zasada właściciela: wszystkie ceny (też przekreślone) kończą się na **,99**.
- W Shopify: cena wariantu 249,99, „cena przed obniżką” (compareAtPrice) 349,99. Automatyczne rabaty kwotowe na zamówienie: „Zestaw 2 Lumorek – rabat” −9,99 zł od 2 szt., „Zestaw 3 Lumorek – rabat” −29,98 zł od 3 szt. (nie łączą się – Shopify bierze lepszy).
- Gratisy od 2 szt. (podstawka, zawieszka, ściereczka) – agent KungfuBuy ma je dorzucać.

## Stan Shopify (sklep lumorka.pl, fr5iiy-nv.myshopify.com)
- Produkt: „Lumorka – świecąca kula wspomnień ze zdjęciami i filmami”, handle `kula-wspomnien`, aktywny, w Sklepie online, 5 zdjęć, sprzedaż przy braku stanu.
- Dostawa: „Paczkomat InPost” 0 zł i „Kurier pod adres” 0 zł (tylko Polska).
- Motyw „Lumorka FINAL” wgrany – właściciel ma go OPUBLIKOWAĆ (publikacji motywu nie da się zrobić przez API). Najnowszy zip: `lumorka-motyw.zip` (wgrać: Sklep online → Motywy → Dodaj motyw → Prześlij plik zip → Opublikuj).
- Google Search Console: `https://lumorka.pl` zweryfikowane rekordem TXT w home.pl (nie usuwać).
- Poczta: kontakt@lumorka.pl przez ImprovMX (MX + SPF w home.pl).

## Treści – ustalenia właściciela (ważne)
- NIGDZIE na stronie i w politykach nie podawać imienia, nazwiska ani adresu właściciela. Administrator danych / sprzedawca = „sklep Lumorka”, kontakt: kontakt@lumorka.pl.
- Zwrot: **14 dni**. Dostawa: ogólnie **6–10 dni roboczych** (bez rozbijania na etapy). Pisać ogólnie, bez konkretnych obietnic.
- Polityki: dłuższe, ogólne, każda inaczej napisana, bez powtarzania tych samych zdań.
- FAQ: 8 ogólnych pytań o produkt, odpowiedzi w 1 linijce.
- Sekcja opinii jest USUNIĘTA (ukryta `#sec-rev`), bo nie ma jeszcze opinii od kupujących Lumorki. Plan: aplikacja **Judge.me** → prawdziwe opinie kupujących z „✓ Zweryfikowany zakup”, karty w stylu Kwiatory (zdjęcie u góry, gwiazdki, tekst, imię + miasto, zielony znaczek).
- Licznik promocji 48h kończy się w dacie `promoKoniec` – ustawić nową prawdziwą datę albo usunąć.

## Do zrobienia przez właściciela
1. Opublikować motyw „Lumorka FINAL” (albo wgrać najnowszy zip).
2. Wkleić polityki z `polityki-do-wklejenia.txt`; nazwa sklepu „Lumorka”.
3. Płatności: Shopify Payments (BLIK, karty, Apple Pay, Google Pay) + PayPal, Shop Pay wyłączony.
4. Kasa: telefon wymagany; logo `LUMORKA-NAPIS-granat-przezroczysty.png`, kolor `#14325f`.
5. Aplikacja InPost z mapą paczkomatów; KungfuBuy – podpięcie produktu.
6. Plan Shopify, zdjęcie hasła, zamówienia testowe (2 szt. = 489,99 zł, 3 szt. = 719,99 zł).
7. Po zdjęciu hasła: Search Console → `sitemap.xml` + prośba o zindeksowanie.
8. Social media (IG/FB z logo i bio, ManyChat), Judge.me, potem reklamy.

## Styl współpracy
Właściciel pisze po polsku, krótko i potocznie. Odpowiadać po polsku, krok po kroku, konkretnie co kliknąć. Zmieniać tylko to, o co prosi.
