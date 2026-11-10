# Twój szablon sklepu w Shopify

## Pliki
- `Szablon_motyw.zip` – OGÓLNY szablon (pomarańczowo-granatowy, z [PLACEHOLDERAMI]) jako gotowy motyw Shopify.
- `szablon.html` – ten sam szablon jako kod do wypełniania przez czat.
- `Kwiatora_motyw.zip` – przykład gotowego sklepu zrobionego z szablonu.
- `zrob_ogolny.py`, `zbuduj_motyw.py`, `zbuduj.py` – skrypty (robi je za Ciebie czat).

## NAJPROŚCIEJ: jeden plik `Kwiatora_motyw.zip`
W środku jest wszystko: strona, zdjęcia, koszyk, polityki.
1. Shopify → **Sklep online → Motywy → Dodaj motyw → Prześlij plik zip** → wybierz `Kwiatora_motyw.zip`.
2. Przy nowym motywie kliknij **Podgląd**, sprawdź, potem **Opublikuj**.
3. Rabat za 2 i 3 sztuki ustaw w Shopify (Rabaty → automatyczny).

Uwaga: opublikowanie motywu zmienia wygląd CAŁEGO sklepu (strona główna = ten produkt).
Jeśli w tym sklepie masz też inny produkt (np. Lulavi), użyj sposobu ręcznego poniżej.

Nowy produkt = jedna komenda:
`python3 szablon/zbuduj_motyw.py <src.html> <folder-zdjęć> <Nazwa> <uchwyt-produktu>` → nowy zip.

---

## Sposób ręczny (gdy w sklepie jest kilka produktów)

Robisz to raz na sklep (na nowy produkt wymieniasz tylko plik sekcji i zdjęcia).

## Pliki (folder `szablon/shopify/`)

| Plik | Co to jest |
|---|---|
| `layout/landing.liquid` | „Rama” strony: czcionki i kod Shopify, bez nagłówka i stopki motywu (strona ma własne). |
| `sections/landing.liquid` | Cała strona produktu: pasek, galeria, zestawy, sekcje, opinie, licznik 48h, FAQ, polityki, koszyk i okno dostawy. |
| `templates/product.landing.json` | Krótki kod szablonu, który łączy jedno z drugim (taki jak u ziomka). |

## Krok 1: wgraj zdjęcia
Shopify → **Treści → Pliki → Prześlij pliki**. Wrzuć wszystkie zdjęcia z folderu `img/` danego sklepu (np. `kwiatora/img/`) **bez zmieniania nazw**.

## Krok 2: dodaj 3 pliki do motywu
Shopify → **Sklep online → Motywy → … → Edytuj kod**.
1. Folder **layout** → *Dodaj nowy layout* → nazwa `landing` → wklej całą zawartość `layout/landing.liquid` → Zapisz.
2. Folder **sections** → *Dodaj nową sekcję* → nazwa `landing` → wklej `sections/landing.liquid` → Zapisz.
3. Folder **templates** → *Dodaj nowy szablon* → typ **product**, format **JSON**, nazwa `landing` → wklej `templates/product.landing.json` → Zapisz.

## Krok 3: podepnij szablon pod produkt
Produkty → Twój produkt → po prawej **Szablon motywu** → wybierz `landing` → Zapisz.

Gotowe. Strona produktu wygląda jak podgląd, a „Przejdź do płatności” dodaje kalendarze do koszyka Shopify i otwiera kasę.

## Ważne
- **Rabat za 2 i 3 sztuki** musisz ustawić w Shopify: Rabaty → Rabat automatyczny → „Kup X, rabat na ilość” (strona tylko pokazuje ceny zestawów).
- **Nowy produkt** = nowy `src.html` → w terminalu: `python3 szablon/zbuduj.py <ścieżka-do-src.html>` → podmieniasz tylko `sections/landing.liquid` (layout i JSON zostają) + wgrywasz nowe zdjęcia.
- Plik sekcji ma ok. 80 KB, mieści się w limicie Shopify (256 KB).
